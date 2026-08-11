from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.extract_lucky_frontend import extract


class ExtractorTests(unittest.TestCase):
    def test_fixture_methods_parameters_bodies_and_literal_route(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "frontend.js"
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "frontend.js").write_bytes(fixture.read_bytes())
            snapshot = extract(Path(directory), "test")
        routes = {(item["path"], item["method"]): item for item in snapshot["routes"]}
        containers = routes[("/api/docker/containers", "GET")]
        self.assertEqual(containers["query_keys"], ["all", "includeStats"])
        update = routes[("/api/ddns/task/{key}", "PUT")]
        self.assertTrue(update["has_body"])
        self.assertIn(("/api/status/ws", "UNKNOWN"), routes)
        self.assertEqual(snapshot["bundle_count"], 1)


if __name__ == "__main__":
    unittest.main()
