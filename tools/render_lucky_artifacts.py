#!/usr/bin/env python3
"""Render Markdown and OpenAPI artifacts from a committed endpoint snapshot."""

from __future__ import annotations

import argparse
from pathlib import Path

from extract_lucky_frontend import write_markdown, write_openapi
from lucky_api import load_merged_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--openapi", type=Path, required=True)
    args = parser.parse_args()
    runtime_path = args.snapshot.with_name("lucky-v3-runtime-verification.json")
    snapshot = load_merged_snapshot(
        args.snapshot,
        runtime_verification=runtime_path if runtime_path.is_file() else None,
    )
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.openapi.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(snapshot, args.markdown)
    write_openapi(snapshot, args.openapi)


if __name__ == "__main__":
    main()
