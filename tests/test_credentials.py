from __future__ import annotations

import os
import stat
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock

from tools.lucky_credentials import (
    CredentialError,
    command_run,
    default_credentials_path,
    load_credentials,
    normalize_base_url,
    redacted_base_url,
    token_fingerprint,
    validate_token,
    write_credentials,
)


class CredentialTests(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "XDG config-home test")
    def test_empty_xdg_config_home_falls_back_to_home(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"XDG_CONFIG_HOME": "", "LUCKY_CREDENTIALS_FILE": ""},
            clear=False,
        ), mock.patch("tools.lucky_credentials.Path.home", return_value=Path("/home/tester")):
            self.assertEqual(
                default_credentials_path(),
                Path("/home/tester/.config/lucky-skills/credentials.json"),
            )

    def test_loopback_http_and_https_are_accepted(self) -> None:
        self.assertEqual(
            normalize_base_url("http://127.0.0.1:16601/safe-entry/"),
            "http://127.0.0.1:16601/safe-entry",
        )
        self.assertEqual(
            normalize_base_url("https://lucky.example.test/safe-entry"),
            "https://lucky.example.test/safe-entry",
        )

    def test_non_loopback_http_requires_explicit_override(self) -> None:
        with self.assertRaises(CredentialError):
            normalize_base_url("http://192.0.2.10:16601/safe-entry")
        self.assertEqual(
            normalize_base_url("http://192.0.2.10:16601/safe-entry", allow_http=True),
            "http://192.0.2.10:16601/safe-entry",
        )

    def test_safe_entry_is_required(self) -> None:
        with self.assertRaises(CredentialError):
            normalize_base_url("https://lucky.example.test")

    def test_token_validation_and_fingerprint(self) -> None:
        token = "A" * 32
        self.assertEqual(validate_token(token), token)
        self.assertEqual(len(token_fingerprint(token)), 12)
        with self.assertRaises(CredentialError):
            validate_token("short")

    def test_safe_entry_is_redacted_for_display(self) -> None:
        self.assertEqual(
            redacted_base_url("https://lucky.example.test/private-entry"),
            "https://lucky.example.test/<redacted-safe-entry>",
        )

    def test_atomic_private_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "config" / "credentials.json"
            token = "B" * 32
            write_credentials(target, "https://lucky.example.test/safe-entry", token)
            loaded = load_credentials(target)
            self.assertEqual(loaded["open_token"], token)
            self.assertEqual(loaded["base_url"], "https://lucky.example.test/safe-entry")
            if os.name != "nt":
                self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(target.parent.stat().st_mode), 0o700)

    def test_explicit_http_override_is_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "config" / "credentials.json"
            write_credentials(
                target,
                "http://192.0.2.10:16601/safe-entry",
                "D" * 32,
                allow_http=True,
            )
            self.assertEqual(
                load_credentials(target)["base_url"],
                "http://192.0.2.10:16601/safe-entry",
            )

    @mock.patch("tools.lucky_credentials.os.execvpe")
    def test_run_injects_only_into_child_environment(self, execvpe: mock.Mock) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "config" / "credentials.json"
            token = "E" * 32
            write_credentials(target, "https://lucky.example.test/safe-entry", token)
            result = command_run(Namespace(file=target, command=["--", "client", "status"]))
            self.assertEqual(result, 127)
            command, arguments, environment = execvpe.call_args.args
            self.assertEqual(command, "client")
            self.assertEqual(arguments, ["client", "status"])
            self.assertEqual(environment["LUCKY_OPEN_TOKEN"], token)
            self.assertEqual(environment["LUCKY_BASE_URL"], "https://lucky.example.test/safe-entry")
            self.assertNotIn(token, arguments)

    @unittest.skipIf(os.name == "nt", "POSIX mode test")
    def test_overly_permissive_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "config" / "credentials.json"
            write_credentials(target, "https://lucky.example.test/safe-entry", "C" * 32)
            os.chmod(target, 0o644)
            with self.assertRaises(CredentialError):
                load_credentials(target)

    @unittest.skipIf(os.name == "nt", "POSIX mode test")
    def test_overly_permissive_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "config" / "credentials.json"
            write_credentials(target, "https://lucky.example.test/safe-entry", "F" * 32)
            os.chmod(target.parent, 0o755)
            with self.assertRaises(CredentialError):
                load_credentials(target)


if __name__ == "__main__":
    unittest.main()
