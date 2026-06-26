---
type: concept
title: "Result Tiers: Regular / Advanced / HTML"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, serp]
related:
 - "[[cap-serp-api]]"
 - "[[cap-task-vs-live-execution]]"
 - "[[cap-queue-priority-cost-model]]"
---

# Result Tiers: Regular / Advanced / HTML

> Three depths of parsed output you can request from SERP and OnPage endpoints: Regular (organic + paid only), Advanced (full structured parse of every element), and HTML (the raw unparsed page). Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
DataForSEO lets you choose how richly a result is parsed. The tier you request controls which SERP element types you get back and, on some endpoints, the price. Regular returns only organic and paid items; Advanced returns the full structured parse of all SERP feature/element types; HTML returns the raw page so you can parse it yourself or audit what was scraped. The tier is selected in the path tail of `task_get` (or the Live path).

## What it covers
- Regular: organic + paid results only (limited to organic search types).
- Advanced: full structured parse of all SERP feature/element types across engines (e.g. AI Overview, featured snippets, People Also Ask, local pack, knowledge graph, images).
- HTML: the raw unparsed SERP HTML page.
- Tier is set per request and applies across SERP verticals and, for OnPage, raw page retrieval.

## Key parameters / inputs
- Path tail selects tier: `.../task_get/regular/$id`, `.../task_get/advanced/$id`, `.../task_get/html/$id`; Live uses `.../live/advanced` etc.
- `postback_data` mirrors the tier when pushing results via postback ("advanced"/"html"/sometimes "regular"). See [[cap-webhooks-pingback-postback]].
- `depth` controls how many results are parsed within a tier (cost scales above the base 10). See [[cap-queue-priority-cost-model]].

## Response / what you get back
- Regular: `items[]` of organic/paid types only.
- Advanced: `items[]` covering every detected element type, including AI features; `item_types` lists what was found (e.g. `ai_overview` auto-included when detected).
- HTML: a single field with the raw page markup (no structured `items`).
- Live-observed: all SERP Live calls in `_cost-log.json` use `/live/advanced` at $0.002/SERP (google organic, maps, bing, youtube, news, images).

## Cost & method notes
Regular and Advanced are the common analytical tiers; HTML is for raw capture/auditing. HTML results have a shorter retention (7 days) than Standard parsed results (30 days), and once a Page Screenshot is generated its URL is accessible only 1 day. Advanced is the default for full SERP-feature tracking. Async AI Overview expansion (`load_async_ai_overview=true`) bills extra; `expand_ai_overview=true` is free on HTML endpoints. See [[cap-serp-google-verticals]].

## When to use / how it fits
- Tracking organic positions only → Regular (lighter).
- Tracking SERP features, AI Overviews, local packs → Advanced.
- Auditing exactly what was scraped or doing custom parsing → HTML.
This choice feeds [[play-rank-tracking-pipeline]], [[play-content-strategy-brief]], and the routing in [[dec-which-api-for-which-job]].

## Gotchas / limits
- Regular excludes most SERP features - do not use it for AI Overview or feature tracking.
- HTML retention is 7 days vs 30 for parsed Standard results; capture promptly. See [[cap-account-usage-userdata]].
- Higher `depth` multiplies cost within any tier.
- Tier availability and element coverage vary by engine/vertical. See [[cap-serp-non-google-engines]].

- Advanced is the default for full SERP-feature and AI Overview tracking. See [[cap-serp-google-verticals]].
- HTML is for raw capture/auditing or custom parsing where no structured `items` are needed.
- HTML results retain for 7 days versus 30 days for parsed Standard results. See [[cap-account-usage-userdata]].
- Page Screenshot URLs are accessible only 1 day once generated. See [[cap-onpage-api]].
- `load_async_ai_overview=true` bills extra; `expand_ai_overview=true` is free on HTML endpoints.
- Tier is mirrored by `postback_data` when results are pushed via postback. See [[cap-webhooks-pingback-postback]].
- Element coverage in Advanced varies by engine and vertical. See [[cap-serp-non-google-engines]].
- All SERP Live calls observed in `_cost-log.json` used `/live/advanced` at $0.002/SERP.
- Higher `depth` multiplies cost within any tier. See [[cap-queue-priority-cost-model]].
- Tier choice routes into [[dec-which-api-for-which-job]] and [[play-rank-tracking-pipeline]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-serp-api]]
- [[cap-serp-google-verticals]]
- [[cap-serp-non-google-engines]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-onpage-api]]
- [[cap-webhooks-pingback-postback]]
- [[dec-which-api-for-which-job]]
- [[play-rank-tracking-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/serp-overview/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/how-long-do-you-keep-results (retrieved 2026-06-26)
- https://dataforseo.com/update/ai-overview-in-google-serp-api (retrieved 2026-06-26)
- https://dataforseo.com/apis/serp-api/pricing (retrieved 2026-06-26)
