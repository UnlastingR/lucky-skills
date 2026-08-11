---
name: lucky
description: Manage and troubleshoot authorized Lucky v3 instances through this repository's safe OpenToken client. Use for Lucky status/modules, Web Service and reverse-proxy rules, DDNS, certificates, Docker, cloudflared, FRP, STUN, or a specific Lucky configuration change. 用于查询或修改 Lucky 管理后台/OpenToken API；默认只读，写操作仅在用户明确要求时执行，并遵循客户端风险分级与确认机制。
---

# Lucky management workflow

Use the repository's guarded OpenToken tooling instead of ad-hoc authenticated `curl` commands.

## Locate the client

1. Prefer the current repository root when it contains both `tools/lucky_credentials.py` and `tools/lucky_api.py`.
2. Otherwise, locate the full `lucky-skills` checkout/plugin that contains those files. Do not assume a standalone copied `SKILL.md` includes the client.
3. Run Lucky commands from that root so the endpoint catalog and helper modules resolve correctly.

## Authenticate safely

- Treat OpenToken as an administrator secret. Never print it, place it in command-line arguments, commit it, or expose the safe-entry path unnecessarily.
- Check credentials without revealing them:

```bash
python3 tools/lucky_credentials.py doctor
```

- If credentials are missing, use the interactive installer described in `docs/credentials.md`:

```bash
python3 tools/lucky_credentials.py install
```

- Prefer direct in-process credential loading so the OpenToken never has to be copied into a child-process environment:

```bash
python3 tools/lucky_api.py status
```

- With no credential environment variables, the CLI reads the platform/configured default credential path from `lucky_credentials.py`. `--credentials-file PATH` explicitly overrides it. The older `lucky_credentials.py run -- ...` wrapper remains available for compatibility.

## Start read-only

For inspection or troubleshooting, establish a baseline before proposing changes:

```bash
python3 tools/lucky_api.py status
python3 tools/lucky_api.py info
python3 tools/lucky_api.py modules
```

Search the catalog before using an arbitrary endpoint:

```bash
python3 tools/lucky_api.py catalog --search webservice
python3 tools/lucky_api.py catalog --search ddns
```

Then call cataloged read-only routes with `call`. Prefer narrow responses and the smallest endpoint that answers the question.

## Apply changes conservatively

- Only mutate Lucky when the user explicitly asks for the configuration change.
- Trust the repository's route risk classification, not HTTP method alone. Lucky has historically exposed some side-effecting operations through `GET`.
- Read the current object first and preserve the identifiers/fields required for rollback.
- Make the smallest targeted change. Do not replace unrelated rules or settings.
- The client rejects writes by default. For a confirmed write, use both `--allow-write` and the exact confirmation string required by `--confirm`, for example:

```bash
python3 tools/lucky_api.py call /api/example \
  --method PUT --json-file /path/to/reviewed-payload.json \
  --allow-write --confirm 'PUT /api/example'
```

- Verify the resulting object/state immediately after the write. If the change is reversible and verification fails, restore the captured baseline when safe to do so.
- Never perform dangerous actions such as deleting data, clearing sessions/statistics, terminal/file operations, container destruction, or broad rule replacement unless that exact destructive outcome was requested.

## Web Service / reverse proxy work

For domain migration or reverse-proxy changes, inspect `/api/webservice/rules` (or the narrow rule-detail endpoint) first. Preserve the existing rule key, listener/TLS settings, proxy target, authentication, security groups, WAF, and unrelated domains. When adding a new hostname for a migration, prefer temporarily keeping both old and new hostnames until end-to-end validation succeeds.

For Lucky v3 Web-service redirects, the redirect status is stored at `DefaultProxy.OtherParams.RedirectType` (and equivalently on redirect subrules). Lucky 3.0.0 has been API-verified to accept `"308"`; a rule with `WebServiceType: "redirect"`, `Locations: ["https://{host}{path}{args}"]`, and `RedirectType: "308"` returned HTTP 308 for both GET and POST. Create a new listener with `POST /api/webservice/rules`; update an existing listener by GETting its full object and PUTting the preserved object to `/api/webservice/rule/{RuleKey}`.

## Report results

Summarize what was read or changed, identify any remaining non-Lucky dependency (DNS, CDN, origin application, firewall, certificate issuance), and avoid reproducing secrets returned by Lucky responses.
