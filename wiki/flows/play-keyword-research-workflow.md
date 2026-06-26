---
type: flow
title: "Play: Keyword Research Workflow"
domain: dataforseo
subdomain: keywords
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, keywords, labs]
related:
  - "[[cap-keywords-data-api]]"
  - "[[cap-labs-keyword-research]]"
  - "[[dec-labs-vs-live-apis]]"
---

# Play: Keyword Research Workflow

> Seed terms to a prioritized keyword list: Keywords Data for ground-truth volume, then DataForSEO Labs for expansion, difficulty, and intent. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
This workflow expands a handful of seed keywords into a scored, intent-tagged target list. It blends two data lineages: the Keywords Data API (Google Ads-sourced volume/CPC/competition) for accuracy on a small set, and DataForSEO Labs (a pre-indexed in-house database of 8B+ keywords) for cheap, large-scale ideation, difficulty, and intent. Labs is the workhorse because it is far cheaper per query than live SERP.

## Trigger
A topic, product, or page needs a keyword universe: a new content cluster, a PPC build, or a site launch. Inputs are 1-200 seed keywords plus a `location_code` and `language_code`.

## Endpoints used (in order)
- `POST /v3/keywords_data/google_ads/search_volume/live` (ground-truth volume/CPC for the seeds).
- `POST /v3/dataforseo_labs/google/keyword_ideas/live` (category-relevant expansion).
- `POST /v3/dataforseo_labs/google/keyword_suggestions/live` and `/related_keywords/live` (phrase and "searches related" expansion).
- `POST /v3/dataforseo_labs/google/bulk_keyword_difficulty/live` (KD for up to 1,000 keywords/request).
- `POST /v3/dataforseo_labs/google/search_intent/live` (intent for up to 1,000 keywords/request).
- `POST /v3/dataforseo_labs/google/keyword_overview/live` (consolidated metrics for a final shortlist).

## Pipeline
1. Validate the seeds (UTF-8, lowercase) and resolve `location_code` + `language_code`.
2. Pull anchor volume: send up to 1,000 seeds to Keywords Data `search_volume` (Google Ads lineage). Read `search_volume`, `competition`/`competition_index` (0-100), `cpc`, and `monthly_searches[]` for seasonality. One request covers 1 or 1,000 keywords at the same price.
3. Expand with Labs `keyword_ideas` (up to 200 seeds, returns category-relevant terms with `keyword_info` volume/CPC/competition, `keyword_properties.keyword_difficulty`, and inline `search_intent_info`). Use `closely_variants`, `ignore_synonyms`, and `filters` to shape the set; page with `offset_token` beyond 10,000 results.
4. Deepen with `keyword_suggestions` (long-tail phrase-match around a seed) and `related_keywords` (the "searches related to" graph) to capture demand the ideas endpoint misses.
5. Score difficulty in bulk: batch up to 1,000 candidates into `bulk_keyword_difficulty` to get the 0-100 logarithmic KD per term in one billed task.
6. Tag intent: send up to 1,000 keywords to `search_intent` (language-only) for `keyword_intent.label` (informational/navigational/commercial/transactional) plus `probability` and `secondary_keyword_intents[]`.
7. Prioritize: combine volume x intent x KD x CPC into a score, drop irrelevant or out-of-language terms (`keyword_properties.is_another_language`), and run `keyword_overview` on the shortlist for a clean consolidated record per keyword.
8. Hand the scored list to [[play-content-strategy-brief]] or a PPC build.

## Cost & cadence
- Labs ideation/expansion endpoints bill about $0.0105 per request (cost-log: keyword_ideas, keyword_suggestions, related_keywords, ranked_keywords all $0.0105).
- Labs analytical endpoints bill about $0.0101 (keyword_overview, bulk_keyword_difficulty); search_intent is cheapest at about $0.0011 (cost-log: $0.0011).
- Keywords Data Google Ads endpoints bill per request regardless of keyword count; the cost-log shows `search_volume` and `keywords_for_site` at $0.075 each.
- Cadence: run on demand per topic. Volume/difficulty/intent change slowly, so a monthly refresh is plenty; Labs is Live-only so results return in roughly 1 second.

## Output
A prioritized keyword table: keyword, search_volume, monthly trend, competition/CPC, keyword_difficulty, main_intent, and a composite priority score, ready for clustering, briefs, or campaign builds.

## Pitfalls / limits
- Keywords Data Google Ads is capped at 12 requests/min/account and returns combined volume for groups of similar keywords; certain emojis/UTF symbols are rejected.
- Labs `include_clickstream_data: true` doubles the request cost; only enable when you need demographic/clickstream volume.
- `keyword_ideas` takes max 200 seeds; `keyword_suggestions`/`related_keywords` take a single seed; do not over-batch.
- Labs volume is a pre-computed estimate, not live Google Ads data; for ad-bidding accuracy confirm the final set against Keywords Data `search_volume`.
- `search_intent` is language-only (no location) and Google-specific; there is no marketplace equivalent.

## Decisions in play
- [[dec-labs-vs-live-apis]]: route bulk expansion and difficulty/intent to pre-indexed Labs, reserve Keywords Data live volume for the anchor seeds and the final shortlist.
- [[dec-which-api-for-which-job]]: Keywords Data for Google Ads ground-truth volume; Labs for ideation, KD, and intent at scale.
- [[dec-cost-control-strategy]]: batch up to 1,000 keywords per Keywords Data request (flat price) and avoid `include_clickstream_data` unless demographics are needed.

## Related
- [[cap-keywords-data-api]]
- [[cap-labs-keyword-research]]
- [[cap-labs-market-analysis]]
- [[cap-trends-and-clickstream]]
- [[cap-queue-priority-cost-model]]
- [[ent-google-ads-keyword-planner]]
- [[ent-clickstream-data]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[dec-cost-control-strategy]]
- [[play-content-strategy-brief]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/search_intent/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/overview/ (retrieved 2026-06-26)
