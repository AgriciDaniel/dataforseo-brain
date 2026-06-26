---
type: concept
title: "Labs Market Analysis (Capability)"
domain: dataforseo
subdomain: labs
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, labs, market-analysis]
related:
  - "[[cap-labs-keyword-research]]"
  - "[[cap-labs-competitor-research]]"
  - "[[cap-keywords-data-api]]"
  - "[[play-content-strategy-brief]]"
---

# Labs Market Analysis (Capability)

> The DataForSEO Labs market-analysis endpoints map demand by Google product/service category: which categories a domain ranks in, which categories a keyword belongs to, the top searches in a market, and the keywords inside any category. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
This Labs family shifts the unit of analysis from one keyword or domain to a whole market segment, expressed through Google's product and service category taxonomy. It answers "what categories does this domain compete in", "what is this keyword about", "what are the highest-volume searches in this market", and "give me every keyword in this category". It is the demand-mapping layer beneath content strategy and total-addressable-market sizing. All endpoints are Live POST calls under `/v3/dataforseo_labs/google/{function}/live`, except the free `categories` metadata endpoint.

## What it covers
- `/v3/dataforseo_labs/google/categories_for_domain/live` - the categories a domain ranks for, with ranking distribution and estimated traffic per category.
- `/v3/dataforseo_labs/google/categories_for_keywords/live` - the categories associated with each of up to 1000 keywords.
- `/v3/dataforseo_labs/google/top_searches/live` - access to 7B+ keywords from the DataForSEO Keyword Database for a location/language, with Google Ads metrics and product categories.
- `/v3/dataforseo_labs/google/keywords_for_categories/live` - keywords relevant to specified categories, with volume, trends, CPC, and competition.
- `/v3/dataforseo_labs/google/domain_metrics_by_categories/live` - the change in a domain's category metrics between two dates (historical SERP ranking distribution and current ETV/counts).
- `/v3/dataforseo_labs/categories` (GET, free) - the complete Google-based category taxonomy.

## Key parameters / inputs
| field | notes |
|---|---|
| category_codes / categories | category ids from the categories reference; max 20 (keywords_for_categories), max 5 (domain_metrics_by_categories) |
| keywords | up to 1000 keywords (categories_for_keywords) |
| target | domain or subdomain (categories_for_domain), without https:// or www. |
| location_code / location_name, language_code / language_name | location and language identifiers |
| first_date / second_date | yyyy-mm-dd; minimum 2020-10-01 (domain_metrics_by_categories) |
| category_intersection | true = keywords in ALL categories, false = ANY; default true |
| include_clickstream_data | doubles cost; default false |
| filters / order_by / limit / offset_token | max 8 filters, max 3 sort rules, limit up to 1000 |

## Response / what you get back
Category results carry `categories` (arrays of integer category ids) and the `metrics.<type>.*` block where `<type>` is `organic`, `paid`, `featured_snippet`, or `local_pack`, including `metrics.organic.count` and `metrics.organic.etv`. Keyword-bearing endpoints (top_searches, keywords_for_categories) add `keyword`, `keyword_info.search_volume`, `keyword_info.competition`, and `keyword_info.cpc`. Standard envelope fields `total_count`, `items_count`, `location_code`, and `language_code` accompany every result. The `categories` reference returns `category_code`, `category_name`, and `category_code_parent` for a roughly 3000-node hierarchy.

## Cost & method notes
- All analysis endpoints are Live; per-request billing. The cost log shows `categories_for_domain` at $0.02 per request; the `categories` reference endpoint is free.
- `include_clickstream_data: true` doubles the request cost where supported.
- Pre-indexed Labs data is cheaper than live [[cap-keywords-data-api]] or [[cap-serp-api]] calls; see [[dec-labs-vs-live-apis]].

## When to use / how it fits
Use this family to size a niche before committing to content. It feeds [[play-content-strategy-brief]] (market sizing + keyword pool) and complements [[cap-labs-keyword-research]] (term-level expansion) and [[cap-labs-competitor-research]] (who already owns the category). Route jobs through [[dec-which-api-for-which-job]]. The underlying taxonomy mirrors the categories used in [[cap-content-analysis-api]].

## Gotchas / limits
- The category taxonomy is Google product/service categories only; there is no Amazon, Google Play, or App Store category set here.
- `domain_metrics_by_categories` dates must be on or after 2020-10-01 and not in the future; it caps at 5 category codes.
- 2000 API calls/min, max 30 simultaneous requests; data updates weekly and is pre-indexed, so treat category traffic as estimates.
- `offset` is valid only under 10000 results; use `offset_token` beyond that.
- The `categories` reference is also published as a downloadable CSV with `category_code`, `category_name`, and `category_code_parent` columns, so you can resolve the parent-child hierarchy offline before issuing calls.
- `keywords_for_categories` uses `category_intersection` to switch between AND (keywords in every listed category) and OR (any listed category) matching; the default is AND, which can return far fewer keywords than expected.

## Related
- [[cap-labs-keyword-research]]
- [[cap-labs-competitor-research]]
- [[cap-keywords-data-api]]
- [[cap-content-analysis-api]]
- [[cap-databases]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[plat-google-search]]
- [[play-content-strategy-brief]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/dataforseo_labs/google/top_searches/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/categories_for_domain/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/keywords_for_categories/live/ (retrieved 2026-06-26)
