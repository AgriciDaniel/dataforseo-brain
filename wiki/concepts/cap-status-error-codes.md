---
type: concept
title: "Status & Error Codes"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, errors]
related:
 - "[[cap-platform-architecture]]"
 - "[[cap-rate-limits-throughput]]"
 - "[[cap-task-vs-live-execution]]"
---

# Status & Error Codes

> The dual-layer status system: HTTP codes plus DataForSEO internal `status_code` values (20000 OK, 20100 Task Created, 40xxx client, 50xxx server) and which are retryable. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
DataForSEO reports outcome at two layers: the HTTP response code and an internal `status_code` field that appears both at the response top level and per task. A request can be HTTP 200 yet carry a per-task error code (e.g. 40204 "subscription required"), so robust clients must inspect both. Codes group into success (200xx), client errors (40xxx), and server/3rd-party errors (50xxx). Knowing the retryable set is essential for reliable pipelines.

## What it covers
- HTTP codes: 401 Unauthorized, 402 Payment Required, 404 Not Found, 500 Internal Server Error.
- Success: 20000 "Ok." (request completed), 20100 "Task Created." (Standard task accepted).
- Task management (40000-40006): 40000 multiple tasks not allowed, 40006 >100 tasks per POST.
- Auth/verification (40100-40104): 40100 not authorized, 40102 no search results, 40103 task execution failed (resubmit), 40104 account verification required.
- Payment/account (40200-40210): 40200 insufficient balance, 40202 rate limit (2000/min), 40203 daily cost limit, 40204 Backlinks subscription required, 40207 IP not whitelisted, 40209 >30 simultaneous, 40210 insufficient funds.
- Not found (40400-40408): 40401 task doesn't exist, 40403 "Results Expired" (data older than one month), 40404 sandbox missing prepared data, 40408 target URL invalid/404.
- Validation (40501-40506): 40501 invalid POST field, 40502 empty POST, 40503 invalid POST, 40506 unknown fields.
- Task status (40601 "Task Handed", 40602 "Task in Queue").
- Server (50xxx): 50000 internal error, 50301 3rd-party unavailable, 50303 update in progress, 50401 Live 120s timeout, 50402 target page 50s timeout.

## Key parameters / inputs
- Inspect `status_code` and `status_message` at both the envelope and per-task level.
- `tasks_error` counts tasks with errors in a batch response.

## Response / what you get back
- Live-observed task-level codes (2026-06-26, `_cost-log.json`): 40204 on Backlinks and LLM Mentions endpoints (subscription not active, $0 charged); 40501 on a malformed Labs `categories_for_domain` and a YouTube SERP call; 40402 on a Google Shopping products call (invalid URL path). Charged tasks all returned 20000.
- A failed task returns `result_count: 0` and `cost: 0` - you are not billed for errored tasks.

## Cost & method notes
Errored tasks are not charged, so cost-control depends on not retrying non-retryable errors blindly. Subscription-gated 40204 (Backlinks, LLM Mentions) means you pay a subscription, not per-call balance. See [[cap-account-usage-userdata]] and [[cap-queue-priority-cost-model]].

## When to use / how it fits
Build your retry/error matrix from this note before shipping [[play-cost-optimized-pipeline]] or [[play-rank-tracking-pipeline]]. It underpins reliability in [[dec-live-vs-standard-vs-priority]].

## Gotchas / limits
- Retryable (re-set after a delay): 40103, 40601, 40602, 50301, 50303, 50401, 50402. For a single 50401 timeout, retry the same payload; for widespread failures, pause 5-10 min.
- Not retryable until you fix the cause: auth (40100, 40104), billing (40200, 40210), validation (40501-40506), not-found (40400-40408).
- A task returning an error is not processed further; you must re-set it.
- 40403 means results aged past the 30-day window - re-run the task. See [[cap-account-usage-userdata]].
- Failed pingbacks/postbacks can be re-sent via the Webhook Resend endpoint. See [[cap-webhooks-pingback-postback]].

- 40202 maps to the 2000 calls/min ceiling; 40209 to the 30-simultaneous cap. See [[cap-rate-limits-throughput]].
- 40204 gates the Backlinks and LLM Mentions APIs behind active subscriptions. The official `/appendix/errors/` 40204 message references the Backlinks subscription URL only; LLM Mentions reuses the same code with its own separate $100/mo subscription. See [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]].
- 40505 ("Outdated location parameters") fails geo-targeted tasks; refresh from the helper endpoint. See [[cap-locations-languages-targeting]].
- 40404 ("Sandbox missing prepared data") only occurs in the sandbox environment. See [[cap-sandbox-testing]].
- 50401 is the Live 120-second timeout; 50402 is the 50-second target-page cap. See [[cap-task-vs-live-execution]].
- 40006 caps a POST at 100 tasks; special endpoints cap at 20. See [[cap-rate-limits-throughput]].
- 40601 ("Task Handed") and 40602 ("Task in Queue") are transient Standard states, not failures.
- General rule: 50xxx server errors retry in a few minutes; input-validation errors require fixing the payload.
- Whitelisting issues surface as 40207 when IP whitelisting is enabled. See [[cap-authentication-security]].
- Build the retry matrix into [[play-cost-optimized-pipeline]] and [[dec-cost-control-strategy]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-platform-architecture]]
- [[cap-rate-limits-throughput]]
- [[cap-task-vs-live-execution]]
- [[cap-webhooks-pingback-postback]]
- [[cap-account-usage-userdata]]
- [[cap-queue-priority-cost-model]]
- [[cap-backlinks-api]]
- [[dec-live-vs-standard-vs-priority]]
- [[play-cost-optimized-pipeline]]
- [[play-rank-tracking-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/appendix/errors/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/best-practices-live-endpoints-in-dataforseo-api (retrieved 2026-06-26)
