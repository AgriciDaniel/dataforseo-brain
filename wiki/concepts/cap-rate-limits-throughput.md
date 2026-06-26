---
type: concept
title: "Rate Limits & Throughput"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, rate-limits]
related:
 - "[[cap-platform-architecture]]"
 - "[[cap-status-error-codes]]"
 - "[[cap-task-vs-live-execution]]"
---

# Rate Limits & Throughput

> The hard ceilings every integration must respect: 2000 calls/min, 30 simultaneous queries, ≤100 tasks per POST, and a 120s Live timeout, plus how batching multiplies throughput. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
DataForSEO enforces account-wide throughput limits that govern all v3 endpoints. Hitting a limit returns a specific status_code rather than silently dropping the request, so a correct client reads the code and backs off. The same limits apply in the sandbox. Architecting around them - batch tasks, prefer the Standard queue, collect via webhooks - is the main scaling pattern.

## What it covers
- 2000 API calls per minute total (POST + GET combined); exceeding → status 40202.
- Up to 100 tasks per POST request; exceeding → 40006. Live methods: 1 task per POST.
- Maximum 30 simultaneous queries (for database-backed/Live APIs: Labs, Backlinks, Content Analysis, Trends, Domain Analytics, OnPage, Clickstream, AI Optimization); exceeding → 40209.
- Daily cost limit (configurable) → 40203 when exceeded.
- Duplicate task limits: hourly (40205) and daily (40206).
- IP whitelisting: non-whitelisted IPs → 40207.
- Live timeout 120 seconds → 50401; target page response cap 50 seconds → 50402.

## Key parameters / inputs
- Special POST caps: Instant Pages, Content Parsing Live, and Page Screenshot allow max 20 tasks/POST.
- Endpoint-specific minute limits: Live Google Ads (Keywords Data) = 12/min; Live Google Trends = 250/min system-wide; `tasks_ready` = 20/min (per the live help-center); `appendix/user_data` = 6/min; status/errors = 10/min.
- Set client timeout to 120s for Live so requests are not cut early.

## Response / what you get back
- Live response headers `X-RateLimit-Limit` and `X-RateLimit-Remaining` let clients self-throttle.
- Throughput math: 1 task/call caps you at 2,000 tasks/min; 100 tasks/call yields 200,000 tasks/min - batching is the primary scaling multiplier.
- Official volume guidance: pingbacks/postbacks "enable you to work with more than 1000 tasks per minute or 100,000 tasks a day."

## Cost & method notes
Rate limits are independent of cost, but the cheapest path also scales best: batch 100 tasks per `task_post` (Standard), then collect via webhooks instead of polling `tasks_ready`. This both raises throughput and cuts wasted billable calls. See [[cap-queue-priority-cost-model]] and [[cap-webhooks-pingback-postback]].

## When to use / how it fits
Plan capacity here before building [[play-rank-tracking-pipeline]] or [[play-cost-optimized-pipeline]]. The 30-simultaneous cap shapes [[dec-live-vs-standard-vs-priority]] and [[dec-labs-vs-live-apis]] (Labs is Live and counts against the concurrency cap).

## Gotchas / limits
- Volume tiers (official): up to ~100,000 tasks/day → Standard + `tasks_ready` polled ~once/minute; 100,000+/day → postback/pingback architecture.
- Cap Live/database worker pools at ~30 threads; on widespread failures pause 5-10 minutes before resuming.
- DataForSEO explicitly advises preferring Standard POST/GET over engineering concurrency to beat the 30-simultaneous cap.
- Need more throughput → contact DataForSEO support for a custom limit increase.
- Sandbox shares the identical limits (2000/min, 100 tasks/POST). See [[cap-sandbox-testing]].

- The 30-simultaneous cap applies to database-backed/Live APIs: Labs, Backlinks, Content Analysis, Trends, Domain Analytics, OnPage, Clickstream, AI Optimization.
- Instant Pages, Content Parsing Live, and Page Screenshot allow a maximum of 20 tasks per POST. See [[cap-onpage-api]].
- Live Google Ads (Keywords Data) is limited to 12 calls/min; Live Google Trends to 250/min system-wide. See [[cap-keywords-data-api]].
- `tasks_ready` is limited to 20/min (per the live help-center; an earlier 60/min figure was unverified); `appendix/user_data` to 6/min; status/errors to 10/min. See [[cap-account-usage-userdata]].
- Live responses expose `X-RateLimit-Limit`/`X-RateLimit-Remaining` headers for client self-throttling.
- Batching is the main multiplier: 1 task/call caps at 2,000 tasks/min, 100 tasks/call reaches 200,000 tasks/min.
- Errored tasks (e.g. 40006, 40209) are not billed but still count as calls against the 2000/min ceiling. See [[cap-status-error-codes]].
- Labs being Live-only means heavy Labs use must respect the concurrency cap. See [[cap-labs-keyword-research]].
- Prefer Standard queue over engineering concurrency to beat the simultaneous cap. See [[cap-task-vs-live-execution]].
- Validate throughput handling for free in the sandbox, which shares the same limits. See [[cap-sandbox-testing]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-platform-architecture]]
- [[cap-status-error-codes]]
- [[cap-task-vs-live-execution]]
- [[cap-webhooks-pingback-postback]]
- [[cap-queue-priority-cost-model]]
- [[cap-sandbox-testing]]
- [[cap-account-usage-userdata]]
- [[dec-live-vs-standard-vs-priority]]
- [[play-cost-optimized-pipeline]]
- [[play-rank-tracking-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/appendix/errors/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/rate-limits-and-request-limits (retrieved 2026-06-26)
- https://dataforseo.com/help-center/best-practices-live-endpoints-in-dataforseo-api (retrieved 2026-06-26)
- https://dataforseo.com/help-center/collect-serp-data-from-dataforseo-api (retrieved 2026-06-26)
