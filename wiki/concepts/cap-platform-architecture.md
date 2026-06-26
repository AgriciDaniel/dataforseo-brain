---
type: concept
title: "Platform Architecture (v3 API shape)"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, architecture]
related:
 - "[[cap-task-vs-live-execution]]"
 - "[[cap-queue-priority-cost-model]]"
 - "[[cap-status-error-codes]]"
---

# Platform Architecture (v3 API shape)

> The v3 REST contract every DataForSEO call shares: one base URL, a `/v3/{module}/{function}` path, Basic auth, and a uniform tasks/result/cost/status envelope. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
DataForSEO is an API-first, raw-data provider with no dashboard: every product is a REST endpoint that returns structured JSON. All endpoints share one base URL, one auth scheme, one URL grammar, and one response envelope, so learning one module transfers to all others. This note is the master hub: most capability notes link back here because they all inherit this shape. The platform spans roughly a dozen modules (SERP, Keywords Data, DataForSEO Labs, Domain Analytics, Backlinks, OnPage, Content Analysis, Merchant, App Data, Business Data, AI Optimization, and the pre-indexed Databases) plus an `appendix` namespace for account/utility endpoints.

## What it covers
- Base URL: `https://api.dataforseo.com/` (sandbox swaps the host to `https://sandbox.dataforseo.com/v3/`).
- Path grammar: `/v3/{module}/{function}` then the method/result tail, e.g. `/v3/serp/google/organic/live/advanced`, `/v3/dataforseo_labs/google/keyword_ideas/live`, `/v3/on_page/instant_pages`, `/v3/appendix/user_data`.
- The module map: serp, keywords_data, dataforseo_labs, domain_analytics, backlinks, on_page, content_analysis, merchant, app_data, business_data, ai_optimization, databases.
- Two execution shapes per module where supported: Standard (task_post → tasks_ready → task_get) and Live (synchronous). See [[cap-task-vs-live-execution]].
- Auth: HTTP Basic, base64(login:password). See [[cap-authentication-security]].
- A single JSON envelope returned by every endpoint (below).

## Key parameters / inputs
- Method: POST for task_post and Live; GET for task_get, tasks_ready, and utility endpoints like `appendix/user_data`.
- Header `Content-Type: application/json` plus the `Authorization: Basic ...` header on every call.
- POST body is an array of task objects (up to 100 per request on Standard, 1 on Live).
- Common task fields cross-module: `location_code`/`location_name`, `language_code`, `tag`, `pingback_url`, `postback_url`, `postback_data`. See [[cap-locations-languages-targeting]] and [[cap-webhooks-pingback-postback]].

## Response / what you get back
Top-level envelope fields (verbatim from `appendix/user_data`): `version`, `status_code`, `status_message`, `time` (total execution seconds), `cost` (total tasks cost in USD), `tasks_count`, `tasks_error`, and `tasks` (array). Each `tasks[]` entry carries its own `id` (UUID), `status_code`, `status_message`, and a `result` array holding the actual payload. So errors and cost are reported at both the response level and the per-task level. Success is `20000` ("Ok.") on a response and `20100` ("Task Created.") when a Standard task is accepted into the queue. See [[cap-status-error-codes]].

## Cost & method notes
The `cost` field on the envelope is the authoritative per-call charge; per-task `cost` lets you attribute spend. Standard Normal (priority 1) is cheapest, Standard High (priority 2) ~2x, Live ~3.3x of Standard Normal for the same SERP. Billing is per task you set, not per result page collected; you can re-collect Standard results free for 30 days. Cost mechanics live in [[cap-queue-priority-cost-model]]; live-observed per-call costs (2026-06-26) range from $0.000125 (OnPage instant_pages) to $0.15 (clickstream search volume).

## When to use / how it fits
Read this first when integrating any module. It underpins every workflow ([[play-rank-tracking-pipeline]], [[play-cost-optimized-pipeline]]) and the master routing decision [[dec-which-api-for-which-job]]. The MCP server ([[cap-mcp-server-integration]]) wraps this same shape for agents.

## Gotchas / limits
- You cannot pass login/password as URL params, and you do not call a separate auth endpoint.
- 2000 calls/min, 30 simultaneous, ≤100 tasks/POST apply platform-wide. See [[cap-rate-limits-throughput]].
- Live results are not stored; Standard results expire after 30 days (status 40403). See [[cap-account-usage-userdata]].
- `databases` is a separate pre-indexed product delivered as datasets, not the 30-day task window. See [[cap-databases]].

- The `appendix` namespace holds utility endpoints (`user_data`, `webhook_resend`, `errors`, `sandbox`) alongside the 12 data modules.
- Standard task IDs are UUIDs valid for 30 days; results are re-collectable free within that window. See [[cap-account-usage-userdata]].
- The `tag` you set is echoed back and substituted into webhook `$tag` for your own routing. See [[cap-webhooks-pingback-postback]].
- SERP and OnPage responses can be requested at Regular, Advanced, or HTML depth via the path tail. See [[cap-result-tiers-regular-advanced-html]].
- Live responses carry `X-RateLimit-Limit`/`X-RateLimit-Remaining` headers so clients can self-throttle. See [[cap-rate-limits-throughput]].
- DataForSEO returns raw JSON only with no dashboard; a no-code or BI layer is needed for human consumption. See [[ent-dataforseo]].
- The official MCP server exposes the same modules to agents over a wrapped interface. See [[cap-mcp-server-integration]].
- Pre-indexed Databases are a separate delivery channel (S3, SFTP, Google Cloud), not REST task results. See [[cap-databases]].
- Locations and languages are set per task and validated against helper endpoints. See [[cap-locations-languages-targeting]].
- Subscription-gated modules (Backlinks, LLM Mentions) return 40204 until the subscription is active. See [[cap-status-error-codes]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-status-error-codes]]
- [[cap-authentication-security]]
- [[cap-rate-limits-throughput]]
- [[cap-webhooks-pingback-postback]]
- [[cap-account-usage-userdata]]
- [[ent-dataforseo]]
- [[dec-which-api-for-which-job]]
- [[play-cost-optimized-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/auth/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/user_data/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/errors/ (retrieved 2026-06-26)
