---
type: decision
title: "Which API for which job (master router)"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, decision, routing, module-map]
related:
  - "[[cap-platform-architecture]]"
  - "[[dec-labs-vs-live-apis]]"
  - "[[dec-live-vs-standard-vs-priority]]"
---

# Which API for which job (master router)

> The job-to-be-done decision table: pick the DataForSEO module/endpoint for the task in front of you. Sits under [[index|DataForSEO Brain]] → [[decisions/_index|Decisions]].

## Overview
DataForSEO exposes 12 modules under one v3 envelope ([[cap-platform-architecture]]). The common failure mode is reaching for live SERP when a cheaper pre-indexed Labs query would do, or polling raw REST when a bulk endpoint exists. This page maps jobs to endpoints. Two cross-cutting choices ride on top of every row: pre-indexed vs live ([[dec-labs-vs-live-apis]]) and Live vs Standard vs Priority ([[dec-live-vs-standard-vs-priority]]).

## Decision table (job → module / endpoint)
| Job to be done | Module / endpoint | Why this one |
|---|---|---|
| Read a live ranking SERP for a keyword | SERP API `/v3/serp/google/organic/live/advanced` | Fresh, full structured parse; ~$0.002/live SERP ([[cap-serp-api]]) |
| Track AI Overview / AI Mode presence | SERP API `ai_overview` element + `/v3/serp/google/ai_mode` | Dedicated AI-search surfaces ([[cap-serp-google-verticals]]) |
| Get raw search volume / CPC | Keywords Data `/v3/keywords_data/google_ads/search_volume/live` | Google Ads lineage; ~$0.075/call ([[cap-keywords-data-api]]) |
| Find keyword ideas/suggestions/related | Labs `/v3/dataforseo_labs/google/keyword_ideas/live` (and suggestions, related) | Pre-indexed, ~$0.0105/call ([[cap-labs-keyword-research]]) |
| Score keyword difficulty in bulk | Labs `/v3/dataforseo_labs/google/bulk_keyword_difficulty/live` | Up to 1,000 keywords per billable task |
| Classify search intent | Labs `/v3/dataforseo_labs/google/search_intent/live` | Cheap (~$0.0011/call observed) intent labels |
| Find competitors / ranked keywords / gaps | Labs `serp_competitors`, `ranked_keywords`, `domain_intersection` | Pre-indexed competitor research ([[cap-labs-competitor-research]]) |
| Estimate domain traffic in bulk | Labs `/v3/dataforseo_labs/google/bulk_traffic_estimation/live` | Up to 1,000 domains per task |
| Audit a site's on-page health | OnPage API (crawl) + `/v3/on_page/instant_pages` | Crawler + per-URL instant checks ([[cap-onpage-api]]) |
| Analyze a backlink profile | Backlinks `/v3/backlinks/summary/live`, `referring_domains`, `anchors` | Own crawler index ([[cap-backlinks-api]]) |
| Bulk link/spam metrics for many targets | Backlinks `bulk_ranks`, `bulk_spam_score` (≤1000 targets) | One billable task, many results ([[cap-backlinks-bulk-metrics]]) |
| Detect a site's tech stack / Whois | Domain Analytics `technologies`, `whois/overview` | Stack + registration intel ([[cap-domain-analytics]]) |
| Product / price / review data | Merchant `/v3/merchant/google/products/live/advanced` (+ Amazon) | Shopping & Amazon ([[cap-merchant-api]]) |
| App store / ASO data | App Data API (Google Play + App Store) | Listings, reviews, ASO ([[cap-app-data-api]]) |
| Reviews / listings / GBP | Business Data `/v3/business_data/business_listings/search/live` | Reputation surfaces ([[cap-business-data-api]]) |
| Track brand mentions in AI answers | AI Optimization `llm_mentions`, `llm_responses` | Cross-model visibility ([[cap-llm-mentions-visibility]]) |
| Sentiment / citation analysis over a corpus | Content Analysis `search`, `summary` | Citation DB ([[cap-content-analysis-api]]) |
| Cheap historical/analytical lookups | DataForSEO Labs / Databases | Pre-indexed, no live crawl ([[cap-databases]]) |

## Decision rules
- If the query does NOT need the last 24-48h of fresh SERP data, serve it from Labs/Databases, not live SERP.
- If you can express the job as "N items in one call," prefer a bulk endpoint (≤1000 keywords/domains/targets) to cut billable tasks.
- For agent-native, conversational access to any of the above, route through [[cap-mcp-server-integration]] rather than hand-wiring REST - see [[dec-mcp-vs-raw-rest]].
- DataForSEO Labs is Live-only; SERP/Merchant/Business Data support both Live and Standard.

## When to use / how it fits
- This is the spine page: most flows ([[play-keyword-research-workflow]], [[play-backlink-audit]], [[play-competitor-gap-analysis]], [[play-technical-site-audit]]) are sequences of rows from this table.
- Pair every routing choice with [[dec-cost-control-strategy]] to keep spend down.

## Gotchas / limits
- Endpoint paths and costs above are quoted from this brain's own runs and the official pricing pages; verify on your live invoice before scaling.
- Some jobs have both a live and a pre-indexed path (e.g. SERP vs Labs ranked_keywords) - picking wrong is the main cost leak.
- Several endpoints returned task-level errors in testing. The 40204 seen on Backlinks in the 2026-06-26 run is legacy after the 2026-07-01 pay-as-you-go move, while 40402 on merchant still needs path handling. Handle per [[cap-status-error-codes]].

## Worked examples
- "Rank-track 500 keywords daily" -> SERP Standard High + webhooks, store time series ([[play-rank-tracking-pipeline]]).
- "Build a keyword map for a new site" -> Labs keyword_ideas/suggestions/related + bulk_keyword_difficulty + search_intent ([[play-keyword-research-workflow]]).
- "Audit a prospect's backlinks" -> Backlinks summary + referring_domains + new/lost + bulk_spam_score ([[play-backlink-audit]]).
- "Find content gaps vs a competitor" -> Labs domain_intersection + ranked_keywords + Backlinks intersection ([[play-competitor-gap-analysis]]).

## Related
- [[index]]
- [[decisions/_index]]
- [[cap-platform-architecture]]
- [[cap-serp-api]]
- [[cap-labs-keyword-research]]
- [[cap-keywords-data-api]]
- [[cap-backlinks-api]]
- [[cap-onpage-api]]
- [[dec-labs-vs-live-apis]]
- [[dec-live-vs-standard-vs-priority]]
- [[dec-cost-control-strategy]]
- [[dec-mcp-vs-raw-rest]]

## Sources
- DataForSEO API v3 (intro: modules, methods) - https://docs.dataforseo.com/v3/ - retrieved 2026-06-26
- serp/overview - https://docs.dataforseo.com/v3/serp-overview/ - retrieved 2026-06-26
- dataforseo_labs/google/overview - https://docs.dataforseo.com/v3/dataforseo_labs-google-overview/ - retrieved 2026-06-26
- dataforseo_labs/google/keyword_ideas/live - https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/ - retrieved 2026-06-26
- SERP API pricing - https://dataforseo.com/apis/serp-api/pricing - retrieved 2026-06-26
- DataForSEO pricing update - https://dataforseo.com/update/pricing-update-in-dataforseo-apis - retrieved 2026-07-08
