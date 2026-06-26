---
type: concept
title: "Queue Priority & Cost Model"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, pricing]
related:
 - "[[cap-task-vs-live-execution]]"
 - "[[cap-platform-architecture]]"
 - "[[cap-account-usage-userdata]]"
---

# Queue Priority & Cost Model

> How DataForSEO bills: pay-as-you-go with a $50 minimum, per-task pricing, and two Standard priorities (Normal=1, High=2) plus Live that trade latency for cost. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
DataForSEO is pay-as-you-go: you deposit funds ($50 minimum) and are billed per task you set, not per seat. The single biggest cost lever is execution mode. Standard Normal (priority 1) is cheapest and slowest; Standard High (priority 2) is ~2x for ~1 minute turnaround; Live is ~3.3x of Standard Normal for ~6 second turnaround. This is a hub note linked from nearly every module note because cost is module-specific but the model is universal.

## What it covers
- Pricing model: pay-as-you-go, $50 minimum deposit, new accounts get a $1 free credit usable for an unlimited period; "Your account will be billed only for setting a task."
- Priority levels (Standard only): Normal `1` = lower cost, slower; High `2` = faster, higher cost.
- Per-result vs per-request billing: many endpoints bill per block of results (e.g. Google Shopping products billed "for every 40 results"; reviews/sellers "every 10 items"; App Store reviews per 50, Play reviews per 150).
- The `cost` field on the envelope and per-task `cost` for spend attribution.
- Depth tuning: base price covers the first 10 results; raising `depth` "doubles the price for every extra 100 results" (directional, verify on invoice).

## Key parameters / inputs
- `priority`: 1 or 2 (Standard).
- `depth`: number of results requested; drives cost above the base 10.
- `include_clickstream_data: true` on Labs multiplies request cost by 2.
- Choice of `/live` vs task-based path selects the mode premium.

## Response / what you get back
- Reference per Google SERP (10 results): Standard Normal $0.0006 ($600/1M), Standard High $0.0012 ($1,200/1M), Live $0.002 ($2,000/1M). Catalog range overall "$0.60 / 1,000 SERPs to $100 / purchase."
- Live-observed costs (2026-06-26, `_cost-log.json`): Labs keyword endpoints ~$0.0105/task; Labs overview/difficulty ~$0.0101; SERP Live advanced $0.002; Google Ads search volume $0.075; clickstream DFS search volume $0.15; Whois overview $0.101; OnPage instant_pages $0.000125; business_listings search $0.0103.
- Example scaled SERP price for 100 results: Standard Normal $0.00465, High $0.0093, Live $0.0155.

## Cost & method notes
Pre-indexed DataForSEO Labs and Databases are far cheaper than live SERP because they query stored data, not live crawls (basic Labs ≈ $0.01/task + $0.0001/item). Refreshed Databases are 50% of standard price. Bulk endpoints (Bulk Keyword Difficulty, Bulk Traffic Estimation) return up to 1,000 results per single billed task. Batching 100 tasks per `task_post` cuts HTTP overhead (still one billed task each). Pair this with [[cap-task-vs-live-execution]] and [[cap-databases]].

## When to use / how it fits
This model is the basis of every spend decision: [[dec-cost-control-strategy]], [[dec-live-vs-standard-vs-priority]], [[dec-labs-vs-live-apis]], and the money-saving flow [[play-cost-optimized-pipeline]]. Monitor actual spend via [[cap-account-usage-userdata]].

## Gotchas / limits
- Accidental Live usage costs ~3.3x the Standard batch rate - a common cost footgun.
- Insufficient balance → status 40200/40210; daily cost limit exceeded → 40203. See [[cap-status-error-codes]].
- The "doubles per extra 100 results" depth multiplier wording was only partially exposed; treat as directional.
- Some endpoints have flat-plus-per-item pricing (e.g. Business Listings Live: $0.01/task + $0.0003/item, capped 1000 items/request). See [[cap-business-data-api]].

- New accounts get a $1 free credit valid for an unlimited period to test real endpoints. See [[cap-sandbox-testing]].
- "Your account will be billed only for setting a task"; Standard results are re-collectable free for 30 days. See [[cap-account-usage-userdata]].
- Turnaround estimates: Standard Normal ~5 min, Standard High ~1 min, Live ~6 sec (some endpoints ~2 sec real-time).
- Merchant Amazon ASIN pricing: Standard $0.0015/product, Priority $0.003, Live $0.005. See [[cap-merchant-api]].
- App Data reviews bill per block (Google Play per 150 reviews, Apple App Store per 50 reviews). See [[cap-app-data-api]].
- Business Listings Live bills $0.01/task plus $0.0003/item, capped at 1000 items/request. See [[cap-business-data-api]].
- Databases cost depends on dataset size and location; refreshed datasets are 50% of standard price. See [[cap-databases]].
- Monitor `money.balance` and `money.limits` to avoid 40200, 40203, and 40210. See [[cap-status-error-codes]].
- Setting `include_clickstream_data: true` on Labs doubles request cost. See [[cap-trends-and-clickstream]].
- The cheapest scalable path is Standard High plus webhooks. See [[cap-webhooks-pingback-postback]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-platform-architecture]]
- [[cap-task-vs-live-execution]]
- [[cap-account-usage-userdata]]
- [[cap-databases]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-sandbox-testing]]
- [[dec-cost-control-strategy]]
- [[dec-live-vs-standard-vs-priority]]
- [[dec-labs-vs-live-apis]]
- [[play-cost-optimized-pipeline]]

## Sources
- https://dataforseo.com/pricing (retrieved 2026-06-26)
- https://dataforseo.com/apis/serp-api/pricing (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs-google-overview/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/multiple-tasks-in-one-api-request (retrieved 2026-06-26)
