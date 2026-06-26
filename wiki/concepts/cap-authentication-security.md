---
type: concept
title: "Authentication & Security"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, auth]
related:
 - "[[cap-platform-architecture]]"
 - "[[cap-status-error-codes]]"
 - "[[cap-rate-limits-throughput]]"
---

# Authentication & Security

> DataForSEO v3 uses HTTP Basic auth: a base64-encoded `login:password` header on every call, where the API password is auto-generated and differs from the account password. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
Authentication is deliberately simple so the API works "with almost any programming language." There is no token exchange and no separate auth call: you attach a Basic Authorization header to every request. The credential pair is the API Login and a distinct auto-generated API Password from the account API Access tab, not the dashboard login. Security hygiene therefore centers on protecting that header value and optionally whitelisting source IPs.

## What it covers
- Method: standard HTTP Basic Authentication on every endpoint.
- Credentials: API Login + API Password from https://app.dataforseo.com/api-access; the API password is auto-generated and differs from the account password.
- Header format: `Authorization: Basic [base64(login:password)]`.
- Base URL: `https://api.dataforseo.com/` (sandbox: `https://sandbox.dataforseo.com/v3/`).
- Optional IP whitelisting (enforced via status 40207 for non-whitelisted IPs).

## Key parameters / inputs
- Example: `login:password` → base64 `bG9naW46cGFzc3dvcmQ=` → `Authorization: Basic bG9naW46cGFzc3dvcmQ=`.
- cURL: `--header "Authorization: Basic [credentials]" --header "Content-Type: application/json"`.
- Python client: `client = RestClient("login", "password")`.
- Node.js (axios): `auth: { username: 'login', password: 'password' }`.

## Response / what you get back
- Successful auth proceeds to the normal envelope (status 20000/20100).
- Bad credentials → HTTP 401 and/or internal status 40100 ("You are not authorized to access this resource").
- Account not yet verified → 40104 (verification required before API access).
- The `appendix/user_data` result echoes your account `login` and `timezone`, useful to confirm which credential set is active. See [[cap-account-usage-userdata]].

## Cost & method notes
Auth itself is free and adds no cost; you are billed only for tasks you set. There is no rate cost to attaching credentials, but every call must carry them. Pair credential management with spend monitoring in [[cap-account-usage-userdata]] and the cost model in [[cap-queue-priority-cost-model]].

## When to use / how it fits
This is the first integration step for every workflow and the MCP server ([[cap-mcp-server-integration]]) which stores the same login/password in env config. It underpins [[dec-mcp-vs-raw-rest]] (where credentials live) and every play, e.g. [[play-cost-optimized-pipeline]].

## Gotchas / limits
- "It is not possible to pass the login and password in URL parameters" - credentials go only in the header.
- "You do not have to make a separate authentication call to obtain API credentials" - no token flow.
- The API password is distinct from and rotatable independently of the account password; rotate it if leaked.
- Store credentials as secrets, never in source or a repo; combine with IP whitelisting for production.
- Unusual activity can temporarily pause an account (status 40201). See [[cap-status-error-codes]].

- Bad credentials surface as HTTP 401 and/or internal status 40100. See [[cap-status-error-codes]].
- Unverified accounts get 40104 (verification required before API access).
- The same login/password also authenticates the sandbox host. See [[cap-sandbox-testing]].
- IP whitelisting (optional) rejects non-whitelisted IPs with 40207. See [[cap-rate-limits-throughput]].
- `appendix/user_data` echoes the active account `login` and `timezone` to confirm which credentials are in use. See [[cap-account-usage-userdata]].
- The MCP server reads the same login/password from environment config. See [[cap-mcp-server-integration]].
- DataForSEO sends webhooks from fixed IPs (e.g. 144.76.154.130, 144.76.153.113) worth whitelisting inbound. See [[cap-webhooks-pingback-postback]].
- Credentials must be stored as secrets, never committed to a repo or pasted into the vault.
- Rotate the API password independently if it leaks; it does not affect the dashboard login.
- Auth is the first step of every workflow, including [[play-rank-tracking-pipeline]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-platform-architecture]]
- [[cap-status-error-codes]]
- [[cap-rate-limits-throughput]]
- [[cap-account-usage-userdata]]
- [[cap-sandbox-testing]]
- [[cap-mcp-server-integration]]
- [[ent-dataforseo]]
- [[dec-mcp-vs-raw-rest]]
- [[play-cost-optimized-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/auth/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/errors/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/user_data/ (retrieved 2026-06-26)
