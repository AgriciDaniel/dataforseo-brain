---
type: platform
title: "Google Shopping as a DataForSEO Surface"
domain: dataforseo
subdomain: merchant
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, merchant, google-shopping, ecommerce]
related:
  - "[[cap-merchant-api]]"
  - "[[cap-serp-google-verticals]]"
  - "[[play-ecommerce-product-research]]"
---

# Google Shopping as a DataForSEO Surface

> Google Shopping product results, per-product detail, multi-seller price comparison, and product reviews exposed through the Merchant API. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
The Merchant API's Google group turns Google Shopping into structured commerce data. Five endpoints cover the funnel: a product SERP (sponsored carousels, paid units, and organic listings for a keyword), a product-info detail view (sellers, variations, specifications), a product-spec view (specification attributes by `product_id`), a sellers view (every shop offering a product, with total price including tax and shipping), and a reviews view (rating distribution, review text, and the keywords reviewers mention most). This is the price-comparison and product-research counterpart to Amazon, useful for pricing intelligence and Shopping SEO.

## What it covers
- Merchant `google/products`: Google Shopping SERP with item types `google_shopping_sponsored_carousel`, `google_shopping_paid`, `google_shopping_serp`, `google_shopping_carousel`, `related_searches`.
- Merchant `google/product_info`: one product's sellers, rating, variations, and specifications by `product_id`.
- Merchant `google/product_spec`: specification attributes for one product by `product_id` (the dedicated spec endpoint, distinct from the inline specifications in product_info).
- Merchant `google/sellers`: shops offering a product (`shops_list` or `buy_on_google`) with `total_price`, `seller_name`, `domain`, `rating`.
- Merchant `google/reviews`: product reviews with `rating_groups` (1-5 star distribution), `top_keywords` (keyword plus mention count), and per-review `review_text`, `author`, `rating`.
- The SERP API also surfaces Shopping inside Google web results (`shopping`, `popular_products` elements), but Merchant gives the dedicated commerce structure.

## Key parameters / inputs
- Products: `keyword`, one location field, one language field, `se_domain`, `priority`, `depth`, postback/pingback.
- Product Info / Sellers / Reviews: `product_id` (the Google Shopping product identifier), location and language, `priority`.
- Sellers can alternatively take a `keyword`; an `ad_url` GET helper resolves sponsored seller URLs.
- task_get uses `id` (UUID), valid for 30 days.

## Response / what you get back
- Product SERP item: `title`, `seller`, `price`, `currency` (ISO 4217), `product_images[]`, `product_rating`, `delivery_info`, `special_offer_info`, plus `google_shopping_serp` extras like `shopping_url`, `product_id`, `reviews_count`, `is_best_match`, `stores_count_info`.
- `delivery_info.delivery_price`: current, regular, max_value, currency, is_price_range, displayed_price.
- Sellers item: `total_price` (tax and shipping included), `seller_name`, `domain`, `rating`.
- Reviews: `rating` (Max5), `rating_groups[]`, `top_keywords[]`, and per-review images, title, review_text, provided_by, author, publication_date.

## Cost & method notes
- All five Google Merchant endpoints use the Standard method: charge only for posting the task, results free for 30 days. See [[cap-task-vs-live-execution]].
- Priority 1 (normal) versus 2 (high); high costs more. See [[cap-queue-priority-cost-model]].
- 2000 calls/min; 100 tasks/POST. See [[cap-rate-limits-throughput]].

## When to use / how it fits
- Pricing and product intelligence inside an e-commerce research loop: [[play-ecommerce-product-research]].
- Pairing Shopping price comparison with Amazon product data for cross-marketplace pricing: [[plat-amazon-marketplace]].
- Reviews and `top_keywords` feed sentiment and content work alongside [[cap-content-analysis-api]].
- Choosing the right commerce endpoint: [[dec-which-api-for-which-job]].

## Gotchas / limits
- `product_id` is the join key for Product Info, Sellers, and Reviews; obtain it from the Products SERP first.
- The Google Shopping endpoints are Standard-only in the docs (no Live variant), unlike the Amazon Merchant endpoints.
- Shopping inventory is geo and currency dependent; pin location, language, and expect `currency` to vary.
- The legacy `url` field on `google_shopping_serp` is deprecated in favor of `shopping_url`.

## Related
- [[cap-merchant-api]]
- [[cap-serp-google-verticals]]
- [[cap-content-analysis-api]]
- [[cap-task-vs-live-execution]]
- [[cap-locations-languages-targeting]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[play-ecommerce-product-research]]
- [[play-content-strategy-brief]]
- [[plat-amazon-marketplace]]
- [[plat-review-platforms]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/merchant/google/products/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/merchant/google/product_info/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/merchant/google/product_spec/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/merchant/google/sellers/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/merchant/google/reviews/task_get/advanced/ - retrieved 2026-06-26
