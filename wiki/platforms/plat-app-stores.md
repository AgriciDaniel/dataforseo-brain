---
type: platform
title: "App Stores as DataForSEO Surfaces"
domain: dataforseo
subdomain: app-data
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, app-data, aso, mobile]
related:
  - "[[cap-app-data-api]]"
  - "[[cap-labs-keyword-research]]"
  - "[[play-ecommerce-product-research]]"
---

# App Stores as DataForSEO Surfaces

> Apple App Store and Google Play exposed as ASO surfaces, split between the live App Data API and the pre-indexed Labs app datasets. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
DataForSEO covers both major app stores for app store optimization (ASO). The App Data API reads live store data: keyword search results, app listings, full app info, and reviews for both Apple App Store and Google Play. DataForSEO Labs keeps a pre-indexed app database that answers the keyword side of ASO, the keywords an app ranks for and the app's position per keyword, mirroring how the Labs Google and Amazon datasets work. The live App Data side captures the current listing and review state; the Labs side gives cheap, bulk keyword-rank intelligence.

## What it covers
- App Data `apple/app_searches` and `google/app_searches`: apps ranking for a keyword, with app_id, title, rating, reviews_count, is_free, price, icon, url.
- App Data `apple/app_info` and `google/app_info`: full app detail (developer, version, size, screenshots, rating, price).
- App Data `apple/app_reviews` and `google/app_reviews`: review items with rating (Max5), review_text, user_profile, timestamp, and developer responses.
- App Data `apple/app_listings` and `google/app_listings`: bulk listing pulls.
- Labs `apple/keywords_for_app` and `google/keywords_for_app`: keywords an app ranks for, with search volume and rank (serp types `app_store_search_organic` and `google_play_search_organic`).
- Labs also offers `app_competitors`, `app_intersection`, and `bulk_app_metrics` for both stores.

## Key parameters / inputs
- App Data searches: `keyword` (up to 700 chars), one location field, optional language, `priority`, `depth`. Depth differs by store: Google Play default 30, max 200, multiples of 30, billed per SERP of 30; Apple default 100, max 700, multiples of 100, billed per SERP of 100.
- App Data info / reviews: `app_id`, location and language, `depth`, `sort_by` for reviews.
- Labs Keywords For App: `app_id` (Apple numeric like `835599320`; Google Play package name like `org.telegram.messenger`), one location field, one language field, `limit` (max 1000), `filters` (max 8), `order_by` (max 3).

## Response / what you get back
- App search item: `app_id`, `title`, `url`, `icon`, `rating` (type, value, votes, max), `reviews_count`, `is_free`, `price`, `developer`, `rank_group`, `rank_absolute`.
- App reviews item: `version` (app version), `rating`, `timestamp`, `title`, `review_text`, `user_profile`, `responses[]` (developer replies).
- Labs Keywords For App: `keyword_data.keyword_info.search_volume` and `ranked_serp_element.serp_item` with rank_group, rank_absolute, title, url, rating, is_free.

## Cost & method notes
- App Data endpoints are Standard: charge only for setting the task; results free for 30 days; Normal/High priority. `app_searches` billing differs by store: Google Play bills per SERP of up to 30 results, Apple bills per SERP of up to 100 results. See [[cap-task-vs-live-execution]].
- Labs app endpoints are Live-only POST against the pre-indexed database (example tasks around $0.011), cheaper than a live store scrape. See [[dec-labs-vs-live-apis]].
- 2000 calls/min; App Data 100 tasks/POST; Labs 30 simultaneous requests. See [[cap-rate-limits-throughput]].

## When to use / how it fits
- ASO and product research blending App Data reviews with Labs keyword ranks: [[play-ecommerce-product-research]].
- App keyword targeting inside broader keyword research: [[play-keyword-research-workflow]].
- Choosing live App Data versus pre-indexed Labs: [[dec-labs-vs-live-apis]].
- Routing the ASO job to the right module: [[dec-which-api-for-which-job]].

## Gotchas / limits
- Labs Keywords For App currently supports the US location and English language only for both stores.
- App identifiers differ by store: Apple uses the numeric App Store id, Google Play uses the package name; get them from the URL or app_searches.
- Advertising keyword_info fields (competition, cpc, bids) are null for the Labs app endpoints.
- Labs data is pre-indexed and can lag the live store listing. See [[cap-data-collection-methodology]].

## Related
- [[cap-app-data-api]]
- [[cap-labs-keyword-research]]
- [[cap-labs-competitor-research]]
- [[cap-databases]]
- [[cap-task-vs-live-execution]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[cap-data-collection-methodology]]
- [[play-ecommerce-product-research]]
- [[play-keyword-research-workflow]]
- [[plat-amazon-marketplace]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/app_data/apple/app_searches/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/app_data/apple/app_info/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/app_data/google/app_searches/task_post/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/dataforseo_labs/apple/keywords_for_app/live/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/dataforseo_labs/google/keywords_for_app/live/ - retrieved 2026-06-26
