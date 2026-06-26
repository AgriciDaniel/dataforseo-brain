---
type: concept
title: "Merchant API (Capability)"
domain: dataforseo
subdomain: merchant
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, merchant, ecommerce]
related:
  - "[[plat-amazon-marketplace]]"
  - "[[plat-google-shopping]]"
  - "[[play-ecommerce-product-research]]"
  - "[[cap-task-vs-live-execution]]"
---

# Merchant API (Capability)

> The Merchant API returns ecommerce search data from Amazon and Google Shopping: keyword product results, ASIN/product detail, seller offers, specifications, and reviews, delivered through the Task workflow (Amazon also offers Live). Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
Merchant is DataForSEO's product-marketplace scraping layer. It covers two engines: Amazon (`/v3/merchant/amazon/...`) and Google Shopping (`/v3/merchant/google/...`). You search by keyword to get a product SERP, look up a single product by ASIN or product_id for full detail, list the sellers offering a product, pull specifications, or fetch reviews. It is the data source behind product research, price monitoring, and competitive merchandising. Most endpoints follow the Task lifecycle (POST then poll `tasks_ready` then `task_get/advanced`); Amazon additionally exposes Live variants.

## What it covers
- Amazon: `/v3/merchant/amazon/products/task_post` (keyword product SERP), `/v3/merchant/amazon/asin/task_post` (product and its modifications by ASIN), `/v3/merchant/amazon/sellers/task_post` (seller offers, pricing, ratings). Each has Live `live/advanced` and `live/html` variants.
- Google Shopping: `/v3/merchant/google/products/task_post` (Shopping product SERP), `/v3/merchant/google/product_info/task_post` (product detail with sellers, rating, variations), `/v3/merchant/google/product_spec/task_post` (specification attributes), `/v3/merchant/google/sellers/task_post` (shops offering a product), `/v3/merchant/google/reviews/task_post` (product reviews).
- Config helpers: `/v3/merchant/{amazon,google}/locations/` and `.../languages/`.

## Key parameters / inputs
| field | notes |
|---|---|
| keyword | search term for products endpoints; up to 700 chars |
| asin / product_id | product identifier for detail, sellers, spec, reviews |
| location_code / location_name | one location identifier required |
| language_code / language_name | one language identifier required |
| depth | Amazon products default 100, max 700 |
| sort_by | relevance, price_low_to_high, price_high_to_low, featured, avg_customer_review, newest_arrival (Amazon) |
| price_min / price_max / department | Amazon product filters |
| priority | 1 normal or 2 high (costs more) |
| id | task UUID for task_get (valid 30 days) |

## Response / what you get back
Amazon ASIN returns `asin`, `title`, `author` (brand), `price_from`, `price_to`, `currency`, a `rating` object (`value`, `votes_count`, `rating_max`), `sellers`, `product_information`, `categories`, `product_images_list`, and `top_global_reviews`. Amazon Products SERP returns `items[]` with `type`, `rank`, `title`, `url`, `price`, `asin`, `rating`, and `delivery_info`, plus `se_results_count`. Google Shopping Products returns `items[]` with `rank_group`, `rank_absolute`, `title`, `seller`, `price`, `currency`, `product_images`, `product_rating`, and `delivery_info`. Product Info adds `sellers`, `rating`, `variations`, and `specifications`; Sellers returns `domain`, `total_price`, `seller_name`, and `rating`; Reviews returns `rating`, `rating_groups`, `top_keywords`, and per-review `review_text`, `author`, `publication_date`, and `rating`.

## Cost & method notes
- Billing is per task at POST time; results are retrievable free for 30 days. See [[cap-task-vs-live-execution]] and [[cap-queue-priority-cost-model]].
- **Recent change (2026-06-10): real-time Live endpoints added to the Amazon Merchant API.** Amazon Merchant was task-based only before this; the update introduced **Live mode** for real-time Amazon data (no task-post then poll `tasks_ready` then `task_get` wait). Live applies to the Amazon `products`, `asin`, and `sellers` functions via their `live/advanced` and `live/html` paths where applicable, so latency-sensitive ASIN/product lookups no longer need the queue. Google Shopping is still Standard/task-only and has no Live variant (calling a Shopping `live` path returns 40402, a non-existent-path error, not an add-on block). See [[cap-task-vs-live-execution]] and [[dec-live-vs-standard-vs-priority]].
- Amazon endpoints support both Standard (task) and Live methods; Google Shopping endpoints are Standard-only.
- Priority 2 (high) costs more than priority 1. In the cost log, a `/v3/merchant/google/products/live/advanced` call returned `task_status_code 40402` with `cost: 0.0`. 40402 means the URL path does not exist: Google Shopping simply has no Live variant, so that path is invalid. It is not an add-on or permission error (an add-on block returns 40204, not 40402).

## When to use / how it fits
Merchant is the core of [[play-ecommerce-product-research]] (Amazon/Shopping SERP + product detail + reviews), paired with [[cap-labs-keyword-research]] Amazon keywords and [[cap-app-data-api]] for apps. For pure Amazon keyword/competitor analytics over a pre-indexed database, use the Labs Amazon endpoints instead. Route jobs via [[dec-which-api-for-which-job]] and weigh queue vs live via [[dec-live-vs-standard-vs-priority]].

## Gotchas / limits
- Merchant is an add-on; Google Shopping is Standard-only (no Live variant). The 40402 on the live call is a "URL path does not exist" error from calling a non-existent Live path, not an add-on/permission block (those return 40204).
- 2000 combined POST+GET calls/min; max 100 tasks per POST; task ids valid 30 days.
- Location/language support varies by marketplace; validate with the locations/languages helpers before posting.
- Use `product_id` (not ASIN) for Google Shopping detail endpoints; the two engines do not share identifiers.
- Amazon `asin` lookups return the product plus the ASINs of all its modifications (size, color, variant), so a single call can fan out into a family of related listings.
- The `advanced` task_get returns structured fields while `html` returns the raw page; choose `advanced` for parsing and `html` only when you need the original markup.
- Amazon `sort_by` and `price_min`/`price_max` only apply to the products SERP endpoint, not to ASIN or sellers lookups.
- Reviews and ratings come from the marketplace at scrape time, so a product with few reviews returns a sparse `rating` object rather than an error.

## Related
- [[plat-amazon-marketplace]]
- [[plat-google-shopping]]
- [[cap-labs-keyword-research]]
- [[cap-app-data-api]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-platform-architecture]]
- [[play-ecommerce-product-research]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/merchant/amazon/products/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/merchant/amazon/asin/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/merchant/google/products/task_get/advanced/ (retrieved 2026-06-26)
- https://dataforseo.com/updates/category/merchant-api (retrieved 2026-06-26 - Live Endpoints in Amazon Merchant API, published 2026-06-10)
- https://docs.dataforseo.com/v3/merchant/amazon/asin/live/advanced/ (retrieved 2026-06-26)
