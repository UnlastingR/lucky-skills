from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from lucky_api import Route, RouteCatalog
from tools.lucky_api import command_call, parse_query, read_json_body


class CLITests(unittest.TestCase):
    def test_query_parsing_preserves_repeated_keys(self) -> None:
        self.assertEqual(
            parse_query(["tag=one", "tag=two", "empty="]),
            [("tag", "one"), ("tag", "two"), ("empty", "")],
        )
        with self.assertRaises(ValueError):
            parse_query(["missing-separator"])

    def test_json_file_and_stdin_are_mutually_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "body.json"
            source.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_json_body(Namespace(json_file=str(source), json_stdin=True))

    def test_write_requires_exact_confirmation(self) -> None:
        catalog = RouteCatalog(
            [Route("/api/ddns", "PUT", "ddns", "test", (), (), True, "json")]
        )
        base = {
            "method": "PUT",
            "path": "/api/ddns",
            "allow_write": True,
            "confirm": "PUT /api/other",
        }
        with self.assertRaises(ValueError) as context:
            command_call(Namespace(**base), catalog)
        self.assertIn("--confirm 'PUT /api/ddns'", str(context.exception))


if __name__ == "__main__":
    unittest.main()
