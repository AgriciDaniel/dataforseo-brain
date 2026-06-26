---
type: concept
title: "Content Analysis API (Capability)"
domain: dataforseo
subdomain: content-analysis
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, content-analysis, sentiment]
related:
  - "[[cap-labs-market-analysis]]"
  - "[[plat-review-platforms]]"
  - "[[play-content-strategy-brief]]"
  - "[[cap-platform-architecture]]"
---

# Content Analysis API (Capability)

> The Content Analysis API searches a global citation database of web mentions for a keyword or category, then returns the citations, their sentiment and rating distributions, and how mention volume and phrasing trend over time. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
This module is brand-mention and sentiment intelligence over a pre-built citation corpus, aggregating content from news sites, ecommerce, blogs, forums, and organization pages. You query it like a search engine for mentions: give it a keyword (or a category code) and it returns every place that term is cited, each scored for sentiment and connotation, plus aggregate summaries, rating distributions, and time-series trends. All endpoints are Live/synchronous POST calls under `/v3/content_analysis/{function}/live`; there is no task queue. It is the listening layer for reputation tracking and content-gap research.

## What it covers
- `/v3/content_analysis/search/live` - detailed citation data for a keyword: snippet, sentiment, domain metrics, page categorization.
- `/v3/content_analysis/summary/live` - an aggregate overview (sentiment, top domains, categorical breakdowns) of the citation set.
- `/v3/content_analysis/sentiment_analysis/live` - emotional-reaction and polarity distribution for a keyword.
- `/v3/content_analysis/rating_distribution/live` - rating-distribution metrics across domains, categories, and regions.
- `/v3/content_analysis/phrase_trends/live` and `/v3/content_analysis/category_trends/live` - citation statistics over time for a keyword or category (history from 2022-10-31).
- Free helpers: `/v3/content_analysis/categories/`, `GET /v3/content_analysis/available_filters` (the filterable-fields reference; the `/filters/` form 404s for this module), and `/v3/content_analysis/id_list/`.

## Key parameters / inputs
| field | applies to | notes |
|---|---|---|
| keyword | search, summary, sentiment_analysis, rating_distribution, phrase_trends | target term, UTF-8, lowercased; quotes for exact phrase |
| category_code | category_trends (ids come from the categories helper) | target category id |
| keyword_fields | search, summary | restrict to title / main_title / previous_title / snippet |
| page_type | search, summary | ecommerce / news / blogs / message-boards / organization |
| search_mode | search, summary | as_is (all citations) or one_per_domain |
| positive_connotation_threshold / sentiments_connotation_threshold | summary, sentiment_analysis (NOT search) | sentiment thresholds 0-1; default 0.4 |
| date_from / date_to / date_group | phrase_trends, category_trends only | trends window (min 2022-10-31), grouped by day/week/month |
| filters / internal_list_limit / limit / offset_token | search and other list-returning endpoints | max 8 filters, nested-array cap, limit up to 1000, token pagination beyond 10000 |

## Response / what you get back
Search returns `total_count`, `items_count`, `offset_token`, and per-citation `type`, `url`, `domain`, `main_domain`, `url_rank`, `domain_rank`, `content_info.title`, `content_info.snippet`, `content_info.sentiment_connotations`, `content_info.connotation_types`, `content_info.rating`, `page_category`, and `fetch_time`. The sentiment object holds `anger`, `happiness`, `love`, `sadness`, `share`, and `fun`; the connotation object holds `positive`, `negative`, and `neutral`. Aggregate endpoints add `top_domains`, `text_categories`, `page_categories`, `page_types`, `countries`, and `languages`; rating distribution adds bucketed `rating_distribution`; trends add a `date` series.

## Cost & method notes
- All analysis endpoints are Live; per-request billing. The cost log shows `/v3/content_analysis/search/live` at $0.02015 and `/v3/content_analysis/summary/live` at $0.02003.
- The `categories`, `filters`, and `id_list` helpers are free.
- Because the corpus is pre-indexed, costs are flat per request rather than per result; see [[cap-queue-priority-cost-model]].

## When to use / how it fits
Use Content Analysis to gauge how a brand, product, or topic is talked about and where the content gaps are. It feeds the sentiment step of [[play-content-strategy-brief]] and complements review intelligence in [[cap-business-data-api]] and [[plat-review-platforms]]. Its category taxonomy mirrors [[cap-labs-market-analysis]], so the two pair well for demand-plus-sentiment mapping. Route jobs via [[dec-which-api-for-which-job]].

## Gotchas / limits
- Trend history starts 2022-10-31; there is nothing earlier.
- All endpoints are synchronous only, with no POST-then-GET queue; `id_list` is rate-limited to 10 calls/min and returns task IDs up to 6 months back, but metadata is only available for tasks from the past month, and `include_metadata: true` caps the lookback to 1 month.
- 2000 API calls/min, max 8 filters, max 3 sort rules; use `offset_token` past 10000 results.
- Sentiment is model-derived from text, not verified human labels; treat thresholds as tunable heuristics.
- `search_mode: one_per_domain` collapses many citations from the same site into a single row, which changes both `total_count` and the apparent sentiment mix versus `as_is`.
- The `keyword_fields` and `page_type` filters scope where the term is matched (title vs snippet, news vs ecommerce vs forum), so the same keyword can yield very different citation sets depending on how you constrain it.

## Related
- [[cap-labs-market-analysis]]
- [[cap-business-data-api]]
- [[cap-ai-optimization-api]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[plat-review-platforms]]
- [[plat-ai-assistants]]
- [[play-content-strategy-brief]]
- [[dec-which-api-for-which-job]]
- [[dec-labs-vs-live-apis]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/content_analysis/search/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/content_analysis/summary/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/content_analysis/sentiment_analysis/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/content_analysis/available_filters/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/content_analysis/id_list/ (retrieved 2026-06-26)
