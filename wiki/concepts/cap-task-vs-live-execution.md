---
type: concept
title: "Task (Standard) vs Live Execution"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, execution]
related:
 - "[[cap-platform-architecture]]"
 - "[[cap-queue-priority-cost-model]]"
 - "[[cap-webhooks-pingback-postback]]"
---

# Task (Standard) vs Live Execution

> Two ways to run any DataForSEO job: the asynchronous Standard queue (task_post → tasks_ready → task_get) or synchronous Live that returns results in the same request. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
Every applicable module exposes one or both of two execution modes. Standard (task-based) is asynchronous and uses three separate calls; Live is synchronous and returns data inside one open connection. The choice drives latency, cost, throughput, retry logic, and whether results are stored. This is a hub note: most module notes reference it to explain how their endpoints are invoked.

## What it covers
- Standard method: `task_post` (submit), `tasks_ready` (list completed-but-uncollected task IDs), `task_get` (retrieve results). Described as "more affordable" and preferred for planned, scalable collection.
- Live method: synchronous, no separate POST/GET; the connection stays open until data is ready ("on average it takes up to 6 seconds," longer for large queries). Most expensive mode.
- Mode availability by API: SERP, Merchant, and Business Data support both Live and Standard (with priority options); DataForSEO Labs is Live-only; OnPage is Standard-based with cost/speed set by crawl parameters.
- Collection without polling: register `pingback_url` or `postback_url` so completion is pushed to you. See [[cap-webhooks-pingback-postback]].

## Key parameters / inputs
- Standard POST body: array of up to 100 task objects; each can carry `tag`, `pingback_url`, `postback_url`, `postback_data` ("advanced"/"html"/"regular").
- Live POST: 1 task per request (Live methods generally allow only one task/POST).
- `priority`: 1 (Normal) or 2 (High) on Standard only - trades latency for cost.
- `task_get` tail selects result depth: `.../task_get/advanced/$id` or `.../task_get/regular/$id` or `.../task_get/html/$id`. See [[cap-result-tiers-regular-advanced-html]].

## Response / what you get back
- `task_post` returns `20100` ("Task Created.") with a per-task `id` (UUID) you later poll/collect; no result payload yet.
- `tasks_ready` returns the IDs of finished tasks not yet collected.
- `task_get` and Live return the full `result` array in the standard envelope (`status_code` 20000 on success).
- Live returns `result` immediately; nothing is queued or stored.

## Cost & method notes
Live costs roughly 3.3x Standard-Normal and ~1.65x Standard-High for the same SERP ($0.002 vs $0.0006 vs $0.0012 per Google SERP, 10 results). For bulk, Standard with High priority is explicitly recommended because it collects asynchronously instead of holding a persistent connection per request. Live-observed (2026-06-26): `serp/google/organic/live/advanced` = $0.002; Labs Live `keyword_ideas` = $0.0105. Cost detail lives in [[cap-queue-priority-cost-model]].

## When to use / how it fits
- Need instant/real-time results for a single query → Live. 
- Scaling large planned volumes → Standard (ideally High) plus webhooks. Official latency ladder: Standard Normal ~5 min, Standard High ~1 min, Live ~6 sec.
- This choice is the spine of [[dec-live-vs-standard-vs-priority]] and [[dec-labs-vs-live-apis]], and shapes [[play-cost-optimized-pipeline]] and [[play-rank-tracking-pipeline]].

## Gotchas / limits
- Live timeout is 120 seconds (status 50401 on overrun); set your client timeout to 120s so requests aren't cut early. Target page response cap is 50s (50402).
- Live results are not stored - capture them from the response; Standard results are stored 30 days and re-collectable free.
- A task returning an error is not processed further; you must re-set it after a delay. Retryable: 40103, 40601, 40602, 50301, 50303, 50401, 50402. See [[cap-status-error-codes]].
- Labs being Live-only means you cannot queue it; budget for synchronous calls. See [[cap-labs-keyword-research]].

- `tasks_ready` lists only completed-but-uncollected tasks; once you `task_get` a task it drops off the list.
- OnPage is Standard-based; its cost/speed is set by crawl parameters rather than a Live/queue toggle. See [[cap-onpage-api]].
- Merchant and Business Data offer both modes with priority options. See [[cap-merchant-api]] and [[cap-business-data-api]].
- Labs is Live-only, so every Labs call counts against the 30-simultaneous concurrency cap. See [[cap-rate-limits-throughput]].
- Live averages up to 6 seconds but large/complex queries take longer; budget for the 120-second ceiling.
- For more than 100,000 tasks/day, use Standard plus postback/pingback rather than Live. See [[cap-webhooks-pingback-postback]].
- `task_get` supports regular/advanced/html depth tails to control parse richness. See [[cap-result-tiers-regular-advanced-html]].
- Spend per mode is monitorable via `appendix/user_data`. See [[cap-account-usage-userdata]].
- Test both modes for free in the sandbox before billed runs. See [[cap-sandbox-testing]].
- Mode choice is the core of the routing in [[dec-which-api-for-which-job]].
- DataForSEO API v2 was fully closed on 2026-05-05: no new v2 requests are accepted (only legacy `task_get` stayed active during the sunset window), so the v3 Standard/Live split documented here is the only live option. The AI Optimization API is v3-exclusive. See [[cap-ai-optimization-api]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[cap-webhooks-pingback-postback]]
- [[cap-rate-limits-throughput]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-status-error-codes]]
- [[cap-serp-api]]
- [[cap-ai-optimization-api]]
- [[dec-live-vs-standard-vs-priority]]
- [[dec-labs-vs-live-apis]]
- [[play-cost-optimized-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/serp-overview/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/live-vs-standard-method (retrieved 2026-06-26)
- https://dataforseo.com/help-center/best-practices-live-endpoints-in-dataforseo-api (retrieved 2026-06-26)
- https://dataforseo.com/update/dataforseo-api-v2-sunset-notice (retrieved 2026-06-26)
- https://dataforseo.com/apis/serp-api/pricing (retrieved 2026-06-26)
