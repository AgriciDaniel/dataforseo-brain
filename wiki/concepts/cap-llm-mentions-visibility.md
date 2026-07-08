---
type: concept
title: "LLM Mentions and Visibility"
domain: dataforseo
subdomain: ai-optimization
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, ai-optimization, geo]
related:
  - "[[cap-ai-optimization-api]]"
  - "[[cap-geo-ai-search-optimization]]"
  - "[[plat-ai-assistants]]"
---

# LLM Mentions and Visibility

> Structured data on where brands, domains, and keywords are mentioned and cited inside AI answers. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
The LLM Mentions API (launched 2025-11-11) is DataForSEO's flagship AI-visibility tracker. It answers the question traditional SEO tools cannot: is my brand named, and is my site cited, inside generative AI answers. It maintains a mentions database collected from Google AI Overview and ChatGPT, each mention being a question-answer pair plus the sources the model cited. It is the measurement half of GEO, paired with the live-querying endpoints in [[cap-ai-optimization-api]]. All five endpoints are Live-only under `/v3/ai_optimization/llm_mentions/`.

## What it covers
- **Search** (`/llm_mentions/search/live`): raw mention records for target keywords/domains, returning `question`, `answer` (markdown), `sources[]`, `search_results[]`, `ai_search_volume`, `monthly_searches[]`, `brand_entities[]`, and `fan_out_queries[]`.
- **Top Pages** (`/llm_mentions/top_pages/live`): mentions metrics grouped by the most-cited pages for a target.
- **Top Domains** (`/llm_mentions/top_domains/live`): mentions metrics grouped by the most-cited domains.
- **Aggregated Metrics** (`/llm_mentions/aggregated_metrics/live`): consolidated metrics for one target across location, language, platform, and source domain.
- **Cross Aggregated Metrics** (`/llm_mentions/cross_aggregated_metrics/live`): the same metrics for 2-10 targets at once, labelled by `aggregation_key`, for side-by-side brand or keyword comparison. Note the task spec slug `cross_model_comparison` maps to this real path.
- Aggregation endpoints accept `initial_dataset_filters` with operators `=`, `<>`, `in`, `not_in`, `like`, `not_like`, `ilike`, `not_ilike`, `match`, `not_match`, applied before grouping.
- `links_scope` (sources or search_results) on Top Pages and Top Domains controls whether grouping uses cited sources or retrieved search results.

## Key parameters / inputs
| field | notes |
|---|---|
| target | array of up to 10 entities, each a domain or a keyword |
| domain | entity; <= 63 chars; no https:// or www; `include_subdomains` optional |
| keyword | entity; <= 250 chars; `match_type` word_match or partial_match |
| search_filter | include or exclude (default include) |
| search_scope | domain: any/sources/search_results; keyword: any/question/answer/brand_entities/fan_out_queries |
| platform | chat_gpt or google (default google; model then always google_ai_overview) |
| location_* / language_* | default 2840 (US) / en; ChatGPT is US/English only |
| initial_dataset_filters | up to 8 filter expressions applied before aggregation |
| targets / aggregation_key | Cross Aggregated only; 2-10 targets, key labels each group |

## Response / what you get back
Search returns `total_count`, `current_offset`, `search_after_token`, and `items[]`. Each item carries `platform`, `model_name`, `question`, `answer`, `sources[]` (source_name, snippet, title, domain, url, position, publication_date), `search_results[]`, `ai_search_volume`, `first_response_at`, `last_response_at`, and `brand_entities[]`. The aggregation endpoints return a `total` object plus grouped arrays: `location[]`, `language[]`, `platform[]`, `sources_domain[]`, `search_results_domain[]`, `brand_entities_title[]`, `brand_entities_category[]`. Group elements carry `key`, `mentions`, and `ai_search_volume` (note `impressions` is deprecated and returns null).

## Cost & method notes
- Per the AI Optimization page, LLM Mentions is pay-as-you-go: roughly $0.10 per request plus $0.001 per row, about $1.10 per 1,000 rows, with no monthly minimum since DataForSEO's 2026-07-01 pricing update.
- All endpoints are Live-only with one task per call. See [[cap-queue-priority-cost-model]] and [[cap-task-vs-live-execution]].

## When to use / how it fits
LLM Mentions is the data engine of [[play-ai-visibility-tracking]] and the GEO loop in [[cap-geo-ai-search-optimization]]. Use Search for evidence (the actual question and answer), Top Domains/Pages to see who AI cites in your category, and Cross Aggregated Metrics to compute Share of Voice across competitors. Practitioner research notes that about 85% of brand mentions come from third-party pages, so the off-domain `sources_domain[]` view matters as much as your own. The answer surfaces are profiled in [[plat-ai-assistants]] and the models in [[ent-llm-model-providers]].

## Gotchas / limits
- Access is now plain pay-as-you-go, with no subscription or activation step. It returned `40204` through 2026-06-26; that gate was removed 2026-07-01 when DataForSEO moved all APIs to pay-as-you-go. A live re-probe on 2026-07-08 returned `20000 Ok` with real data for `/v3/ai_optimization/llm_mentions/search/live`; fixture: `.raw/sources/dataforseo-research/ai-optimization/fixtures/llm-mentions-search.json`. See [[cap-status-error-codes]].
- ChatGPT coverage uses model GPT-5 and covers United States (location_code 2840) and English only; Google AI Overview (`model_name` always `google_ai_overview`) supports multiple locations and languages and is the broad-coverage platform. The launch announcement notes initial coverage is narrower than the marketing list.
- Execution up to 120 seconds; 2000 calls/min; one task per call; `offset` max 9,000 (use `search_after_token` beyond 20,000 results).
- Citation churn is high (industry studies report 40-60% of cited sources change month to month), so trends matter more than any single snapshot. See [[cap-data-collection-methodology]].
- For the `google` platform the `model_name` is always `google_ai_overview`; there is no per-Gemini-version selection here, unlike LLM Responses.
- `impressions` is deprecated and returns null across all aggregation endpoints, so do not build metrics on it.

## Related
- [[cap-ai-optimization-api]]
- [[cap-geo-ai-search-optimization]]
- [[plat-ai-assistants]]
- [[ent-llm-model-providers]]
- [[play-ai-visibility-tracking]]
- [[cap-data-collection-methodology]]
- [[cap-queue-priority-cost-model]]
- [[cap-status-error-codes]]
- [[cap-platform-architecture]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/search/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/top_domains/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/cross_aggregated_metrics/live/ (retrieved 2026-06-26)
- https://dataforseo.com/update/pricing-update-in-dataforseo-apis (published 2026-07-01, retrieved 2026-07-08)
- https://dataforseo.com/pricing/ai-optimization/llm-mentions (retrieved 2026-07-08)
- https://dataforseo.com/help-center/llm-mentions-api-subscription-explained (retrieved 2026-07-08; pricing fields retained, subscription text superseded by the 2026-07-01 update)
- `.raw/sources/dataforseo-research/ai-optimization/fixtures/llm-mentions-search.json` (captured 2026-07-08; `20000 Ok`)
- https://dataforseo.com/update/introducing-llm-mentions-api (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization-llm_mentions-overview/ (retrieved 2026-06-26)
