---
type: flow
title: "Play: Rank Tracking Pipeline"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, serp, rank-tracking]
related:
  - "[[cap-serp-api]]"
  - "[[cap-task-vs-live-execution]]"
  - "[[dec-live-vs-standard-vs-priority]]"
---

# Play: Rank Tracking Pipeline

> Daily/weekly position monitoring for a keyword x location x device set via the SERP API Standard method plus webhooks. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
This pipeline turns a tracked keyword list into a position time-series. It uses the SERP API Google Organic endpoint in Standard (task-based) mode so the cost stays low and large batches scale, with pingback/postback webhooks replacing polling. Rankings are stored per run so you can chart movement and SERP-feature presence over time. It is the canonical "rank tracker you build yourself" on DataForSEO raw data.

## Trigger
A defined tracking set is created or refreshed: each row is a `keyword` plus a `location_code` (or `location_name`/`location_coordinate`), `language_code`, and `device` (desktop/mobile). Cadence is fixed (usually daily or weekly) and a scheduler fires the run.

## Endpoints used (in order)
- `POST /v3/serp/google/organic/task_post` (Advanced result type) to enqueue the batch.
- `GET /v3/serp/google/organic/tasks_ready` to discover completed task ids (fallback to webhooks).
- `GET /v3/serp/google/organic/task_get/advanced/$id` to collect parsed SERPs.
- `POST /v3/appendix/webhook_resend` to recover missed pingbacks/postbacks.
- `GET /v3/appendix/user_data` for balance and daily-cost-limit monitoring.

## Pipeline
1. Build the targeting per row: resolve `location_code` and `language_code` from the locations/languages helper (see [[cap-locations-languages-targeting]]); pick `device` and optional `depth` (default 10, max 200).
2. Batch up to 100 rows into one `task_post` call (one billed task each, one HTTP request). Set `priority: 1` (Normal) for cheapest, or `priority: 2` (High) when same-day freshness matters. Attach a unique `tag` per keyword for routing.
3. Register delivery: set `postback_url` with `postback_data: "advanced"` to receive gzip-compressed parsed results, or `pingback_url` for a completion ping then `task_get`. Use `?id=$id&tag=$tag` macros so each callback self-identifies.
4. On webhook receipt (or via `tasks_ready` polling once per minute as fallback), fetch/decode the result. Each `result.items[]` is a typed SERP element.
5. Filter `items[]` where `type == "organic"` and `domain`/`url` matches the tracked target; read `rank_absolute` (true position incl. features) and `rank_group` (position within organic). Capture `rank_changes` if comparing snapshots and the `item_types` array for SERP-feature presence (featured_snippet, ai_overview, local_pack, etc.).
6. Persist a timestamped row per keyword (`result.datetime`, `check_url`, rank, feature flags). Standard results stay retrievable for 30 days, so re-collection within that window is free if a write fails.
7. Re-fire on the schedule (cron). For any task whose webhook never arrived, call `webhook_resend` with up to 100 ids (no double charge).
8. Poll `user_data` sparingly (limit 6/min) to watch `money.balance` and avoid the daily cost cap (error 40203).

## Cost & cadence
- SERP Google Organic pricing (base 10 results): Standard Normal $0.0006/SERP, Standard High $0.0012/SERP, Live $0.002/SERP. The project cost-log shows `serp/google/organic/live/advanced` billing exactly $0.002.
- Raising `depth` above the default 10 increases cost (roughly doubles per extra 100 results); keep `depth` at 10 unless you genuinely track deep positions.
- 1,000 keywords daily at Standard Normal is about $0.60/day ($18/month); at Live it is about $2/day. The Standard delta is the single biggest lever, so reserve Live for ad-hoc spot checks.
- Cadence: daily for priority terms, weekly for the long tail. Standard Normal turnaround is roughly 5 minutes, High about 1 minute, Live about 2-6 seconds.

## Output
A position time-series table (keyword, location, device, date, rank_absolute, rank_group, url, SERP-feature flags) feeding rank-trend charts, win/loss alerts, share-of-voice rollups, and SERP-feature monitoring. Pairs naturally with [[play-competitor-gap-analysis]] and [[play-content-strategy-brief]].

## Pitfalls / limits
- Keyword special operators (`site:`, `filetype:`, `allinanchor:`, etc.) trigger a 5x keyword-cost multiplier; strip them from tracked terms unless intended.
- Standard results expire after 30 days; requesting them later returns error 40403. Live results are never stored, so a dropped Live response is lost.
- Rate ceiling is 2,000 calls/min and max 100 tasks per `task_post`; Live SERP also has a 120s timeout.
- Do not engineer concurrency to beat the queue. DataForSEO explicitly advises Standard + High priority over Live for bulk; webhooks unlock 100,000+ tasks/day.
- `device: mobile` and `desktop` are different SERPs; track them as separate rows, not one.

## Related
- [[cap-serp-api]]
- [[cap-serp-google-verticals]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-webhooks-pingback-postback]]
- [[cap-rate-limits-throughput]]
- [[cap-locations-languages-targeting]]
- [[plat-google-search]]
- [[dec-live-vs-standard-vs-priority]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[play-local-seo-tracking]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/overview/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/pingbacks-postbacks-with-dataforseo-api (retrieved 2026-06-26)
- https://dataforseo.com/help-center/collect-serp-data-from-dataforseo-api (retrieved 2026-06-26)
- https://dataforseo.com/apis/serp-api/pricing (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/user_data/ (retrieved 2026-06-26)
