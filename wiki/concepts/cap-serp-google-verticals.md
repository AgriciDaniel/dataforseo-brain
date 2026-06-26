---
type: concept
title: "SERP API Google Verticals"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, serp, google]
related:
  - "[[cap-serp-api]]"
  - "[[cap-serp-non-google-engines]]"
  - "[[plat-google-search]]"
---

# SERP API Google Verticals

> The Google-specific SERP endpoints beyond plain organic: AI Mode, AI Overview, Maps, Local Finder, News, Events, Images, Search By Image, Jobs, Autocomplete, Ads, Finance, and Dataset Search/Info. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
Google exposes far more than ten blue links. The SERP API mirrors that with dedicated vertical endpoints, each under `/v3/serp/google/{vertical}/{method}`. They share the standard envelope but return vertical-specific element types and parameters. These verticals are how you capture local packs, news cycles, image carousels, job listings, ad transparency data, finance tickers, and the new generative surfaces (AI Mode and AI Overview) as structured data. This note routes the Google surfaces; see [[cap-serp-api]] for the shared mechanics and [[cap-serp-non-google-engines]] for other engines.

## What it covers
- **Google AI Mode** (`/serp/google/ai_mode/`, launched 2025-07-01): AI-generated overview content with markdown, `ai_overview_reference` source citations, and `ai_overview_shopping` product listings. Advanced and HTML only (no regular). Priced as a separate engine at ~2x standard SERP: $0.0012 Standard / $0.0024 Priority / $0.004 Live per request.
- **Google AI Overview**: captured inline on Google Organic via SERP Advanced `load_async_ai_overview: true` (+$0.002) and as `ai_overview` element types.
- **Google Maps** (`/serp/google/maps/`): up to 100 `maps_search` listings (depth max 700; mobile returns 20) with `rating`, `rating_distribution`, `address_info`, `place_id`, `work_hours`, `latitude`/`longitude`, `is_claimed`.
- **Google Local Finder** (`/serp/google/local_finder/`): `local_pack` businesses, default 20 desktop / 10 mobile, with `min_rating` and `time_filter` (open_now) filters and `cid`.
- **Google News** (`/serp/google/news/`): `news_search` articles plus grouped `top_stories`, default depth 10 max 200.
- **Google Events** (`/serp/google/events/`): `event_item` with `event_dates`, `location_info`, `information_and_tickets`; English only; `date_range` presets (today, weekend, next_month).
- **Google Images** (`/serp/google/images/`): top 100 `images_search` plus `carousel` and `related_searches`; fields `source_url`, `encoded_url`, `alt`.
- **Google Search By Image** (`/serp/google/search_by_image/`): reverse-image SERP for an `image_url`, returning organic-style matches and `related_searches`. Task-based only (no Live).
- **Google Jobs** (`/serp/google/jobs/`): `google_jobs_item` with `employer_name`, `salary`, `contract_type`, `time_ago`. Task-based only (no Live); results kept 30 days.
- **Google Autocomplete** (`/serp/google/autocomplete/`): `suggestion` items with `relevance` (500-2000, chrome client only), `cursor_pointer`, `client` (chrome, safari, youtube).
- **Google Ads Search** (`/serp/google/ads_search/`) and **Ads Advertisers**: creatives from the Ads Transparency Center with `advertiser_id`, `creative_id`, `format` (text/image/video), `preview_image`, `first_shown`/`last_shown` (min date 2018-05-31).
- **Google Finance** (`/serp/google/finance_explore|finance_markets|finance_quote|finance_ticker_search/`): `ticker`, `price`/`index_value`, `percentage_delta`, `trend`.
- **Google Dataset Search / Dataset Info** (`/serp/google/dataset_search/` and `/serp/google/dataset_info/`): `dataset_search` returns dataset listings for a query; `dataset_info` is its sibling lookup that returns full metadata for a single dataset by `dataset_id`.

## Key parameters / inputs
| field | notes |
|---|---|
| keyword | required for most verticals; up to 700 chars |
| location_* / language_* | one location and (for most) one language required |
| depth / block_depth | Maps default 100 max 700; News default 10 max 200; Images default 100 |
| date_range | Events only: today, tomorrow, week, weekend, next_week, month, next_month |
| min_rating / time_filter | Local Finder rating and open-hours filters |
| target / advertiser_ids | Ads Search by domain or up to 25 advertiser IDs |
| news_type | Finance Explore: top_stories, local_market, world_markets |
| calculate_rectangles | pixel ranking; doubles cost on AI Mode and News |

## Response / what you get back
Each vertical returns its own `item_types`. Maps returns `maps_search` and `maps_paid_item`; Local Finder returns `local_pack`; News returns `news_search` and `top_stories`; Images returns `images_search`, `carousel`, `related_searches`; Jobs returns `google_jobs_item`; Autocomplete returns suggestion items; Ads Search returns `ads_search`; Finance returns `google_finance_hero_groups`, `google_finance_news`, `google_finance_market_trends`, and siblings.

## Cost & method notes
- Most verticals bill per SERP request at the engine's default result count; deeper requests can add cost. Live Maps and News are billed at $0.002 per result in the cost log.
- AI Mode and News double cost when `calculate_rectangles` is on; Finance Explore doubles for local_market or world_markets news types.
- Jobs charges only at task posting; task_get retrieval is free and results live 30 days. See [[cap-task-vs-live-execution]] and [[cap-queue-priority-cost-model]].

## When to use / how it fits
Maps and Local Finder drive [[play-local-seo-tracking]]; AI Mode and AI Overview feed [[cap-geo-ai-search-optimization]] and [[play-ai-visibility-tracking]]; News, Images, and Autocomplete support [[play-content-strategy-brief]]. Route the right surface with [[dec-which-api-for-which-job]].

## Gotchas / limits
- Events is English-only. Jobs has no Live variant. Mobile Maps caps at 20 results.
- Autocomplete `relevance` populates only for chrome and chrome-omni clients.
- Ads Search `date_from` cannot precede 2018-05-31; `advertiser_ids` max 25.
- All verticals share the 2000 calls/min limit and the 700-char keyword cap.

## Related
- [[cap-serp-api]]
- [[cap-serp-non-google-engines]]
- [[plat-google-search]]
- [[plat-google-maps-local]]
- [[cap-geo-ai-search-optimization]]
- [[cap-result-tiers-regular-advanced-html]]
- [[play-local-seo-tracking]]
- [[cap-platform-architecture]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/google/ai_mode/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/maps/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/local_finder/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/news/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/images/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/jobs/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/ads_search/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/finance_explore/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/search_by_image/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/google/dataset_info/live/advanced/ (retrieved 2026-06-26)
- https://dataforseo.com/apis/serp-api/google-ai-mode-serp-api (retrieved 2026-06-26)
