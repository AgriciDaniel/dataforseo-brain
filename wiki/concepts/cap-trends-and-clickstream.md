---
type: concept
title: "Trends and Clickstream"
domain: dataforseo
subdomain: keywords
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, keywords, clickstream]
related:
  - "[[cap-keywords-data-api]]"
  - "[[ent-clickstream-data]]"
  - "[[cap-data-collection-methodology]]"
---

# Trends and Clickstream

> Popularity-over-time and real-volume keyword signals from Google Trends, DataForSEO Trends, and anonymized clickstream data. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
Within the Keywords Data module sit three trend and clickstream sub-APIs that answer "is interest rising or falling" and "what is the real (not ad-platform-rounded) search volume." Google Trends is a passthrough of Google's Explore feature; DataForSEO Trends is a proprietary index that blends web content popularity with anonymous user behavior; and Clickstream Data derives volume from anonymized clickstream panels normalized against Bing search volume. Together they complement the ad-network numbers in [[cap-keywords-data-api]] with demand-shape and real-behavior signals.

## What it covers
- **Google Trends Explore** (`/v3/keywords_data/google_trends/explore/live`): relative popularity (0-100) across web, news, youtube, images, froogle; item types `google_trends_graph`, `google_trends_map`, `google_trends_topics_list`, `google_trends_queries_list`. Max 5 keywords (1 for topics/queries).
- **DataForSEO Trends** (`/v3/keywords_data/dataforseo_trends/`): four Live-only endpoints: `explore` (graph over time), `subregion_interests` (geo breakdown), `demography` (age 18-24..55-64 and gender), and `merged_data` (all three combined). Max 5 keywords; no language param (country-based). Combines web content popularity with clickstream behavior across Google Search, News, and Shopping.
- **Clickstream Data** (`/v3/keywords_data/clickstream_data/`): three Live-only endpoints: `dataforseo_search_volume` (clickstream-normalized volume, up to 1,000 keywords), `global_search_volume` (global volume with `country_distribution[]` percentages, no location param), and `bulk_search_volume` (up to 1,000 keywords with ~12 months history).

## Key parameters / inputs
| field | notes |
|---|---|
| keywords | Google Trends max 5; DataForSEO Trends max 5; Clickstream up to 1,000 (min 3 chars) |
| location_* | country-level for DataForSEO Trends; required for clickstream dataforseo_search_volume |
| language_* | Google Trends and clickstream dataforseo_search_volume; not used by DataForSEO Trends |
| type | Google Trends: web/news/youtube/images/froogle; DataForSEO Trends: web/news/ecommerce |
| time_range | presets past_hour..past_5_years (engine-specific) |
| item_types | Google Trends: graph, map, topics_list, queries_list |
| category_code | Google Trends: restrict results to a Google Trends category; default 0 (all categories) |
| use_clickstream | clickstream dataforseo_search_volume; default true |

## Response / what you get back
Google Trends returns `items[]` of typed elements; the graph carries `data[]` with `values` (0-100) and an `averages` field, the map carries `geo_id`/`geo_name`/`values`, and topics/queries lists carry `top` and `rising` arrays. DataForSEO Trends `dataforseo_trends_graph` returns weekly `values` (100 = peak); subregion_interests returns `interests` and `interests_comparison`; demography returns age and gender breakdowns with comparison objects. Clickstream returns `search_volume` and `monthly_searches[]`; global_search_volume adds `country_distribution[]` with `country_iso_code`, per-country `search_volume`, and `percentage`.

## Data lineage
- Google Trends is a passthrough of Google's own Explore feature, so values are Google's relative-popularity index, not raw counts.
- DataForSEO Trends is proprietary: it blends web page and content popularity with anonymous user behavior across Google Search, News, and Shopping, and multi-keyword requests average popularity to the highest value across all keywords.
- Clickstream Data is derived from anonymized clickstream panels, with Bing search volume used as a normalization baseline for supported locations; misspelled keywords auto-correct via Google Ads API validation.

## Cost & method notes
- All charged per request regardless of keyword count. In the cost log: Google Trends Explore $0.009, DataForSEO Trends Explore $0.001, and Clickstream DataForSEO Search Volume $0.15 (the priciest single keyword call in the sample).
- Clickstream global_search_volume cost varies by volume rather than being flat, since it returns a full per-country distribution.
- DataForSEO Trends and Clickstream are Live-only. Google Trends supports Live and Standard. See [[cap-task-vs-live-execution]] and [[cap-queue-priority-cost-model]].

## When to use / how it fits
Use these to add timing and real-volume context to [[play-keyword-research-workflow]]: Google Trends for seasonality and breakout topics, DataForSEO Trends for demographic and subregional targeting, and Clickstream when ad-network "rounded to nearest tens" volume is too coarse. The clickstream panels behind these signals are profiled in [[ent-clickstream-data]] and the sourcing methodology in [[cap-data-collection-methodology]].

## Gotchas / limits
- Google Trends throttles at 250 Live tasks/min and 500K total daily requests across all Trends endpoints; DataForSEO recommends spreading requests over days.
- DataForSEO Trends and Clickstream allow 2000 calls/min and 30 simultaneous requests.
- Google Trends values are relative (0-100), not absolute volume; for absolute real-volume use Clickstream.
- Historical web data starts 2004-01-01; news/ecommerce start 2008-01-01.
- Google Trends rejects special characters in keywords and limits topics/queries item types to a single keyword per request.
- Clickstream global_search_volume takes no location or language param and returns global volume with a per-country breakdown, so use bulk_search_volume when you need a specific location.

## Related
- [[ent-google-ads-keyword-planner]]
- [[cap-keywords-data-api]]
- [[ent-clickstream-data]]
- [[cap-data-collection-methodology]]
- [[cap-labs-keyword-research]]
- [[play-keyword-research-workflow]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-platform-architecture]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/keywords_data/google_trends/explore/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/dataforseo_trends/explore/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/dataforseo_trends/demography/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/clickstream_data/dataforseo_search_volume/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/clickstream_data/global_search_volume/live/ (retrieved 2026-06-26)
