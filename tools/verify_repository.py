#!/usr/bin/env python3
"""Dependency-free repository checks used locally and in GitHub Actions."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from extract_lucky_frontend import write_markdown, write_openapi
from lucky_api import OperationRisk, RouteCatalog, load_merged_snapshot


ROOT = Path(__file__).resolve().parents[1]
TOKEN_ASSIGNMENT = re.compile(
    r"(?i)(?:open[_-]?token|authorization)\s*[:=]\s*[\"']?(?!\$\{|<|your-|example|replace)[A-Za-z0-9_-]{24,}"
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")
SKILL_FRONTMATTER = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
HEX_COLOR = re.compile(r"^#[0-9A-F]{6}$", re.IGNORECASE)
TODO_MARKER = "[TODO:"
PLUGIN_MANIFEST_FIELDS = {
    "id",
    "name",
    "version",
    "description",
    "skills",
    "apps",
    "mcpServers",
    "interface",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
}
PLUGIN_AUTHOR_FIELDS = {"name", "email", "url"}
PLUGIN_INTERFACE_FIELDS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "websiteURL",
    "privacyPolicyURL",
    "termsOfServiceURL",
    "brandColor",
    "composerIcon",
    "logo",
    "logoDark",
    "screenshots",
    "defaultPrompt",
    "default_prompt",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_non_empty_string(payload: dict[str, object], field: str, *, prefix: str = "") -> str:
    value = payload.get(field)
    qualified = f"{prefix}.{field}" if prefix else field
    if not isinstance(value, str) or not value.strip():
        fail(f"Codex plugin {qualified} must be a non-empty string")
    return value


def validate_optional_non_empty_string(
    payload: dict[str, object], field: str, *, prefix: str = ""
) -> None:
    if payload.get(field) is not None:
        require_non_empty_string(payload, field, prefix=prefix)


def validate_optional_https_url(
    payload: dict[str, object], field: str, *, prefix: str = ""
) -> None:
    value = payload.get(field)
    if value is None:
        return
    qualified = f"{prefix}.{field}" if prefix else field
    parsed = urlparse(value) if isinstance(value, str) else None
    if parsed is None or parsed.scheme != "https" or not parsed.netloc:
        fail(f"Codex plugin {qualified} must be an absolute https URL")


def reject_unknown_fields(payload: dict[str, object], allowed: set[str], *, prefix: str = "") -> None:
    unknown = sorted(set(payload) - allowed)
    if unknown:
        qualified = f"{prefix} fields" if prefix else "fields"
        fail(f"Codex plugin has unsupported {qualified}: {', '.join(unknown)}")


def reject_todo_markers(value: object, path: str = "$") -> None:
    if isinstance(value, str):
        if TODO_MARKER in value:
            fail(f"Codex plugin {path} still contains a TODO placeholder")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_todo_markers(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_todo_markers(item, f"{path}.{key}")


def normalize_contract_path(raw_path: object) -> str | None:
    if not isinstance(raw_path, str):
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return None
    normalized = path.as_posix().rstrip("/")
    return normalized or None


def validate_optional_contract_path(
    payload: dict[str, object], field: str, expected: str
) -> None:
    value = payload.get(field)
    if value is not None and normalize_contract_path(value) != expected:
        fail(f"Codex plugin {field} must resolve to {expected}")


def validate_asset_path(raw_path: object, field: str) -> None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        fail(f"Codex plugin {field} must be a non-empty relative path")
    candidate = PurePosixPath(raw_path.replace("\\", "/"))
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        fail(f"Codex plugin {field} must stay inside the plugin archive")
    resolved = (ROOT / candidate.as_posix()).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        fail(f"Codex plugin {field} must stay inside the plugin archive")
    if not resolved.is_file():
        fail(f"Codex plugin {field} points to a missing file")


def validate_optional_asset_path(payload: dict[str, object], field: str) -> None:
    value = payload.get(field)
    if value is not None:
        validate_asset_path(value, f"interface.{field}")


def validate_prompt_list(value: object, field: str) -> None:
    if not isinstance(value, list) or not 1 <= len(value) <= 3:
        fail(f"Codex plugin {field} must contain 1 to 3 prompts")
    if not all(
        isinstance(item, str) and item.strip() and len(item) <= 128 for item in value
    ):
        fail(f"Codex plugin {field} prompts must be non-empty strings up to 128 characters")


def validate_default_prompts(interface: dict[str, object]) -> None:
    if "defaultPrompt" not in interface and "default_prompt" not in interface:
        fail("Codex plugin interface.defaultPrompt or interface.default_prompt is required")
    # The public plugin spec defines the camelCase field as 1–3 strings capped at
    # 128 characters. The legacy snake_case alias is accepted by the canonical
    # ingestion validator based on key presence alone, so do not narrow it here.
    if "defaultPrompt" in interface:
        validate_prompt_list(interface.get("defaultPrompt"), "interface.defaultPrompt")


def load_companion_json(path: Path, label: str) -> dict[str, object]:
    if not path.is_file():
        fail(f"Codex plugin {label} is required when its manifest field is present")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        fail(f"Codex plugin {label} must contain valid JSON")
    if not isinstance(payload, dict):
        fail(f"Codex plugin {label} must contain a JSON object")
    return payload


def validate_mcp_server_entries(servers: object, label: str) -> None:
    if not isinstance(servers, dict):
        fail(f"Codex plugin {label} must be an object")
    for key, value in servers.items():
        if not isinstance(key, str) or not key.strip():
            fail(f"Codex plugin {label} server names must be non-empty strings")
        if not isinstance(value, dict):
            fail(f"Codex plugin {label} server {key!r} must be an object")


def validate_manifest_mcp_servers(manifest: dict[str, object]) -> None:
    value = manifest.get("mcpServers")
    if value is None:
        return
    if isinstance(value, str):
        validate_optional_contract_path(manifest, "mcpServers", ".mcp.json")
        payload = load_companion_json(ROOT / ".mcp.json", ".mcp.json")
        reject_unknown_fields(payload, {"mcpServers"}, prefix=".mcp.json")
        validate_mcp_server_entries(payload.get("mcpServers"), ".mcp.json mcpServers")
        return
    if isinstance(value, dict):
        validate_mcp_server_entries(value, "mcpServers")
        return
    fail("Codex plugin mcpServers must be a string path or object")


def validate_app_manifest() -> None:
    payload = load_companion_json(ROOT / ".app.json", ".app.json")
    reject_unknown_fields(payload, {"apps"}, prefix=".app.json")
    apps = payload.get("apps")
    if not isinstance(apps, dict):
        fail("Codex plugin .app.json apps must be an object")
    for key, value in apps.items():
        if not isinstance(value, dict):
            fail(f"Codex plugin .app.json app {key!r} must be an object")
        reject_unknown_fields(value, {"id", "category"}, prefix=f".app.json app {key}")
        require_non_empty_string(value, "id", prefix=f".app.json app {key}")
        validate_optional_non_empty_string(value, "category", prefix=f".app.json app {key}")


def check_secrets() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py", ".sh", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if TOKEN_ASSIGNMENT.search(text):
            fail(f"possible hard-coded credential in {path.relative_to(ROOT)}")


def check_local_links() -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {target}")


def check_skill_packaging() -> None:
    repo_skill_path = ROOT / ".agents" / "skills" / "lucky" / "SKILL.md"
    plugin_skill_path = ROOT / "skills" / "lucky" / "SKILL.md"
    for path in (repo_skill_path, plugin_skill_path):
        if not path.is_file():
            fail(f"Lucky skill is missing from {path.relative_to(ROOT)}")
    if repo_skill_path.read_bytes() != plugin_skill_path.read_bytes():
        fail("repository and plugin Lucky SKILL.md copies must remain byte-identical")

    text = repo_skill_path.read_text(encoding="utf-8")
    match = SKILL_FRONTMATTER.match(text)
    if not match:
        fail("Lucky SKILL.md is missing YAML frontmatter")

    metadata: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            fail(f"invalid Lucky SKILL.md frontmatter line: {line}")
        metadata[key.strip()] = value.strip()

    if metadata.get("name") != "lucky":
        fail("Lucky SKILL.md name must be 'lucky'")
    description = metadata.get("description", "")
    if not description:
        fail("Lucky SKILL.md description is required")
    if len(description) > 1024:
        fail("Lucky SKILL.md description exceeds the 1024-character host limit")

    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        fail("Codex plugin manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        fail("Codex plugin manifest must be a JSON object")
    reject_todo_markers(manifest)
    reject_unknown_fields(manifest, PLUGIN_MANIFEST_FIELDS)
    validate_optional_non_empty_string(manifest, "id")
    if require_non_empty_string(manifest, "name") != "lucky-skills":
        fail("Codex plugin name must be 'lucky-skills'")
    version = require_non_empty_string(manifest, "version")
    if not SEMVER.fullmatch(version):
        fail("Codex plugin version must use strict semver")
    require_non_empty_string(manifest, "description")

    author = manifest.get("author")
    if not isinstance(author, dict):
        fail("Codex plugin author must be an object")
    reject_unknown_fields(author, PLUGIN_AUTHOR_FIELDS, prefix="author")
    require_non_empty_string(author, "name", prefix="author")
    validate_optional_non_empty_string(author, "email", prefix="author")
    validate_optional_https_url(author, "url", prefix="author")

    validate_optional_contract_path(manifest, "skills", "skills")
    validate_optional_contract_path(manifest, "apps", ".app.json")
    validate_manifest_mcp_servers(manifest)
    if manifest.get("apps") is not None:
        validate_app_manifest()

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("Codex plugin interface metadata is required")
    reject_unknown_fields(interface, PLUGIN_INTERFACE_FIELDS, prefix="interface")
    for field in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
    ):
        require_non_empty_string(interface, field, prefix="interface")
    validate_default_prompts(interface)
    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not all(
        isinstance(item, str) and item.strip() for item in capabilities
    ):
        fail("Codex plugin interface.capabilities must be an array of strings")
    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        validate_optional_https_url(interface, field, prefix="interface")
    brand_color = interface.get("brandColor")
    if brand_color is not None and (
        not isinstance(brand_color, str) or HEX_COLOR.fullmatch(brand_color) is None
    ):
        fail("Codex plugin interface.brandColor must use #RRGGBB")
    for field in ("composerIcon", "logo", "logoDark"):
        validate_optional_asset_path(interface, field)
    screenshots = interface.get("screenshots", [])
    if not isinstance(screenshots, list):
        fail("Codex plugin interface.screenshots must be an array")
    for index, raw_path in enumerate(screenshots):
        validate_asset_path(raw_path, f"interface.screenshots[{index}]")


def check_runtime_verification(snapshot_path: Path, snapshot: dict[str, object]) -> None:
    runtime_path = snapshot_path.with_name("lucky-v3-runtime-verification.json")
    if not runtime_path.is_file():
        fail("runtime route verification file is missing")
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    if runtime.get("schema_version") != 1:
        fail("runtime route verification schema is unsupported")
    target = snapshot.get("target", {})
    runtime_target = runtime.get("target", {})
    if not isinstance(target, dict) or not isinstance(runtime_target, dict):
        fail("runtime route verification target is malformed")
    if runtime_target.get("version") != target.get("version"):
        fail("runtime route verification version does not match endpoint snapshot")
    snapshot_sha256 = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
    if runtime.get("static_snapshot_sha256") != snapshot_sha256:
        fail("runtime route verification is not bound to the exact endpoint snapshot")

    suppress = runtime.get("suppress_literals")
    if not isinstance(suppress, list) or not all(
        isinstance(path, str) and path.startswith("/api/") for path in suppress
    ):
        fail("runtime suppress_literals must contain /api/... paths")
    if len(suppress) != len(set(suppress)):
        fail("runtime suppress_literals contains duplicates")
    suppression_evidence = runtime.get("suppression_evidence")
    if not isinstance(suppression_evidence, dict):
        fail("runtime suppression_evidence must be an object")
    prefix_evidence = suppression_evidence.get("same_bundle_prefix_artifacts")
    no_route_evidence = suppression_evidence.get("no_route_literals")
    if not isinstance(prefix_evidence, dict) or not isinstance(no_route_evidence, dict):
        fail("runtime suppression_evidence categories are missing")
    no_route_paths = no_route_evidence.get("paths")
    if not isinstance(no_route_paths, list) or not all(
        isinstance(path, str) and path in suppress for path in no_route_paths
    ):
        fail("runtime no-route suppression paths must be suppressed API paths")
    if no_route_evidence.get("count") != len(no_route_paths):
        fail("runtime no-route suppression count is stale")
    prefix_count = prefix_evidence.get("count")
    if not isinstance(prefix_count, int) or prefix_count + len(no_route_paths) != len(suppress):
        fail("runtime suppression evidence counts do not cover suppress_literals")

    verified = runtime.get("routes")
    if not isinstance(verified, list):
        fail("runtime verified routes must be an array")
    keys: list[tuple[str, str]] = []
    for item in verified:
        if not isinstance(item, dict):
            fail("runtime verified route must be an object")
        path = item.get("path")
        method = item.get("method")
        risk = item.get("risk")
        if not isinstance(path, str) or not path.startswith("/api/"):
            fail("runtime verified route has invalid path")
        if method not in {"GET", "POST", "PUT", "DELETE", "PATCH"}:
            fail(f"runtime verified route has invalid method: {method}")
        if risk not in {item.value for item in OperationRisk if item is not OperationRisk.UNKNOWN}:
            fail(f"runtime verified route has invalid risk: {risk}")
        for field in ("query_keys", "body_keys"):
            value = item.get(field)
            if value is not None and (
                not isinstance(value, list) or not all(isinstance(key, str) and key for key in value)
            ):
                fail(f"runtime verified route {field} must be an array of non-empty strings")
        for field in ("request_body_schema", "response_schema"):
            value = item.get(field)
            if value is not None and not isinstance(value, dict):
                fail(f"runtime verified route {field} must be an object")
        for field in ("request_content_type", "schema_evidence"):
            value = item.get(field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                fail(f"runtime verified route {field} must be a non-empty string")
        keys.append((path, str(method)))
    if len(keys) != len(set(keys)):
        fail("runtime verified routes contain duplicate path/method entries")

    merged = RouteCatalog.from_file(snapshot_path, runtime_verification=runtime_path)
    unknown = merged.search(risk=OperationRisk.UNKNOWN)
    if unknown:
        fail(f"runtime route verification leaves {len(unknown)} unknown route(s)")

    expected_body_schema_gaps: set[tuple[str, str]] = set()
    actual_body_schema_gaps = {
        (route.method, route.path)
        for route in merged.routes
        if route.method in {"POST", "PUT", "PATCH"}
        and route.has_body
        and not route.body_keys
        and route.request_body_schema is None
    }
    if actual_body_schema_gaps != expected_body_schema_gaps:
        missing = sorted(expected_body_schema_gaps - actual_body_schema_gaps)
        added = sorted(actual_body_schema_gaps - expected_body_schema_gaps)
        fail(
            "request-body schema gap set changed; "
            f"resolved={missing or 'none'} new={added or 'none'}"
        )

    legacy_docker_schemas = {
        ("POST", "/api/docker/containers/{param}/upgrade"): {
            "type": "object",
            "properties": {},
        },
        ("POST", "/api/docker/images/build"): {
            "type": "object",
            "properties": {"dockerfile": {"type": "string"}},
            "required": ["dockerfile"],
        },
        ("POST", "/api/docker/images/build-from-git"): {
            "type": "object",
            "properties": {"git_url": {"type": "string"}},
            "required": ["git_url"],
        },
        ("POST", "/api/docker/images/build-from-zip"): {
            "type": "object",
            "properties": {"zip_path": {"type": "string"}},
            "required": ["zip_path"],
        },
        ("POST", "/api/docker/images/import"): {
            "type": "object",
            "properties": {"source": {"type": "string"}},
            "required": ["source"],
        },
        ("POST", "/api/docker/prune"): {
            "type": "object",
            "properties": {
                "all": {"type": "boolean"},
                "volumes": {"type": "boolean"},
            },
        },
    }
    merged_by_key = {(route.method, route.path): route for route in merged.routes}

    conservative_get_risks = {
        ("GET", "/api/docker/volumes/export"): OperationRisk.DANGEROUS,
        ("GET", "/api/ipfliter/oneclickrecord"): OperationRisk.MUTATING,
        ("GET", "/api/ipfliter/porttrap/blockedips/export"): OperationRisk.DANGEROUS,
        ("GET", "/api/third/filebrowser/resetadmin"): OperationRisk.DANGEROUS,
        ("GET", "/api/webservice/statistics/export"): OperationRisk.DANGEROUS,
        ("GET", "/api/ddns/getipfromcmdtest"): OperationRisk.DANGEROUS,
    }
    for route_key, expected_risk in conservative_get_risks.items():
        route = merged_by_key.get(route_key)
        if route is None or route.risk is not expected_risk:
            fail(f"conservative GET risk classification regressed for {route_key}: {getattr(route, 'risk', None)}")
    for route_key in {
        ("GET", "/api/docker/compose/backup/status"),
        ("GET", "/api/docker/volumes/backup/status"),
        ("GET", "/api/webservice/statistics/import/status"),
    }:
        route = merged_by_key.get(route_key)
        if route is None or route.risk is not OperationRisk.READ_ONLY:
            fail(f"read-only status GET was over-classified by action-name hardening: {route_key}")

    for key, expected_schema in legacy_docker_schemas.items():
        route = merged_by_key.get(key)
        if route is None or route.request_body_schema != expected_schema:
            fail(f"legacy Docker schema evidence changed unexpectedly for {key[0]} {key[1]}")

    untyped_request_routes = [
        route
        for route in merged.routes
        if route.method in {"POST", "PUT", "PATCH"}
        and route.has_body
        and route.body_keys
        and route.request_body_schema is None
    ]
    if len(untyped_request_routes) > 66:
        fail(
            "typed request-schema coverage regressed; "
            f"expected at most 66 field-bearing write routes without explicit schemas, got {len(untyped_request_routes)}"
        )

    explicit_small_request_schemas = {
        ("PUT", "/api/frontend-preferences"): {
            "type": "object", "properties": {"theme": {"type": "string"}, "language": {"type": "string"}}
        },
        ("POST", "/api/cloudflared/{param}/cname/create"): {
            "type": "object", "properties": {"hostname": {"type": "string"}, "proxied": {"type": "boolean"}}
        },
        ("PUT", "/api/ipdb/configure"): {
            "type": "object", "properties": {"CustomIPDBPath": {"type": "string"}}
        },
        ("POST", "/api/login"): {
            "type": "object", "properties": {"challengeId": {"type": "string"}, "cipherText": {"type": "string"}}
        },
        ("POST", "/api/oauth/login"): {
            "type": "object", "properties": {"challengeId": {"type": "string"}, "cipherText": {"type": "string"}}
        },
        ("PUT", "/api/password/verify"): {
            "type": "object", "properties": {"oldPassword": {"type": "string"}}
        },
        ("POST", "/api/v2l"): {
            "type": "object", "properties": {"v2l": {"type": "string"}}
        },
        ("PUT", "/api/cron/taskgrouporderupdate"): {
            "type": "object",
            "properties": {
                "tasksMap": {"type": "object", "additionalProperties": {"type": "string"}},
                "orderList": {"type": "array", "items": {"type": "string"}},
            },
        },
        ("POST", "/api/webservice/statistics/geo/rebuild"): {
            "type": "object", "properties": {"mode": {"type": "string"}}
        },
        ("POST", "/api/webservice/statistics/ip-info-refresh"): {
            "type": "object", "properties": {"mode": {"type": "string"}}
        },
        ("POST", "/api/docker/images/load"): {
            "type": "object", "properties": {"path": {"type": "string"}, "cleanup": {"type": "boolean"}}
        },
    }
    for route_key, expected in explicit_small_request_schemas.items():
        request_schema = merged_by_key[route_key].request_body_schema
        if request_schema != expected:
            fail(f"explicit small request schema regressed for {route_key}")
        if isinstance(request_schema, dict) and "required" in request_schema:
            fail(f"explicit small request schema must not invent required fields for {route_key}")

    login_challenge = merged_by_key[("GET", "/api/login/challenge")].response_schema
    challenge_id_schema = (
        login_challenge.get("properties", {}).get("challengeId")
        if isinstance(login_challenge, dict)
        else None
    )
    if challenge_id_schema != {"type": "string"}:
        fail("login challengeId runtime evidence regressed")

    ipdb_config = merged_by_key[("GET", "/api/ipdb/configure")].response_schema
    custom_ipdb_path_schema = (
        ipdb_config.get("properties", {}).get("customIPDBPath")
        if isinstance(ipdb_config, dict)
        else None
    )
    if custom_ipdb_path_schema != {"type": "string"}:
        fail("IPDB custom path runtime evidence regressed")

    base_put_route = merged_by_key[("PUT", "/api/baseconfigure")]
    base_put = base_put_route.request_body_schema
    base_props = base_put.get("properties", {}) if isinstance(base_put, dict) else {}
    if not isinstance(base_put, dict) or base_put.get("type") != "object":
        fail("baseconfigure PUT request schema must remain an object")
    if set(base_props) != set(base_put_route.body_keys):
        fail("baseconfigure PUT request schema must cover exactly the frontend body fields")
    base_string_fields = {
        "AdminAccount", "AdminPassword", "AdminWebListenIP", "BackendServerListBackup",
        "BackgroundColor", "BackgroundImage", "CustomDNSA", "CustomDNSB", "CustomDNSC",
        "CustomDNSD", "CustomDNSList", "DeviceID", "FrontendLanguage", "FrontendTheme",
        "GlobalNoLimitCIDRs", "OldPassword", "OpenToken", "OriginsList",
        "ProxyProtocolTrustedCIDRs", "SafeURL", "TimeZone", "TwoFAKey",
    }
    base_integer_fields = {
        "AdminWebListenHttpsPort", "AdminWebListenPort", "BackgroundBlur", "ConfVer",
        "FirewallInitDelay", "GCPercent", "GOMAXPROCS", "HttpClientTimeout", "LogMaxSize",
        "MaxConsecutiveLoginFailures", "StatusHistoryRetentionDays",
        "StatusHistorySampleIntervalSeconds", "TokenExpirationHour", "TwoFADigits",
    }
    base_boolean_fields = {
        "AdminWebListenTLS", "AllowAllThirdAuthUsers", "AllowInternetaccess",
        "AutoOptionsFirewall", "CatchPanic", "DisableAllowAllOrigins", "DisableNTPSync",
        "DisableNTPSyncLog", "EnableCustomBackgroundColor", "EnableCustomBackgroundImage",
        "EnableOpenToken", "EnableStatusHistory", "EnableThirdAuthLogin", "ForceHTTPS",
        "FrontendDisableAutoExpandLeftMenu", "GlobalDisableFirewallOpt", "IgnoreAuthInfoCheck",
        "IgnoreSafeURLCheck", "InsecureSkipVerify", "OpenTokenConfirmed", "RestartAfterPanic",
        "SetGCPercent", "ThirdAuthLoginSkipTwoFA", "TwoFAEnable",
    }
    for field in base_string_fields:
        if base_props.get(field) != {"type": "string"}:
            fail(f"baseconfigure string request type regressed for {field}")
    for field in base_integer_fields:
        if base_props.get(field) != {"type": "integer"}:
            fail(f"baseconfigure integer request type regressed for {field}")
    for field in base_boolean_fields:
        if base_props.get(field) != {"type": "boolean"}:
            fail(f"baseconfigure boolean request type regressed for {field}")
    for field in ("DisableModules", "Keys", "StatNetInterfaceList", "ThirdAuthLoginUserList"):
        if base_props.get(field) != {}:
            fail(f"baseconfigure null-only runtime field must remain untyped for {field}")
    if base_props.get("hiddenModules") != {"type": ["array", "null"], "items": {}}:
        fail("baseconfigure hiddenModules request type must reuse verified module model")
    if "required" in base_put:
        fail("baseconfigure PUT request schema must not invent required fields")

    filebrowser_put = merged_by_key[("PUT", "/api/third/filebrowser/configure")].request_body_schema
    filebrowser_get = merged_by_key[("GET", "/api/third/filebrowser/configure")].response_schema
    filebrowser_get_props = (
        filebrowser_get.get("properties", {}).get("configure", {}).get("properties", {})
        if isinstance(filebrowser_get, dict)
        else {}
    )
    expected_filebrowser_props = dict(filebrowser_get_props)
    expected_filebrowser_props["RedisCacheUrl"] = {"type": "string"}
    if filebrowser_put != {"type": "object", "properties": expected_filebrowser_props}:
        fail("FileBrowser PUT request schema must match safe GET projection plus RedisCacheUrl:string")
    if isinstance(filebrowser_put, dict) and "required" in filebrowser_put:
        fail("FileBrowser PUT request schema must not invent required fields")

    wol_webhook = merged_by_key[("POST", "/api/wol/webhooktest")].request_body_schema
    wol_get = merged_by_key[("GET", "/api/wol/service/configure")].response_schema
    wol_server_props = (
        wol_get.get("properties", {}).get("configure", {}).get("properties", {}).get("Server", {}).get("properties", {})
        if isinstance(wol_get, dict)
        else {}
    )
    wol_webhook_fields = tuple(merged_by_key[("POST", "/api/wol/webhooktest")].body_keys)
    expected_wol_webhook_props = {
        field: ({"type": "string"} if field == "WebhookProxyPassword" else wol_server_props.get(field))
        for field in wol_webhook_fields
    }
    if any(value is None for value in expected_wol_webhook_props.values()):
        fail("WOL webhook request fields must remain backed by the verified Server read model")
    if wol_webhook != {"type": "object", "properties": expected_wol_webhook_props}:
        fail("WOL webhook-test request schema regressed")
    if isinstance(wol_webhook, dict) and "required" in wol_webhook:
        fail("WOL webhook-test request schema must not invent required fields")

    wol_device_request = {
        "type": "object",
        "properties": {
            "Key": {"type": "string"},
            "DeviceName": {"type": "string"},
            "MacList": {"type": "array", "items": {"type": "string"}},
            "BroadcastIPs": {"type": "array", "items": {}},
            "ProbeTargets": {"type": "array", "items": {}},
            "Port": {"type": "integer"},
            "Relay": {"type": "boolean"},
            "Repeat": {"type": "integer"},
            "IOT_DianDeng_Enable": {"type": "boolean"},
            "IOT_DianDeng_AUTHKEY": {"type": "string"},
            "IOT_DianDeng_InsecureSkipVerify": {"type": "boolean"},
            "IOT_DianDengBindComponentEnable": {"type": "boolean"},
            "IOT_DianDengBindComponent": {"type": "string"},
            "IOT_Bemfa_Enable": {"type": "boolean"},
            "IOT_Bemfa_SecretKey": {"type": "string"},
            "IOT_Bemfa_Topic": {"type": "string"},
            "IOT_Bemfa_InsecureSkipVerify": {"type": "boolean"},
        },
    }
    for route_key in {
        ("POST", "/api/wol/device"),
        ("PUT", "/api/wol/device"),
    }:
        route = merged_by_key[route_key]
        if route.request_body_schema != wol_device_request:
            fail(f"WOL disposable-device request schema regressed for {route_key}")
        if isinstance(route.request_body_schema, dict) and "required" in route.request_body_schema:
            fail(f"WOL device request schema must not invent required fields for {route_key}")
        if route.response_schema != {"type": "object", "properties": {"ret": {"type": "integer"}}}:
            fail(f"WOL disposable-device ret-only response schema regressed for {route_key}")
    if merged_by_key[("DELETE", "/api/wol/device")].response_schema != {
        "type": "object", "properties": {"ret": {"type": "integer"}}
    }:
        fail("WOL disposable-device delete response schema regressed")

    wol_devices = merged_by_key[("GET", "/api/wol/devices")].response_schema
    wol_device_props = (
        wol_devices.get("properties", {}).get("list", {}).get("items", {}).get("properties", {})
        if isinstance(wol_devices, dict)
        else {}
    )
    for secret_field in ("IOT_DianDeng_AUTHKEY", "IOT_Bemfa_SecretKey"):
        if secret_field in wol_device_props:
            fail(f"WOL device response schema must omit secret field {secret_field}")
    for field, expected in {
        "Key": {"type": "string"},
        "DeviceName": {"type": "string"},
        "MacList": {"type": "array", "items": {"type": "string"}},
        "BroadcastIPs": {"type": "array", "items": {}},
        "ProbeTargets": {"type": "array", "items": {}},
        "Port": {"type": "integer"},
        "Relay": {"type": "boolean"},
        "Repeat": {"type": "integer"},
        "Probe": {"type": "object"},
        "CanShutdown": {"type": "boolean"},
        "CanWakeup": {"type": "boolean"},
    }.items():
        if wol_device_props.get(field) != expected:
            fail(f"WOL device safe response type regressed for {field}")

    update_confirm = merged_by_key[("PUT", "/api/update/comfire")].request_body_schema
    expected_update_confirm = {
        "type": "object",
        "properties": {
            "Name": {"type": "string"},
            "ARCH": {"type": "string"},
            "OS": {"type": "string"},
            "Version": {"type": "string"},
            "GoVersion": {"type": "string"},
            "Date": {"type": "string"},
            "MD5": {"type": "string"},
        },
    }
    if update_confirm != expected_update_confirm:
        fail("program-update confirm request schema regressed")
    info_schema = merged_by_key[("GET", "/api/info")].response_schema
    info_props = (
        info_schema.get("properties", {}).get("info", {}).get("properties", {})
        if isinstance(info_schema, dict)
        else {}
    )
    for field in ("ARCH", "OS", "Version", "GoVersion", "Date", "MD5"):
        if info_props.get(field) != {"type": "string"}:
            fail(f"/api/info string evidence regressed for update field {field}")

    lightpanel_template = merged_by_key[("POST", "/api/webservice/lightpanel/configtemplate")].request_body_schema
    expected_lightpanel = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "path": {"type": "string"},
            "rcloneKey": {"type": "string"},
            "rcloneRoot": {"type": "string"},
            "storeKey": {"type": "string"},
            "storeRoot": {"type": "string"},
        },
    }
    if lightpanel_template != expected_lightpanel:
        fail("WebService lightpanel config-template request schema regressed")
    icon_sources = merged_by_key[("GET", "/api/iconlib/sources")].response_schema
    icon_source_props = (
        icon_sources.get("properties", {}).get("sources", {}).get("items", {}).get("properties", {})
        if isinstance(icon_sources, dict)
        else {}
    )
    for field in ("Type", "Path", "RcloneKey", "RcloneRoot", "StoreKey", "StoreRoot"):
        if icon_source_props.get(field) != {"type": "string"}:
            fail(f"IconLib source string evidence regressed for {field}")

    crosschecked_resource_request_schemas = {
        ("PUT", "/api/modules/hidden"): {
            "type": "object", "properties": {"hiddenModules": {"type": ["array", "null"], "items": {}}}
        },
        ("POST", "/api/docker/images/pull-async"): {
            "type": "object", "properties": {"architecture": {"type": "string"}, "image": {"type": "string"}, "tag": {"type": "string"}}
        },
        ("POST", "/api/docker/images/pull-with-backup"): {
            "type": "object", "properties": {"architecture": {"type": "string"}, "backup_tag": {"type": "string"}, "image_ref": {"type": "string"}}
        },
        ("POST", "/api/docker/images/pull-with-backup-async"): {
            "type": "object", "properties": {"architecture": {"type": "string"}, "backup_tag": {"type": "string"}, "image_ref": {"type": "string"}}
        },
        ("POST", "/api/docker/images/push"): {
            "type": "object", "properties": {"image": {"type": "string"}, "tag": {"type": "string"}}
        },
        ("POST", "/api/docker/images/remove-saved-digest"): {
            "type": "object", "properties": {"image_id": {"type": "string"}}
        },
        ("POST", "/api/docker/images/backup-tag"): {
            "type": "object", "properties": {"image_ref": {"type": "string"}}
        },
        ("POST", "/api/docker/images/upgrade-check"): {
            "type": "object", "properties": {"image_ref": {"type": "string"}}
        },
        ("POST", "/api/docker/images/upgrade-dismiss"): {
            "type": "object", "properties": {"image_id": {"type": "string"}, "image_ref": {"type": "string"}}
        },
        ("POST", "/api/docker/images/{param}/tag"): {
            "type": "object", "properties": {"repository": {"type": "string"}, "tag": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/commit"): {
            "type": "object", "properties": {"repository": {"type": "string"}, "tag": {"type": "string"}, "comment": {"type": "string"}}
        },
    }
    for route_key, expected in crosschecked_resource_request_schemas.items():
        request_schema = merged_by_key[route_key].request_body_schema
        if request_schema != expected:
            fail(f"cross-checked resource request schema regressed for {route_key}")
        if isinstance(request_schema, dict) and "required" in request_schema:
            fail(f"cross-checked resource request schema must not invent required fields for {route_key}")

    modules_list = merged_by_key[("GET", "/api/modules/list")].response_schema
    hidden_modules_schema = (
        modules_list.get("properties", {}).get("hiddenModules")
        if isinstance(modules_list, dict)
        else None
    )
    if hidden_modules_schema != {"type": ["array", "null"], "items": {}}:
        fail("modules hiddenModules runtime evidence regressed")

    docker_images = merged_by_key[("GET", "/api/docker/images")].response_schema
    docker_image_props = (
        docker_images.get("properties", {}).get("images", {}).get("items", {}).get("properties", {})
        if isinstance(docker_images, dict)
        else {}
    )
    for field in ("Id", "Architecture"):
        if docker_image_props.get(field) != {"type": "string"}:
            fail(f"Docker image metadata string evidence regressed for {field}")
    if docker_image_props.get("RepoTags") != {"type": "array", "items": {"type": "string"}}:
        fail("Docker image RepoTags evidence regressed")

    docker_search = merged_by_key[("POST", "/api/docker/images/search")]
    if docker_search.risk is not OperationRisk.READ_ONLY:
        fail("Docker image search must remain runtime-verified read-only")
    if docker_search.request_body_schema != {
        "type": "object",
        "properties": {"limit": {"type": "integer"}, "term": {"type": "string"}},
    }:
        fail("Docker image search request schema regressed")
    if docker_search.response_schema != {
        "type": "object",
        "properties": {
            "ret": {"type": "integer"},
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "star_count": {"type": "integer"},
                        "is_official": {"type": "boolean"},
                        "name": {"type": "string"},
                        "is_automated": {"type": "boolean"},
                        "description": {"type": "string"},
                    },
                },
            },
        },
    }:
        fail("Docker image search response schema regressed")

    compose_identity_schema = {
        "type": "object",
        "properties": {
            "project_name": {"type": "string"},
            "project_path": {"type": "string"},
            "config_file_name": {"type": "string"},
        },
    }
    compose_down_schema = {
        "type": "object",
        "properties": {
            **compose_identity_schema["properties"],
            "remove_volumes": {"type": "boolean"},
        },
    }
    for route_key in {
        ("POST", "/api/docker/compose/restart"),
        ("POST", "/api/docker/compose/start"),
        ("POST", "/api/docker/compose/stop"),
        ("POST", "/api/docker/compose/stop-async"),
    }:
        if merged_by_key[route_key].request_body_schema != compose_identity_schema:
            fail(f"Docker Compose project identity request schema regressed for {route_key}")
    for route_key in {
        ("POST", "/api/docker/compose/down"),
        ("POST", "/api/docker/compose/down-async"),
    }:
        if merged_by_key[route_key].request_body_schema != compose_down_schema:
            fail(f"Docker Compose down request schema regressed for {route_key}")

    compose_projects = merged_by_key[("GET", "/api/docker/compose/projects")].response_schema
    compose_project_props = (
        compose_projects.get("properties", {}).get("projects", {}).get("items", {}).get("properties", {})
        if isinstance(compose_projects, dict)
        else {}
    )
    for field in ("name", "path", "configFileName"):
        if compose_project_props.get(field) != {"type": "string"}:
            fail(f"Docker Compose project string evidence regressed for {field}")

    compose_file_request_schemas = {
        ("POST", "/api/docker/compose/backup"): {
            "type": "object", "properties": {"project_name": {"type": "string"}, "project_path": {"type": "string"}}
        },
        ("POST", "/api/docker/compose/config"): {
            "type": "object", "properties": {"project_path": {"type": "string"}}
        },
        ("POST", "/api/docker/compose/discover"): {
            "type": "object", "properties": {"scan_path": {"type": "string"}}
        },
        ("POST", "/api/docker/compose/dockerfile"): {
            "type": "object", "properties": {"project_path": {"type": "string"}}
        },
        ("POST", "/api/docker/compose/read-file"): {
            "type": "object", "properties": {"filename": {"type": "string"}, "working_dir": {"type": "string"}}
        },
        ("POST", "/api/docker/compose/update-config"): {
            "type": "object", "properties": {"content": {"type": "string"}, "project_path": {"type": "string"}}
        },
        ("POST", "/api/docker/compose/update-dockerfile"): {
            "type": "object", "properties": {"content": {"type": "string"}, "project_path": {"type": "string"}}
        },
    }
    for route_key, expected in compose_file_request_schemas.items():
        request_schema = merged_by_key[route_key].request_body_schema
        if request_schema != expected:
            fail(f"Docker Compose file request schema regressed for {route_key}")
        if isinstance(request_schema, dict) and "required" in request_schema:
            fail(f"Docker Compose file request schema must not invent required fields for {route_key}")

    local_path_list = merged_by_key[("GET", "/api/local-path-browser/list")].response_schema
    local_path_data = (
        local_path_list.get("properties", {}).get("data", {}).get("properties", {})
        if isinstance(local_path_list, dict)
        else {}
    )
    local_path_entry = local_path_data.get("entries", {}).get("items", {}).get("properties", {})
    if local_path_data.get("path") != {"type": "string"}:
        fail("Local Path Browser path string evidence regressed")
    for field in ("name", "path"):
        if local_path_entry.get(field) != {"type": "string"}:
            fail(f"Local Path Browser entry string evidence regressed for {field}")

    docker_create_request = merged_by_key[("POST", "/api/docker/containers")].request_body_schema
    docker_create_props = docker_create_request.get("properties", {}) if isinstance(docker_create_request, dict) else {}
    expected_edit_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "config": docker_create_props.get("config"),
            "hostConfig": docker_create_props.get("hostConfig"),
            "auto_start": {"type": "boolean"},
            "remove_old": {"type": "boolean"},
        },
    }
    docker_edit = merged_by_key[("POST", "/api/docker/containers/{param}/edit")].request_body_schema
    if docker_edit != expected_edit_schema:
        fail("Docker container edit request schema must reuse the verified create-container config/hostConfig model")
    if isinstance(docker_edit, dict) and "required" in docker_edit:
        fail("Docker container edit request schema must not invent required fields")

    container_copy_rename_schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    for route_key in {
        ("POST", "/api/docker/containers/{param}/copy"),
        ("POST", "/api/docker/containers/{param}/rename"),
    }:
        if merged_by_key[route_key].request_body_schema != container_copy_rename_schema:
            fail(f"Docker container name request schema regressed for {route_key}")
    docker_container = merged_by_key[("GET", "/api/docker/containers/{param}")].response_schema
    docker_container_name = (
        docker_container.get("properties", {}).get("data", {}).get("properties", {}).get("container", {}).get("properties", {}).get("Name")
        if isinstance(docker_container, dict)
        else None
    )
    if docker_container_name != {"type": "string"}:
        fail("Docker container Name runtime evidence regressed")

    dlna_put = merged_by_key[("PUT", "/api/dlnaservice/configure")].request_body_schema
    dlna_get = merged_by_key[("GET", "/api/dlnaservice/configure")].response_schema
    dlna_config_props = (
        dlna_get.get("properties", {}).get("configure", {}).get("properties", {})
        if isinstance(dlna_get, dict)
        else {}
    )
    dlna_fields = ("Enable", "ListenIP", "ListenPort", "NetInterfaceList", "FriendlyName", "DeviceUUID", "MountList")
    expected_dlna_put = {"type": "object", "properties": {field: dlna_config_props.get(field) for field in dlna_fields}}
    if dlna_put != expected_dlna_put:
        fail("DLNA PUT request schema must match the verified GET configure projection")
    if isinstance(dlna_put, dict) and "required" in dlna_put:
        fail("DLNA PUT request schema must not invent required fields")

    read_model_put_schemas = {
        "/api/webterminal/config": "config",
        "/api/rclone/globalconfig": "globalConfig",
        "/api/ipfliter/list/{param}": "rule",
        "/api/thirdPartyAuthManager/config": "config",
        "/api/ftpserver/configure": "configure",
        "/api/smb/configure": "configure",
        "/api/webdav/configure": "configure",
        "/api/wol/service/configure": "configure",
    }
    for path, response_field in read_model_put_schemas.items():
        put_schema = merged_by_key[("PUT", path)].request_body_schema
        get_schema = merged_by_key[("GET", path)].response_schema
        expected = (
            get_schema.get("properties", {}).get(response_field)
            if isinstance(get_schema, dict)
            else None
        )
        if put_schema != expected:
            fail(f"PUT request schema must match verified GET {response_field} model for {path}")
        if isinstance(put_schema, dict) and "required" in put_schema:
            fail(f"read-model-derived PUT schema must not invent required fields for {path}")

    wol_put = merged_by_key[("PUT", "/api/wol/service/configure")].request_body_schema
    wol_server_props = (
        wol_put.get("properties", {}).get("Server", {}).get("properties", {})
        if isinstance(wol_put, dict)
        else {}
    )
    if "WebhookProxyPassword" in wol_server_props:
        fail("WOL safe read-model PUT schema must not document request-only proxy password")

    about_put = merged_by_key[("PUT", "/api/about-content")].request_body_schema
    about_get = merged_by_key[("GET", "/api/about-content")].response_schema
    if about_put != about_get:
        fail("About-content PUT request schema must match verified GET public-content model")
    if isinstance(about_put, dict) and "required" in about_put:
        fail("About-content PUT schema must not invent required fields")

    cron_group_requests = {
        ("POST", "/api/cron/groups"): {
            "type": "object",
            "properties": {"Name": {"type": "string"}},
        },
        ("PUT", "/api/cron/groups"): {
            "type": "object",
            "properties": {"Key": {"type": "string"}, "Name": {"type": "string"}},
        },
        ("PUT", "/api/cron/groups/collapsed"): {
            "type": "object",
            "properties": {"collapsed": {"type": "boolean"}, "key": {"type": "string"}},
        },
    }
    for route_key, expected in cron_group_requests.items():
        if merged_by_key[route_key].request_body_schema != expected:
            fail(f"Cron disposable-group request schema regressed for {route_key}")

    ret_only_schema = {"type": "object", "properties": {"ret": {"type": "integer"}}}
    if merged_by_key[("POST", "/api/cron/groups")].response_schema != {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "key": {"type": "string"}},
    }:
        fail("Cron group create response schema regressed")
    for route_key in {
        ("PUT", "/api/cron/groups"),
        ("PUT", "/api/cron/groups/collapsed"),
        ("DELETE", "/api/cron/groups"),
    }:
        if merged_by_key[route_key].response_schema != ret_only_schema:
            fail(f"Cron disposable-group ret-only response schema regressed for {route_key}")

    cron_groups = merged_by_key[("GET", "/api/cron/groups")].response_schema
    cron_group_item = (
        cron_groups.get("properties", {}).get("list", {}).get("items")
        if isinstance(cron_groups, dict)
        else None
    )
    if cron_group_item != {
        "type": "object",
        "properties": {"Key": {"type": "string"}, "Name": {"type": "string"}},
    }:
        fail("Cron group list item schema regressed")

    collapsed_states = merged_by_key[("GET", "/api/cron/groups/collapsed/states")].response_schema
    states_schema = (
        collapsed_states.get("properties", {}).get("states")
        if isinstance(collapsed_states, dict)
        else None
    )
    if states_schema != {"type": "object", "additionalProperties": {"type": "boolean"}}:
        fail("Cron group collapsed-state map schema regressed")

    host_kill = merged_by_key[("POST", "/api/status/host-process-kill")].request_body_schema
    if host_kill != {
        "type": "object",
        "properties": {"pid": {"type": "integer"}},
    }:
        fail("host-process kill request schema regressed")
    host_processes = merged_by_key[("GET", "/api/status/host-processes")].response_schema
    host_pid_schema = (
        host_processes.get("properties", {}).get("list", {}).get("items", {}).get("properties", {}).get("pid")
        if isinstance(host_processes, dict)
        else None
    )
    if host_pid_schema != {"type": "integer"}:
        fail("host-process list pid evidence regressed")

    local_path_requests = {
        ("POST", "/api/local-path-browser/mkdir"): {
            "type": "object",
            "properties": {"path": {"type": "string"}},
        },
        ("PUT", "/api/local-path-browser/rename"): {
            "type": "object",
            "properties": {"path": {"type": "string"}, "newName": {"type": "string"}},
        },
        ("DELETE", "/api/local-path-browser/path"): {
            "type": "object",
            "properties": {"confirmName": {"type": "string"}, "path": {"type": "string"}},
        },
    }
    for route_key, expected in local_path_requests.items():
        if merged_by_key[route_key].request_body_schema != expected:
            fail(f"Local Path Browser disposable-probe request schema regressed for {route_key}")

    path_response_schema = {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "path": {"type": "string"}},
    }
    for route_key in {
        ("POST", "/api/local-path-browser/mkdir"),
        ("PUT", "/api/local-path-browser/rename"),
    }:
        if merged_by_key[route_key].response_schema != path_response_schema:
            fail(f"Local Path Browser path response schema regressed for {route_key}")
    if merged_by_key[("DELETE", "/api/local-path-browser/path")].response_schema != ret_only_schema:
        fail("Local Path Browser delete response schema regressed")

    response_schema_count = sum(route.response_schema is not None for route in merged.routes)
    if response_schema_count < 237:
        fail(f"response-schema coverage regressed below 237 routes: {response_schema_count}")

    safe_utility_response_routes = {
        ("GET", "/api/baseconfigure"),
        ("GET", "/api/docker/info"),
        ("GET", "/api/ipfliter/porttrap/blockedips"),
        ("GET", "/api/ipfliter/porttrap/blockedips/search"),
        ("GET", "/api/cron/expressioncheck"),
        ("GET", "/api/cron/groups"),
        ("GET", "/api/cron/groups/collapsed/states"),
        ("GET", "/api/cron/groups/taskcount"),
        ("GET", "/api/modules/{param}/2fa/status"),
        ("GET", "/api/webservice/cgi/list"),
        ("GET", "/api/webservice/groups/subrulecount"),
        ("GET", "/api/webservice/statistics/ip-profile"),
        ("GET", "/api/login/challenge"),
        ("GET", "/api/ipregtest"),
        ("GET", "/api/webservice/statistics/recent-ips/visits"),
        ("GET", "/api/ssl/lastlogs"),
        ("GET", "/api/ssl/logs"),
        ("GET", "/api/ssl/syncclients"),
        ("GET", "/api/thirdPartyAuthManager/list"),
        ("GET", "/api/thirdPartyAuthManager/config"),
        ("GET", "/api/webservice/webauth/sessions"),
        ("GET", "/api/webterminal/config"),
        ("GET", "/api/webterminal/connections"),
        ("GET", "/api/webterminal/globalshortcuts"),
        ("GET", "/api/webterminal/sessions"),
        ("GET", "/api/webterminal/shells"),
        ("GET", "/api/webterminal/splitlayout"),
    }
    for route_key in safe_utility_response_routes:
        if not isinstance(merged_by_key[route_key].response_schema, dict):
            fail(f"safe utility response schema missing for {route_key}")

    baseconfigure = merged_by_key[("GET", "/api/baseconfigure")].response_schema
    baseconfigure_props = (
        baseconfigure.get("properties", {}).get("baseconfigure", {}).get("properties", {})
        if isinstance(baseconfigure, dict)
        else {}
    )
    expected_safe_baseconfigure_fields = {
        "AdminWebListenPort", "AdminWebListenTLS", "AdminWebListenHttpsPort", "ForceHTTPS",
        "TokenExpirationHour", "MaxConsecutiveLoginFailures", "TimeZone", "FrontendTheme",
        "FrontendLanguage", "EnableStatusHistory", "StatusHistoryRetentionDays",
        "StatusHistorySampleIntervalSeconds",
    }
    if set(baseconfigure_props) != expected_safe_baseconfigure_fields:
        fail("baseconfigure safe response whitelist regressed")
    forbidden_baseconfigure_fields = {
        "AdminAccount", "AdminPassword", "OpenToken", "TwoFAKey", "SafeURL", "DeviceID",
        "Keys", "ThirdAuthLoginUserList", "BackendServerListBackup", "CustomDNSA", "CustomDNSB",
        "CustomDNSC", "CustomDNSD", "CustomDNSList", "OriginsList", "ProxyProtocolTrustedCIDRs",
        "GlobalNoLimitCIDRs", "StatNetInterfaceList", "DisableModules", "hiddenModules", "BackgroundImage",
    }
    if set(baseconfigure_props) & forbidden_baseconfigure_fields:
        fail("baseconfigure sensitive/network-identifying fields leaked into response schema")

    docker_info = merged_by_key[("GET", "/api/docker/info")].response_schema
    docker_info_props = (
        docker_info.get("properties", {}).get("info", {}).get("properties", {})
        if isinstance(docker_info, dict)
        else {}
    )
    expected_safe_docker_info_fields = {
        "Containers", "ContainersRunning", "ContainersPaused", "ContainersStopped", "Images",
        "MemoryLimit", "SwapLimit", "CpuCfsPeriod", "CpuCfsQuota", "CPUShares", "CPUSet",
        "PidsLimit", "IPv4Forwarding", "OomKillDisable", "Debug", "LoggingDriver",
        "CgroupDriver", "CgroupVersion", "KernelVersion", "OperatingSystem", "OSVersion",
        "OSType", "Architecture", "NCPU", "MemTotal", "ExperimentalBuild", "ServerVersion",
        "DefaultRuntime", "LiveRestoreEnabled", "Isolation",
    }
    if set(docker_info_props) != expected_safe_docker_info_fields:
        fail("Docker info safe response whitelist regressed")
    forbidden_docker_info_fields = {
        "ID", "Name", "DockerRootDir", "HttpProxy", "HttpsProxy", "NoProxy", "RegistryConfig",
        "IndexServerAddress", "Runtimes", "Swarm", "Containerd", "CDISpecDirs", "Labels",
        "GenericResources",
    }
    if set(docker_info_props) & forbidden_docker_info_fields:
        fail("Docker info host/network-identifying fields leaked into response schema")

    portforward_response_routes = {
        ("POST", "/api/portforward"),
        ("PUT", "/api/portforward"),
        ("DELETE", "/api/portforward"),
        ("GET", "/api/portforward/{param}"),
        ("GET", "/api/portforward/{param}/lastlogs"),
        ("GET", "/api/portforward/{param}/logs"),
    }
    for route_key in portforward_response_routes:
        if not isinstance(merged_by_key[route_key].response_schema, dict):
            fail(f"PortForward disposable-probe response schema missing for {route_key}")

    portforward_post = merged_by_key[("POST", "/api/portforward")].response_schema
    if portforward_post != {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "key": {"type": "string"}},
    }:
        fail("PortForward create response schema regressed")
    for route_key in {
        ("PUT", "/api/portforward"),
        ("DELETE", "/api/portforward"),
    }:
        if merged_by_key[route_key].response_schema != {
            "type": "object",
            "properties": {"ret": {"type": "integer"}},
        }:
            fail(f"PortForward ret-only write response schema regressed for {route_key}")

    portforward_detail = merged_by_key[("GET", "/api/portforward/{param}")].response_schema
    portforward_rule_props = (
        portforward_detail.get("properties", {}).get("rule", {}).get("properties", {})
        if isinstance(portforward_detail, dict)
        else {}
    )
    if "Options" in portforward_rule_props:
        fail("PortForward Options must remain omitted from response documentation because it contains encryption-key fields")
    for field in ("ForwardTypes", "TargetAddressList"):
        if portforward_rule_props.get(field) != {"type": ["array", "null"], "items": {}}:
            fail(f"PortForward nullable list item schema must remain unspecified: {field}")
    if portforward_rule_props.get("Enable") != {"type": "boolean"}:
        fail("PortForward Enable response schema regressed")

    expected_portforward_request_props = dict(portforward_rule_props)
    expected_portforward_request_props["Options"] = {"type": "object"}
    expected_portforward_request_props["LogStreamSettings"] = {"type": "object"}
    for route_key in {
        ("POST", "/api/portforward"),
        ("PUT", "/api/portforward"),
    }:
        route = merged_by_key[route_key]
        if route.request_body_schema != {"type": "object", "properties": expected_portforward_request_props}:
            fail(f"PortForward request schema regressed for {route_key}")
        if set(route.body_keys) != set(expected_portforward_request_props):
            fail(f"PortForward request schema must cover exactly the frontend body fields for {route_key}")
        if isinstance(route.request_body_schema, dict) and "required" in route.request_body_schema:
            fail(f"PortForward request schema must not invent required fields for {route_key}")

    for route_key, field in {
        ("GET", "/api/portforward/{param}/lastlogs"): "lastLogs",
        ("GET", "/api/portforward/{param}/logs"): "logs",
    }.items():
        response_schema = merged_by_key[route_key].response_schema
        collection = response_schema.get("properties", {}).get(field) if isinstance(response_schema, dict) else None
        if collection != {"type": ["array", "null"], "items": {}}:
            fail(f"PortForward disposable log item schema must remain unspecified for {route_key}")

    for route_key in {
        ("GET", "/api/ipfliter/porttrap/blockedips"),
        ("GET", "/api/ipfliter/porttrap/blockedips/search"),
    }:
        response_schema = merged_by_key[route_key].response_schema
        ips = response_schema.get("properties", {}).get("ips") if isinstance(response_schema, dict) else None
        if ips != {"type": ["array", "null"], "items": {}}:
            fail(f"blocked-IP item schema must remain unspecified for {route_key}")

    ip_profile_schema = merged_by_key[("GET", "/api/webservice/statistics/ip-profile")].response_schema
    if ip_profile_schema != {"type": "object", "properties": {"ret": {"type": "integer"}}}:
        fail("WebService empty IP-profile success schema must remain ret-only")

    login_challenge = merged_by_key[("GET", "/api/login/challenge")].response_schema
    login_challenge_props = login_challenge.get("properties", {}) if isinstance(login_challenge, dict) else {}
    if login_challenge_props != {
        "ret": {"type": "integer"},
        "challengeId": {"type": "string"},
        "expiresIn": {"type": "integer"},
        "nonce": {"type": "string"},
        "publicKey": {"type": "string"},
    }:
        fail("login challenge response schema regressed")

    ipregtest_schema = merged_by_key[("GET", "/api/ipregtest")].response_schema
    if ipregtest_schema != {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "ip": {"type": "string"}},
    }:
        fail("IP regex test response schema regressed")

    recent_visits = merged_by_key[("GET", "/api/webservice/statistics/recent-ips/visits")].response_schema
    recent_visit_props = recent_visits.get("properties", {}) if isinstance(recent_visits, dict) else {}
    if recent_visit_props.get("visits") != {"type": "array", "items": {}}:
        fail("WebService recent-IP visit item schema must remain unspecified")
    recent_item_props = recent_visit_props.get("item", {}).get("properties", {})
    if recent_item_props != {
        "clientIP": {"type": "string"},
        "clientIPGeo": {"type": "object"},
    }:
        fail("WebService recent-IP minimal profile schema regressed")

    cgi_schema = merged_by_key[("GET", "/api/webservice/cgi/list")].response_schema
    cgi_list = cgi_schema.get("properties", {}).get("list") if isinstance(cgi_schema, dict) else None
    if cgi_list != {"type": ["array", "null"], "items": {}}:
        fail("WebService CGI item schema must remain unspecified")

    twofa_status = merged_by_key[("GET", "/api/modules/{param}/2fa/status")].response_schema
    twofa_props = (
        twofa_status.get("properties", {}).get("data", {}).get("properties", {})
        if isinstance(twofa_status, dict)
        else {}
    )
    if set(twofa_props) != {"enable", "validated", "hasKey"} or any(
        twofa_props.get(field) != {"type": "boolean"} for field in ("enable", "validated", "hasKey")
    ):
        fail("module 2FA status schema must remain boolean-only and secret-free")

    auth_manager_config = merged_by_key[("GET", "/api/thirdPartyAuthManager/config")].response_schema
    auth_manager_props = (
        auth_manager_config.get("properties", {}).get("config", {}).get("properties", {})
        if isinstance(auth_manager_config, dict)
        else {}
    )
    expected_auth_manager_fields = {
        "GithubRedirectURI",
        "GithubClientID",
        "GoogleRedirectURI",
        "GoogleClientID",
        "QQRedirectURI",
        "QQClientID",
        "WeiboRedirectURI",
        "WeiboClientKey",
        "AuthentikRedirectURI",
        "AuthentikClientID",
        "AuthentikServer",
        "OIDCRedirectURI",
        "OIDCClientID",
        "OIDCAuthorizationEndpoint",
    }
    if set(auth_manager_props) != expected_auth_manager_fields or any(
        value != {"type": "string"} for value in auth_manager_props.values()
    ):
        fail("third-party auth public metadata schema regressed or gained secret-bearing fields")
    if any("secret" in field.lower() or "token" in field.lower() or "password" in field.lower() for field in auth_manager_props):
        fail("third-party auth config schema must remain secret/token/password-free")

    webauth_sessions = merged_by_key[("GET", "/api/webservice/webauth/sessions")].response_schema
    webauth_props = webauth_sessions.get("properties", {}) if isinstance(webauth_sessions, dict) else {}
    if webauth_props.get("list") != {"type": "array", "items": {}}:
        fail("WebAuth session item schema must remain unspecified")
    for field in ("page", "pageSize", "total"):
        if webauth_props.get(field) != {"type": "integer"}:
            fail(f"WebAuth session pagination field regressed: {field}")

    webterminal_config = merged_by_key[("GET", "/api/webterminal/config")].response_schema
    webterminal_config_props = (
        webterminal_config.get("properties", {}).get("config", {}).get("properties", {})
        if isinstance(webterminal_config, dict)
        else {}
    )
    if set(webterminal_config_props) != {
        "idleTimeout",
        "bufferSize",
        "heartbeatInterval",
        "maxSessions",
        "sessionKeepAlive",
    } or any(value != {"type": "integer"} for value in webterminal_config_props.values()):
        fail("WebTerminal safe numeric config schema regressed")

    for route_key in {
        ("GET", "/api/webterminal/connections"),
        ("GET", "/api/webterminal/sessions"),
    }:
        response_schema = merged_by_key[route_key].response_schema
        collection = response_schema.get("properties", {}).get("list") if isinstance(response_schema, dict) else None
        if collection != {"type": ["array", "null"], "items": {}}:
            fail(f"WebTerminal session/connection item schema must remain unspecified for {route_key}")

    shortcuts = merged_by_key[("GET", "/api/webterminal/globalshortcuts")].response_schema
    shortcut_items = shortcuts.get("properties", {}).get("shortcuts") if isinstance(shortcuts, dict) else None
    if shortcut_items != {"type": ["array", "null"], "items": {}}:
        fail("WebTerminal shortcut command/key item schema must remain unspecified")

    shells = merged_by_key[("GET", "/api/webterminal/shells")].response_schema
    shell_props = (
        shells.get("properties", {}).get("shells", {}).get("items", {}).get("properties", {})
        if isinstance(shells, dict)
        else {}
    )
    if shell_props != {"name": {"type": "string"}, "platform": {"type": "string"}}:
        fail("WebTerminal shell schema must remain path-free")

    splitlayout = merged_by_key[("GET", "/api/webterminal/splitlayout")].response_schema
    splitlayout_props = splitlayout.get("properties", {}) if isinstance(splitlayout, dict) else {}
    if splitlayout_props.get("layout") != {"type": ["object", "null"]}:
        fail("WebTerminal split-layout details must remain unspecified")

    nullable_list_response_routes = {
        ("GET", "/api/portforwards"): ("list", "Moduledisable"),
        ("GET", "/api/portforwards_lite"): ("list", "Moduledisable"),
        ("GET", "/api/stunrulelist"): ("list", "ModuleEnable"),
        ("GET", "/api/stunrulelist_lite"): ("list", "ModuleEnable"),
        ("GET", "/api/ipdb/avalidDBFiles"): ("list", None),
        ("GET", "/api/ssl/syncclients"): ("list", None),
        ("GET", "/api/thirdPartyAuthManager/list"): ("list", None),
    }
    for route_key, (list_field, flag_field) in nullable_list_response_routes.items():
        response_schema = merged_by_key[route_key].response_schema
        props = response_schema.get("properties", {}) if isinstance(response_schema, dict) else {}
        if props.get(list_field) != {"type": ["array", "null"], "items": {}}:
            fail(f"nullable list schema regressed for {route_key}")
        if flag_field is not None and props.get(flag_field) != {"type": "boolean"}:
            fail(f"module enable/disable flag schema regressed for {route_key}")

    for route_key in {
        ("GET", "/api/rclone/third/115pan/authuserlist"),
        ("GET", "/api/rclone/third/alipan/authuserlist"),
        ("GET", "/api/rclone/third/baidupan/authuserlist"),
    }:
        response_schema = merged_by_key[route_key].response_schema
        data_schema = response_schema.get("properties", {}).get("data") if isinstance(response_schema, dict) else None
        if data_schema != {"type": ["array", "null"], "items": {}}:
            fail(f"Rclone auth-user item schema must remain unspecified for {route_key}")

    expected_rclone_authurl_schema = {
        "type": "object",
        "properties": {
            "ret": {"type": "integer"},
            "authurl": {"type": "string"},
            "tmpkey": {"type": "string"},
        },
    }
    for route_key in {
        ("GET", "/api/rclone/third/115pan/authurl"),
        ("GET", "/api/rclone/third/alipan/authurl"),
        ("GET", "/api/rclone/third/baidupan/authurl"),
    }:
        if merged_by_key[route_key].response_schema != expected_rclone_authurl_schema:
            fail(f"Rclone authorization-URL response schema regressed for {route_key}")

    storage_auth_schema = merged_by_key[("GET", "/api/storagemanagement/aliyunpan_auth")].response_schema
    if storage_auth_schema != {
        "type": "object",
        "properties": {
            "ret": {"type": "integer"},
            "url": {"type": "string"},
            "key": {"type": "string"},
        },
    }:
        fail("storage-management AliyunPan authorization-URL response schema regressed")

    docker_resource_response_routes = {
        ("POST", "/api/docker/containers"),
        ("POST", "/api/docker/containers/{param}/start"),
        ("DELETE", "/api/docker/containers/{param}"),
        ("DELETE", "/api/docker/images/remove"),
        ("GET", "/api/docker/containers/{param}/processes"),
        ("GET", "/api/docker/containers/{param}/logs"),
        ("POST", "/api/docker/images/pull"),
        ("GET", "/api/docker/images/{param}"),
        ("GET", "/api/docker/images/{param}/history"),
        ("GET", "/api/docker/images/containers"),
        ("GET", "/api/docker/containers/{param}/stats"),
        ("GET", "/api/docker/containers/{param}/stats-cached"),
        ("GET", "/api/docker/container-groups/count"),
        ("GET", "/api/docker/compose/{param}/backups"),
        ("GET", "/api/docker/compose/{param}/ps"),
        ("GET", "/api/docker/labels/{param}/containers"),
        ("GET", "/api/docker/volumes/{param}/backups"),
    }
    for route_key in docker_resource_response_routes:
        if not isinstance(merged_by_key[route_key].response_schema, dict):
            fail(f"Docker resource response schema missing for {route_key}")

    docker_pull = merged_by_key[("POST", "/api/docker/images/pull")]
    if docker_pull.request_body_schema != {
        "type": "object",
        "properties": {"image": {"type": "string"}, "tag": {"type": "string"}},
    }:
        fail("Docker image pull request schema regressed")
    if docker_pull.response_schema != {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "output": {"type": "string"}},
    }:
        fail("Docker image pull response schema regressed")

    docker_create_response = merged_by_key[("POST", "/api/docker/containers")].response_schema
    if docker_create_response != {
        "type": "object",
        "properties": {
            "ret": {"type": "integer"},
            "container_id": {"type": "string"},
            "warnings": {"type": "array", "items": {}},
        },
    }:
        fail("Docker disposable create response schema regressed")

    docker_ret_only = {"type": "object", "properties": {"ret": {"type": "integer"}}}
    for route_key in {
        ("POST", "/api/docker/containers/{param}/start"),
        ("DELETE", "/api/docker/containers/{param}"),
    }:
        if merged_by_key[route_key].response_schema != docker_ret_only:
            fail(f"Docker disposable lifecycle ret-only response schema regressed for {route_key}")

    docker_remove_image = merged_by_key[("DELETE", "/api/docker/images/remove")].response_schema
    if docker_remove_image != {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "removed": {"type": "array", "items": {}}},
    }:
        fail("Docker image-remove response schema regressed")

    docker_processes = merged_by_key[("GET", "/api/docker/containers/{param}/processes")].response_schema
    if docker_processes != {
        "type": "object",
        "properties": {
            "ret": {"type": "integer"},
            "processes": {
                "type": "object",
                "properties": {
                    "Titles": {"type": "array", "items": {"type": "string"}},
                    "Processes": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
                },
            },
        },
    }:
        fail("Docker process-table response schema regressed")

    docker_logs = merged_by_key[("GET", "/api/docker/containers/{param}/logs")].response_schema
    if docker_logs != {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "logs": {"type": "string"}},
    }:
        fail("Docker logs response schema regressed")

    docker_file_requests = {
        ("POST", "/api/docker/containers/{param}/files/mkdir"): {
            "type": "object", "properties": {"path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/touch"): {
            "type": "object", "properties": {"path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/write"): {
            "type": "object", "properties": {"content": {"type": "string"}, "path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/rename"): {
            "type": "object", "properties": {"new_path": {"type": "string"}, "old_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/copy"): {
            "type": "object", "properties": {"dst_path": {"type": "string"}, "src_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/chmod"): {
            "type": "object", "properties": {"path": {"type": "string"}, "permissions": {"type": "string"}}
        },
        ("DELETE", "/api/docker/containers/{param}/files"): {
            "type": "object", "properties": {"path": {"type": "string"}, "recursive": {"type": "boolean"}}
        },
        ("POST", "/api/docker/containers/{param}/files/compress"): {
            "type": "object", "properties": {"output_name": {"type": "string"}, "output_path": {"type": "string"}, "paths": {"type": "array", "items": {"type": "string"}}}
        },
        ("POST", "/api/docker/containers/{param}/files/compress-async"): {
            "type": "object", "properties": {"output_name": {"type": "string"}, "output_path": {"type": "string"}, "paths": {"type": "array", "items": {"type": "string"}}}
        },
        ("POST", "/api/docker/containers/{param}/files/decompress"): {
            "type": "object", "properties": {"file_path": {"type": "string"}, "output_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/decompress-async"): {
            "type": "object", "properties": {"file_path": {"type": "string"}, "output_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/search"): {
            "type": "object", "properties": {"file_type": {"type": "string"}, "keyword": {"type": "string"}, "max_depth": {"type": "integer"}, "max_result": {"type": "integer"}, "path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/label"): {
            "type": "object", "properties": {"label": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/restart"): {
            "type": "object", "properties": {"timeout": {"type": "integer"}}
        },
        ("POST", "/api/docker/containers/{param}/stop"): {
            "type": "object", "properties": {"timeout": {"type": "integer"}}
        },
    }
    for route_key, expected in docker_file_requests.items():
        if merged_by_key[route_key].request_body_schema != expected:
            fail(f"Docker disposable file request schema regressed for {route_key}")

    docker_file_path_response = {
        "type": "object",
        "properties": {"ret": {"type": "integer"}, "msg": {"type": "string"}, "path": {"type": "string"}},
    }
    for route_key in {
        ("POST", "/api/docker/containers/{param}/files/mkdir"),
        ("POST", "/api/docker/containers/{param}/files/touch"),
        ("POST", "/api/docker/containers/{param}/files/write"),
        ("DELETE", "/api/docker/containers/{param}/files"),
    }:
        if merged_by_key[route_key].response_schema != docker_file_path_response:
            fail(f"Docker disposable file path response schema regressed for {route_key}")

    docker_file_responses = {
        ("GET", "/api/docker/containers/{param}/files/list"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "output": {"type": "string"}, "path": {"type": "string"}}
        },
        ("GET", "/api/docker/containers/{param}/files/read"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "content": {"type": "string"}, "path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/rename"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "msg": {"type": "string"}, "new_path": {"type": "string"}, "old_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/copy"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "msg": {"type": "string"}, "dst_path": {"type": "string"}, "src_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/chmod"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "msg": {"type": "string"}, "path": {"type": "string"}, "permissions": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/compress"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "command": {"type": "string"}, "msg": {"type": "string"}, "output_name": {"type": "string"}, "output_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/decompress"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "command": {"type": "string"}, "file_path": {"type": "string"}, "msg": {"type": "string"}, "output_path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/files/search"): {
            "type": "object", "properties": {"ret": {"type": "integer"}, "command": {"type": "string"}, "count": {"type": "integer"}, "files": {"type": "array", "items": {}}, "keyword": {"type": "string"}, "limit": {"type": "integer"}, "path": {"type": "string"}}
        },
        ("POST", "/api/docker/containers/{param}/label"): docker_ret_only,
        ("POST", "/api/docker/containers/{param}/restart"): docker_ret_only,
        ("POST", "/api/docker/containers/{param}/stop"): docker_ret_only,
    }
    for route_key, expected in docker_file_responses.items():
        if merged_by_key[route_key].response_schema != expected:
            fail(f"Docker disposable file response schema regressed for {route_key}")

    docker_file_search = merged_by_key[("POST", "/api/docker/containers/{param}/files/search")]
    if docker_file_search.risk is not OperationRisk.READ_ONLY:
        fail("Docker container file search must remain runtime-verified read-only")
    search_files = (
        docker_file_search.response_schema.get("properties", {}).get("files")
        if isinstance(docker_file_search.response_schema, dict)
        else None
    )
    if search_files != {"type": "array", "items": {}}:
        fail("Docker file-search item schema must remain unspecified")
    for route_key in {
        ("POST", "/api/docker/containers/{param}/files/compress-async"),
        ("POST", "/api/docker/containers/{param}/files/decompress-async"),
    }:
        if merged_by_key[route_key].response_schema is not None:
            fail(f"Docker async file route must not claim an unverified response schema for {route_key}")

    image_schema = merged_by_key[("GET", "/api/docker/images/{param}")].response_schema
    image_props = image_schema.get("properties", {}).get("image", {}).get("properties", {}) if isinstance(image_schema, dict) else {}
    if "Config" in image_props:
        fail("Docker image inspect schema must not document Config/env/volume/port details")
    if image_props.get("RepoTags") != {"type": "array", "items": {"type": "string"}}:
        fail("Docker image RepoTags schema regressed")

    history_schema = merged_by_key[("GET", "/api/docker/images/{param}/history")].response_schema
    history_props = (
        history_schema.get("properties", {}).get("history", {}).get("items", {}).get("properties", {})
        if isinstance(history_schema, dict)
        else {}
    )
    if history_props.get("CreatedBy") != {"type": "string"} or history_props.get("Tags") != {
        "type": "array",
        "items": {"type": "string"},
    }:
        fail("Docker image history schema regressed")

    resource_cached_stats = merged_by_key[("GET", "/api/docker/containers/{param}/stats-cached")].response_schema
    resource_cached_props = (
        resource_cached_stats.get("properties", {}).get("data", {}).get("properties", {})
        if isinstance(resource_cached_stats, dict)
        else {}
    )
    if resource_cached_props.get("port_services") != {"type": "object"}:
        fail("Docker per-container cached-stat dynamic port map schema regressed")

    for route_key in {
        ("GET", "/api/docker/compose/{param}/backups"),
        ("GET", "/api/docker/volumes/{param}/backups"),
    }:
        response_schema = merged_by_key[route_key].response_schema
        backups = response_schema.get("properties", {}).get("backups") if isinstance(response_schema, dict) else None
        if backups != {"type": "array", "items": {}}:
            fail(f"Docker backup item schema must remain unspecified for {route_key}")

    label_containers = merged_by_key[("GET", "/api/docker/labels/{param}/containers")].response_schema
    label_container_items = (
        label_containers.get("properties", {}).get("containers")
        if isinstance(label_containers, dict)
        else None
    )
    if label_container_items != {"type": ["array", "null"], "items": {}}:
        fail("Docker label-container item schema must remain unspecified")

    compose_ps = merged_by_key[("GET", "/api/docker/compose/{param}/ps")].response_schema
    compose_ps_props = (
        compose_ps.get("properties", {}).get("containers", {}).get("items", {}).get("properties", {})
        if isinstance(compose_ps, dict)
        else {}
    )
    if set(compose_ps_props) != {"Health", "ID", "Name", "Project", "Service", "State"}:
        fail("Docker compose ps summary schema regressed")

    webservice_stat_response_routes = {
        ("GET", "/api/webservice/statistics/capabilities"),
        ("GET", "/api/webservice/statistics/daily"),
        ("GET", "/api/webservice/statistics/realtime"),
        ("GET", "/api/webservice/statistics/events"),
        ("GET", "/api/webservice/statistics/geo/aggregate"),
        ("GET", "/api/webservice/statistics/geo/rebuild/status"),
        ("GET", "/api/webservice/statistics/history"),
        ("GET", "/api/webservice/statistics/import/status"),
        ("GET", "/api/webservice/statistics/rankings"),
        ("GET", "/api/webservice/statistics/recent-ips"),
        ("GET", "/api/webservice/statistics/waf/events"),
        ("GET", "/api/webservice/statistics/waf/summary"),
        ("GET", "/api/webservice/discovery/active"),
    }
    for route_key in webservice_stat_response_routes:
        if not isinstance(merged_by_key[route_key].response_schema, dict):
            fail(f"WebService statistics response schema missing for {route_key}")

    for route_key in {
        ("GET", "/api/webservice/statistics/capabilities"),
        ("GET", "/api/webservice/statistics/daily"),
        ("GET", "/api/webservice/statistics/realtime"),
    }:
        response_schema = merged_by_key[route_key].response_schema
        top_props = response_schema.get("properties", {}) if isinstance(response_schema, dict) else {}
        if "meta" in top_props or "settings" in top_props:
            fail(f"WebService statistics sensitive config fields leaked into schema for {route_key}")

    capabilities = merged_by_key[("GET", "/api/webservice/statistics/capabilities")].response_schema
    capability_props = (
        capabilities.get("properties", {}).get("capabilities", {}).get("properties", {})
        if isinstance(capabilities, dict)
        else {}
    )
    if set(capability_props) != {
        "contractVersion",
        "timeRangeSemantics",
        "bucketBoundary",
        "granularities",
        "retention",
        "metrics",
        "filters",
        "rankingDimensions",
        "geoDimensions",
    }:
        fail("WebService statistics capabilities schema must remain contract-only")

    realtime = merged_by_key[("GET", "/api/webservice/statistics/realtime")].response_schema
    realtime_props = realtime.get("properties", {}) if isinstance(realtime, dict) else {}
    if realtime_props.get("lastMinute") != {"type": "array", "items": {}}:
        fail("WebService realtime lastMinute item schema must remain unspecified")

    for route_key, field in {
        ("GET", "/api/webservice/statistics/events"): "list",
        ("GET", "/api/webservice/statistics/history"): "points",
        ("GET", "/api/webservice/statistics/rankings"): "items",
        ("GET", "/api/webservice/statistics/waf/events"): "list",
    }.items():
        response_schema = merged_by_key[route_key].response_schema
        collection = response_schema.get("properties", {}).get(field) if isinstance(response_schema, dict) else None
        if collection != {"type": "array", "items": {}}:
            fail(f"empty WebService statistics collection must remain untyped for {route_key}")

    recent_ips = merged_by_key[("GET", "/api/webservice/statistics/recent-ips")].response_schema
    recent_ip_props = recent_ips.get("properties", {}) if isinstance(recent_ips, dict) else {}
    if recent_ip_props.get("items") != {"type": "array", "items": {}}:
        fail("WebService recent-IP item schema must remain unspecified")
    activity_items = recent_ip_props.get("activity", {}).get("properties", {}).get("items")
    if activity_items != {"type": "array", "items": {}}:
        fail("WebService recent-IP activity item schema must remain unspecified")

    docker_status_response_routes = {
        ("GET", "/api/netinterfaces"),
        ("GET", "/api/docker/compose/backup/status"),
        ("GET", "/api/docker/compose/containers-for-cron"),
        ("GET", "/api/docker/compose/projects"),
        ("GET", "/api/docker/container-groups"),
        ("GET", "/api/docker/container-groups/collapsed/states"),
        ("GET", "/api/docker/containers/sort-config"),
        ("GET", "/api/docker/containers/stats-cached"),
        ("GET", "/api/docker/disk-usage"),
        ("GET", "/api/docker/images/upgrade-status"),
        ("GET", "/api/docker/registry/mirrors"),
        ("GET", "/api/docker/volumes/backup/status"),
    }
    for route_key in docker_status_response_routes:
        if not isinstance(merged_by_key[route_key].response_schema, dict):
            fail(f"Docker/status response schema missing for {route_key}")

    cached_stats = merged_by_key[("GET", "/api/docker/containers/stats-cached")].response_schema
    cached_stat_item = (
        cached_stats.get("properties", {})
        .get("data", {})
        .get("additionalProperties", {})
        .get("properties", {})
        if isinstance(cached_stats, dict)
        else {}
    )
    if cached_stat_item.get("cpu_percent") != {"type": "string"} or cached_stat_item.get(
        "port_services"
    ) != {"type": "object"}:
        fail("Docker cached-stat dynamic map schema regressed")

    disk_usage = merged_by_key[("GET", "/api/docker/disk-usage")].response_schema
    disk_usage_props = (
        disk_usage.get("properties", {}).get("disk_usage", {}).get("properties", {})
        if isinstance(disk_usage, dict)
        else {}
    )
    for field in ("Images", "Containers", "Volumes", "BuildCache"):
        if disk_usage_props.get(field) != {"type": "array", "items": {}}:
            fail(f"Docker disk-usage resource detail schema must remain unspecified: {field}")

    service_response_routes = {
        ("GET", "/api/dlnaservice/configure"),
        ("GET", "/api/dlnaservice/status"),
        ("GET", "/api/dlnaservice/lastlogs"),
        ("GET", "/api/dlnaservice/logs"),
        ("GET", "/api/ftpserver/configure"),
        ("GET", "/api/ftpserver/status"),
        ("GET", "/api/ftpserver/lastlogs"),
        ("GET", "/api/ftpserver/logs"),
        ("GET", "/api/smb/configure"),
        ("GET", "/api/smb/runtime"),
        ("GET", "/api/smb/status"),
        ("GET", "/api/smb/lastlogs"),
        ("GET", "/api/smb/logs"),
        ("GET", "/api/webdav/configure"),
        ("GET", "/api/webdav/status"),
        ("GET", "/api/webdav/lastlogs"),
        ("GET", "/api/webdav/logs"),
        ("GET", "/api/wol/client/state"),
    }
    for route_key in service_response_routes:
        if not isinstance(merged_by_key[route_key].response_schema, dict):
            fail(f"service response schema missing for {route_key}")

    for route_key in {
        ("GET", "/api/ftpserver/configure"),
        ("GET", "/api/smb/configure"),
        ("GET", "/api/webdav/configure"),
    }:
        response_schema = merged_by_key[route_key].response_schema
        configure_props = response_schema.get("properties", {}).get("configure", {}).get("properties", {})
        users = configure_props.get("Users")
        if not isinstance(users, dict) or users.get("items") != {}:
            fail(f"credential-bearing user item schema must remain unspecified for {route_key}")

    expected_log_item_properties = {
        "LogContent": {"type": "string"},
        "LogTime": {"type": "string"},
        "ShowTime": {"type": "boolean"},
        "Level": {"type": "string"},
    }
    typed_log_routes = {
        ("GET", "/api/dlnaservice/lastlogs"): "lastLogs",
        ("GET", "/api/dlnaservice/logs"): "logs",
        ("GET", "/api/ftpserver/lastlogs"): "lastLogs",
        ("GET", "/api/ftpserver/logs"): "logs",
        ("GET", "/api/smb/lastlogs"): "lastLogs",
        ("GET", "/api/smb/logs"): "logs",
        ("GET", "/api/webdav/lastlogs"): "lastLogs",
        ("GET", "/api/webdav/logs"): "logs",
        ("GET", "/api/cron/lastlogs"): "lastLogs",
        ("GET", "/api/cron/logs"): "logs",
        ("GET", "/api/ddns/lastlogs"): "lastLogs",
        ("GET", "/api/ddns/logs"): "logs",
        ("GET", "/api/docker/logs"): "logs",
        ("GET", "/api/ipfliter/porttrap/logs"): "logs",
        ("GET", "/api/third/filebrowser/lastlogs"): "lastLogs",
        ("GET", "/api/third/filebrowser/logs"): "logs",
        ("GET", "/api/webservice/lastlogs"): "lastLogs",
        ("GET", "/api/webservice/logs"): "logs",
        ("GET", "/api/webterminal/logs"): "logs",
    }
    for route_key, field in typed_log_routes.items():
        response_schema = merged_by_key[route_key].response_schema
        if not isinstance(response_schema, dict):
            fail(f"typed log response schema missing for {route_key}")
        item_properties = (
            response_schema.get("properties", {})
            .get(field, {})
            .get("items", {})
            .get("properties", {})
        )
        if item_properties != expected_log_item_properties:
            fail(f"typed log item schema regressed for {route_key}")

    nullable_log_routes = {
        ("GET", "/api/coraza/logs"): "logs",
        ("GET", "/api/frp/logs"): "logs",
        ("GET", "/api/ipdb/logs"): "logs",
        ("GET", "/api/rclone/lastlogs"): "lastLogs",
        ("GET", "/api/rclone/logs"): "logs",
        ("GET", "/api/ssl/lastlogs"): "lastLogs",
        ("GET", "/api/ssl/logs"): "logs",
        ("GET", "/api/storagemanagement/lastlogs"): "lastLogs",
        ("GET", "/api/storagemanagement/logs"): "logs",
        ("GET", "/api/thirdPartyAuthManager/logs"): "logs",
        ("GET", "/api/wol/lastlogs"): "lastLogs",
        ("GET", "/api/wol/logs"): "logs",
    }
    for route_key, field in nullable_log_routes.items():
        response_schema = merged_by_key[route_key].response_schema
        if not isinstance(response_schema, dict):
            fail(f"nullable log response schema missing for {route_key}")
        collection_schema = response_schema.get("properties", {}).get(field)
        if collection_schema != {"type": ["array", "null"], "items": {}}:
            fail(f"nullable log collection schema regressed for {route_key}")

    global_logs = merged_by_key[("GET", "/api/logs")].response_schema
    if not isinstance(global_logs, dict):
        fail("global log response schema is missing")
    global_log_item = global_logs.get("properties", {}).get("logs", {}).get("items", {})
    if global_log_item.get("properties") != {
        "timestamp": {"type": "string"},
        "log": {"type": "string"},
        "time": {"type": "string"},
    }:
        fail("global log item schema regressed")

    webservice_logs = merged_by_key[("GET", "/api/webservice/logs")].response_schema
    webservice_log_props = webservice_logs.get("properties", {}) if isinstance(webservice_logs, dict) else {}
    for field, expected in {
        "hasMore": {"type": "boolean"},
        "loadedCount": {"type": "integer"},
        "totalExact": {"type": "boolean"},
    }.items():
        if webservice_log_props.get(field) != expected:
            fail(f"WebService log pagination field regressed: {field}")

    ddns_task = merged_by_key[("POST", "/api/ddns")].request_body_schema
    if not isinstance(ddns_task, dict):
        fail("DDNS task request schema is missing")
    ddns_props = ddns_task.get("properties", {})
    callback_props = (
        ddns_props.get("DNS", {}).get("properties", {}).get("Callback", {}).get("properties", {})
    )
    if callback_props.get("Headers") != {
        "type": ["array", "null"],
        "items": {"type": "string"},
    }:
        fail("DDNS callback header schema regressed")
    if ddns_props.get("TaskType", {}).get("enum") != ["IPv4", "IPv6", "IPv4&IPv6"]:
        fail("DDNS TaskType enum evidence regressed")

    web_rule = merged_by_key[("POST", "/api/webservice/rules")].request_body_schema
    if not isinstance(web_rule, dict):
        fail("WebService rule request schema is missing")
    web_rule_update = merged_by_key[("PUT", "/api/webservice/rule/{param}")].request_body_schema
    if web_rule_update != web_rule:
        fail("WebService create/update request schemas drifted apart")
    web_props = web_rule.get("properties", {})
    if web_props.get("TLSMinVersion") != {"type": "integer", "minimum": 0, "maximum": 3}:
        fail("WebService TLSMinVersion bounds regressed")
    redirect_type = (
        web_props.get("DefaultProxy", {})
        .get("properties", {})
        .get("OtherParams", {})
        .get("properties", {})
        .get("RedirectType")
    )
    if redirect_type != {"type": "string"}:
        fail("WebService DefaultProxy.OtherParams.RedirectType schema regressed")

    autorecord_schema = merged_by_key[("PUT", "/api/ipfliter/autorecordipconf")].request_body_schema
    if not isinstance(autorecord_schema, dict) or autorecord_schema.get("properties", {}).get(
        "BasicPassword"
    ) != {"type": "string"}:
        fail("IPFilter AutoRecord request schema regressed")
    porttrap_schema = merged_by_key[("PUT", "/api/ipfliter/porttrapconf")].request_body_schema
    if not isinstance(porttrap_schema, dict) or porttrap_schema.get("properties", {}).get(
        "AllowRuleKeys"
    ) != {"type": "array", "items": {"type": "string"}}:
        fail("IPFilter PortTrap request schema regressed")

    def schema_property_names(schema: object) -> set[str]:
        if isinstance(schema, list):
            names: set[str] = set()
            for entry in schema:
                names.update(schema_property_names(entry))
            return names
        if not isinstance(schema, dict):
            return set()
        names = set(schema.get("properties", {})) if isinstance(schema.get("properties"), dict) else set()
        for value in schema.values():
            if isinstance(value, (dict, list)):
                names.update(schema_property_names(value))
        return names

    ssl_setting_response = merged_by_key[("GET", "/api/ssl/setting")].response_schema
    if not isinstance(ssl_setting_response, dict):
        fail("SSL settings response schema is missing")
    ssl_setting_props = ssl_setting_response.get("properties", {})
    if ssl_setting_props.get("syncClientList") != {
        "type": ["array", "null"],
        "items": {},
    }:
        fail("SSL syncClientList response schema regressed")
    certificate_check_time = ssl_setting_props.get("certificateCheckTime", {})
    if not isinstance(certificate_check_time, dict) or "syncClientList" in certificate_check_time:
        fail("SSL syncClientList must remain a top-level settings response field")

    sensitive_response_fields = {
        ("GET", "/api/ssl"): {
            "CertBase64",
            "KeyBase64",
            "IssuerCertificate",
            "acmeDNSSecret",
            "acmeHMAC",
            "preACMEHMAC",
            "acmeProxyPassword",
            "prePrivateKeyBase64",
        },
        ("GET", "/api/ssl/setting"): {"globalPrivateKey"},
        ("GET", "/api/ssl/credential-sources"): {"secretValue", "proxyPassword"},
        ("GET", "/api/ssl/{param}"): {
            "CertBase64",
            "KeyBase64",
            "IssuerCertificate",
            "acmeDNSSecret",
            "acmeHMAC",
            "preACMEHMAC",
            "acmeProxyPassword",
            "prePrivateKeyBase64",
        },
        ("GET", "/api/ipfliter/porttrapconf"): {"WebhookProxyPassword"},
        ("GET", "/api/ipfliter/autorecordipconf"): {"BasicPassword"},
        ("GET", "/api/stun/configure"): {"WebhookProxyPassword"},
        ("GET", "/api/ddns/configure"): {"WebhookProxyPassword"},
        ("GET", "/api/ddns/credential-sources"): {"secretValue", "proxyPassword"},
        ("GET", "/api/ddns/task/{param}"): {"Secret", "HttpClientProxyPassword", "WebhookProxyPassword"},
        ("GET", "/api/wol/service/configure"): {
            "Token",
            "QuickControlSafeURL",
            "QuickControlBasicAuthPasswd",
            "WebhookProxyPassword",
        },
        ("GET", "/api/third/filebrowser/configure"): {"RedisCacheUrl"},
        ("GET", "/api/status/host-processes"): {"command"},
        ("GET", "/api/modules/list"): {"baseURL"},
    }
    for route_key, forbidden in sensitive_response_fields.items():
        response_schema = merged_by_key[route_key].response_schema
        if not isinstance(response_schema, dict):
            fail(f"protected response schema missing for {route_key}")
        leaked = schema_property_names(response_schema) & forbidden
        if leaked:
            fail(f"sensitive response fields leaked into documented schema for {route_key}: {sorted(leaked)}")

    docker_create = merged_by_key[("POST", "/api/docker/containers")].request_body_schema
    if not isinstance(docker_create, dict):
        fail("Docker create-container request schema is missing")
    docker_host_props = docker_create.get("properties", {}).get("hostConfig", {}).get("properties", {})
    restart_policy = docker_host_props.get("RestartPolicy", {}).get("properties", {})
    if restart_policy.get("Name") != {"type": "string"} or restart_policy.get(
        "MaximumRetryCount"
    ) != {"type": "integer"}:
        fail("Docker RestartPolicy nested schema regressed")
    if docker_host_props.get("Mounts", {}).get("items", {}).get("properties", {}).get(
        "ReadOnly"
    ) != {"type": "boolean"}:
        fail("Docker Mounts nested schema regressed")

    frp_proxy = merged_by_key[("POST", "/api/frp/{param}/proxies")].request_body_schema
    if not isinstance(frp_proxy, dict):
        fail("FRP proxy request schema is missing")
    frp_props = frp_proxy.get("properties", {})
    if frp_props.get("healthCheckType", {}).get("enum") != ["tcp", "http"]:
        fail("FRP health-check enum evidence regressed")
    if (
        frp_props.get("natTraversal", {})
        .get("properties", {})
        .get("disableAssistedAddrs")
        != {"type": "boolean"}
    ):
        fail("FRP natTraversal nested schema regressed")


def check_generated_artifacts() -> None:
    snapshot_path = ROOT / "evidence" / "lucky-v3-endpoints.json"
    openapi_path = ROOT / "openapi" / "lucky-v3.openapi.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    openapi = json.loads(openapi_path.read_text(encoding="utf-8"))
    check_runtime_verification(snapshot_path, snapshot)
    runtime_path = snapshot_path.with_name("lucky-v3-runtime-verification.json")
    merged_snapshot = load_merged_snapshot(snapshot_path, runtime_verification=runtime_path)
    if snapshot["route_count"] != len(snapshot["routes"]):
        fail("snapshot route_count does not match routes")
    if snapshot["bundle_count"] != len(snapshot["bundle_sha256"]):
        fail("snapshot bundle_count does not match bundle hashes")
    route_keys = [(item["path"], item["method"]) for item in snapshot["routes"]]
    if len(route_keys) != len(set(route_keys)):
        fail("snapshot contains duplicate path/method routes")
    for item in snapshot["routes"]:
        if not item["path"].startswith("/api/"):
            fail(f"snapshot contains invalid API path: {item['path']}")
        if item["method"] not in {"GET", "POST", "PUT", "DELETE", "PATCH", "UNKNOWN"}:
            fail(f"snapshot contains invalid HTTP method: {item['method']}")
    if openapi.get("openapi") != "3.1.0":
        fail("OpenAPI document is not 3.1.0")
    if openapi["components"]["securitySchemes"]["OpenToken"]["name"] != "openToken":
        fail("OpenAPI security header is incorrect")
    for server in openapi.get("servers", []):
        if "{safeEntry}" not in server["url"]:
            fail("OpenAPI server URL must use the safeEntry placeholder")
        if server.get("variables", {}).get("safeEntry", {}).get("default") != "your-safe-entry":
            fail("OpenAPI safeEntry default must remain a non-live placeholder")
    documented = {
        (path, method.upper())
        for path, item in openapi["paths"].items()
        for method in item
        if method.upper() in {"GET", "POST", "PUT", "DELETE", "PATCH"}
    }
    inferred = {
        (item["path"], item["method"])
        for item in merged_snapshot["routes"]
        if item["method"] != "UNKNOWN"
    }
    if documented != inferred:
        fail("OpenAPI paths are out of sync with the endpoint snapshot")
    operation_ids = [
        operation["operationId"]
        for item in openapi["paths"].values()
        for method, operation in item.items()
        if method.upper() in {"GET", "POST", "PUT", "DELETE", "PATCH"}
    ]
    if len(operation_ids) != len(set(operation_ids)):
        fail("OpenAPI operationId values are not unique")
    with tempfile.TemporaryDirectory() as directory:
        generated_markdown = Path(directory) / "api-routes.md"
        generated_openapi = Path(directory) / "lucky-v3.openapi.json"
        write_markdown(merged_snapshot, generated_markdown)
        write_openapi(merged_snapshot, generated_openapi)
        committed_markdown = ROOT / "docs" / "generated" / "api-routes.md"
        if generated_markdown.read_bytes() != committed_markdown.read_bytes():
            fail("generated API route Markdown is stale")
        if generated_openapi.read_bytes() != openapi_path.read_bytes():
            fail("generated OpenAPI document is stale")


def main() -> None:
    check_secrets()
    check_local_links()
    check_skill_packaging()
    check_generated_artifacts()
    print("repository verification passed")


if __name__ == "__main__":
    main()
