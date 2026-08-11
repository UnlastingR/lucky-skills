#!/usr/bin/env python3
"""Dependency-free repository checks used locally and in GitHub Actions."""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

from extract_lucky_frontend import write_markdown, write_openapi


ROOT = Path(__file__).resolve().parents[1]
TOKEN_ASSIGNMENT = re.compile(
    r"(?i)(?:open[_-]?token|authorization)\s*[:=]\s*[\"']?(?!\$\{|<|your-|example|replace)[A-Za-z0-9_-]{24,}"
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")
SKILL_FRONTMATTER = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


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
    if manifest.get("name") != "lucky-skills":
        fail("Codex plugin name must be 'lucky-skills'")
    version = manifest.get("version", "")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        fail("Codex plugin version must use strict semver")
    if not manifest.get("description"):
        fail("Codex plugin description is required")
    author = manifest.get("author")
    if not isinstance(author, dict) or not author.get("name"):
        fail("Codex plugin author.name is required")
    if manifest.get("skills") != "./skills/":
        fail("Codex plugin skills must use the supported ./skills/ directory")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("Codex plugin interface metadata is required")
    required_interface_fields = {
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "defaultPrompt",
    }
    missing = sorted(field for field in required_interface_fields if not interface.get(field))
    if missing:
        fail(f"Codex plugin interface is missing required fields: {', '.join(missing)}")
    capabilities = interface["capabilities"]
    if not isinstance(capabilities, list) or not all(isinstance(item, str) and item for item in capabilities):
        fail("Codex plugin interface.capabilities must be a non-empty string array")
    default_prompt = interface["defaultPrompt"]
    if not isinstance(default_prompt, list) or not 1 <= len(default_prompt) <= 3:
        fail("Codex plugin interface.defaultPrompt must contain 1 to 3 prompts")
    if not all(isinstance(item, str) and 0 < len(item) <= 128 for item in default_prompt):
        fail("Codex plugin default prompts must be non-empty strings up to 128 characters")
    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        value = interface.get(field)
        if value is not None and (not isinstance(value, str) or not value.startswith("https://")):
            fail(f"Codex plugin interface.{field} must be an absolute https URL when present")


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
