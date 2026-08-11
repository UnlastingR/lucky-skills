from __future__ import annotations

import io
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from lucky_api import Route, RouteCatalog
from tools.lucky_api import command_call, main, make_client, parse_query, read_json_body
from tools.lucky_credentials import CredentialError


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

    def test_make_client_reads_private_credentials_file_directly(self) -> None:
        path = Path("/tmp/test-lucky-credentials.json")
        args = Namespace(
            credentials_file=path,
            timeout=3.0,
            retries=0,
            max_response_bytes=1024,
        )
        with patch(
            "tools.lucky_api.load_credentials",
            return_value={
                "base_url": "http://127.0.0.1:16601/safe-entry",
                "open_token": "test-token",
            },
        ) as loader:
            client = make_client(args, RouteCatalog([]))
        loader.assert_called_once_with(path)
        self.assertEqual(client.base_url, "http://127.0.0.1:16601/safe-entry")

    def test_make_client_uses_configured_default_when_env_is_unset(self) -> None:
        path = Path("/tmp/default-lucky-credentials.json")
        args = Namespace(
            credentials_file=None,
            timeout=3.0,
            retries=0,
            max_response_bytes=1024,
        )
        with patch.dict("tools.lucky_api.os.environ", {}, clear=True), patch(
            "tools.lucky_api.default_credentials_path", return_value=path
        ), patch(
            "tools.lucky_api.load_credentials",
            return_value={
                "base_url": "http://127.0.0.1:16601/safe-entry",
                "open_token": "test-token",
            },
        ) as loader:
            client = make_client(args, RouteCatalog([]))
        loader.assert_called_once_with(path)
        self.assertEqual(client.base_url, "http://127.0.0.1:16601/safe-entry")

    def test_make_client_rejects_partial_legacy_environment(self) -> None:
        args = Namespace(
            credentials_file=None,
            timeout=3.0,
            retries=0,
            max_response_bytes=1024,
        )
        with patch.dict(
            "tools.lucky_api.os.environ", {"LUCKY_BASE_URL": "https://stale.example/safe"}, clear=True
        ), patch("tools.lucky_api.load_credentials") as loader:
            with self.assertRaises(CredentialError) as context:
                make_client(args, RouteCatalog([]))
        loader.assert_not_called()
        self.assertIn("incomplete Lucky credential environment", str(context.exception))

    def test_make_client_treats_blank_legacy_environment_as_unset(self) -> None:
        path = Path("/tmp/default-lucky-credentials.json")
        args = Namespace(
            credentials_file=None,
            timeout=3.0,
            retries=0,
            max_response_bytes=1024,
        )
        with patch.dict(
            "tools.lucky_api.os.environ",
            {"LUCKY_BASE_URL": "", "LUCKY_OPEN_TOKEN": "   "},
            clear=True,
        ), patch(
            "tools.lucky_api.default_credentials_path", return_value=path
        ), patch(
            "tools.lucky_api.load_credentials",
            return_value={
                "base_url": "http://127.0.0.1:16601/safe-entry",
                "open_token": "test-token",
            },
        ) as loader:
            client = make_client(args, RouteCatalog([]))
        loader.assert_called_once_with(path)
        self.assertEqual(client.base_url, "http://127.0.0.1:16601/safe-entry")

    def test_main_reports_credential_error_without_traceback(self) -> None:
        stderr = io.StringIO()
        with patch("tools.lucky_api.sys.argv", ["lucky_api.py", "status"]), patch(
            "tools.lucky_api.load_credentials",
            side_effect=CredentialError("credential file not found"),
        ), redirect_stderr(stderr):
            result = main()
        self.assertEqual(result, 2)
        self.assertEqual(stderr.getvalue().strip(), "error: credential file not found")

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
