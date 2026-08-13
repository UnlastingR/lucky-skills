from __future__ import annotations

import unittest

from lucky_api.client import TransportError
from tools.lucky_web_rule_smoke import NAME_PREFIX, build_disabled_rule, rule_list, run_smoke_test


class WebRuleSmokeTests(unittest.TestCase):
    def test_payload_is_disabled_loopback_only_and_firewall_safe(self) -> None:
        name = NAME_PREFIX + "fixture"
        payload = build_disabled_rule(name)
        self.assertEqual(payload["RuleName"], name)
        self.assertEqual(payload["RuleKey"], "")
        self.assertIs(payload["Enable"], False)
        self.assertIs(payload["AutoOptionsFirewall"], False)
        self.assertEqual(payload["ListenIP"], "127.0.0.1")
        self.assertIs(payload["EnableTLS"], False)
        self.assertEqual(payload["ProxyList"], [])
        default = payload["DefaultProxy"]
        self.assertIs(default["Enable"], False)
        self.assertEqual(default["Domains"], [])
        self.assertEqual(default["Locations"], [])
        self.assertEqual(default["ProxyAddr"], "")
        self.assertEqual(default["ProxyPassword"], "")
        self.assertEqual(default["OtherParams"]["RedirectType"], "307")

    def test_rule_list_requires_the_observed_envelope(self) -> None:
        self.assertEqual(rule_list({"ret": 0, "ruleList": [{"RuleKey": "fixture"}]}), [{"RuleKey": "fixture"}])
        with self.assertRaises(RuntimeError):
            rule_list({"ret": 0, "data": []})

    def test_transport_error_after_create_still_finds_and_deletes_rule(self) -> None:
        class PersistThenFailClient:
            def __init__(self) -> None:
                self.rules: list[dict[str, object]] = []

            def request_json(self, method: str, path: str, **kwargs: object) -> object:
                if method == "GET" and path == "/api/webservice/rules":
                    return {"ret": 0, "ruleList": list(self.rules)}
                if method == "POST" and path == "/api/webservice/rules":
                    body = kwargs["json_body"]
                    assert isinstance(body, dict)
                    self.rules.append({"RuleKey": "probe-key", "RuleName": body["RuleName"]})
                    raise TransportError("simulated lost response after persistence")
                if method == "DELETE" and path == "/api/webservice/rule/probe-key":
                    self.rules.clear()
                    return {"ret": 0}
                raise AssertionError(f"unexpected request: {method} {path}")

        client = PersistThenFailClient()
        with self.assertRaises(TransportError):
            run_smoke_test(client, NAME_PREFIX + "transport-error")  # type: ignore[arg-type]
        self.assertEqual(client.rules, [])


if __name__ == "__main__":
    unittest.main()
