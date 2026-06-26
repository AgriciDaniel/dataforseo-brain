---
type: concept
title: "OnPage API (Capability)"
domain: dataforseo
subdomain: onpage
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, onpage, technical-seo]
related:
  - "[[cap-task-vs-live-execution]]"
  - "[[cap-result-tiers-regular-advanced-html]]"
  - "[[play-technical-site-audit]]"
  - "[[cap-platform-architecture]]"
---

# OnPage API (Capability)

> The OnPage API is DataForSEO's website crawler: you queue a crawl of a domain, then pull a summary, page list, resources, duplicates, links, redirects, non-indexable pages, page-speed waterfalls, keyword density, raw HTML, parsed content, microdata, and Lighthouse audits. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
OnPage replicates what a technical-SEO crawler like Screaming Frog does, as an API. You POST a crawl task with a `target` and `max_crawl_pages`; the crawler fetches pages, optionally rendering JavaScript and loading resources, and computes an `onpage_score` plus dozens of per-page checks. You then poll `tasks_ready` and retrieve the data through a set of free reporting endpoints. A separate Instant Pages endpoint scans a single URL synchronously, and a Lighthouse sub-API runs Google's performance audit. It is the data layer behind site audits and technical health monitoring.

## What it covers
- Task lifecycle: `POST /v3/on_page/task_post`, `GET /v3/on_page/tasks_ready`, `POST /v3/on_page/force_stop`.
- Aggregate and page data: `/v3/on_page/summary`, `/v3/on_page/pages`, `/v3/on_page/pages_by_resource`, `/v3/on_page/resources`.
- **Uncrawlable resources (added 2026-04-21):** a new endpoint plus expanded `summary` data that expose resources which fail expected crawl conditions (e.g. blocked, unreachable, or non-fetchable assets). It improves crawl-result clarity and reporting accuracy, so audits can flag what the crawler could not reach instead of silently dropping it.
- Issue reports: `/v3/on_page/duplicate_tags`, `/v3/on_page/duplicate_content` (SimHash 0-10 similarity), `/v3/on_page/links`, `/v3/on_page/redirect_chains`, `/v3/on_page/non_indexable`.
- Performance and content: `/v3/on_page/waterfall` (page-speed timings), `/v3/on_page/keyword_density`, `/v3/on_page/raw_html`, `/v3/on_page/content_parsing`, `/v3/on_page/microdata`.
- Live single-page tools: `/v3/on_page/instant_pages` (synchronous scan with Core Web Vitals) and `/v3/on_page/page_screenshot`.
- Lighthouse sub-API: `/v3/on_page/lighthouse/task_post`, `.../tasks_ready`, `.../task_get/json/$id` (task_get also supports `.../task_get/html/$id`), and `/v3/on_page/lighthouse/live/json`. Three free helper endpoints back it: `/v3/on_page/lighthouse/languages` (supported audit locales), `/v3/on_page/lighthouse/audits` (the full audit catalog), and `/v3/on_page/lighthouse/versions` (available Lighthouse versions). **Update (2026-04-27): seven new browser-simulation parameters** were added to the Lighthouse API to customize the simulated browser/device/network environment for an audit (e.g. device class, network throttling, and emulation settings), giving tighter control over the conditions under which performance is measured.

## Key parameters / inputs
| field | notes |
|---|---|
| target | domain to crawl, without https:// or www. (task_post) |
| url | absolute URL for single-page endpoints (instant_pages, page_screenshot) |
| id | task UUID returned by task_post, used by every retrieval endpoint |
| max_crawl_pages | page limit for the crawl |
| enable_javascript / enable_browser_rendering / load_resources | render JS and load assets for Core Web Vitals; each adds cost |
| custom_js | custom script, max 2000 chars, 700ms timeout |
| store_raw_html | required to later retrieve via raw_html |
| calculate_keyword_density / validate_micromarkup | prerequisites for the keyword_density and microdata endpoints |
| filters / order_by / limit / offset | reporting-endpoint pagination (limit up to 1000) |

## Response / what you get back
The summary reports crawl state via `crawl_progress`, `crawl_status` (`max_crawl_pages`, `pages_in_queue`, `pages_crawled`), `crawl_stop_reason`, and the overall `onpage_score` (0-100). Page-level rollups appear under `page_metrics` (`links_internal`, `links_external`, `duplicate_title`, `duplicate_description`, `duplicate_content`, `broken_links`, `broken_resources`, `non_indexable`). Each page exposes a `checks.*` map of boolean SEO flags (for example `no_h1_tag`, `is_https`, `canonical`), a `page_timing` block with `time_to_interactive`, `dom_complete`, `largest_contentful_paint`, and `first_input_delay`, plus `meta` (`title`, `description`, `canonical`, `internal_links_count`, `images_count`) and `total_dom_size`. Links carry `type`, `dofollow`, `direction`, and `is_broken`. Lighthouse returns `lighthouseVersion`, `categories` (performance, accessibility, best_practices, seo, and pwa scores), and per-`audits` detail.

## Cost & method notes
- OnPage is primarily queue/task-based: POST charges immediately, then `tasks_ready` and every retrieval endpoint return `cost: 0`. See [[cap-task-vs-live-execution]].
- Billing is per page crawled. The cost log shows `/v3/on_page/instant_pages` at $0.000125 per result.
- `load_resources`, `enable_javascript`, `enable_browser_rendering`, `custom_js`, and `calculate_keyword_density` each add cost; the Lighthouse sub-API is billed separately.
- Crawl depth and rendering options are the main cost levers; see [[cap-queue-priority-cost-model]] and [[cap-result-tiers-regular-advanced-html]].

## When to use / how it fits
OnPage is the spine of [[play-technical-site-audit]] (crawl -> summary -> duplicates/redirects/non-indexable -> Lighthouse -> fix list) and contributes to [[play-cost-optimized-pipeline]] when paired with webhooks. Use Instant Pages for spot checks and the queue for full-site crawls. Route jobs via [[dec-which-api-for-which-job]] and weigh queue vs live via [[dec-live-vs-standard-vs-priority]].

## Gotchas / limits
- 2000 API calls/min, max 100 tasks per POST, max 30 simultaneous requests; Instant Pages allows max 20 tasks per request and no more than 5 identical domains per request.
- Task results are retained for 30 days; raw HTML for 7 days; completed tasks sit in `tasks_ready` up to 3 days.
- `enable_browser_rendering` requires both `enable_javascript` and `load_resources`; `store_raw_html`, `calculate_keyword_density`, and `validate_micromarkup` must be set at task_post or their reports return nothing.
- Duplicate content uses SimHash with a 0-10 similarity scale (default threshold 6); a 1-page crawl disables sitewide checks unless `force_sitewide_checks` is set.

## Related
- [[cap-task-vs-live-execution]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-webhooks-pingback-postback]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[cap-databases]]
- [[plat-google-search]]
- [[play-technical-site-audit]]
- [[play-cost-optimized-pipeline]]
- [[dec-which-api-for-which-job]]
- [[dec-live-vs-standard-vs-priority]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/on_page/task_post/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/on_page/instant_pages/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/on_page/lighthouse/overview/ (retrieved 2026-06-26)
- https://dataforseo.com/updates (retrieved 2026-06-26 - New Browser Simulation Parameters in OnPage Lighthouse API, published 2026-04-27; Uncrawlable Resources Data Added to On-Page API, published 2026-04-21)
