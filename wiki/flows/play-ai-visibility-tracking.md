---
type: flow
title: "Play: AI Visibility Tracking"
domain: dataforseo
subdomain: ai-optimization
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, ai-optimization, geo]
related:
  - "[[cap-llm-mentions-visibility]]"
  - "[[cap-ai-optimization-api]]"
  - "[[cap-geo-ai-search-optimization]]"
---

# Play: AI Visibility Tracking

> The GEO loop: measure brand mentions/citations inside AI answers with LLM Mentions, sample fresh model answers with LLM Responses, and roll it into a share-of-voice dashboard. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
Generative Engine Optimization (GEO) tracks whether a brand is named, cited, or recommended inside AI answers rather than ranked in blue links. This flow has two engines: the LLM Mentions API (a pre-indexed mentions/citations database with its own AI search-volume index) for aggregated visibility, and LLM Responses (live model querying across ChatGPT, Claude, Gemini, Perplexity) for fresh prompt sampling. Together they give a repeatable AI-era rank tracker.

## Trigger
A brand wants to know how it shows up in AI answers: a GEO program launch, a competitive share-of-voice study, or monitoring after a content push. Inputs are target entities (brand domain and/or keywords) and a prompt set of real buyer questions.

## Endpoints used (in order)
- `POST /v3/ai_optimization/llm_mentions/search/live` (raw mention records).
- `POST /v3/ai_optimization/llm_mentions/aggregated_metrics/live` (consolidated metrics).
- `POST /v3/ai_optimization/llm_mentions/cross_aggregated_metrics/live` (multi-brand comparison).
- `POST /v3/ai_optimization/llm_mentions/top_domains/live` and `/top_pages/live` (most-cited sources).
- `POST /v3/ai_optimization/{chat_gpt|claude|gemini|perplexity}/llm_responses/live` (live answer sampling).
- `POST /v3/ai_optimization/ai_keyword_data/keywords_search_volume/live` (AI search volume).

## Pipeline
1. Define targets: build the `target` array (up to 10 entities) of domains (`domain`, `search_filter`, `search_scope` sources/search_results) and keywords (`keyword`, `match_type`, `search_scope` question/answer/brand_entities). Set `platform` (`google` for AI Overview, `chat_gpt`) plus `location_code`/`language_code`.
2. Pull mentions with `llm_mentions/search`: each item returns the `question`, the `answer` (markdown), cited `sources[]` (title, url, domain, position), `search_results[]`, `brand_entities[]`, `fan_out_queries[]`, and `ai_search_volume` with `monthly_searches[]`.
3. Aggregate visibility with `aggregated_metrics` (mentions + ai_search_volume grouped by location/language/platform/source domain) and compute share of voice = your mentions / total tracked-brand mentions.
4. Benchmark competitors with `cross_aggregated_metrics`: supply 2-10 `targets` each with an `aggregation_key` label to get side-by-side group totals in one call.
5. Find citation surfaces with `top_domains`/`top_pages` to see which domains and pages the models cite for your topic (often third-party/UGC, not your own site).
6. Sample fresh answers with `llm_responses`: send the same prompt set across ChatGPT, Claude, Gemini, and Perplexity (`user_prompt` <=500 chars, choose `model_name`, set `web_search: true` to force current citations) and parse `items[]` message `sections[]` and `annotations[]` for mention presence and sentiment.
7. Score and chart: per engine, record mention rate, citation rate, share of voice, position, and sentiment over time; alert on drops.

## Cost & cadence
- LLM Mentions is Live-only and pay-as-you-go, priced about $0.10/request + $0.001/row, roughly $1.10 per 1,000 rows; turnaround about 2 seconds. It returned `40204` through 2026-06-26, then the subscription and activation step were removed on 2026-07-01. A 2026-07-08 re-probe of `/v3/ai_optimization/llm_mentions/search/live` returned `20000 Ok` with real data; fixture: `.raw/sources/dataforseo-research/ai-optimization/fixtures/llm-mentions-search.json`.
- LLM Responses bills DataForSEO's per-task cost (about $0.0006/task) plus a pass-through `money_spent` for the underlying model tokens. AI Keyword Data bills about $0.0101/task (cost-log: $0.0101).
- Cadence: mentions/aggregates weekly or monthly (the data has churn but stable patterns); live prompt sampling weekly across the model set.

## Output
An AI visibility dashboard per engine: mention rate, citation rate, AI share of voice, sentiment, the most-cited source domains/pages, and the fan-out queries driving answers. Pairs with [[play-content-strategy-brief]] to act on citation gaps.

## Pitfalls / limits
- Coverage is narrower than the headline: ChatGPT mentions data is US (`location_code 2840`) and English only; Google AI Overview supports multiple locations/languages.
- `impressions` is deprecated and returns null; do not build on it.
- LLM Responses `annotations[]` can be empty even when `web_search: true`, and `web_search` is unsupported on some reasoning models (o1, o3-mini); validate per model.
- Most brand validation is off-domain (third-party pages), so track earned/UGC sources, not just your own site.
- Track each engine separately; cross-engine citation overlap is low, so a single blended number hides the real picture.

## Decisions in play
- [[dec-which-api-for-which-job]]: LLM Mentions for aggregated brand/citation visibility; LLM Responses for fresh, controllable prompt sampling across models.
- [[dec-cost-control-strategy]]: LLM Mentions bills per request and per row, so design a fixed prompt/target set and cache; LLM Responses adds a pass-through `money_spent` token charge per model.
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]: DataForSEO is raw GEO infrastructure, not a finished SOV dashboard; you build the scoring and charts.

## Related
- [[cap-ai-optimization-api]]
- [[cap-llm-mentions-visibility]]
- [[cap-geo-ai-search-optimization]]
- [[cap-serp-google-verticals]]
- [[cap-account-usage-userdata]]
- [[plat-ai-assistants]]
- [[ent-llm-model-providers]]
- [[dec-which-api-for-which-job]]
- [[dec-cost-control-strategy]]
- [[play-content-strategy-brief]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/search/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/aggregated_metrics/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization/chat_gpt/llm_responses/live/ (retrieved 2026-06-26)
- https://dataforseo.com/update/introducing-llm-mentions-api (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/ai_optimization-overview/ (retrieved 2026-06-26)
- https://dataforseo.com/update/pricing-update-in-dataforseo-apis (published 2026-07-01, retrieved 2026-07-08)
- https://dataforseo.com/pricing/ai-optimization/llm-mentions (retrieved 2026-07-08)
- `.raw/sources/dataforseo-research/ai-optimization/fixtures/llm-mentions-search.json` (captured 2026-07-08; `20000 Ok`)
