---
type: concept
title: "Locations, Languages & Targeting"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, targeting]
related:
 - "[[cap-serp-api]]"
 - "[[cap-platform-architecture]]"
 - "[[cap-task-vs-live-execution]]"
---

# Locations, Languages & Targeting

> The geo/language/device parameters that pin a query to a market: `location_code`/`location_name`/coordinate, `language_code`, and device/os, plus helper endpoints that list valid values per API. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
Search results depend on where and how a query is run, so most DataForSEO endpoints accept targeting parameters that specify the market, language, and device. You can target by numeric location code, human-readable location name, or coordinate (for Maps/local), and set the interface language. Each API publishes helper endpoints listing the locations and languages it supports, because coverage differs by module and engine.

## What it covers
- Location targeting: `location_code` (numeric), `location_name` (string), or `location_coordinate` (lat,lng,radius for Maps/Local Finder).
- Language targeting: `language_code` (and `language_name`).
- Device/OS: `device` (desktop/mobile) and `os` where supported.
- Helper endpoints: per-API `locations` and `languages` lists (e.g. `serp/google/locations`, `serp/.../languages`) that enumerate valid values.
- These parameters are shared across SERP, Keywords Data, Labs, Merchant, App Data, and Business Data.

## Key parameters / inputs
- `location_code` / `location_name` - one is required for most SERP/keyword endpoints.
- `language_code` / `language_name`.
- `location_coordinate` - for Maps/Local Finder geo-grid targeting.
- `device`, `os` - for mobile vs desktop SERP shape.
- `keyword` plus targeting determines the exact SERP scraped.

## Response / what you get back
- Helper endpoints return the catalog of supported `location_code`/`location_name` and `language_code` values per API.
- Result items echo the resolved location and language so you can confirm the market that was queried.
- Live-observed: SERP and keyword calls in `_cost-log.json` run with explicit location/language targeting (e.g. Google organic, Maps, News, Images at $0.002 each).

## Cost & method notes
Targeting parameters do not themselves add cost, but using a stale/invalid location triggers status 40505 ("Outdated location parameters used") and the task fails (no charge). Maps/Local Finder coordinate targeting drives local-pack pipelines. Database pricing depends on the location parameters chosen. See [[cap-queue-priority-cost-model]] and [[cap-databases]].

## When to use / how it fits
Set targeting on every market-specific job: rank tracking ([[play-rank-tracking-pipeline]]), local SEO ([[play-local-seo-tracking]]), and keyword research ([[play-keyword-research-workflow]]). It maps surfaces in [[plat-google-search]], [[plat-google-maps-local]], and [[plat-bing-search]], and feeds routing in [[dec-which-api-for-which-job]].

## Gotchas / limits
- Outdated/invalid location parameters → status 40505; refresh from the helper endpoint.
- Coverage differs by API and engine - non-Google engines support fewer locations/languages. See [[cap-serp-non-google-engines]].
- Maps/local require coordinate targeting for accurate geo-grid results, not just a city name.
- Always resolve `location_code` from the helper list rather than hardcoding, since codes change.

- Resolve `location_code` from the helper endpoint rather than hardcoding, since codes change.
- Stale or invalid location parameters fail the task with status 40505. See [[cap-status-error-codes]].
- Maps and Local Finder need `location_coordinate` (lat,lng,radius) for accurate geo-grid results. See [[plat-google-maps-local]].
- Coverage differs by API and engine; non-Google engines support fewer locations/languages. See [[cap-serp-non-google-engines]].
- `device` and `os` change the SERP shape (mobile vs desktop). See [[cap-serp-google-verticals]].
- Targeting parameters add no cost themselves, but Database pricing depends on the location chosen. See [[cap-databases]].
- Result items echo the resolved location/language so you can confirm the queried market.
- Helper `locations`/`languages` endpoints are free to call. See [[cap-account-usage-userdata]].
- Targeting is shared across SERP, Keywords Data, Labs, Merchant, App Data, and Business Data. See [[cap-keywords-data-api]].
- Validate targeting for free in the sandbox before billed runs. See [[cap-sandbox-testing]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-serp-api]]
- [[cap-platform-architecture]]
- [[cap-task-vs-live-execution]]
- [[cap-serp-non-google-engines]]
- [[cap-databases]]
- [[plat-google-maps-local]]
- [[plat-google-search]]
- [[dec-which-api-for-which-job]]
- [[play-local-seo-tracking]]
- [[play-rank-tracking-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/serp-overview/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/errors/ (retrieved 2026-06-26)
- https://dataforseo.com/apis/serp-api/pricing (retrieved 2026-06-26)
