from __future__ import annotations

import io
import json
import unittest
import urllib.error
from email.message import Message

from lucky_api import (
    LuckyAPIError,
    LuckyClient,
    OperationRisk,
    ResponseTooLargeError,
    Route,
    RouteCatalog,
    UnsafeOperationError,
)


class FakeResponse:
    def __init__(self, payload: bytes, *, status: int = 200, content_type: str = "application/json") -> None:
        self.status = status
        self.payload = payload
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        self.headers["Content-Length"] = str(len(payload))
        self.headers["RateLimit-Limit"] = "20"
        self.headers["RateLimit-Remaining"] = "19"
        self.headers["RateLimit-Reset"] = "1"

    def read(self, amount: int = -1) -> bytes:
        return self.payload if amount < 0 else self.payload[:amount]

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None


def route(
    path: str,
    method: str,
    *,
    success_response_markers: tuple[tuple[int, str], ...] = (),
) -> Route:
    return Route(
        path,
        method,
        path.split("/")[2],
        "test",
        (),
        (),
        False,
        "json",
        success_response_markers=success_response_markers,
    )


class ClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = RouteCatalog(
            [
                route("/api/status", "GET"),
                route("/api/docker/compose/backup/status", "GET"),
                route("/api/docker/volumes/export", "GET"),
                route("/api/ipfliter/oneclickrecord", "GET"),
                route("/api/third/filebrowser/resetadmin", "GET"),
                route("/api/ddns/getipfromcmdtest", "GET"),
                route("/api/cron/enable", "GET"),
                route("/api/ddns", "PUT"),
                route("/api/about-content", "PUT", success_response_markers=((1, "成功"),)),
                route("/api/docker/containers/{param}/restart", "POST"),
                route("/api/status/ws", "UNKNOWN"),
            ],
            version="test",
        )

    def client(self, urlopen: object, **kwargs: object) -> LuckyClient:
        return LuckyClient(
            "https://lucky.example.test/private-entry",
            "T" * 32,
            catalog=self.catalog,
            urlopen=urlopen,  # type: ignore[arg-type]
            **kwargs,
        )

    def test_authenticated_json_request_and_rate_limit(self) -> None:
        observed = {}

        def open_request(request: object, timeout: float) -> FakeResponse:
            observed["url"] = request.full_url  # type: ignore[attr-defined]
            observed["headers"] = dict(request.header_items())  # type: ignore[attr-defined]
            observed["timeout"] = timeout
            return FakeResponse(b'{"ret":0,"data":{"ok":true}}')

        response = self.client(open_request).request("GET", "/api/status", query={"window": "1m"})
        self.assertEqual(response.json()["data"]["ok"], True)
        self.assertEqual(observed["url"], "https://lucky.example.test/private-entry/api/status?window=1m")
        self.assertEqual(observed["headers"]["Opentoken"], "T" * 32)
        self.assertNotIn("T" * 32, observed["url"])
        self.assertEqual(response.rate_limit.limit, 20)
        self.assertEqual(response.rate_limit.remaining, 19)

    def test_business_error_is_typed_and_does_not_leak_token(self) -> None:
        response = FakeResponse(json.dumps({"ret": -1, "msg": "OpenToken error"}).encode())
        with self.assertRaises(LuckyAPIError) as context:
            self.client(lambda request, timeout: response).request("GET", "/api/status")
        self.assertNotIn("T" * 32, str(context.exception))
        self.assertEqual(context.exception.ret, -1)

    def test_business_error_redacts_token_and_safe_entry(self) -> None:
        payload = {
            "ret": -1,
            "msg": "bad " + ("T" * 32) + " at /private-entry",
        }
        response = FakeResponse(json.dumps(payload).encode(), content_type="application/problem+json")
        with self.assertRaises(LuckyAPIError) as context:
            self.client(lambda request, timeout: response).request("GET", "/api/status")
        message = str(context.exception)
        self.assertNotIn("T" * 32, message)
        self.assertNotIn("private-entry", message)

    def test_positive_business_error_still_raises_without_route_override(self) -> None:
        response = FakeResponse(json.dumps({"ret": 1, "msg": "validation failed"}).encode())
        with self.assertRaises(LuckyAPIError) as context:
            self.client(lambda request, timeout: response).request("GET", "/api/status")
        self.assertEqual(context.exception.ret, 1)

    def test_route_specific_positive_success_ret_is_accepted(self) -> None:
        response = FakeResponse(json.dumps({"ret": 1, "msg": "成功"}).encode())
        payload = self.client(lambda request, timeout: response).request_json(
            "PUT",
            "/api/about-content",
            json_body={},
            allow_unsafe=True,
        )
        self.assertEqual(payload, {"ret": 1, "msg": "成功"})

    def test_route_specific_positive_ret_with_other_message_still_raises(self) -> None:
        response = FakeResponse(json.dumps({"ret": 1, "msg": "validation failed"}).encode())
        with self.assertRaises(LuckyAPIError):
            self.client(lambda request, timeout: response).request(
                "PUT",
                "/api/about-content",
                json_body={},
                allow_unsafe=True,
            )

    def test_base_url_rejects_embedded_credentials(self) -> None:
        with self.assertRaises(ValueError):
            LuckyClient("https://user:password@example.test/safe", "T" * 32)

    def test_side_effect_get_classification_is_conservative_and_status_safe(self) -> None:
        self.assertEqual(
            self.catalog.classify("GET", "/api/docker/compose/backup/status"),
            OperationRisk.READ_ONLY,
        )
        self.assertEqual(
            self.catalog.classify("GET", "/api/docker/volumes/export"),
            OperationRisk.DANGEROUS,
        )
        self.assertEqual(
            self.catalog.classify("GET", "/api/ipfliter/oneclickrecord"),
            OperationRisk.MUTATING,
        )
        self.assertEqual(
            self.catalog.classify("GET", "/api/third/filebrowser/resetadmin"),
            OperationRisk.DANGEROUS,
        )
        self.assertEqual(
            self.catalog.classify("GET", "/api/ddns/getipfromcmdtest"),
            OperationRisk.DANGEROUS,
        )

    def test_mutating_unknown_and_side_effect_get_are_blocked(self) -> None:
        client = self.client(lambda request, timeout: FakeResponse(b'{"ret":0}'))
        for method, path in (
            ("PUT", "/api/ddns"),
            ("GET", "/api/cron/enable"),
            ("GET", "/api/docker/volumes/export"),
            ("GET", "/api/ipfliter/oneclickrecord"),
            ("GET", "/api/third/filebrowser/resetadmin"),
            ("GET", "/api/ddns/getipfromcmdtest"),
            ("GET", "/api/not-in-catalog"),
        ):
            with self.subTest(method=method, path=path):
                with self.assertRaises(UnsafeOperationError):
                    client.request(method, path)

    def test_explicitly_approved_write_uses_json(self) -> None:
        observed = {}

        def open_request(request: object, timeout: float) -> FakeResponse:
            observed["body"] = request.data  # type: ignore[attr-defined]
            observed["content_type"] = request.get_header("Content-type")  # type: ignore[attr-defined]
            return FakeResponse(b'{"ret":0}')

        self.client(open_request).request(
            "PUT", "/api/ddns", json_body={"key": "value"}, allow_unsafe=True
        )
        self.assertEqual(json.loads(observed["body"]), {"key": "value"})
        self.assertEqual(observed["content_type"], "application/json; charset=utf-8")

    def test_read_only_retry_honors_retry_after(self) -> None:
        attempts = []
        delays = []

        def open_request(request: object, timeout: float) -> FakeResponse:
            attempts.append(1)
            if len(attempts) == 1:
                headers = Message()
                headers["Retry-After"] = "0"
                raise urllib.error.HTTPError(
                    request.full_url, 429, "rate limited", headers, io.BytesIO(b"slow down")  # type: ignore[attr-defined]
                )
            return FakeResponse(b'{"ret":0}')

        self.client(open_request, retries=1, sleeper=delays.append).request("GET", "/api/status")
        self.assertEqual(len(attempts), 2)
        self.assertEqual(delays, [0.0])

    def test_mutation_is_never_retried(self) -> None:
        attempts = []

        def open_request(request: object, timeout: float) -> FakeResponse:
            attempts.append(1)
            raise urllib.error.HTTPError(
                request.full_url, 503, "unavailable", Message(), io.BytesIO(b"unavailable")  # type: ignore[attr-defined]
            )

        with self.assertRaises(Exception):
            self.client(open_request, retries=3).request(
                "PUT", "/api/ddns", json_body={}, allow_unsafe=True
            )
        self.assertEqual(len(attempts), 1)

    def test_response_size_limit(self) -> None:
        with self.assertRaises(ResponseTooLargeError):
            self.client(
                lambda request, timeout: FakeResponse(b"12345", content_type="application/octet-stream"),
                max_response_bytes=4,
            ).request("GET", "/api/status")

    def test_catalog_matching_and_risk(self) -> None:
        matched = self.catalog.match("POST", "/api/docker/containers/abc/restart")
        self.assertIsNotNone(matched)
        self.assertEqual(matched.path, "/api/docker/containers/{param}/restart")  # type: ignore[union-attr]
        self.assertEqual(self.catalog.classify("GET", "/api/status"), OperationRisk.READ_ONLY)
        self.assertEqual(
            self.catalog.classify("GET", "/api/docker/compose/backup/status"),
            OperationRisk.READ_ONLY,
        )
        self.assertEqual(self.catalog.classify("GET", "/api/cron/enable"), OperationRisk.MUTATING)
        self.assertEqual(
            self.catalog.classify("POST", "/api/docker/containers/abc/restart"),
            OperationRisk.DANGEROUS,
        )
        self.assertEqual(self.catalog.search(risk=OperationRisk.UNKNOWN)[0].path, "/api/status/ws")


if __name__ == "__main__":
    unittest.main()
