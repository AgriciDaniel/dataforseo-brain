---
type: platform
title: "Google Search as a DataForSEO Surface"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, serp, google]
related:
  - "[[cap-serp-api]]"
  - "[[cap-serp-google-verticals]]"
  - "[[play-rank-tracking-pipeline]]"
---

# Google Search as a DataForSEO Surface

> Google organic results, paid units, and 50+ SERP features (including AI Overviews and AI Mode) exposed as structured data. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
Google web search is the single richest surface DataForSEO indexes. The SERP API Google Organic endpoint returns the full ranked page for a keyword, location, and language, decomposed into typed elements instead of an HTML blob. The same surface is enriched by DataForSEO Labs (pre-indexed keyword and competitor intelligence drawn from Google data) and by the AI Optimization API (which tracks Google AI Overview citations). For most rank tracking, keyword research, and competitor analysis jobs this is the first surface a practitioner reaches.

## What it covers
- `serp/google/organic` (Regular / Advanced / HTML) returns organic, paid, and 50+ feature element types in one call.
- `result.items[]` element types include: organic, paid, featured_snippet, people_also_ask, local_pack, hotels_pack, knowledge_graph, top_stories, video, images, shopping, popular_products, discussions_and_forums, perspectives, and `ai_overview`.
- `serp/google/ai_mode` returns AI Mode answers as `ai_overview`, `ai_overview_reference` (source citations with domain, url, title, text), and `ai_overview_shopping` elements (Advanced and HTML only).
- `load_async_ai_overview` on the organic endpoint pulls the async-loaded AI Overview for +$0.002.
- Sibling Google verticals share the same envelope: `serp/google/news` (news_search, top_stories), `serp/google/images`, `serp/google/jobs`, `serp/google/events`, `serp/google/autocomplete`, `serp/google/finance`, `serp/google/ads_search`.
- DataForSEO Labs Google datasets (Keyword Ideas, Keyword Suggestions, Related Keywords, Ranked Keywords, SERP Competitors, Domain Intersection) sit on top of the same Google SERP corpus, pre-indexed for cheaper bulk reads.

## Key parameters / inputs
- `keyword` (required, up to 700 chars; special operators like `site:`, `filetype:`, `allinanchor` incur a 5x charge).
- One of `location_code` / `location_name` / `location_coordinate` (GPS as "latitude,longitude,radius").
- `language_code` or `language_name`.
- `device` ("desktop" default or "mobile"), `os`, `depth` (default 10, max 200).
- `people_also_ask_click_depth` (1-4 deep, +$0.00015/click), `calculate_rectangles` (pixel rankings, +$0.002).
- `target` plus `stop_crawl_on_match` / `max_crawl_pages` (max 100) for targeted domain crawls.

## Response / what you get back
- Envelope: `version`, `status_code` (20000 OK), `cost`, `tasks[]`, each task carrying `result[]`.
- `result.item_types` lists the element types present; `result.se_results_count` is the total indexed result count; `result.items[]` holds the typed elements.
- Per organic item: `rank_group`, `rank_absolute`, `page`, `position`, `xpath`, `domain`, `title`, `url`, `description`, `is_featured_snippet`, `rating`, `price`, `links`, `about_this_result`.
- AI Mode items carry nested `ai_overview_element`, `ai_overview_table_element`, `ai_overview_shopping_element`, and reference citations.

## Cost & method notes
- Base charge is per SERP request for up to 10 results; `depth` beyond 10 adds cost when the engine returns more. See [[cap-queue-priority-cost-model]].
- Regular returns organic plus paid only; Advanced returns every element type; HTML returns the raw page. See [[cap-result-tiers-regular-advanced-html]].
- Standard (POST then Tasks Ready then Task GET) is cheaper than Live (synchronous, no GET). Priority 1 is normal, 2 is high. See [[cap-task-vs-live-execution]].
- Labs Google endpoints are Live-only POST but read from a pre-indexed database, so they are cheaper than live SERP for bulk keyword work. See [[dec-labs-vs-live-apis]].

## When to use / how it fits
- Daily or weekly rank tracking via Standard plus webhooks: [[play-rank-tracking-pipeline]].
- Seed-to-prioritized keyword discovery blending Keywords Data volume with Labs ideas and difficulty: [[play-keyword-research-workflow]].
- Building a content brief from live SERP scrape plus Labs market data: [[play-content-strategy-brief]].
- Tracking AI Overview presence as part of a GEO loop: [[cap-geo-ai-search-optimization]].

## Gotchas / limits
- Special search operators multiply keyword cost by 5x; AI Overview and pixel rectangles add surcharges.
- Up to 2000 POST plus GET calls per minute; max 100 tasks per POST; `keyword` capped at 700 chars. See [[cap-rate-limits-throughput]].
- AI Overview citation sourcing is volatile and only partially tracks the classic top 10, so AI Mode coverage should be tracked separately from organic rank.
- Mobile and desktop return different element sets; always pin `device`.

## Related
- [[cap-serp-api]]
- [[cap-serp-google-verticals]]
- [[cap-labs-keyword-research]]
- [[cap-labs-competitor-research]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-locations-languages-targeting]]
- [[cap-geo-ai-search-optimization]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[play-rank-tracking-pipeline]]
- [[play-keyword-research-workflow]]
- [[play-content-strategy-brief]]
- [[dec-which-api-for-which-job]]
- [[dec-labs-vs-live-apis]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/google/ai_mode/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/google/news/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/overview/ - retrieved 2026-06-26
