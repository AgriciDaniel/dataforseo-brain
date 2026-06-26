---
type: platform
title: "Other Search Engines as DataForSEO Surfaces"
domain: dataforseo
subdomain: serp
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, serp, regional]
related:
  - "[[cap-serp-non-google-engines]]"
  - "[[cap-serp-api]]"
  - "[[play-rank-tracking-pipeline]]"
---

# Other Search Engines as DataForSEO Surfaces

> Baidu, Yahoo, Seznam, and Naver organic SERPs for regional coverage where Google does not dominate. Sits under [[index|DataForSEO Brain]] then [[platforms/_index|Platforms]].

## Overview
Beyond Google, Bing, and YouTube, the SERP API exposes four regional engines that matter where local market share is high: Baidu (China), Yahoo (still significant in Japan and as a portal), Seznam (Czech Republic), and Naver (South Korea). Each returns a typed organic SERP in the same response envelope, so the same parsing code works across engines. The important practical difference is execution mode: Baidu and Seznam are Standard-only (no Live endpoint), Naver adds a Live Advanced variant, and Yahoo offers the full Standard plus Live range.

## What it covers
- `serp/baidu/organic` (China): organic, paid, related_searches, local_pack, map, video, images, stocks_box, dictionary, shopping. Standard only.
- `serp/yahoo/organic`: organic, paid, images, video, shopping, featured_snippet, top_stories, local_pack, hotels_pack, recipes, people_also_ask, related_searches, ai_overview. Standard plus Live.
- `serp/seznam/organic` (Czech): organic, paid, images, local_pack, related_searches, top_stories, featured_snippet, video, shopping. Standard only.
- `serp/naver/organic` (South Korea): organic, paid, related_searches, images, video, local_pack, map. Standard plus a Live Advanced variant.

## Key parameters / inputs
- All four: `keyword` (Yahoo allows up to 700 chars), `location_code`, `language_code`, `device`, `os`, `tag`.
- Baidu and Naver add `priority` (1 normal / 2 high) for the queue.
- Seznam adds `calculate_rectangles` (pixel coordinates) and `postback_url` / `postback_data` for webhook delivery.
- Yahoo adds `depth` (default 6, max 200), `max_crawl_pages` (max 100), `target`, `stop_crawl_on_match`, and `location_coordinate`.

## Response / what you get back
- Shared envelope: `version`, `status_code`, `cost`, `tasks[]` then `result[]`.
- `result.keyword`, `result.check_url`, `result.datetime`, `result.item_types`, `result.se_results_count`, `result.items[]`.
- Per item: `type`, `rank_group`, `rank_absolute`, `domain`, `title`, `url`, `description`, plus enriched `rating` and `price` where present, and `rectangle` when pixel calculation is enabled.

## Cost & method notes
- Baidu and Seznam charge only for posting the task; results are retrievable free for 30 days via the GET endpoints, with no Live option. See [[cap-task-vs-live-execution]].
- Yahoo supports both Standard and Live (Regular, Advanced, HTML); Naver supports Standard plus Live Advanced.
- Standard is cheaper than Live across the board. See [[cap-queue-priority-cost-model]] and [[dec-live-vs-standard-vs-priority]].

## When to use / how it fits
- Rank tracking in markets where the regional engine leads: [[play-rank-tracking-pipeline]].
- Regional competitor gap analysis where Google data understates true visibility: [[play-competitor-gap-analysis]].
- Choosing whether a job even needs a non-Google engine: [[dec-when-not-to-use-dataforseo]].
- Engine-by-engine routing: [[dec-which-api-for-which-job]].

## Gotchas / limits
- Baidu and Seznam have no Live endpoint, so latency-sensitive workflows must use the queue and poll or use webhooks.
- Task results for the Standard-only engines are retained for 30 days; retrieve within that window.
- Yahoo SERPs can return fewer than 10 results; the default `depth` is only 6.
- Element coverage varies by engine, so do not assume a feature type exists everywhere; check `result.item_types`. See [[cap-locations-languages-targeting]].
- `location_code` and `language_code` are optional on Baidu, Seznam, and Naver but required (one each) on Yahoo, so target settings are not interchangeable across engines.
- Baidu and Seznam expose `task_get/regular`, `task_get/advanced`, and `task_get/html`, so result depth still follows the Regular versus Advanced versus HTML tiers even without a Live path.
- Naver's `task_get` requires the task `id` (UUID), with results retained 30 days like the other queue-only engines.

## Related
- [[cap-serp-non-google-engines]]
- [[cap-serp-api]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-task-vs-live-execution]]
- [[cap-locations-languages-targeting]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[play-rank-tracking-pipeline]]
- [[play-competitor-gap-analysis]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[dec-when-not-to-use-dataforseo]]
- [[index]]
- [[platforms/_index]]

## Sources
- https://docs.dataforseo.com/v3/serp/baidu/organic/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/yahoo/organic/live/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/seznam/organic/task_get/advanced/ - retrieved 2026-06-26
- https://docs.dataforseo.com/v3/serp/naver/organic/task_get/advanced/ - retrieved 2026-06-26
