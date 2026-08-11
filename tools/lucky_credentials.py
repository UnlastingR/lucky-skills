#!/usr/bin/env python3
"""Install and inject Lucky credentials without exposing the token in argv.

The credential file is JSON, is written atomically, and is restricted to the
current user on POSIX systems. The `run` command injects credentials only into
the child process environment.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import ipaddress
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{24,128}$")


class CredentialError(RuntimeError):
    """A safe, user-facing credential configuration error."""


def default_credentials_path() -> Path:
    override = os.environ.get("LUCKY_CREDENTIALS_FILE")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        root = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "lucky-skills" / "credentials.json"


def is_loopback_host(hostname: str) -> bool:
    if hostname.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def normalize_base_url(raw: str, allow_http: bool = False) -> str:
    value = raw.strip().rstrip("/")
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"}:
        raise CredentialError("base URL must use http or https")
    if not parsed.hostname:
        raise CredentialError("base URL must include a hostname")
    if parsed.username or parsed.password:
        raise CredentialError("base URL must not contain user information")
    if parsed.query or parsed.fragment:
        raise CredentialError("base URL must not contain a query string or fragment")
    if parsed.path in {"", "/"}:
        raise CredentialError("base URL must include the Lucky safe-entry path")
    if parsed.scheme == "http" and not is_loopback_host(parsed.hostname) and not allow_http:
        raise CredentialError("non-loopback HTTP exposes the token; use HTTPS or pass --allow-http knowingly")
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", ""))


def validate_token(token: str) -> str:
    value = token.strip()
    if not TOKEN_RE.fullmatch(value):
        raise CredentialError("OpenToken must be 24-128 URL-safe characters")
    return value


def token_fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:12]


def redacted_base_url(base_url: str) -> str:
    parsed = urlsplit(base_url)
    return urlunsplit((parsed.scheme, parsed.netloc, "/<redacted-safe-entry>", "", ""))


def ensure_private_directory(directory: Path) -> None:
    if directory.is_symlink():
        raise CredentialError(f"refusing symlinked credential directory: {directory}")
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(directory, 0o700)
        info = directory.stat()
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise CredentialError(f"credential directory is not owned by the current user: {directory}")


def write_credentials(path: Path, base_url: str, token: str, allow_http: bool = False) -> None:
    path = path.expanduser()
    base_url = normalize_base_url(base_url, allow_http=allow_http)
    token = validate_token(token)
    if path.is_symlink():
        raise CredentialError(f"refusing symlinked credential file: {path}")
    ensure_private_directory(path.parent)
    payload = {
        "schema_version": 1,
        "base_url": base_url,
        "open_token": token,
        "allow_insecure_http": allow_http,
    }
    descriptor, temporary_name = tempfile.mkstemp(prefix=".credentials-", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        if os.name != "nt":
            os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        if os.name != "nt":
            os.chmod(path, 0o600)
    finally:
        if temporary.exists():
            temporary.unlink()


def check_private_file(path: Path) -> None:
    directory = path.parent
    if directory.is_symlink():
        raise CredentialError(f"refusing symlinked credential directory: {directory}")
    directory_info = directory.stat()
    if not stat.S_ISDIR(directory_info.st_mode):
        raise CredentialError(f"credential parent is not a directory: {directory}")
    if path.is_symlink():
        raise CredentialError(f"refusing symlinked credential file: {path}")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise CredentialError(f"credential path is not a regular file: {path}")
    if os.name != "nt":
        if stat.S_IMODE(directory_info.st_mode) & 0o077:
            raise CredentialError(f"credential directory is accessible by group/others; run: chmod 700 {directory}")
        if hasattr(os, "getuid") and directory_info.st_uid != os.getuid():
            raise CredentialError(f"credential directory is not owned by the current user: {directory}")
        if stat.S_IMODE(info.st_mode) & 0o077:
            raise CredentialError(f"credential file is accessible by group/others; run: chmod 600 {path}")
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise CredentialError(f"credential file is not owned by the current user: {path}")


def load_credentials(path: Path) -> dict[str, str]:
    path = path.expanduser()
    if not path.exists():
        raise CredentialError(f"credential file not found; run the install command first: {path}")
    check_private_file(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CredentialError(f"cannot read credential file: {path}") from error
    if payload.get("schema_version") != 1:
        raise CredentialError("unsupported credential schema version")
    base_url = normalize_base_url(
        str(payload.get("base_url", "")),
        allow_http=payload.get("allow_insecure_http") is True,
    )
    token = validate_token(str(payload.get("open_token", "")))
    return {"base_url": base_url, "open_token": token}


def credentials_path(args: argparse.Namespace) -> Path:
    return (args.file or default_credentials_path()).expanduser()


def command_install(args: argparse.Namespace) -> int:
    path = credentials_path(args)
    if path.exists() and not args.force:
        answer = input(f"Credential file exists at {path}. Replace it? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("No changes made.")
            return 1
    raw_base_url = args.base_url or input("Lucky base URL including safe entry: ")
    base_url = normalize_base_url(raw_base_url, allow_http=args.allow_http)
    token = validate_token(getpass.getpass("Lucky OpenToken (hidden): "))
    confirmation = validate_token(getpass.getpass("Repeat OpenToken (hidden): "))
    if token != confirmation:
        raise CredentialError("OpenToken values do not match")
    write_credentials(path, base_url, token, allow_http=args.allow_http)
    print(f"Credentials installed at {path}")
    print(f"Base URL: {redacted_base_url(base_url)}")
    print(f"Token fingerprint: sha256:{token_fingerprint(token)}")
    if os.name == "nt":
        print("Warning: verify the Windows ACL grants access only to your account.")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    path = credentials_path(args)
    values = load_credentials(path)
    mode = "ACL-managed" if os.name == "nt" else oct(stat.S_IMODE(path.stat().st_mode))
    print(f"Credential file: {path}")
    print(f"Permissions: {mode}")
    print(f"Base URL: {redacted_base_url(values['base_url'])}")
    print(f"Token fingerprint: sha256:{token_fingerprint(values['open_token'])}")
    print("Credential checks passed.")
    return 0


def command_run(args: argparse.Namespace) -> int:
    command = list(args.command)
    if command and command[0] == "--":
        command.pop(0)
    if not command:
        raise CredentialError("run requires a command after --")
    values = load_credentials(credentials_path(args))
    environment = os.environ.copy()
    environment["LUCKY_BASE_URL"] = values["base_url"]
    environment["LUCKY_OPEN_TOKEN"] = values["open_token"]
    try:
        os.execvpe(command[0], command, environment)
    except FileNotFoundError as error:
        raise CredentialError(f"command not found: {command[0]}") from error
    return 127


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    install = subparsers.add_parser("install", help="interactively install credentials")
    install.add_argument("--file", type=Path, help="override the credential file")
    install.add_argument("--base-url", help="base URL including the Lucky safe entry; token is still prompted")
    install.add_argument("--allow-http", action="store_true", help="allow non-loopback HTTP despite token exposure risk")
    install.add_argument("--force", action="store_true", help="replace an existing credential file without prompting")
    install.set_defaults(handler=command_install)

    doctor = subparsers.add_parser("doctor", help="validate storage, URL, and token format")
    doctor.add_argument("--file", type=Path, help="override the credential file")
    doctor.set_defaults(handler=command_doctor)

    run = subparsers.add_parser("run", help="inject credentials into one child command")
    run.add_argument("--file", type=Path, help="override the credential file")
    run.add_argument("command", nargs=argparse.REMAINDER)
    run.set_defaults(handler=command_run)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        raise_code = args.handler(args)
    except CredentialError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(raise_code)


if __name__ == "__main__":
    main()
