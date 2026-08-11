#!/usr/bin/env python3
"""Compatibility entry point for the safer tools/lucky_api.py client."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.lucky_api import main  # noqa: E402


if len(sys.argv) > 1 and sys.argv[1].startswith("/api/"):
    sys.argv.insert(1, "call")

raise SystemExit(main())
