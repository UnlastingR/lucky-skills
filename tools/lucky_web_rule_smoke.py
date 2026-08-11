#!/usr/bin/env python3
"""Create, verify, and delete one disabled Lucky Web service rule.

This is an explicitly destructive integration smoke test. It requires a fixed
confirmation phrase, never enables the rule, never asks Lucky to adjust the
firewall, and makes a best-effort cleanup in a finally block.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from lucky_api import LuckyClient, LuckyClientError, RouteCatalog  # noqa: E402


CONFIRMATION = "CREATE-AND-DELETE-DISABLED-WEB-RULE"
NAME_PREFIX = "codex-api-write-test-"


def build_disabled_rule(name: str) -> dict[str, Any]:
    """Return the Lucky v3 frontend's new-rule defaults in a disabled form."""
    return {
        "RuleName": name,
        "RuleKey": "",
        "DiaglogShowMode": "diy",
        "Enable": False,
        "DisableStatistics": True,
        "Network": "tcp4",
        "CorazaWAFInstance": "",
        "ListenIP": "127.0.0.1",
        "ListenPort": 16666,
        "AutoOptionsFirewall": False,
        "EnableTLS": False,
        "TLSMinVersion": 2,
        "MaxHeaderKBytes": 32,
        "IPFilterRule": "globalblacklist",
        "MaxContinuous404Count": 0,
        "MaxCorazaInterceptionCount": 0,
        "SendRateLimitEnabled": False,
        "SendRateLimit": 0,
        "ReceRateLimitEnabled": False,
        "ReceRateLimit": 0,
        "SingleConnSendRateLimitEnabled": False,
        "SingleConnSendRateLimit": 0,
        "SingleConnReceRateLimitEnabled": False,
        "SingleConnReceRateLimit": 0,
        "GlobalAllowAllThirdAuthUsers": False,
        "GlobalThirdAuthLoginUserList": [],
        "GlobalAllowThirdUserSkipTwoFA": False,
        "SingleIPSendRateLimitEnabled": False,
        "SingleIPSendRateLimit": 0,
        "SingleIPReceRateLimitEnabled": False,
        "SingleIPReceRateLimit": 0,
        "SingleIPConnectionsLimitEnabled": False,
        "SingleIPConnectionsLimit": 0,
        "Http3": False,
        "GlobalBasicAuthUserList": "",
        "ECH": False,
        "ECHDomain": "",
        "ECDHPrivateKey": "",
        "ECHConfigList": "",
        "DefaultProxy": build_disabled_default_proxy(),
        "ProxyList": [],
    }


def build_disabled_default_proxy() -> dict[str, Any]:
    return {
        "GroupKey": "",
        "Key": "default",
        "Enable": False,
        "WebServiceType": "reverseproxy",
        "CorazaWAFInstance": "",
        "Domains": [],
        "Locations": [],
        "LocationInsecureSkipVerify": False,
        "EnableAccessLog": False,
        "DisableStatistics": True,
        "LogLevel": 4,
        "LogOutputToConsole": False,
        "AccessLogMaxNum": 256,
        "WafLogMaxNum": 128,
        "WebListShowLastLogMaxCount": 10,
        "RequestInfoLogFormat": "[#{clientIP}][#{remoteIP}]#{tab}[#{method}][#{host}#{url}]",
        "ForwardedByClientIP": False,
        "TrustedCIDRsStrList": [],
        "UseRuleGlobalAuthSettings": True,
        "UseTargetHost": False,
        "DisableLongConnection": False,
        "CustomCrossDomain": "",
        "CustomCrossMethods": "",
        "RemoteIPHeaders": ["X-Forwarded-For", "X-Real-IP"],
        "AddRemoteIPToHeader": False,
        "AddRemoteIPHeaderKey": "",
        "EnableCrossDomain": False,
        "EnableBasicAuth": False,
        "BasicAuthRegConf": "",
        "BasicAuthUser": "",
        "BasicAuthPasswd": "",
        "BasicAuthUserList": "",
        "BasicAuthMaxLoginErrorCount": 0,
        "AuthSource": "local",
        "SecurityGroupKeys": [],
        "SecurityGroupAccessMode": "disabled",
        "SecurityGroupGrantBasicAuth": False,
        "SafeIPMode": "blacklist",
        "SafeUserAgentMode": "blacklist",
        "UserAgentfilter": [""],
        "CustomRobotTxt": False,
        "RobotTxt": "User-agent:  *\nDisallow:  /",
        "AddProtoToHeader": False,
        "ProtoHeaderKey": "",
        "EasyLucky": False,
        "FileServerShowDir": True,
        "CacheBodyOnlyPath": "",
        "FileServerIndexNames": "index.html\n",
        "FileServerHideFiles": "",
        "FileServerForbiddenPaths": "",
        "FileServerMountList": [],
        "fileServerCollapsectiveName": 0,
        "NginxConf": "",
        "CustomOutputText": "",
        "DisableHTTP3": False,
        "MaxContinuous404Count": 0,
        "MaxCorazaInterceptionCount": 0,
        "HttpClientNetwork": "tcp",
        "DisableKeepAlives": True,
        "HttpClientTimeout": 30,
        "MaxConnsPerHost": 128,
        "ProxyType": "",
        "ProxyAddr": "",
        "ProxyUser": "",
        "ProxyPassword": "",
        "AutoProxyLocation": False,
        "AutoProxyLocationWithoutSameHost": False,
        "CacheEnabled": False,
        "CachePath": "",
        "CacheKey": "",
        "CacheLimit": 0,
        "CacheBodyMinLimit": 0,
        "CacheBodyMaxLimit": 0,
        "CacheOnlyKeyReg": "",
        "CacheValidityPeriod": 0,
        "DealCacheBeforeReverseProxy": True,
        "GRPCSecureConnection": False,
        "CertificateSyncToken": "",
        "OtherParams": {
            "ProxyProtocolV2": True,
            "RedirectType": "307",
            "SpeedTestFrontSource": "",
            "OauthType": "github",
            "OauthClientID": "",
            "OauthClientSecret": "",
            "OauthClientKey": "",
            "OauthRedirectURI": "",
            "OauthServer": "",
            "HttpClientProxyType": "",
            "HttpClientProxyAddr": "",
            "HttpClientProxyUser": "",
            "HttpClientProxyPassword": "",
            "WebAuth": False,
            "WebAuthUseDedicatedPath": True,
            "WebAuthPathPrefix": "/__6c75636b79_webauth__",
            "WebAuthSessionScopeMode": "subrule",
            "WebAuthAllowNonBrowserReuse": False,
            "WebAuthAllowNonBrowserUserAgents": ["*"],
            "AllowAllThirdUsers": False,
            "AllowThirdUserList": [],
            "AllowThirdUserSkipTwoFA": False,
        },
    }


def rule_list(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("ruleList"), list):
        raise RuntimeError("unexpected /api/webservice/rules response shape")
    return [item for item in payload["ruleList"] if isinstance(item, dict)]


def rule_key(item: dict[str, Any]) -> str:
    value = item.get("RuleKey")
    return value if isinstance(value, str) else ""


def find_created_keys(
    client: LuckyClient, name: str, baseline_keys: set[str]
) -> set[str]:
    current = rule_list(client.request_json("GET", "/api/webservice/rules"))
    return {
        rule_key(item)
        for item in current
        if item.get("RuleName") == name and rule_key(item) and rule_key(item) not in baseline_keys
    }


def delete_rule(client: LuckyClient, key: str) -> None:
    encoded = urllib.parse.quote(key, safe="")
    client.request_json(
        "DELETE",
        f"/api/webservice/rule/{encoded}",
        allow_unsafe=True,
    )


def run_smoke_test(client: LuckyClient, name: str) -> dict[str, Any]:
    baseline = rule_list(client.request_json("GET", "/api/webservice/rules"))
    baseline_keys = {rule_key(item) for item in baseline if rule_key(item)}
    cleanup_keys: set[str] = set()
    create_succeeded = False
    disabled_verified = False
    cleanup_errors: list[str] = []
    primary_error: BaseException | None = None
    try:
        client.request_json(
            "POST",
            "/api/webservice/rules",
            json_body=build_disabled_rule(name),
            allow_unsafe=True,
        )
        create_succeeded = True
        cleanup_keys = find_created_keys(client, name, baseline_keys)
        if len(cleanup_keys) != 1:
            raise RuntimeError(f"expected one newly created test rule, found {len(cleanup_keys)}")
        key = next(iter(cleanup_keys))
        encoded = urllib.parse.quote(key, safe="")
        fetched = client.request_json("GET", f"/api/webservice/rule/{encoded}")
        if isinstance(fetched, dict):
            candidate = fetched.get("rule", fetched.get("ruleInfo", fetched))
        else:
            candidate = fetched
        if not isinstance(candidate, dict):
            raise RuntimeError("unexpected Web rule detail response shape")
        if candidate.get("RuleName") != name or candidate.get("Enable") is not False:
            raise RuntimeError("created rule did not round-trip as the expected disabled rule")
        disabled_verified = True
    except BaseException as error:
        primary_error = error
    finally:
        if create_succeeded and not cleanup_keys:
            try:
                cleanup_keys = find_created_keys(client, name, baseline_keys)
            except BaseException as error:
                cleanup_errors.append(f"could not locate test rule for cleanup: {type(error).__name__}")
        for key in sorted(cleanup_keys):
            try:
                delete_rule(client, key)
            except BaseException as error:
                cleanup_errors.append(f"could not delete test rule: {type(error).__name__}")

    final_rules = rule_list(client.request_json("GET", "/api/webservice/rules"))
    final_keys = {rule_key(item) for item in final_rules if rule_key(item)}
    restored = final_keys == baseline_keys and not any(item.get("RuleName") == name for item in final_rules)
    if cleanup_errors:
        raise RuntimeError("; ".join(cleanup_errors)) from primary_error
    if not restored:
        raise RuntimeError("Web rule cleanup verification failed") from primary_error
    if primary_error is not None:
        raise primary_error
    return {
        "created": create_succeeded,
        "disabled_round_trip_verified": disabled_verified,
        "deleted": bool(cleanup_keys),
        "baseline_rule_count": len(baseline),
        "final_rule_count": len(final_rules),
        "baseline_restored": restored,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    if args.confirm != CONFIRMATION:
        parser.error(f"confirmation must be exactly: {CONFIRMATION}")
    name = NAME_PREFIX + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    try:
        client = LuckyClient.from_environment(catalog=RouteCatalog.load_default(), retries=1)
        result = run_smoke_test(client, name)
    except (LuckyClientError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
