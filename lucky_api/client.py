"""A small, dependency-free Lucky OpenToken HTTP client."""

from __future__ import annotations

import email.utils
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from .catalog import OperationRisk, RouteCatalog


class LuckyClientError(RuntimeError):
    """Base class for errors safe to display without leaking credentials."""


class UnsafeOperationError(LuckyClientError):
    pass


class TransportError(LuckyClientError):
    pass


class HTTPStatusError(LuckyClientError):
    def __init__(self, status: int, method: str, path: str, detail: str = "") -> None:
        suffix = f": {detail}" if detail else ""
        super().__init__(f"Lucky HTTP {status} for {method} {path}{suffix}")
        self.status = status
        self.method = method
        self.path = path


class LuckyAPIError(LuckyClientError):
    def __init__(self, ret: Any, message: str, method: str, path: str) -> None:
        safe_message = message[:500] if message else "business error"
        super().__init__(f"Lucky API ret={ret} for {method} {path}: {safe_message}")
        self.ret = ret
        self.method = method
        self.path = path


class ResponseDecodeError(LuckyClientError):
    pass


class ResponseTooLargeError(LuckyClientError):
    pass


@dataclass(frozen=True)
class RateLimit:
    limit: int | None
    remaining: int | None
    reset_seconds: float | None


@dataclass(frozen=True)
class APIResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes
    content_type: str
    method: str
    path: str

    def json(self) -> Any:
        try:
            return json.loads(self.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ResponseDecodeError(
                f"invalid JSON response for {self.method} {self.path}"
            ) from error

    @property
    def is_json(self) -> bool:
        return self.content_type == "application/json" or self.content_type.endswith("+json")

    @property
    def rate_limit(self) -> RateLimit:
        lowered = {key.lower(): value for key, value in self.headers.items()}

        def integer(name: str) -> int | None:
            try:
                return int(lowered[name])
            except (KeyError, TypeError, ValueError):
                return None

        try:
            reset = float(lowered.get("ratelimit-reset", ""))
        except ValueError:
            reset = None
        return RateLimit(integer("ratelimit-limit"), integer("ratelimit-remaining"), reset)


_UNSET = object()
RETRY_STATUSES = {429, 502, 503, 504}


class LuckyClient:
    def __init__(
        self,
        base_url: str,
        open_token: str,
        *,
        timeout: float = 10.0,
        retries: int = 2,
        max_response_bytes: int = 16 * 1024 * 1024,
        catalog: RouteCatalog | None = None,
        urlopen: Callable[..., Any] = urllib.request.urlopen,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        parsed = urllib.parse.urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("base_url must not embed a username or password")
        if parsed.query or parsed.fragment:
            raise ValueError("base_url must not contain query or fragment components")
        if parsed.path in {"", "/"}:
            raise ValueError("base_url must include the Lucky safe entry")
        if not open_token or any(char.isspace() for char in open_token):
            raise ValueError("open_token must be non-empty and contain no whitespace")
        if timeout <= 0 or retries < 0 or max_response_bytes <= 0:
            raise ValueError("timeout/max_response_bytes must be positive and retries non-negative")
        self.base_url = base_url.rstrip("/")
        self._safe_entry = parsed.path.rstrip("/")
        self._open_token = open_token
        self.timeout = timeout
        self.retries = retries
        self.max_response_bytes = max_response_bytes
        self.catalog = catalog
        self._urlopen = urlopen
        self._sleep = sleeper

    @classmethod
    def from_environment(cls, **kwargs: Any) -> "LuckyClient":
        import os

        base_url = os.environ.get("LUCKY_BASE_URL", "")
        token = os.environ.get("LUCKY_OPEN_TOKEN", "")
        if not base_url or not token:
            raise ValueError("LUCKY_BASE_URL and LUCKY_OPEN_TOKEN are required")
        return cls(base_url, token, **kwargs)

    def operation_risk(self, method: str, path: str) -> OperationRisk:
        if self.catalog is None:
            return OperationRisk.UNKNOWN
        return self.catalog.classify(method, path)

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Mapping[str, Any] | Sequence[tuple[str, Any]] | None = None,
        json_body: Any = _UNSET,
        raw_body: bytes | None = None,
        content_type: str | None = None,
        allow_unsafe: bool = False,
        raise_for_lucky: bool = True,
    ) -> APIResponse:
        method = method.upper()
        self._validate_api_path(path)
        if json_body is not _UNSET and raw_body is not None:
            raise ValueError("json_body and raw_body are mutually exclusive")
        risk = self.operation_risk(method, path)
        if risk is not OperationRisk.READ_ONLY and not allow_unsafe:
            raise UnsafeOperationError(
                f"refusing {risk.value} operation {method} {path}; explicit approval is required"
            )

        url = self.base_url + path
        if query:
            encoded = urllib.parse.urlencode(query, doseq=True)
            url += "?" + encoded
        headers = {
            "Accept": "application/json, application/octet-stream;q=0.8",
            "User-Agent": "lucky-skills/1",
            "openToken": self._open_token,
        }
        body = raw_body
        if json_body is not _UNSET:
            body = json.dumps(json_body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"
        elif raw_body is not None:
            headers["Content-Type"] = content_type or "application/octet-stream"
        request = urllib.request.Request(url, data=body, headers=headers, method=method)

        for attempt in range(self.retries + 1):
            try:
                with self._urlopen(request, timeout=self.timeout) as response:
                    result = self._response(response, method, path)
                if raise_for_lucky:
                    self._raise_for_lucky(result)
                return result
            except urllib.error.HTTPError as error:
                if (
                    risk is OperationRisk.READ_ONLY
                    and error.code in RETRY_STATUSES
                    and attempt < self.retries
                ):
                    self._sleep(self._retry_delay(error.headers or {}, attempt))
                    continue
                detail = self._error_detail(error)
                raise HTTPStatusError(error.code, method, path, detail) from None
            except (urllib.error.URLError, TimeoutError, socket.timeout) as error:
                reason = getattr(error, "reason", None)
                label = type(reason or error).__name__
                raise TransportError(f"Lucky transport error for {method} {path} ({label})") from None
        raise AssertionError("unreachable")

    def request_json(self, method: str, path: str, **kwargs: Any) -> Any:
        response = self.request(method, path, **kwargs)
        return response.json()

    @staticmethod
    def _validate_api_path(path: str) -> None:
        parsed = urllib.parse.urlsplit(path)
        if (
            not path.startswith("/api/")
            or parsed.scheme
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or ".." in parsed.path.split("/")
            or any(ord(char) < 32 for char in path)
        ):
            raise ValueError("path must be a clean /api/... path; pass query separately")

    def _response(self, response: Any, method: str, path: str) -> APIResponse:
        headers = {key: value for key, value in response.headers.items()}
        content_length = response.headers.get("Content-Length")
        if content_length:
            try:
                if int(content_length) > self.max_response_bytes:
                    raise ResponseTooLargeError(
                        f"response exceeds {self.max_response_bytes} bytes for {method} {path}"
                    )
            except ValueError:
                pass
        body = response.read(self.max_response_bytes + 1)
        if len(body) > self.max_response_bytes:
            raise ResponseTooLargeError(
                f"response exceeds {self.max_response_bytes} bytes for {method} {path}"
            )
        content_type = response.headers.get_content_type()
        return APIResponse(int(response.status), headers, body, content_type, method, path)

    def _raise_for_lucky(self, response: APIResponse) -> None:
        if not response.is_json or not response.body:
            return
        payload = response.json()
        if not isinstance(payload, dict):
            return
        ret = payload.get("ret", 0)
        if ret in {0, None}:
            return
        message = str(payload.get("msg") or payload.get("message") or "")
        if self.catalog is not None:
            route = self.catalog.match(response.method, response.path)
            if route is not None and (ret, message) in route.success_response_markers:
                return
        message = message.replace(self._open_token, "<redacted>")
        if self._safe_entry:
            message = message.replace(self._safe_entry, "/<redacted-safe-entry>")
        raise LuckyAPIError(ret, message, response.method, response.path)

    def _error_detail(self, error: urllib.error.HTTPError) -> str:
        body = error.read(min(self.max_response_bytes, 4096)) if error.fp is not None else b""
        text = body.decode("utf-8", errors="replace").replace(self._open_token, "<redacted>")
        text = text.replace(self.base_url, "<redacted-base-url>")
        if self._safe_entry:
            text = text.replace(self._safe_entry, "/<redacted-safe-entry>")
        return " ".join(text.split())[:500]

    @staticmethod
    def _retry_delay(headers: Mapping[str, str], attempt: int) -> float:
        retry_after = headers.get("Retry-After")
        if retry_after:
            try:
                return min(30.0, max(0.0, float(retry_after)))
            except ValueError:
                try:
                    when = email.utils.parsedate_to_datetime(retry_after)
                    if when.tzinfo is None:
                        when = when.replace(tzinfo=timezone.utc)
                    return min(30.0, max(0.0, (when - datetime.now(timezone.utc)).total_seconds()))
                except (TypeError, ValueError):
                    pass
        reset = headers.get("RateLimit-Reset")
        if reset:
            try:
                return min(30.0, max(0.0, float(reset)))
            except ValueError:
                pass
        return min(8.0, 0.5 * (2**attempt))
