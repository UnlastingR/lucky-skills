from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from lucky_api import OperationRisk, RouteCatalog
from lucky_api.catalog import CatalogError


class RuntimeVerificationTests(unittest.TestCase):
    def test_runtime_verification_suppresses_literals_and_overrides_risk(self) -> None:
        snapshot = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.0"},
            "routes": [
                {
                    "path": "/api/configure",
                    "method": "UNKNOWN",
                    "module": "configure",
                    "confidence": "route-literal-only",
                },
                {
                    "path": "/api/prefix",
                    "method": "UNKNOWN",
                    "module": "prefix",
                    "confidence": "route-literal-only",
                },
                {
                    "path": "/api/prefix/{param}",
                    "method": "GET",
                    "module": "prefix",
                    "confidence": "frontend-call",
                },
            ],
        }
        verification = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.0"},
            "suppress_literals": ["/api/prefix"],
            "routes": [
                {
                    "path": "/api/configure",
                    "method": "GET",
                    "risk": "dangerous",
                    "response_type": "blob",
                    "confidence": "runtime-verified",
                },
                {
                    "path": "/api/configure",
                    "method": "POST",
                    "risk": "dangerous",
                    "confidence": "runtime-verified",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "snapshot.json"
            runtime_path = Path(directory) / "runtime.json"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            verification["static_snapshot_sha256"] = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
            runtime_path.write_text(json.dumps(verification), encoding="utf-8")
            catalog = RouteCatalog.from_file(
                snapshot_path,
                runtime_verification=runtime_path,
            )

        self.assertEqual(catalog.search(risk=OperationRisk.UNKNOWN), [])
        configure = catalog.match("GET", "/api/configure")
        self.assertIsNotNone(configure)
        self.assertEqual(configure.confidence, "runtime-verified")  # type: ignore[union-attr]
        self.assertEqual(configure.response_type, "blob")  # type: ignore[union-attr]
        self.assertEqual(configure.risk, OperationRisk.DANGEROUS)  # type: ignore[union-attr]
        self.assertEqual(
            catalog.classify("POST", "/api/configure"),
            OperationRisk.DANGEROUS,
        )
        self.assertIsNotNone(catalog.match("GET", "/api/prefix/value"))

    def test_runtime_verification_rejects_different_same_version_snapshot(self) -> None:
        snapshot = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.0"},
            "routes": [],
        }
        verification = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.0"},
            "static_snapshot_sha256": "0" * 64,
            "suppress_literals": [],
            "routes": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "snapshot.json"
            runtime_path = Path(directory) / "runtime.json"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            runtime_path.write_text(json.dumps(verification), encoding="utf-8")
            with self.assertRaises(CatalogError):
                RouteCatalog.from_file(snapshot_path, runtime_verification=runtime_path)

    def test_runtime_route_must_be_backed_by_static_evidence(self) -> None:
        snapshot = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.0"},
            "routes": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "snapshot.json"
            runtime_path = Path(directory) / "runtime.json"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            verification = {
                "schema_version": 1,
                "target": {"product": "Lucky", "version": "3.0.0"},
                "static_snapshot_sha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
                "suppress_literals": [],
                "routes": [
                    {
                        "path": "/api/not-in-static-snapshot",
                        "method": "GET",
                        "risk": "read-only",
                    }
                ],
            }
            runtime_path.write_text(json.dumps(verification), encoding="utf-8")
            with self.assertRaises(CatalogError):
                RouteCatalog.from_file(snapshot_path, runtime_verification=runtime_path)

    def test_suppression_must_target_static_unknown_evidence(self) -> None:
        snapshot = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.0"},
            "routes": [
                {"path": "/api/status", "method": "GET", "module": "status"}
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "snapshot.json"
            runtime_path = Path(directory) / "runtime.json"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            verification = {
                "schema_version": 1,
                "target": {"product": "Lucky", "version": "3.0.0"},
                "static_snapshot_sha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
                "suppress_literals": ["/api/status"],
                "routes": [],
            }
            runtime_path.write_text(json.dumps(verification), encoding="utf-8")
            with self.assertRaises(CatalogError):
                RouteCatalog.from_file(snapshot_path, runtime_verification=runtime_path)

    def test_malformed_static_routes_raise_catalog_error(self) -> None:
        for routes in (["nope"], [{"module": "missing-path-and-method"}]):
            with self.subTest(routes=routes), tempfile.TemporaryDirectory() as directory:
                snapshot = {
                    "schema_version": 1,
                    "target": {"product": "Lucky", "version": "3.0.0"},
                    "routes": routes,
                }
                snapshot_path = Path(directory) / "snapshot.json"
                runtime_path = Path(directory) / "runtime.json"
                snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
                verification = {
                    "schema_version": 1,
                    "target": {"product": "Lucky", "version": "3.0.0"},
                    "static_snapshot_sha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
                    "suppress_literals": [],
                    "routes": [],
                }
                runtime_path.write_text(json.dumps(verification), encoding="utf-8")
                with self.assertRaises(CatalogError):
                    RouteCatalog.from_file(snapshot_path, runtime_verification=runtime_path)

    def test_runtime_verification_version_must_match_snapshot(self) -> None:
        snapshot = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.0"},
            "routes": [],
        }
        verification = {
            "schema_version": 1,
            "target": {"product": "Lucky", "version": "3.0.1"},
            "static_snapshot_sha256": "0" * 64,
            "suppress_literals": [],
            "routes": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "snapshot.json"
            runtime_path = Path(directory) / "runtime.json"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            runtime_path.write_text(json.dumps(verification), encoding="utf-8")
            with self.assertRaises(CatalogError):
                RouteCatalog.from_file(
                    snapshot_path,
                    runtime_verification=runtime_path,
                )


if __name__ == "__main__":
    unittest.main()
