#!/usr/bin/env python3
"""Dependency-free repository checks used locally and in GitHub Actions."""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from extract_lucky_frontend import write_markdown, write_openapi


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
    if "defaultPrompt" in interface:
        validate_prompt_list(interface.get("defaultPrompt"), "interface.defaultPrompt")
    if "default_prompt" in interface:
        legacy = interface.get("default_prompt")
        if isinstance(legacy, list):
            validate_prompt_list(legacy, "interface.default_prompt")
        elif not isinstance(legacy, str) or not legacy.strip() or len(legacy) > 128:
            fail("Codex plugin interface.default_prompt must be a non-empty prompt or prompt list")


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


def check_generated_artifacts() -> None:
    snapshot_path = ROOT / "evidence" / "lucky-v3-endpoints.json"
    openapi_path = ROOT / "openapi" / "lucky-v3.openapi.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    openapi = json.loads(openapi_path.read_text(encoding="utf-8"))
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
        for item in snapshot["routes"]
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
        write_markdown(snapshot, generated_markdown)
        write_openapi(snapshot, generated_openapi)
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
