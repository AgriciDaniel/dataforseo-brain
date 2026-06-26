---
type: flow
title: "Play: Content Strategy Brief"
domain: dataforseo
subdomain: content-analysis
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, serp, labs, content-analysis]
related:
  - "[[cap-serp-api]]"
  - "[[cap-content-analysis-api]]"
  - "[[cap-labs-market-analysis]]"
---

# Play: Content Strategy Brief

> Turn a topic into a writer-ready brief: scrape the live SERP, map demand and intent with Labs, and read citation sentiment with Content Analysis. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
This flow produces a data-backed content brief. It reads the actual SERP a piece must compete in (SERP API), sizes and shapes demand around the topic (Labs keyword and market analysis), and gauges how the topic is discussed across the web (Content Analysis sentiment and trends). The result is a brief that tells a writer what to cover, at what depth, and with what angle.

## Trigger
A content topic is selected and needs a brief: a new article in a cluster, a refresh of an underperforming page, or a pillar build. Inputs are the target keyword/topic plus `location_code` and `language_code`.

## Endpoints used (in order)
- `POST /v3/serp/google/organic/live/advanced` (the live competitive SERP).
- `POST /v3/dataforseo_labs/google/keyword_ideas/live` and `/related_keywords/live` (subtopics).
- `POST /v3/dataforseo_labs/google/search_intent/live` (intent of the topic + subtopics).
- `POST /v3/dataforseo_labs/google/top_searches/live` (demand/trend context).
- `POST /v3/content_analysis/search/live` and `/summary/live` (citation corpus).
- `POST /v3/content_analysis/sentiment_analysis/live` (sentiment + connotations).

## Pipeline
1. Scrape the SERP: call `serp/google/organic/live/advanced` for the target keyword. Read `result.items[]` to capture the ranking organic URLs (titles, descriptions, `is_featured_snippet`), the `item_types` present (people_also_ask, featured_snippet, ai_overview, video, etc.), and the `people_also_ask`/`related_searches` elements for questions to answer.
2. Map subtopics: run Labs `keyword_ideas` and `related_keywords` to build the semantic field around the topic, with `search_volume` and inline `keyword_difficulty` to weight coverage.
3. Tag intent: pass the topic plus key subtopics through `search_intent` to confirm whether the brief should be informational, commercial, etc., and shape the format accordingly.
4. Add demand context: use Labs `top_searches` (and optionally Keywords Data trends) to see rising vs declining interest and seasonal timing.
5. Read the discourse: run Content Analysis `search` for the topic to pull the citation corpus (titles, snippets, `page_category`, `domain_rank`, and `content_info.sentiment_connotations`), then `summary` for the aggregate view.
6. Gauge sentiment: run `sentiment_analysis` for `connotation_types` (positive/negative/neutral) and `sentiment_connotations` (anger, happiness, love, sadness, fun) plus `top_domains` and `text_categories` to pick an angle and tone.
7. Assemble the brief: target keyword + subtopics to cover, the questions (PAA) to answer, SERP features to win, recommended depth/format from competitor analysis, intent, and a tone/angle informed by sentiment.

## Cost & cadence
- SERP `live/advanced` bills $0.002/request (cost-log). Run a few queries per topic (main keyword + a couple of variants).
- Labs ideation bills about $0.0105/request; `top_searches` $0.0105; `search_intent` about $0.0011 (cost-log).
- Content Analysis is Live-only and pricier per call: the cost-log shows `search` at $0.02015 and `summary` at $0.02003; budget accordingly and cache results.
- Cadence: per content brief (on demand). Refresh the SERP scrape near publish time since live SERPs move.

## Output
A writer-ready content brief: target keyword and weighted subtopics, the questions to answer, SERP features to target, competitor depth/format benchmark, intent classification, and a sentiment-informed angle. Feeds the editorial pipeline and complements [[play-keyword-research-workflow]].

## Pitfalls / limits
- Use Live SERP here (not Labs) because the brief must reflect the current competitive page set; Live results are not stored, so capture them when received.
- Keyword special operators in the SERP query trigger a 5x charge; keep the topic query clean.
- Content Analysis is the costliest step per call; scope it with `page_type`, `filters` (max 8), and `limit` instead of pulling the full corpus.
- Labs intent is Google-specific and language-only; do not pass a location to it.
- Content Analysis runs over a citation database, not a live crawl, so very fresh content may be under-represented.

## Decisions in play
- [[dec-labs-vs-live-apis]]: use Live SERP for the competitive page set (must be current) but Labs for the cheaper subtopic/demand expansion.
- [[dec-which-api-for-which-job]]: SERP for the competitive surface, Labs for demand/intent, Content Analysis for discourse sentiment.
- [[dec-cost-control-strategy]]: Content Analysis is the costliest step per call, so scope it with `page_type`, `filters`, and `limit` rather than pulling the full corpus.

## Related
- [[cap-serp-api]]
- [[cap-serp-google-verticals]]
- [[cap-labs-keyword-research]]
- [[cap-labs-market-analysis]]
- [[cap-content-analysis-api]]
- [[plat-google-search]]
- [[plat-review-platforms]]
- [[dec-which-api-for-which-job]]
- [[dec-labs-vs-live-apis]]
- [[play-keyword-research-workflow]]
- [[play-ai-visibility-tracking]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/content_analysis/search/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/content_analysis/sentiment_analysis/live/ (retrieved 2026-06-26)
