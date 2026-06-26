---
type: concept
title: "Account Usage & User Data"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, account]
related:
 - "[[cap-queue-priority-cost-model]]"
 - "[[cap-status-error-codes]]"
 - "[[cap-platform-architecture]]"
---

# Account Usage & User Data

> The `appendix/user_data` endpoint returns live balance, rate limits, spend statistics, prices, and subscription expiry dates for real-time account monitoring. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
`GET /v3/appendix/user_data` gives "detailed information about your API usage, prices, spending and other account details." It is the programmatic way to watch balance and limits before and during a run, so pipelines can self-throttle or pause before hitting billing errors. The endpoint is free but rate-limited, so poll it sparingly rather than per request. It also surfaces retention-relevant subscription expiry dates (Backlinks, LLM Mentions).

## What it covers
- Path/method: `GET https://api.dataforseo.com/v3/appendix/user_data` (Basic auth, no params).
- Top-level envelope: `version`, `status_code`, `status_message`, `time`, `cost`, `tasks_count`, `tasks_error`, `tasks`.
- Result object (`tasks[0].result[0]`): `login`, `timezone`, `rates`, `money`, `price`, `backlinks_subscription_expiry_date`, `llm_mentions_subscription_expiry_date`.
- `money`: `total` (total deposited), `balance` (remaining), `limits` (cost caps by period), `statistics` (spend by period).
- `rates`: nested `limits` and `statistics` by `day`/`minute` with per-function and aggregate call limits across SERP, Keywords Data, Labs, Domain Analytics, Merchant, OnPage, Business Data, Backlinks, App Data, Content Analysis.

## Key parameters / inputs
- None - it is a GET with Basic auth only.
- Read `money.balance` and `money.limits` to enforce your own spend guardrails.
- Read `rates.limits.minute` vs `rates.statistics` to see remaining call headroom.

## Response / what you get back
- `price` object: pricing information by API.
- `money` object: live balance and spend.
- `rates` object: call limits and usage by time grouping.
- Subscription expiry strings (UTC) for Backlinks and LLM Mentions APIs.

## Cost & method notes
The endpoint itself is free to call. It is the monitoring half of the cost model: it pairs with balance/limit errors 40200 (insufficient balance), 40203 (daily cost limit), and 40210 (insufficient funds). Standard task results are stored 30 days (free re-collect); Live results are not stored; HTML results 7 days; Page Screenshot URL 1 day; past-retention requests return 40403. See [[cap-queue-priority-cost-model]] and [[cap-status-error-codes]].

## When to use / how it fits
Wire it into spend dashboards and pre-flight checks for [[play-cost-optimized-pipeline]] and [[play-rank-tracking-pipeline]]. It is central to [[dec-cost-control-strategy]] and confirms which credential/account is active for [[cap-authentication-security]].

## Gotchas / limits
- Rate-limited to 6 calls/minute - poll sparingly, not per-request (status/errors endpoints capped at 10/min, `tasks_ready` at 20/min per the live help-center). See [[cap-rate-limits-throughput]].
- Daily cost caps surface as 40203 when exceeded; set caps to bound spend.
- Subscription-gated APIs (Backlinks 40204, LLM Mentions 40204) require an active subscription, separate from balance; check the expiry fields.
- Spend is also visible in the dashboard, but the endpoint is the programmatic source of truth.

- The endpoint is free but limited to 6 calls/minute; poll sparingly, not per-request.
- `money.total` is total deposited, `money.balance` is remaining; `limits`/`statistics` give caps and spend by period.
- `rates` exposes per-function and aggregate call limits by day and minute across all modules.
- `price` returns pricing information by API for programmatic cost estimates. See [[cap-queue-priority-cost-model]].
- Subscription expiry fields cover Backlinks and LLM Mentions (UTC). See [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]].
- Balance/limit breaches surface as 40200, 40203, and 40210. See [[cap-status-error-codes]].
- Retention: Standard results 30 days, Live not stored, HTML 7 days, Page Screenshot URL 1 day; past-retention returns 40403.
- The result echoes `login` and `timezone`, confirming the active credentials. See [[cap-authentication-security]].
- Wire it into pre-flight checks for [[play-cost-optimized-pipeline]] and [[play-rank-tracking-pipeline]].
- It is the monitoring half of [[dec-cost-control-strategy]].
- Spend is also visible in the dashboard, but this endpoint is the programmatic source of truth.

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-queue-priority-cost-model]]
- [[cap-status-error-codes]]
- [[cap-platform-architecture]]
- [[cap-authentication-security]]
- [[cap-rate-limits-throughput]]
- [[cap-backlinks-api]]
- [[cap-llm-mentions-visibility]]
- [[dec-cost-control-strategy]]
- [[play-cost-optimized-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/appendix/user_data/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/errors/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/how-long-do-you-keep-results (retrieved 2026-06-26)
