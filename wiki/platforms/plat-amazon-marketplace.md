---
type: platform
title: "Amazon Marketplace as a DataForSEO Surface"
domain: dataforseo
subdomain: merchant
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, merchant, amazon, ecommerce]
related:
  - "[[cap-merchant-api]]"
  - "[[cap-labs-keyword-research]]"
  - "[[play-ecommerce-product-research]]"
---

# Amazon Marketplace as a DataForSEO Surface

> Amazon as a product-search, product-detail, seller, and review surface, split across the live Merchant API and the pre-indexed Labs Amazon datasets. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
DataForSEO reaches Amazon two ways. The Merchant API scrapes live Amazon: keyword search results, full ASIN product detail, and seller listings. DataForSEO Labs keeps a pre-indexed in-house Amazon database that powers keyword and competitor research: which keywords an ASIN ranks for, related keyword ideas, product competitors, and bulk search volume. The live side answers "what is on this page right now"; the Labs side answers "what should I target and who competes" without a fresh scrape, at lower cost. Together they cover Amazon SEO and product research end to end.

## What it covers
- Merchant `amazon/products`: keyword-based product SERP with `amazon_serp`, `amazon_paid`, `editorial_recommendations`, `top_rated_from_our_brands`, and `related_searches` item types.
- Merchant `amazon/asin`: full product detail including modifications, `top_local_reviews`, `top_global_reviews`, `product_information`, `categories`, `product_images_list`, `product_videos_list`.
- Merchant `amazon/sellers`: seller listings for an ASIN with `seller_name`, `price.current`, `rating.value`, `delivery_info`.
- Labs `amazon/ranked_keywords`: keywords an ASIN ranks for, with rank_group, rank_absolute, and search volume.
- Labs `amazon/related_keywords`: related-search keyword ideas (depth 0-4, up to ~1554 keywords) with search volume.
- Labs also offers `amazon/bulk_search_volume`, `amazon/product_competitors`, `amazon/product_rank_overview`, and `amazon/product_keyword_intersections`.

## Key parameters / inputs
- Merchant Products: `keyword` (up to 700 chars), one location field, one language field, `depth` (default 100, max 700), `max_crawl_pages` (max 7), `department`, `price_min`/`price_max`, `sort_by` (relevance, price_low_to_high, avg_customer_review, newest_arrival).
- Merchant ASIN / Sellers: `asin` (required), location and language, `priority`, postback/pingback.
- Labs Ranked Keywords: `asin`, location and language, `limit` (max 1000), `filters` (max 8), `order_by`.
- Labs Related Keywords: `keyword` (lowercase), `depth` (0-4), `include_seed_keyword`, `limit` (max 1000).

## Response / what you get back
- Product SERP items: `type`, `rank`, `title`, `url`, `price`, `asin`, `rating`, `delivery_info`; `result.categories` lists Amazon departments.
- ASIN result: `title`, `author` (brand), `price_from`, `price_to`, `currency`, `rating` object, plus review and media arrays.
- Labs Ranked Keywords: `keyword_data.keyword_info.search_volume` and `ranked_serp_element.serp_item` (rank, title, url, asin, price_from, rating).

## Cost & method notes
- Merchant tasks charge only for posting; results are retrievable free for 30 days; Standard and Live both exist; priority 2 costs more. See [[cap-task-vs-live-execution]].
- Labs Amazon endpoints are Live-only POST against the pre-indexed database, so they cost less than a live scrape (example tasks around $0.011). See [[dec-labs-vs-live-apis]].
- 2000 calls/min; Merchant allows 100 tasks/POST; Labs allows 30 simultaneous requests. See [[cap-rate-limits-throughput]].

## When to use / how it fits
- Full product and ASO intelligence loop blending Merchant, Labs, and App Data: [[play-ecommerce-product-research]].
- Amazon keyword targeting as part of broader keyword research: [[play-keyword-research-workflow]].
- Deciding live Merchant versus pre-indexed Labs: [[dec-labs-vs-live-apis]].
- Routing the product job to the right module: [[dec-which-api-for-which-job]].

## Gotchas / limits
- Labs Amazon endpoints currently support only United States, Egypt, Saudi Arabia, and United Arab Emirates locations (typically US/English).
- Merchant Products `max_crawl_pages` is capped at 7 (lower than the web SERP cap of 100).
- ASINs are the join key; get them from Merchant Products before calling ASIN, Sellers, or Labs Ranked Keywords.
- Labs data is pre-indexed and can lag live Amazon; use Merchant for the freshest page state. See [[cap-data-collection-methodology]].

## Related
- [[cap-merchant-api]]
- [[cap-labs-keyword-research]]
- [[cap-labs-competitor-research]]
- [[cap-databases]]
- [[cap-task-vs-live-execution]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[cap-data-collection-methodology]]
- [[play-ecommerce-product-research]]
- [[play-keyword-research-workflow]]
- [[plat-google-shopping]]
- [[plat-app-stores]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/merchant/amazon/products/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/merchant/amazon/asin/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/merchant/amazon/sellers/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/dataforseo_labs/amazon/ranked_keywords/live/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/dataforseo_labs/amazon/related_keywords/live/ - retrieved 2026-06-26
