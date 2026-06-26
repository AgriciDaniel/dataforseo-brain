---
type: flow
title: "Play: Ecommerce Product Research"
domain: dataforseo
subdomain: merchant
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, merchant, app-data, labs]
related:
  - "[[cap-merchant-api]]"
  - "[[cap-app-data-api]]"
  - "[[cap-labs-keyword-research]]"
---

# Play: Ecommerce Product Research

> Combine Amazon/Google Shopping product data, Amazon keyword demand from Labs, and app-store reviews into product and ASO intelligence. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
This flow assembles a product-research picture across three surfaces: marketplace SERPs and product detail (Merchant API for Amazon and Google Shopping), marketplace keyword demand (DataForSEO Labs Amazon dataset), and app discovery/reviews (App Data for Google Play and Apple App Store). It supports listing optimization, pricing analysis, competitor product mapping, and ASO.

## Trigger
A seller, brand, or app publisher needs market intelligence: a new product launch, a pricing review, a listing/ASO optimization pass, or competitor product monitoring. Inputs are seed keywords, target ASINs/product URLs, and/or app ids.

## Endpoints used (in order)
- `POST /v3/merchant/amazon/products/task_post` then `task_get/advanced/$id` (Amazon keyword SERP).
- `POST /v3/merchant/amazon/asin/task_post` then `task_get/advanced/$id` (product detail).
- `POST /v3/merchant/amazon/reviews/task_post` (Amazon reviews).
- `POST /v3/merchant/google/products/live/advanced` (Google Shopping products).
- `POST /v3/dataforseo_labs/amazon/related_keywords/live` and `/bulk_search_volume/live` (Amazon demand).
- `POST /v3/app_data/google/app_reviews/task_post` and `/v3/app_data/apple/app_reviews/task_post` (ASO reviews).

## Pipeline
1. Map the marketplace SERP: post Amazon `products` for the seed keyword (`depth` default 100, max 700; `max_crawl_pages` max 7; optional `sort_by`, `price_min`/`price_max`, `department`). Parse `items[]` (`amazon_serp`, `amazon_paid`, `editorial_recommendations`) for rank, title, price, ASIN, rating, delivery info.
2. Pull product detail for the top ASINs via Amazon `asin` to get full attributes, pricing, and seller data; cross-reference Google Shopping with `merchant/google/products` for the same products across that surface.
3. Read reviews: post Amazon `reviews` for the target ASINs to capture rating distribution and review text for sentiment and feature gaps.
4. Size keyword demand: run Labs Amazon `related_keywords` (depth 0-4; depth 4 yields up to ~1,554 ideas, each with `search_volume`) and `bulk_search_volume` to score the keyword universe for listings/PPC.
5. For apps, pull `app_reviews` (Google Play and Apple) to mine rating, `review_text`, `helpful_count`, app `version`, and developer `responses` for ASO and roadmap signals; add app searches/listings for ranking context.
6. Synthesize: a product/competitor matrix (price, rating, review volume, keyword coverage) plus an ASO/listing keyword list and a review-driven feature backlog.

## Cost & cadence
- Merchant Amazon Products/Sellers: Standard $0.001/product (per 40 results), Priority $0.002, Live $0.0033; Amazon ASIN: Standard $0.0015, Priority $0.003, Live $0.005. Google Shopping products: Standard $0.001, Priority $0.002; reviews $0.00075/10 reviews.
- App Data reviews are cheap per batch: Google Play $0.00075/150 reviews, Apple $0.00075/50 reviews (Standard); app Info $0.0006/result.
- Labs Amazon demand endpoints bill about $0.0105 (`related_keywords`) and $0.0101 (`bulk_search_volume`) per request (cost-log).
- Cadence: keyword/competitor research on demand; price and review monitoring daily or weekly.

## Output
A product-research pack: marketplace competitor matrix, product/pricing detail, Amazon keyword demand list, and a review-mined sentiment + feature-gap report for listings and ASO.

## Pitfalls / limits
- Merchant and App Data review/product endpoints are task-based: budget for the post-then-collect latency; results are free to re-collect for 30 days.
- Amazon `products` billing is per 40 results returned; reviews bill per 10 (Amazon/Shopping) or per 50/150 (Apple/Google Play) items, so `depth` drives cost.
- Labs Amazon `related_keywords` location support is limited to United States, Egypt, Saudi Arabia, and UAE (typically US/English); it is not global.
- Google Play review `title` is always null; do not rely on it.
- Marketplace data reflects the queried `location_code`/`language_code` and `se_domain`; keep them consistent when comparing across runs.

## Decisions in play
- [[dec-which-api-for-which-job]]: Merchant for marketplace SERP/product/review data, Labs Amazon for keyword demand, App Data for ASO reviews.
- [[dec-live-vs-standard-vs-priority]]: Merchant and App Data support Standard task-based collection; use it for scheduled monitoring and reserve Live for spot checks.
- [[dec-cost-control-strategy]]: billing scales with `depth` and result count (per 40 products, per 10/50/150 reviews), so cap depth to what you actually analyze.

## Related
- [[cap-merchant-api]]
- [[cap-app-data-api]]
- [[cap-labs-keyword-research]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[plat-amazon-marketplace]]
- [[plat-google-shopping]]
- [[plat-app-stores]]
- [[plat-review-platforms]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/merchant/amazon/products/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/amazon/related_keywords/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/app_data/google/app_reviews/task_get/advanced/ (retrieved 2026-06-26)
- https://dataforseo.com/pricing/merchant/amazon-api (retrieved 2026-06-26)
- https://dataforseo.com/pricing/app-data/google-play (retrieved 2026-06-26)
