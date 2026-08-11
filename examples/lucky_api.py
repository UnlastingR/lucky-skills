#!/usr/bin/env python3
"""Small Lucky OpenToken client with a conservative read-only default."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


SIDE_EFFECT_GET_MARKERS = (
    "/enable",
    "/manualsync",
    "/dojobs",
    "/trigger",
    "/wakeup",
    "/shutdown",
    "/reboot_program",
    "/flush",
    "/download",
    "/refresh",
    "/reset",
    "/kill",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="API path beginning with /api/")
    parser.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "DELETE", "PATCH"])
    parser.add_argument("--data", help="JSON request body")
    parser.add_argument("--allow-write", action="store_true", help="required for non-read-only calls")
    args = parser.parse_args()

    if not args.path.startswith("/api/"):
        parser.error("path must begin with /api/")
    risky_get = any(marker in args.path.lower() for marker in SIDE_EFFECT_GET_MARKERS)
    if not args.allow_write and (args.method != "GET" or args.data or risky_get):
        parser.error("request may change state; review it and pass --allow-write explicitly")

    base_url = os.environ.get("LUCKY_BASE_URL", "").rstrip("/")
    token = os.environ.get("LUCKY_OPEN_TOKEN", "")
    if not base_url or not token:
        parser.error("LUCKY_BASE_URL and LUCKY_OPEN_TOKEN are required")

    body = args.data.encode() if args.data else None
    headers = {"openToken": token, "Accept": "application/json"}
    if body is not None:
        json.loads(args.data)
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(base_url + args.path, data=body, headers=headers, method=args.method)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            content = response.read()
            content_type = response.headers.get_content_type()
    except urllib.error.HTTPError as error:
        content = error.read()
        print(content.decode(errors="replace"), file=sys.stderr)
        raise SystemExit(error.code)

    if content_type == "application/json":
        payload = json.loads(content)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if isinstance(payload, dict) and payload.get("ret", 0) != 0:
            raise SystemExit(1)
    else:
        sys.stdout.buffer.write(content)


if __name__ == "__main__":
    main()
