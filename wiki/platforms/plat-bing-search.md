---
type: platform
title: "Bing Search as a DataForSEO Surface"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, serp, bing, microsoft]
related:
  - "[[cap-serp-non-google-engines]]"
  - "[[cap-keywords-data-api]]"
  - "[[play-keyword-research-workflow]]"
---

# Bing Search as a DataForSEO Surface

> Bing organic SERP plus Microsoft/Bing Ads keyword metrics, the second-largest Western search surface and the index behind ChatGPT web answers. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
Bing matters for two reasons. First, it is a full second SERP surface that DataForSEO exposes through the SERP API exactly like Google, with up to 100 organic results and most of the same feature types. Second, Microsoft Advertising (Bing Ads) is a distinct keyword-metrics source under the Keywords Data API, giving an independent search-volume and CPC signal that DataForSEO also uses to normalize Google Labs volumes. Bing's relevance has grown because ChatGPT's web search leans on Bing's real-time index, making Bing visibility a proxy for one slice of AI answer sourcing.

## What it covers
- `serp/bing/organic` (Regular / Advanced / HTML) returns organic, paid, and feature elements: answer_box, carousel, featured_snippet, people_also_ask, local_pack, shopping, top_stories, video, faq, and `ai_overview`.
- Keywords Data Bing sub-API exposes seven endpoints: Search Volume, Search Volume History, Keywords For Site, Keywords For Keywords, Keyword Performance, Keyword Suggestions For URL, and Audience Estimation.
- Search Volume returns monthly volume, 24-month trend, CPC, and competition sourced from Microsoft Advertising.
- Keyword Performance returns ad clicks, impressions, average CPC, CTR, and average bid by device and match type for the previous month.
- Audience Estimation uses Microsoft/LinkedIn targeting dimensions (age, gender, industry_id, job_function_id) to size reach.

## Key parameters / inputs
- SERP: `keyword` (up to 700 chars), one location field (via `/serp/bing/locations`), one language field (via `/serp/bing/languages`), `depth` (default 10, max 200), `device`.
- Keywords Data Search Volume: `keywords` (up to 1000, max 100 chars each), one location field, one language field, `device` (all/mobile/desktop/tablet), `search_partners`, `date_from`/`date_to`.
- Keywords For Site: `target` domain or URL, returns up to 3000 keywords.
- Keyword Performance: `keywords`, `match` (aggregate/broad/phrase/exact), device.

## Response / what you get back
- SERP items: `rank_group`, `rank_absolute`, `page`, `position`, `domain`, `title`, `url`, `description`, `rating`, `price`, `links`, `faq`.
- Search Volume fields: `competition` (0.1 low / 0.5 medium / 0.9 high), `cpc` (USD), `search_volume` (rounded to nearest tens), `monthly_searches[]` (year, month, search_volume).
- Keyword Performance fields: `ad_position`, `clicks`, `impressions`, `average_cpc`, `ctr`, `total_cost`, `average_bid`.

## Cost & method notes
- SERP bills per SERP up to 10 results; Standard versus Live; Regular versus Advanced versus HTML. See [[cap-result-tiers-regular-advanced-html]].
- Keywords Data endpoints charge a single flat rate per request regardless of keyword count (1 or 1000 keywords cost the same). See [[cap-queue-priority-cost-model]].
- Bing keyword endpoints support Live and Standard; Keyword Performance charges only for setting a task.

## When to use / how it fits
- A second-engine slice of rank tracking and keyword research: [[play-keyword-research-workflow]].
- Cross-engine volume validation, since Google Labs volumes can be normalized with Bing data (`keyword_info_normalized_with_bing`).
- Deciding which keyword source fits the job: [[dec-which-api-for-which-job]].
- Lineage of the keyword numbers: [[ent-google-ads-keyword-planner]] versus Bing Ads.

## Gotchas / limits
- Several Bing Keywords Data endpoints support only English, French, and German (en, fr, de).
- Historical data spans 24 months; weekly is limited to 15 weeks, daily to 45 days; docs advise against custom past-year ranges.
- Bing publishes updated performance data only after the 3rd of each month.
- Keyword Suggestions For URL returns a `confidence_score` (0.0-1.0), the probability a keyword matches a user's query, sorted high to low, which is a different signal from raw volume.
- Audience Estimation returns ranges (`est_impressions`, `est_audience_size`, `est_clicks`, `est_spend`) plus a `suggested_bid` and `suggested_budget`, not point estimates.
- Up to 2000 API calls/min. See [[cap-rate-limits-throughput]].

## Related
- [[cap-serp-non-google-engines]]
- [[cap-keywords-data-api]]
- [[cap-serp-api]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-locations-languages-targeting]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[play-keyword-research-workflow]]
- [[play-rank-tracking-pipeline]]
- [[ent-google-ads-keyword-planner]]
- [[plat-ai-assistants]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/bing/organic/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/keywords_data/bing/search_volume/live/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/keywords_data/bing/keyword_performance/live/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/keywords_data/bing/audience_estimation/live/ - retrieved 2026-06-26
