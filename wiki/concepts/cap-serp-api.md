---
type: concept
title: "SERP API (Capability Hub)"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, serp, api-hub]
related:
  - "[[cap-serp-google-verticals]]"
  - "[[cap-serp-non-google-engines]]"
  - "[[cap-result-tiers-regular-advanced-html]]"
  - "[[cap-platform-architecture]]"
---

# SERP API (Capability Hub)

> The SERP API returns live and queued search-engine results pages for a keyword, location, and language across seven engines. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
The SERP API is DataForSEO's search-results scraping layer. You give it a `keyword`, a location, and a language, and it returns the structured ranked results for that query. It spans Google, Bing, YouTube, Baidu, Yahoo, Seznam, and Naver, each under `/v3/serp/{engine}/{type}/{method}`. Every engine and vertical shares one request envelope and one response envelope (tasks[] -> result[] -> items[]), so once you learn Google Organic the other surfaces are variations on the same shape. It is the source layer behind rank tracking, SERP-feature monitoring, and AI Overview capture.

## What it covers
- Google organic (with 50+ SERP element types) and ~15 verticals (routed in [[cap-serp-google-verticals]]): AI Mode, AI Overview, Maps, Local Finder, News, Events, Images, Jobs, Autocomplete, Ads Search/Advertisers, Finance, Dataset Search/Info, Search By Image.
- Non-Google engines (routed in [[cap-serp-non-google-engines]]): Bing, YouTube, Baidu, Yahoo, Seznam, Naver.
- Three execution shapes per endpoint where supported: Task POST + Tasks Ready + Task GET (Standard queue), and Live (synchronous).
- Three result depths: `regular` (organic + paid only), `advanced` (all 50+ element types), and `html` (raw page HTML). See [[cap-result-tiers-regular-advanced-html]].
- Google Organic `result.items[]` exposes element types including organic, paid, featured_snippet, people_also_ask, local_pack, knowledge_graph, top_stories, shopping, ai_overview, and dozens more.
- Crawl-control inputs: `max_crawl_pages`, `stop_crawl_on_match` with `match_type`/`match_value`, `target` and `target_search_mode`, and `find_targets_in`/`ignore_targets_in` to halt early on a domain hit.
- Helper reference endpoints for locations and languages per engine support the targeting parameters described in [[cap-locations-languages-targeting]].

### Root-level SERP utilities (engine-agnostic, run off a prior SERP `task_id`)
These two endpoints operate on the result of an earlier SERP task rather than on a fresh keyword query, so they live at the root of `/v3/serp/` rather than under an engine.
- **AI Summary** (`POST /v3/serp/ai_summary`, $0.01/req): generates an LLM summary over a stored SERP. Takes the source `task_id` (valid 30 days), a `prompt` (<= 2000 chars), `support_extra` (default true), `fetch_content` (default false), and `include_links` (default false). Feeds GEO and AI-search work in [[cap-geo-ai-search-optimization]] and [[play-ai-visibility-tracking]].
- **Screenshot** (`POST /v3/serp/screenshot`, $0.004/req): renders a full-page image of a prior SERP; the source `task_id` is valid for 7 days.

## Key parameters / inputs
| field | notes |
|---|---|
| keyword | required; up to 700 chars; special operators (site:, filetype:, allinanchor) incur a 5x keyword charge |
| location_code / location_name / location_coordinate | one location identifier required |
| language_code / language_name | language identifier |
| device | desktop (default) or mobile; `os` follows device |
| depth | Google Organic default 10, max 200 |
| group_organic_results | groups related results under the main item; default true |
| load_async_ai_overview | fetches async AI Overview, +$0.002 |
| people_also_ask_click_depth | clicks PAA 1-4 deep, +$0.00015 per click |
| calculate_rectangles | pixel-position ranking, +$0.002 |
| tag / postback_url / pingback_url / priority | task tagging, webhook delivery, queue priority |

## Response / what you get back
The envelope carries `version, status_code, status_message, time, cost, tasks_count, tasks_error` and a `tasks[]` array. Each task holds `id`, status fields, `cost`, `result_count`, `path`, echoed `data`, and `result[]`. Each result reports `keyword`, `type`, `se_domain`, `check_url`, `datetime`, `item_types`, `se_results_count`, `items_count`, and `items[]`. Organic items carry `rank_group`, `rank_absolute`, `position`, `domain`, `title`, `url`, `description`, plus optional `rating`, `price`, `links`, and `rectangle` (pixel box).

## Cost & method notes
- Base charge is per SERP request covering up to 10 results; `depth` above 10 can add cost when the engine returns more. Live Google Organic Advanced billed at $0.002 per SERP request (up to 10 results) in the cost log.
- Standard (POST -> Tasks Ready -> Task GET) is cheaper than Live (instant, no GET round trip). See [[cap-task-vs-live-execution]] and [[cap-queue-priority-cost-model]].
- Priority is 1 (normal) or 2 (high, costs more).
- Add-ons stack: special operators 5x, async AI Overview +$0.002, pixel rectangles +$0.002, PAA clicks +$0.00015/click.

## When to use / how it fits
Use SERP API to track rankings, capture SERP features, and snapshot AI Overviews on a schedule. It is the spine of [[play-rank-tracking-pipeline]] and a feeder for [[play-local-seo-tracking]] and [[play-content-strategy-brief]]. Targeting parameters are detailed in [[cap-locations-languages-targeting]]. For job-to-endpoint routing see [[dec-which-api-for-which-job]]; for the live-vs-queue tradeoff see [[dec-live-vs-standard-vs-priority]].

## Gotchas / limits
- Up to 2000 combined POST + GET calls per minute; max 100 tasks per POST; `keyword` <= 700 chars; `depth` <= 200; `max_crawl_pages` <= 100.
- Standard tasks report status 20100 "Task Created" then 40602 "Task In Queue" until ready.
- Some engines and verticals are Standard-only (no Live) and retain task results for 30 days; this is engine-specific and detailed in the routed notes.
- Live data is fresh-scraped; for cheaper near-real-time keyword and ranking facts, weigh pre-indexed Labs and Databases via [[dec-labs-vs-live-apis]].

## Related
- [[cap-serp-google-verticals]]
- [[cap-serp-non-google-engines]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-locations-languages-targeting]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-platform-architecture]]
- [[plat-google-search]]
- [[play-rank-tracking-pipeline]]
- [[cap-geo-ai-search-optimization]]
- [[play-ai-visibility-tracking]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/overview/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/ai_summary/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/serp/screenshot/ (retrieved 2026-06-26)
