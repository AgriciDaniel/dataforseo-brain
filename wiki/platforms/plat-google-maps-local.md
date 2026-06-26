---
type: platform
title: "Google Maps and Local as a DataForSEO Surface"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, local-seo, business-data]
related:
  - "[[cap-serp-google-verticals]]"
  - "[[cap-business-data-api]]"
  - "[[play-local-seo-tracking]]"
---

# Google Maps and Local as a DataForSEO Surface

> Google Maps, Local Finder, Google Business Profile, Hotels, and the indexed business-listings database exposed as local-SEO data. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
The local surface spans two DataForSEO modules. The SERP API reads the live ranked local results (Maps pack and Local Finder) for a keyword at a location, while the Business Data API reads the durable profile of a single establishment (its description, hours, attributes, reviews, Q&A, and updates). Together they let a practitioner track where a business ranks in the map results and audit the profile that those rankings feed. Geo precision comes from `location_coordinate`, which makes grid-based local rank tracking possible.

## What it covers
- `serp/google/maps` returns up to 100 (desktop) local business listings: `maps_search` organic items and `maps_paid_item` ads.
- `serp/google/local_finder` returns the Local Finder pack (`local_pack` items, up to 20 desktop / 10 mobile by default).
- `business_data/google/my_business_info` returns one establishment's public profile (title, rating, address, phone, work_time, category, attributes, place_id, cid).
- `business_data/google/reviews` returns reviews (review_text, rating, owner_answer, review_highlights, local_guide status, images).
- `business_data/google/questions_and_answers` returns the listing's Q&A (`items` answered, `items_without_answers` unanswered).
- `business_data/google/my_business_updates`, `business_data/google/hotel_searches`, and `business_data/google/hotel_info` cover posts and Google Hotels stays.
- `business_data/business_listings/search` queries DataForSEO's indexed Google Maps POI database by category and coordinate radius.

## Key parameters / inputs
- SERP Maps/Local Finder: `keyword`, one location field (coordinate is key for grid tracking), one language field, `depth`, `device`.
- Local Finder adds `min_rating` and `time_filter` (for example "open_now" or "monday;18").
- My Business Info / Reviews / Q&A: `keyword` plus `place_id` or `cid` to pin the exact establishment; `depth` and `sort_by` for reviews.
- Hotel Searches: `keyword`, `check_in`, `check_out`, `adults`, `children`, `currency`, `sort_by`.
- Business Listings Search: `categories` (max 10), `location_coordinate` ("latitude,longitude,radius" in km, 1-100,000), `is_claimed`, `filters`.

## Response / what you get back
- Maps items: `rank_group`, `rank_absolute`, `title`, `rating` (value, votes_count), `rating_distribution`, `address_info`, `place_id`, `phone`, `category`, `work_hours`, `latitude`, `longitude`, `is_claimed`, `price_level`, `hotel_rating`.
- Local Finder items: `local_pack` with `title`, `rating`, `phone`, `booking_url`, `cid`, `is_paid`.
- My Business Info: a single profile object keyed by `place_id` and `cid`.
- Business Listings items expose `popular_times`, `place_topics`, `attributes`, `services`, `contact_info`.

## Cost & method notes
- SERP Maps and Local Finder bill per SERP (up to 100 / up to 20 results) with Standard and Live methods; priority 2 costs more. See [[cap-queue-priority-cost-model]].
- Business Data tasks charge only for setting the task; results stay retrievable free for 30 days, and a Live method is also available. See [[cap-task-vs-live-execution]].
- Business Listings Search and Pinterest are Live-only and charge per request.

## When to use / how it fits
- Per-location map rank plus profile plus reviews tracking: [[play-local-seo-tracking]].
- Multi-location reputation monitoring blends Maps ranks with Google Reviews and Q&A.
- Local competitor discovery uses Business Listings Search across a category and radius.
- Routing a local job to the right module: [[dec-which-api-for-which-job]].

## Gotchas / limits
- Mobile caps Maps at 20 results and Local Finder at 10; pin `device` and `location_coordinate` for reproducible grids.
- Profile data is only as fresh as the last crawl; `datetime` records when it was captured.
- 2000 calls/min; 100 tasks/POST (1 for Live). See [[cap-rate-limits-throughput]].
- `place_id` and `cid` are the reliable join keys across Maps, Reviews, and Q&A; keyword-only lookups can drift.

## Related
- [[cap-serp-google-verticals]]
- [[cap-business-data-api]]
- [[cap-serp-api]]
- [[cap-locations-languages-targeting]]
- [[cap-task-vs-live-execution]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[play-local-seo-tracking]]
- [[play-competitor-gap-analysis]]
- [[plat-review-platforms]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/google/maps/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/google/local_finder/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/business_data/google/my_business_info/task_get/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/business_data/google/reviews/task_get/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/business_data/business_listings/search/live/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/business_data/google/hotel_searches/task_get/ - retrieved 2026-06-26
