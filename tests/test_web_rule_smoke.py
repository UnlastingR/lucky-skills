from __future__ import annotations

import unittest

from tools.lucky_web_rule_smoke import NAME_PREFIX, build_disabled_rule, rule_list


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

    def test_rule_list_requires_the_observed_envelope(self) -> None:
        self.assertEqual(rule_list({"ret": 0, "ruleList": [{"RuleKey": "fixture"}]}), [{"RuleKey": "fixture"}])
        with self.assertRaises(RuntimeError):
            rule_list({"ret": 0, "data": []})


if __name__ == "__main__":
    unittest.main()
