---
type: flow
title: "Play: Local SEO Tracking"
domain: dataforseo
subdomain: business-data
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, serp, business-data, local]
related:
  - "[[cap-serp-google-verticals]]"
  - "[[cap-business-data-api]]"
  - "[[plat-google-maps-local]]"
---

# Play: Local SEO Tracking

> Track Maps/Local Finder pack rankings per location, then pull the Google Business Profile and review signals behind them. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
Local SEO is location-specific: the same keyword returns different local packs from different coordinates. This flow tracks pack position by precise geo, then enriches the winning/losing listings with Business Profile details and review sentiment. It combines the SERP API local verticals with the Business Data API for a per-location local visibility picture.

## Trigger
A multi-location business (or a local-pack target) needs ranking visibility: a "near me" tracking program, a new storefront launch, or a reputation review. Inputs are a keyword set, a list of `location_coordinate` points (lat,lon,zoom), and the business identity (name/CID).

## Endpoints used (in order)
- `POST /v3/serp/google/local_finder/live/advanced` (Local Finder pack ranks).
- `POST /v3/serp/google/maps/live/advanced` (Maps results by coordinate).
- `POST /v3/business_data/google/my_business_info/task_post` then `task_get/$id` (or `/live`).
- `POST /v3/business_data/google/reviews/task_post` then `task_get/$id` (review stream).
- `POST /v3/business_data/google/my_business_updates/task_post` (profile change monitoring).

## Pipeline
1. Define the geo grid: for each tracked location set a `location_coordinate` (`latitude,longitude,zoom`) so rankings reflect a real searcher position, not a city centroid. Pick `device` and `language_code`.
2. Pull pack ranks: call `local_finder/live/advanced` (default 20 desktop / 10 mobile, max 100) and/or `maps/live/advanced` per keyword x coordinate. Optionally filter with `min_rating` or `time_filter` (e.g. `open_now`).
3. Parse `result.items[]` where `type == "local_pack"`: read `rank_absolute`, `rank_group`, `title`, `rating` (value, votes_count), `cid`, `phone`, `domain`. Match `cid`/`title` to your tracked business to record its pack position per location.
4. Enrich the profile: feed the matched `cid`/keyword to `my_business_info` to capture `address`, `phone`, `work_time`, `category`, `attributes`, `place_id`, and `rating` for NAP and profile-completeness checks.
5. Pull reviews via `reviews` (task-based) for the review stream (rating, text, timestamp, owner responses) to compute volume, average rating, and recency.
6. Watch for drift: schedule `my_business_updates` to catch profile edits, and re-run the pack queries on cadence to chart per-location position.
7. Roll up: build a location x keyword grid of pack position plus rating/review velocity for each storefront.

## Cost & cadence
- SERP local verticals bill like SERP: the cost-log shows `serp/google/maps/live/advanced` at $0.002 per call; Local Finder is billed per SERP (up to 20 desktop / 10 mobile) with extra results charged more, and `priority: 2` costs more.
- Business Data Google endpoints charge only for setting a task, with results free to re-collect for 30 days; `business_listings/search/live` shows $0.0103 in the cost-log as a reference point.
- Cadence: pack ranks weekly per location; reviews daily or weekly to keep the stream fresh; profile updates monitored continuously.

## Output
A per-location local visibility dashboard: pack position by keyword and coordinate, profile completeness/NAP record, review volume and average rating trend, and a profile-change log. Complements [[play-rank-tracking-pipeline]] for organic positions.

## Pitfalls / limits
- A `location_coordinate` without a zoom level, or a coarse city `location_name`, blurs local results; use precise lat,lon,zoom for trustworthy tracking.
- Local Finder/Maps are one task per request (no 100-task batching like organic); plan throughput around the per-location call count.
- Business Data review pulls are task-based; budget for the post-then-collect latency rather than expecting instant data.
- Mobile and desktop local packs differ in size (10 vs 20) and order; track them separately.
- `min_rating` ranges differ by device (3.5-4.5 desktop, 2-4.5 mobile); a filter that works on desktop may be invalid on mobile.

## Decisions in play
- [[dec-which-api-for-which-job]]: SERP local verticals for pack position, Business Data for the profile and review stream behind each listing.
- [[dec-live-vs-standard-vs-priority]]: Live for ad-hoc pack checks; Standard task-based for scheduled multi-location tracking and review pulls.
- [[dec-cost-control-strategy]]: local verticals are one task per request (no 100-task batching), so plan throughput around the location x keyword call count.
- [[dec-when-not-to-use-dataforseo]]: a non-technical single-location owner who needs a dashboard may be better served by a packaged local-SEO tool than raw data.

## Related
- [[cap-serp-api]]
- [[cap-serp-google-verticals]]
- [[cap-business-data-api]]
- [[cap-locations-languages-targeting]]
- [[cap-task-vs-live-execution]]
- [[plat-google-maps-local]]
- [[plat-review-platforms]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[play-rank-tracking-pipeline]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/google/local_finder/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/business_data/google/my_business_info/task_get/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/business_data/overview/ (retrieved 2026-06-26)
- https://dataforseo.com/apis/serp-api/pricing (retrieved 2026-06-26)
