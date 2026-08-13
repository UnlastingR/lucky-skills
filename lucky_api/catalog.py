"""Route inventory loading, matching, and conservative risk classification."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable


class CatalogError(ValueError):
    """Raised when a route catalog is unavailable or malformed."""


class OperationRisk(str, Enum):
    READ_ONLY = "read-only"
    MUTATING = "mutating"
    DANGEROUS = "dangerous"
    UNKNOWN = "unknown"


VERIFIED_READ_ONLY = {
    ("GET", "/api/status"),
    ("GET", "/api/info"),
    ("GET", "/api/modules/list"),
}

# These frontend routes use the final path parameter as the desired enabled state.
# Keep them mutating even when the optional runtime-verification sidecar is absent.
VERIFIED_MUTATING_GET_TEMPLATES = {
    "/api/cloudflared/list/{param}/{param2}",
    "/api/coraza/list/{param}/{param2}",
    "/api/frp/list/{param}/{param2}",
    "/api/ipfliter/list/{param}/{param2}/{param3}",
    "/api/rclone/remotelist/option",
    "/api/rclone/sync/option",
}

# Lucky has state-changing GET routes. Match complete path segments or well-known
# action names instead of assuming all GET requests are safe.
SIDE_EFFECT_GET_ACTIONS = {
    "acmecancel",
    "cancel",
    "clear",
    "comfire",
    "disconnect",
    "dojobs",
    "enable",
    "expanded",
    "export",
    "flush",
    "getipfromcmdtest",
    "host-process-kill",
    "ip-info-refresh",
    "ipsectionexpanded",
    "kill",
    "manualsync",
    "oneclickrecord",
    "reboot_program",
    "refresh-ipinfo",
    "reset",
    "resetadmin",
    "restoreconfigureconfirm",
    "run",
    "shutdown",
    "start",
    "stop",
    "trigger",
    "unlock",
    "wakeup",
}

DANGEROUS_SEGMENTS = {
    "attach",
    "backup",
    "chmod",
    "clear",
    "commit",
    "compress",
    "copy",
    "delete",
    "decompress",
    "disconnect",
    "down",
    "edit",
    "exec",
    "export",
    "getipfromcmdtest",
    "import",
    "kill",
    "prune",
    "reboot_program",
    "remove",
    "rename",
    "reset",
    "resetadmin",
    "restart",
    "restore",
    "shell",
    "shutdown",
    "start",
    "stop",
    "terminal",
    "unpause",
    "update",
    "upgrade",
    "upload",
    "write",
}


def _segments(path: str) -> set[str]:
    return {segment.lower() for segment in path.strip("/").split("/") if segment}


def _template_pattern(template: str) -> re.Pattern[str]:
    cursor = 0
    pieces = ["^"]
    for match in re.finditer(r"\{[^{}]+\}", template):
        pieces.append(re.escape(template[cursor : match.start()]))
        pieces.append(r"[^/?#]+")
        cursor = match.end()
    pieces.append(re.escape(template[cursor:]))
    pieces.append("$")
    return re.compile("".join(pieces))


@dataclass(frozen=True)
class Route:
    path: str
    method: str
    module: str
    confidence: str
    query_keys: tuple[str, ...]
    body_keys: tuple[str, ...]
    has_body: bool
    response_type: str
    risk_override: OperationRisk | None = None
    request_body_schema: dict | None = field(default=None, compare=False)
    request_content_type: str | None = field(default=None, compare=False)
    response_schema: dict | None = field(default=None, compare=False)
    schema_evidence: str | None = field(default=None, compare=False)

    @property
    def risk(self) -> OperationRisk:
        if self.risk_override is not None:
            return self.risk_override
        if self.method == "UNKNOWN":
            return OperationRisk.UNKNOWN
        return classify_known_operation(self.method, self.path)

    def matches(self, method: str, path: str) -> bool:
        return self.method == method.upper() and bool(_template_pattern(self.path).fullmatch(path))


def classify_known_operation(method: str, path: str) -> OperationRisk:
    method = method.upper()
    if (method, path) in VERIFIED_READ_ONLY:
        return OperationRisk.READ_ONLY
    if method == "GET" and path in VERIFIED_MUTATING_GET_TEMPLATES:
        return OperationRisk.MUTATING
    segments = _segments(path)
    if method == "GET":
        if not segments & SIDE_EFFECT_GET_ACTIONS:
            return OperationRisk.READ_ONLY
        if segments & DANGEROUS_SEGMENTS:
            return OperationRisk.DANGEROUS
        return OperationRisk.MUTATING
    return OperationRisk.DANGEROUS if segments & DANGEROUS_SEGMENTS else OperationRisk.MUTATING


def _route_module(path: str) -> str:
    parts = path.split("/")
    return parts[2] if len(parts) > 2 else "unknown"


def _apply_runtime_verification(
    raw_routes: list[dict],
    source: Path,
    *,
    version: str,
    snapshot_sha256: str,
) -> list[dict]:
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CatalogError(f"cannot read runtime route verification: {source}") from error
    if payload.get("schema_version") != 1:
        raise CatalogError("unsupported runtime route verification schema")
    target = payload.get("target", {})
    if str(target.get("version", "unknown")) != version:
        raise CatalogError(
            f"runtime route verification targets Lucky {target.get('version')}, catalog is {version}"
        )
    if payload.get("static_snapshot_sha256") != snapshot_sha256:
        raise CatalogError("runtime route verification does not match this exact static snapshot")
    suppress = payload.get("suppress_literals", [])
    verified = payload.get("routes", [])
    if not isinstance(suppress, list) or not all(isinstance(item, str) for item in suppress):
        raise CatalogError("runtime suppress_literals must be an array of paths")
    if not isinstance(verified, list):
        raise CatalogError("runtime routes must be an array")

    route_map: dict[tuple[str, str], dict] = {}
    suppress_set = set(suppress)
    static_keys: set[tuple[str, str]] = set()
    for item in raw_routes:
        if not isinstance(item, dict) or "path" not in item or "method" not in item:
            raise CatalogError("malformed route catalog entry")
        path = str(item["path"])
        method = str(item["method"]).upper()
        static_keys.add((path, method))
        if method == "UNKNOWN" and path in suppress_set:
            continue
        route_map[(path, method)] = dict(item)
    unknown_paths = {path for path, method in static_keys if method == "UNKNOWN"}
    missing_suppressions = suppress_set - unknown_paths
    if missing_suppressions:
        raise CatalogError("runtime suppression is not backed by static UNKNOWN evidence")

    for item in verified:
        if not isinstance(item, dict):
            raise CatalogError("malformed runtime route verification entry")
        try:
            path = str(item["path"])
            method = str(item["method"]).upper()
        except KeyError as error:
            raise CatalogError("runtime route verification requires path and method") from error
        if not path.startswith("/api/") or method not in {"GET", "POST", "PUT", "DELETE", "PATCH"}:
            raise CatalogError(f"invalid runtime verified route: {method} {path}")
        if (path, "UNKNOWN") not in static_keys and (path, method) not in static_keys:
            raise CatalogError("runtime verified route is not backed by the static snapshot")
        route_map.pop((path, "UNKNOWN"), None)
        base = route_map.get((path, method), {})
        merged = dict(base)
        merged.update(item)
        merged.setdefault("module", _route_module(path))
        merged.setdefault("confidence", "runtime-verified")
        merged.setdefault("query_keys", [])
        merged.setdefault("body_keys", [])
        merged.setdefault("has_body", False)
        merged.setdefault("response_type", "unknown")
        route_map[(path, method)] = merged

    return sorted(route_map.values(), key=lambda item: (str(item.get("module", "")), item["path"], item["method"]))


def load_merged_snapshot(
    path: str | Path,
    *,
    runtime_verification: str | Path | None = None,
) -> dict:
    source = Path(path).expanduser()
    try:
        source_bytes = source.read_bytes()
        payload = json.loads(source_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CatalogError(f"cannot read route catalog: {source}") from error
    raw_routes = payload.get("routes")
    if payload.get("schema_version") != 1 or not isinstance(raw_routes, list):
        raise CatalogError("unsupported route catalog schema")
    target = payload.get("target", {})
    version = str(target.get("version", "unknown"))
    if runtime_verification is not None:
        raw_routes = _apply_runtime_verification(
            raw_routes,
            Path(runtime_verification).expanduser(),
            version=version,
            snapshot_sha256=hashlib.sha256(source_bytes).hexdigest(),
        )
    merged = dict(payload)
    merged["routes"] = raw_routes
    merged["route_count"] = len(raw_routes)
    if runtime_verification is not None:
        merged["runtime_verification_applied"] = True
    return merged


class RouteCatalog:
    def __init__(self, routes: Iterable[Route], *, version: str = "unknown") -> None:
        self.routes = tuple(routes)
        self.version = version

    @classmethod
    def from_file(
        cls,
        path: str | Path,
        *,
        runtime_verification: str | Path | None = None,
    ) -> "RouteCatalog":
        payload = load_merged_snapshot(path, runtime_verification=runtime_verification)
        raw_routes = payload["routes"]
        target = payload.get("target", {})
        version = str(target.get("version", "unknown"))
        routes = []
        for item in raw_routes:
            try:
                if not isinstance(item, dict):
                    raise CatalogError("malformed route catalog entry")
                raw_risk = item.get("risk")
                risk_override = OperationRisk(str(raw_risk)) if raw_risk is not None else None
                routes.append(
                    Route(
                        path=str(item["path"]),
                        method=str(item["method"]).upper(),
                        module=str(item.get("module", "unknown")),
                        confidence=str(item.get("confidence", "unknown")),
                        query_keys=tuple(str(value) for value in item.get("query_keys", [])),
                        body_keys=tuple(str(value) for value in item.get("body_keys", [])),
                        has_body=bool(item.get("has_body", False)),
                        response_type=str(item.get("response_type", "unknown")),
                        risk_override=risk_override,
                        request_body_schema=(
                            dict(item["request_body_schema"])
                            if isinstance(item.get("request_body_schema"), dict)
                            else None
                        ),
                        request_content_type=(
                            str(item["request_content_type"])
                            if item.get("request_content_type") is not None
                            else None
                        ),
                        response_schema=(
                            dict(item["response_schema"])
                            if isinstance(item.get("response_schema"), dict)
                            else None
                        ),
                        schema_evidence=(
                            str(item["schema_evidence"])
                            if item.get("schema_evidence") is not None
                            else None
                        ),
                    )
                )
            except (KeyError, TypeError, ValueError) as error:
                raise CatalogError("malformed route catalog entry") from error
        return cls(routes, version=version)

    @classmethod
    def load_default(cls) -> "RouteCatalog":
        configured = os.environ.get("LUCKY_API_CATALOG")
        candidates = []
        if configured:
            candidates.append(Path(configured))
        candidates.extend(
            [
                Path.cwd() / "evidence" / "lucky-v3-endpoints.json",
                Path(__file__).resolve().parents[1] / "evidence" / "lucky-v3-endpoints.json",
            ]
        )
        runtime_override = os.environ.get("LUCKY_API_RUNTIME_VERIFICATION")
        for candidate in candidates:
            if candidate.is_file():
                if runtime_override:
                    runtime_path: Path | None = Path(runtime_override).expanduser()
                else:
                    sibling = candidate.with_name("lucky-v3-runtime-verification.json")
                    runtime_path = sibling if sibling.is_file() else None
                return cls.from_file(candidate, runtime_verification=runtime_path)
        raise CatalogError("route catalog not found; set LUCKY_API_CATALOG")

    def match(self, method: str, path: str) -> Route | None:
        method = method.upper()
        candidates = [route for route in self.routes if route.matches(method, path)]
        if not candidates:
            return None
        return min(candidates, key=lambda route: route.path.count("{"))

    def classify(self, method: str, path: str) -> OperationRisk:
        if (method.upper(), path) in VERIFIED_READ_ONLY:
            return OperationRisk.READ_ONLY
        route = self.match(method, path)
        return route.risk if route else OperationRisk.UNKNOWN

    def search(
        self,
        *,
        text: str = "",
        module: str | None = None,
        method: str | None = None,
        risk: OperationRisk | None = None,
    ) -> list[Route]:
        needle = text.lower()
        results = []
        for route in self.routes:
            if needle and needle not in route.path.lower():
                continue
            if module and route.module != module:
                continue
            if method and route.method != method.upper():
                continue
            if risk and route.risk is not risk:
                continue
            results.append(route)
        return results
