---
type: concept
title: "App Data API (Capability)"
domain: dataforseo
subdomain: app-data
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, app-data, aso]
related:
  - "[[plat-app-stores]]"
  - "[[cap-labs-keyword-research]]"
  - "[[play-ecommerce-product-research]]"
  - "[[cap-task-vs-live-execution]]"
---

# App Data API (Capability)

> The App Data API returns Apple App Store and Google Play data for app-store optimization: keyword searches, category lists, app detail, reviews, and a live indexed app-catalog query (app_listings). Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
App Data is DataForSEO's ASO layer, mirroring its web-SERP tooling for mobile app stores. It covers two engines, Apple (`/v3/app_data/apple/...`) and Google Play (`/v3/app_data/google/...`), each with parallel endpoints. You search a store by keyword to see which apps rank, pull top-chart lists by category, fetch a single app's full metadata, read its reviews, or query a pre-indexed catalog of apps with filters. The first four are Task-based (POST then poll then `task_get/advanced`); `app_listings` is a Live, database-style query. It is the data behind keyword-rank tracking, competitor monitoring, and review analysis for apps.

## What it covers
- `/v3/app_data/{apple,google}/app_searches/task_post` - SERP-style keyword ranking across the store; returns ranked apps with ratings, prices, review counts.
- `/v3/app_data/{apple,google}/app_list/task_post` - top charts and collections within a category.
- `/v3/app_data/{apple,google}/app_info/task_post` - one app's detail (description, screenshots, installs, category, versions, related apps).
- `/v3/app_data/{apple,google}/app_reviews/task_post` - review data (rating, text, user profile, timestamp, developer responses).
- `/v3/app_data/{apple,google}/app_listings/search/live` - a Live query over DataForSEO's indexed app catalog, filtered by category, title, or description.
- Config helpers: `/v3/app_data/{apple,google}/categories/`, `.../locations/`, `.../languages/`.

## Key parameters / inputs
| field | notes |
|---|---|
| keyword | search term for app_searches; up to 700 chars, URL-encoded |
| app_id | app identifier for app_info and app_reviews |
| location_code / location_name, language_code / language_name | location and language identifiers |
| depth | app_searches differs by store: Google Play default 30, max 200, multiples of 30 (each 30 = one SERP); Apple default 100, max 700, multiples of 100 (each 100 = one SERP) |
| categories | array; app_list 1+, app_listings up to 10 |
| title / description | keyword filters on app_listings (up to 200 chars) |
| filters / order_by / limit / offset_token | app_listings: max 8 filters, max 3 sort rules, limit up to 1000, token beyond 100000 |
| priority | 1 normal or 2 high (faster, costs more) |

## Response / what you get back
App result objects expose `app_id`, `title`, `developer`, `url`, `icon`, a `rating` object (`type`, `value`, `votes`, `maximum`), `reviews_count`, `is_free`, a `price` object, `version`, `size`, `images`, `videos`, `description`, `main_category`, `genres`, `installs` / `installs_count`, and `similar_apps`; search and list endpoints add `rank_group` and `rank_absolute`. Review objects carry `rank_group`, `rank_absolute`, `position`, `version`, a `rating` object, `timestamp`, `review_text`, a `user_profile` object, and `responses` (developer replies), with `helpful_count` on Google Play. `app_listings` returns `total_count`, `count`, `offset_token`, and an `items[]` array of app objects.

## Cost & method notes
- Task endpoints (`app_searches`, `app_list`, `app_info`, `app_reviews`) charge at POST and allow free retrieval within 30 days. `app_searches` billing differs by store: Google Play bills per SERP of up to 30 results (so `depth: 60` is two SERPs and twice the cost), while Apple bills per SERP of up to 100 results (so `depth: 200` is two SERPs). See [[cap-task-vs-live-execution]].
- `app_listings` is Live and billed per request (the docs cite a Google Play example around $0.11 per request); Apple `app_listings` is a separate Live endpoint priced differently. One task per POST.
- Priority 2 costs more than priority 1. See [[cap-queue-priority-cost-model]].

## When to use / how it fits
Use `app_searches` and `app_info` for ASO keyword-rank and competitor monitoring, `app_reviews` for sentiment and feature feedback, and `app_listings` for broad market discovery over the indexed catalog. It pairs with [[cap-labs-keyword-research]] (apple/google `keywords_for_app`) and feeds [[play-ecommerce-product-research]] on the app side. Route jobs via [[dec-which-api-for-which-job]].

## Gotchas / limits
- `app_listings` (database index) differs from `app_searches` (live keyword SERP): the listing endpoint has no relevance ranking and filters/sorts by catalog fields, useful for discovery, not keyword position.
- `depth` granularity differs by store: Google Play uses multiples of 30 (each 30 results is a separately billed SERP), Apple uses multiples of 100 (each 100 results is a separately billed SERP). Do not assume Apple mirrors Google Play.
- 2000 calls/min, max 100 tasks per Task POST, but one task per `app_listings` Live POST.
- Encode special characters in `keyword` (%25 for "%", %2B for "+"); validate categories/locations/languages with the helper endpoints.
- App ids differ by store: the App Store uses a numeric id while Google Play uses a package name (for example `org.telegram.messenger`); passing the wrong format returns no app.
- `installs` is a display string (for example "1,000,000+") while `installs_count` is the exact integer; use the integer for any math.
- Review `responses` capture developer replies, so the same endpoint supports both sentiment tracking and support-responsiveness monitoring.

## Related
- [[plat-app-stores]]
- [[cap-labs-keyword-research]]
- [[cap-merchant-api]]
- [[cap-business-data-api]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-platform-architecture]]
- [[play-ecommerce-product-research]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/app_data/apple/app_searches/task_post/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/app_data/google/app_searches/task_post/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/app_data/apple/app_searches/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/app_data/google/app_listings/search/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/app_data/google/app_reviews/task_get/advanced/ (retrieved 2026-06-26)
