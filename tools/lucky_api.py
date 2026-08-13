#!/usr/bin/env python3
"""Safe command-line client for Lucky's unofficial OpenToken API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from lucky_api import LuckyClient, LuckyClientError, OperationRisk, RouteCatalog  # noqa: E402
from lucky_api.catalog import CatalogError  # noqa: E402
from tools.lucky_credentials import CredentialError, default_credentials_path, load_credentials  # noqa: E402


def parse_query(values: list[str]) -> list[tuple[str, str]]:
    result = []
    for value in values:
        if "=" not in value:
            raise ValueError(f"query must be KEY=VALUE: {value}")
        key, item = value.split("=", 1)
        if not key:
            raise ValueError("query key must not be empty")
        result.append((key, item))
    return result


def read_json_body(args: argparse.Namespace) -> Any:
    if args.json_file and args.json_stdin:
        raise ValueError("--json-file and --json-stdin are mutually exclusive")
    if args.json_file:
        text = Path(args.json_file).read_text(encoding="utf-8")
    elif args.json_stdin:
        text = sys.stdin.read()
    else:
        return None
    return json.loads(text)


def make_client(args: argparse.Namespace, catalog: RouteCatalog) -> LuckyClient:
    credentials_file = getattr(args, "credentials_file", None)
    if credentials_file is None:
        env_base_url = os.environ.get("LUCKY_BASE_URL", "").strip()
        env_open_token = os.environ.get("LUCKY_OPEN_TOKEN", "").strip()
        if env_base_url and env_open_token:
            return LuckyClient.from_environment(
                timeout=args.timeout,
                retries=args.retries,
                max_response_bytes=args.max_response_bytes,
                catalog=catalog,
            )
        if bool(env_base_url) != bool(env_open_token):
            raise CredentialError(
                "incomplete Lucky credential environment; set both LUCKY_BASE_URL and "
                "LUCKY_OPEN_TOKEN, unset both, or use --credentials-file"
            )
    values = load_credentials(Path(credentials_file) if credentials_file else default_credentials_path())
    return LuckyClient(
        values["base_url"],
        values["open_token"],
        timeout=args.timeout,
        retries=args.retries,
        max_response_bytes=args.max_response_bytes,
        catalog=catalog,
    )


def print_response(response: Any, output: str | None) -> None:
    if output:
        target = Path(output)
        target.write_bytes(response.body)
        print(f"wrote {len(response.body)} bytes to {target}", file=sys.stderr)
        return
    if response.is_json:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        return
    if sys.stdout.isatty():
        raise ValueError("binary response requires --output FILE")
    sys.stdout.buffer.write(response.body)


def command_call(args: argparse.Namespace, catalog: RouteCatalog) -> int:
    method = args.method.upper()
    risk = catalog.classify(method, args.path)
    if risk is not OperationRisk.READ_ONLY:
        expected = f"{method} {args.path}"
        if not args.allow_write or args.confirm != expected:
            raise ValueError(
                f"{risk.value} operation requires --allow-write --confirm {expected!r}"
            )
    json_body = read_json_body(args)
    kwargs: dict[str, Any] = {
        "query": parse_query(args.query),
        "allow_unsafe": risk is not OperationRisk.READ_ONLY,
    }
    if args.json_file or args.json_stdin:
        kwargs["json_body"] = json_body
    if args.raw_file:
        if args.json_file or args.json_stdin:
            raise ValueError("JSON and raw request bodies are mutually exclusive")
        kwargs["raw_body"] = Path(args.raw_file).read_bytes()
        kwargs["content_type"] = args.content_type
    response = make_client(args, catalog).request(method, args.path, **kwargs)
    if args.show_meta:
        rate = response.rate_limit
        print(
            f"HTTP {response.status}; content-type={response.content_type}; "
            f"rate-limit={rate.limit}; remaining={rate.remaining}; reset={rate.reset_seconds}",
            file=sys.stderr,
        )
    print_response(response, args.output)
    return 0


def command_catalog(args: argparse.Namespace, catalog: RouteCatalog) -> int:
    risk = OperationRisk(args.risk) if args.risk else None
    routes = catalog.search(text=args.search, module=args.module, method=args.method, risk=risk)
    if args.json:
        payload = [
            {
                "method": route.method,
                "path": route.path,
                "module": route.module,
                "risk": route.risk.value,
                "query_keys": list(route.query_keys),
                "body_keys": list(route.body_keys),
                "has_body": route.has_body,
                "response_type": route.response_type,
                "response_content_type": route.response_content_type,
                "request_body_schema": route.request_body_schema,
                "request_content_type": route.request_content_type,
                "response_schema": route.response_schema,
                "schema_evidence": route.schema_evidence,
                "success_response_markers": [
                    {"ret": ret, "msg": msg} for ret, msg in route.success_response_markers
                ],
                "confidence": route.confidence,
            }
            for route in routes
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for route in routes:
            print(f"{route.method:7} {route.risk.value:10} {route.path}")
    print(f"{len(routes)} route(s), catalog version {catalog.version}", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-file", type=Path, help="override the endpoint evidence JSON")
    parser.add_argument(
        "--credentials-file",
        type=Path,
        help=f"override the private credential file (default when env is unset: {default_credentials_path()})",
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--retries", type=int, default=2, help="read-only 429/502/503/504 retries")
    parser.add_argument("--max-response-bytes", type=int, default=16 * 1024 * 1024)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, path in (("status", "/api/status"), ("info", "/api/info"), ("modules", "/api/modules/list")):
        shortcut = subparsers.add_parser(name, help=f"GET {path}")
        shortcut.set_defaults(shortcut_path=path)
        shortcut.add_argument("--output")
        shortcut.add_argument("--show-meta", action="store_true")

    call = subparsers.add_parser("call", help="call an arbitrary cataloged API route")
    call.add_argument("path")
    call.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "DELETE", "PATCH"])
    call.add_argument("--query", action="append", default=[], metavar="KEY=VALUE")
    call.add_argument("--json-file", metavar="FILE")
    call.add_argument("--json-stdin", action="store_true")
    call.add_argument("--raw-file", metavar="FILE")
    call.add_argument("--content-type")
    call.add_argument("--output", metavar="FILE")
    call.add_argument("--show-meta", action="store_true")
    call.add_argument("--allow-write", action="store_true")
    call.add_argument("--confirm", help="exact confirmation, for example 'PUT /api/ddns'")

    catalog = subparsers.add_parser("catalog", help="search the local endpoint inventory")
    catalog.add_argument("--search", default="")
    catalog.add_argument("--module")
    catalog.add_argument("--method", choices=["GET", "POST", "PUT", "DELETE", "PATCH", "UNKNOWN"])
    catalog.add_argument("--risk", choices=[item.value for item in OperationRisk])
    catalog.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.catalog_file:
            runtime_path = args.catalog_file.with_name("lucky-v3-runtime-verification.json")
            catalog = RouteCatalog.from_file(
                args.catalog_file,
                runtime_verification=runtime_path if runtime_path.is_file() else None,
            )
        else:
            catalog = RouteCatalog.load_default()
        if args.command == "catalog":
            return command_catalog(args, catalog)
        if hasattr(args, "shortcut_path"):
            args.path = args.shortcut_path
            args.method = "GET"
            args.query = []
            args.json_file = None
            args.json_stdin = False
            args.raw_file = None
            args.content_type = None
            args.allow_write = False
            args.confirm = None
        return command_call(args, catalog)
    except (CatalogError, CredentialError, LuckyClientError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
