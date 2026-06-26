---
type: concept
title: "SERP API Non-Google Engines"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, serp, engines]
related:
  - "[[cap-serp-api]]"
  - "[[cap-serp-google-verticals]]"
  - "[[plat-other-search-engines]]"
---

# SERP API Non-Google Engines

> SERP coverage for Bing, YouTube, Baidu, Yahoo, Seznam, and Naver, including which engines are Live and which are task-only. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
Beyond Google, the SERP API scrapes six more engines, each under `/v3/serp/{engine}/`. They share the standard envelope but differ in available methods, default depth, and which feature element types appear. The most important practical split is execution model: Bing and Yahoo offer full Live plus Standard with regular/advanced/html; YouTube and Naver offer a Live Advanced variant; Baidu and Seznam are Standard-only (task-based, no Live). This note routes the non-Google engines; see [[cap-serp-api]] for shared mechanics and [[cap-serp-google-verticals]] for Google surfaces.

## What it covers
- **Bing Organic** (`/serp/bing/organic/`): up to 100 results; Regular, Advanced, HTML; Live and Standard. Element types include organic, paid, answer_box, featured_snippet, people_also_ask, local_pack, shopping, top_stories, video, and ai_overview. Locations and languages via `/serp/bing/locations` and `/serp/bing/languages`.
- **YouTube Organic** (`/serp/youtube/organic/`): up to 20 blocks (`block_depth` 1-200); element types `youtube_video` (video_id, channel_name, views_count, duration_time_seconds, is_shorts, is_live), `youtube_channel`, `youtube_playlist`. Advanced only. Sibling endpoints: Video Info, Video Subtitles, Video Comments.
- **Baidu Organic** (`/serp/baidu/organic/`): Chinese engine; Standard-only (Regular/Advanced/HTML, no Live). Elements: organic, paid, related_searches, local_pack, map, video, images, stocks_box, dictionary, shopping.
- **Yahoo Organic** (`/serp/yahoo/organic/`): Live and Standard; Regular/Advanced/HTML; default depth 6, max 200. Elements include organic, paid, images, video, shopping, featured_snippet, top_stories, local_pack, recipes, ai_overview.
- **Seznam Organic** (`/serp/seznam/organic/`): Czech engine; Standard-only. Supports `calculate_rectangles` and postback webhooks. Elements: organic, paid, images, local_pack, related_searches, top_stories, featured_snippet, video, shopping.
- **Naver Organic** (`/serp/naver/organic/`): Korean engine; Standard plus a Live Advanced variant. Elements: organic, paid, related_searches, images, video, local_pack, map.
- **YouTube companion endpoints**: Video Info, Video Subtitles, and Video Comments extend the YouTube surface beyond search results into per-video metadata, transcripts, and engagement.
- **Bing locations and languages**: resolved through dedicated `/serp/bing/locations` and `/serp/bing/languages` reference endpoints, consistent with the targeting helpers in [[cap-locations-languages-targeting]].

## Key parameters / inputs
| field | notes |
|---|---|
| keyword | required at task_post; up to 700 chars on Bing/Yahoo |
| location_* / language_* | one location and one language required on Bing and Yahoo; optional on Baidu, Seznam, Naver |
| depth | Bing default 10 max 200; Yahoo default 6 max 200 |
| block_depth | YouTube: 1-200, default 20 |
| device / os | desktop or mobile across engines |
| target / stop_crawl_on_match | Bing and Yahoo domain filtering and early-stop |
| id | required for task_get on Baidu, Seznam, Naver (UUID) |
| calculate_rectangles | Bing and Seznam pixel positions (+$0.002 on Bing) |

## Response / what you get back
The envelope and `result[] -> items[]` structure matches Google. Organic items across engines carry `type`, `rank_group`, `rank_absolute`, `page`, `position`, `xpath`, `domain`, `title`, `url`, `description`, and optional `rating`, `price`, `links`, and `rectangle`. YouTube items instead carry video/channel/playlist identifiers and stats. Each result lists its `item_types`, `se_results_count`, `items_count`, and (where paged) `pages_count`.

## Cost & method notes
- Bing, YouTube, Yahoo Live Advanced are billed at $0.002 per result in the cost log.
- Baidu and Seznam charge only at task posting; task_get retrieval is free and results are retained 30 days. Naver task results also persist 30 days. See [[cap-task-vs-live-execution]] and [[cap-queue-priority-cost-model]].
- Result depth (regular vs advanced vs html) follows [[cap-result-tiers-regular-advanced-html]]; Bing and Yahoo expose all three, YouTube and Naver expose advanced.

## When to use / how it fits
Bing underpins [[plat-bing-search]] and pairs with Bing Ads keyword data; YouTube underpins [[plat-youtube]] as a discovery and AI-citation surface; Baidu, Yahoo, Seznam, and Naver cover regional reach in [[plat-other-search-engines]]. Route by job in [[dec-which-api-for-which-job]] and choose execution mode via [[dec-live-vs-standard-vs-priority]].

## Gotchas / limits
- Baidu and Seznam have no Live endpoint; plan for the queue and 30-day retention.
- YouTube returns blocks rather than a flat result count, so `block_depth` is the lever.
- Yahoo SERPs can return fewer than 10 results; default depth is 6.
- All engines share the 2000 calls/min limit; non-Google feature coverage is thinner than Google's, so expect fewer element types per SERP.

## Related
- [[cap-serp-api]]
- [[cap-serp-google-verticals]]
- [[plat-bing-search]]
- [[plat-youtube]]
- [[plat-other-search-engines]]
- [[cap-task-vs-live-execution]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-platform-architecture]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/bing/organic/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/youtube/organic/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/baidu/organic/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/yahoo/organic/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/seznam/organic/task_get/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/naver/organic/task_get/advanced/ (retrieved 2026-06-26)
