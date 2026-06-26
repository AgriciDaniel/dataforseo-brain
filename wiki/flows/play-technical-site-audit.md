---
type: flow
title: "Play: Technical Site Audit"
domain: dataforseo
subdomain: onpage
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, onpage, audit]
related:
  - "[[cap-onpage-api]]"
  - "[[cap-task-vs-live-execution]]"
  - "[[dec-cost-control-strategy]]"
---

# Play: Technical Site Audit

> Crawl a site with the OnPage API, pull the issue summary, drill into duplicates/redirects/non-indexables, run Lighthouse, and emit a prioritized fix list. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
This audit runs DataForSEO's own crawler over a target site and surfaces 60+ on-page checks: meta tags, duplicate content/titles, broken links/resources, redirect chains, non-indexable pages, response codes, and an overall `onpage_score`. It is a task-based (Standard) crawl: you post one task, then read aggregate and per-issue results from retrieval endpoints. Lighthouse adds Core Web Vitals and category scores per page.

## Trigger
A site needs a technical health check: a migration QA, a pre-launch gate, a quarterly audit, or a ranking-drop investigation. Input is a `target` domain plus a `max_crawl_pages` budget.

## Endpoints used (in order)
- `POST /v3/on_page/task_post` (start the crawl).
- `GET /v3/on_page/tasks_ready` then `GET /v3/on_page/summary/$id` (aggregate results).
- `GET /v3/on_page/pages/$id`, `/duplicate_tags/$id`, `/duplicate_content/$id` (page-level issues).
- `GET /v3/on_page/redirect_chains/$id`, `/non_indexable/$id`, `/links/$id` (link/index issues).
- `POST /v3/on_page/lighthouse/task_post` (or `/lighthouse/live/json`) for performance/CWV.
- `POST /v3/on_page/instant_pages` for a fast single-page spot check.

## Pipeline
1. Post the crawl: `task_post` with `target` and `max_crawl_pages`. Optionally set `start_url`, `respect_sitemap`, `enable_javascript`/`load_resources`/`enable_browser_rendering` (for CWV, each an extra charge), `store_raw_html`, and `pingback_url`. You are billed only at this POST step.
2. Wait for completion: poll `tasks_ready` (or receive the pingback). Crawls are async; `summary` can be read while `crawl_progress` is still `in_progress` for partial data.
3. Read `summary/$id`: capture `page_metrics.onpage_score` (0-100), `duplicate_title`, `duplicate_description`, `duplicate_content`, `broken_links`, `broken_resources`, `non_indexable`, `redirect_loop`, plus the `domain_info.checks` (sitemap, robots_txt, ssl, http2, redirects) and `ssl_info`.
4. Triage from `page_metrics.checks` counts: `no_title`, `title_too_long` (>65), `title_too_short` (<30), `no_h1_tag`, `no_description`, `duplicate_meta_tags`, `is_4xx_code`, `is_5xx_code`, `canonical_to_broken`, `is_orphan_page`, `has_render_blocking_resources`, `low_content_rate`, etc.
5. Drill into the offenders: `duplicate_tags`/`duplicate_content` for the actual duplicate clusters, `redirect_chains` for multi-hop redirects, `non_indexable` for accidentally blocked pages, `links` for broken internal links.
6. Run Lighthouse on key templates (home, category, product, article) via `lighthouse/live/json` or task-based; read `categories` (performance, accessibility, best-practices, seo) and the `audits` detail.
7. Compile a prioritized fix list (blocker -> high -> medium) mapped to specific URLs, and re-crawl after fixes to confirm.

## Cost & cadence
- Billing is per crawled page set at `task_post`; unused page allocations are refunded. The cost-log shows a small task cost of $0.00125 for a 10-page crawl, and `on_page/instant_pages` at $0.000125 for a single page.
- Extra charges apply for `load_resources`, `enable_javascript`, `enable_browser_rendering`, `custom_js`, and `calculate_keyword_density`; enable them only when you need rendered/CWV data.
- Retrieving `summary`/pages/links results via GET costs $0 (cost field 0) since you already paid at POST.
- Cadence: full crawl monthly or quarterly; `instant_pages` for ad-hoc single-page checks; Lighthouse on a small template sample, not every page.

## Output
A technical audit report: site `onpage_score`, an issue inventory with page counts, the duplicate/redirect/non-indexable detail tables, Lighthouse category scores per template, and a prioritized remediation backlog.

## Pitfalls / limits
- Setting `max_crawl_pages: 1` disables sitewide checks unless `force_sitewide_checks: true`.
- `crawl_delay` defaults to 2000ms; lowering it on a fragile server can cause crawl errors (`extended_crawl_status` will flag `site_unreachable` or `too_many_redirects`).
- Max 100 tasks per POST; Instant Pages, Content Parsing Live, and Page Screenshot are capped at 20. 2,000 calls/min, 30 simultaneous, 120s timeout.
- `onpage_score` depends on how many pages were crawled; compare like-for-like crawl sizes across runs.
- HTML/raw results have shorter retention (7 days) than standard results (30 days); pull what you need promptly.

## Decisions in play
- [[dec-which-api-for-which-job]]: OnPage API for the full crawl and issue inventory; Instant Pages for fast single-page checks; Lighthouse for performance/CWV.
- [[dec-cost-control-strategy]]: keep `max_crawl_pages` tight, leave JS/resource/CWV flags off unless needed (each adds charge), and reuse the free GET retrievals within the 30-day window.
- [[dec-live-vs-standard-vs-priority]]: the crawl is Standard (task-based) by design; use webhooks rather than polling for completion.

## Related
- [[cap-onpage-api]]
- [[cap-task-vs-live-execution]]
- [[cap-webhooks-pingback-postback]]
- [[cap-result-tiers-regular-advanced-html]]
- [[cap-rate-limits-throughput]]
- [[cap-queue-priority-cost-model]]
- [[plat-google-search]]
- [[dec-which-api-for-which-job]]
- [[dec-cost-control-strategy]]
- [[dec-live-vs-standard-vs-priority]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/on_page/task_post/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/on_page/summary/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/on_page/lighthouse/overview/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/on_page/overview/ (retrieved 2026-06-26)
