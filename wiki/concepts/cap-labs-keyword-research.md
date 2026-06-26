---
type: concept
title: "Labs Keyword Research (Capability)"
domain: dataforseo
subdomain: labs
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, labs, keyword-research]
related:
  - "[[cap-labs-competitor-research]]"
  - "[[cap-labs-market-analysis]]"
  - "[[cap-keywords-data-api]]"
  - "[[dec-labs-vs-live-apis]]"
---

# Labs Keyword Research (Capability)

> The DataForSEO Labs keyword-research endpoints turn one seed keyword or domain into thousands of scored keyword ideas from a pre-indexed in-house database, across Google, Amazon, Google Play, and the App Store. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
Labs is DataForSEO's analytical layer that queries a pre-indexed database rather than live-scraping a SERP. The keyword-research family expands a seed into ideas, suggestions, and related terms, then enriches each with search volume, CPC, competition, keyword difficulty, and search intent. Because the data is pre-computed, these endpoints are cheaper and faster than live SERP or Keywords Data calls, at the cost of slight staleness (the database updates periodically). All endpoints are Live/synchronous POST calls under `/v3/dataforseo_labs/{engine}/{function}/live`.

## What it covers
- `/v3/dataforseo_labs/google/keyword_ideas/live` - search terms relevant to the product/service categories of up to 200 seed keywords.
- `/v3/dataforseo_labs/google/keyword_suggestions/live` - full-text long-tail queries that contain a single seed keyword.
- `/v3/dataforseo_labs/google/related_keywords/live` - keywords from the "searches related to" SERP block via depth-first search (`depth` 0-4 yields roughly 1, 8, 72, 584, 4680 keywords).
- `/v3/dataforseo_labs/google/keyword_overview/live` - consolidated metrics (CPC, competition, volume, intent, SERP, backlinks) for up to 700 keywords.
- `/v3/dataforseo_labs/google/bulk_keyword_difficulty/live` - keyword difficulty (0-100 logarithmic) for up to 1000 keywords per call.
- `/v3/dataforseo_labs/google/search_intent/live` - informational/navigational/commercial/transactional classification with probability for up to 1000 keywords.
- `/v3/dataforseo_labs/google/historical_keyword_data/live` - month-by-month volume/CPC/competition history.
- `/v3/dataforseo_labs/google/keywords_for_site/live` - keywords a target domain ranks for, with volume and 12-month trend.
- `/v3/dataforseo_labs/amazon/related_keywords/live` and `/v3/dataforseo_labs/amazon/bulk_search_volume/live` - Amazon "Related Searches" expansion and bulk Amazon volume (up to 1000 keywords).
- `/v3/dataforseo_labs/apple/keywords_for_app/live` and `/v3/dataforseo_labs/google/keywords_for_app/live` - keywords an App Store or Google Play app ranks for (ASO).

## Key parameters / inputs
| field | notes |
|---|---|
| keywords / keyword | seed input; UTF-8, lowercased; max 200 (ideas), 700 (overview/historical), 1000 (bulk difficulty, search intent) |
| target / app_id | domain (keywords_for_site) or numeric/package app id (keywords_for_app) |
| location_code / location_name | one location identifier required |
| language_code / language_name | one language identifier required |
| include_clickstream_data | adds clickstream metrics; doubles the cost; default false |
| include_serp_info | returns SERP data per keyword; default false |
| depth | related_keywords search depth 0-4 |
| filters / order_by / limit / offset / offset_token | max 8 filters, max 3 sort rules, limit up to 1000, offset_token for >10000 results |

## Response / what you get back
Each item carries `keyword_info.search_volume`, `keyword_info.competition`, `keyword_info.competition_level` (LOW/MEDIUM/HIGH), and `keyword_info.cpc`. Difficulty arrives as `keyword_properties.keyword_difficulty` and grouping as `keyword_properties.core_keyword`. Intent is `search_intent_info.main_intent`. Link context comes via `avg_backlinks_info.backlinks` and `avg_backlinks_info.referring_domains`, and SERP weight via `serp_info.se_results_count`. Clickstream and Bing-normalized variants appear as `keyword_info_normalized_with_clickstream.search_volume` and `keyword_info_normalized_with_bing.search_volume`. App endpoints add `items[].ranked_serp_element.serp_item.rank_absolute`.

## Cost & method notes
- All endpoints are Live/synchronous; billing is per request. The live cost log shows keyword_ideas, keyword_suggestions, related_keywords, keywords_for_site, and amazon related_keywords at $0.0105; keyword_overview, bulk_keyword_difficulty, amazon bulk_search_volume, and historical_keyword_data at $0.0101; and search_intent at $0.0011.
- `include_clickstream_data: true` doubles the cost where supported. Bulk difficulty and search intent have no clickstream option.
- Labs is cheaper than live [[cap-keywords-data-api]] volume calls (which cost $0.075 per request in the same log) but the figures derive from a pre-indexed database. See [[dec-labs-vs-live-apis]].

## When to use / how it fits
This is the engine of [[play-keyword-research-workflow]] (seed -> ideas/related -> difficulty/intent -> prioritize) and feeds [[play-content-strategy-brief]] and [[play-ecommerce-product-research]]. For job-to-endpoint routing use [[dec-which-api-for-which-job]]. Google Ads metrics here trace back to [[ent-google-ads-keyword-planner]], and clickstream-normalized volumes to [[ent-clickstream-data]].

## Gotchas / limits
- 2000 API calls/min, max 30 simultaneous requests across Labs.
- App keyword endpoints support US location and English language only; app ids are numeric for the App Store and package-name format for Google Play.
- Amazon related_keywords covers US, Egypt, Saudi Arabia, and UAE; amazon bulk_search_volume covers a broader set of 16 marketplaces (US, UK, CA, AU, DE, FR, IT, ES, NL, AT, IN, MX, SG, EG, SA, UAE).
- `offset` is not recommended past 10000 results; switch to `offset_token`.
- Data is pre-indexed, so it can lag live SERPs; weigh against [[cap-serp-api]] when freshness matters.

## Related
- [[cap-labs-competitor-research]]
- [[cap-labs-market-analysis]]
- [[cap-keywords-data-api]]
- [[cap-trends-and-clickstream]]
- [[cap-databases]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[plat-google-search]]
- [[play-keyword-research-workflow]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/search_intent/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/amazon/bulk_search_volume/live/ (retrieved 2026-06-26)
