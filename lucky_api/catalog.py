"""Route inventory loading, matching, and conservative risk classification."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
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
    "flush",
    "host-process-kill",
    "ip-info-refresh",
    "ipsectionexpanded",
    "kill",
    "manualsync",
    "reboot_program",
    "refresh-ipinfo",
    "reset",
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
    "import",
    "kill",
    "prune",
    "reboot_program",
    "remove",
    "rename",
    "reset",
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

    @property
    def risk(self) -> OperationRisk:
        return classify_known_operation(self.method, self.path)

    def matches(self, method: str, path: str) -> bool:
        return self.method == method.upper() and bool(_template_pattern(self.path).fullmatch(path))


def classify_known_operation(method: str, path: str) -> OperationRisk:
    method = method.upper()
    if (method, path) in VERIFIED_READ_ONLY:
        return OperationRisk.READ_ONLY
    segments = _segments(path)
    if method == "GET":
        if not segments & SIDE_EFFECT_GET_ACTIONS:
            return OperationRisk.READ_ONLY
        if segments & DANGEROUS_SEGMENTS:
            return OperationRisk.DANGEROUS
        return OperationRisk.MUTATING
    return OperationRisk.DANGEROUS if segments & DANGEROUS_SEGMENTS else OperationRisk.MUTATING


class RouteCatalog:
    def __init__(self, routes: Iterable[Route], *, version: str = "unknown") -> None:
        self.routes = tuple(routes)
        self.version = version

    @classmethod
    def from_file(cls, path: str | Path) -> "RouteCatalog":
        source = Path(path).expanduser()
        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise CatalogError(f"cannot read route catalog: {source}") from error
        raw_routes = payload.get("routes")
        if payload.get("schema_version") != 1 or not isinstance(raw_routes, list):
            raise CatalogError("unsupported route catalog schema")
        routes = []
        for item in raw_routes:
            try:
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
                    )
                )
            except (KeyError, TypeError) as error:
                raise CatalogError("malformed route catalog entry") from error
        target = payload.get("target", {})
        return cls(routes, version=str(target.get("version", "unknown")))

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
        for candidate in candidates:
            if candidate.is_file():
                return cls.from_file(candidate)
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
