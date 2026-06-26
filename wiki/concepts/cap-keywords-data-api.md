---
type: concept
title: "Keywords Data API"
domain: dataforseo
subdomain: keywords
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, keywords, search-volume]
related:
  - "[[cap-trends-and-clickstream]]"
  - "[[cap-labs-keyword-research]]"
  - "[[ent-google-ads-keyword-planner]]"
---

# Keywords Data API

> Search volume, CPC, competition, and keyword discovery sourced straight from Google Ads and Bing Ads. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
The Keywords Data API exposes advertiser-grade keyword metrics from the two big ad platforms. The Google Ads sub-API is sourced from the latest Google Ads API, and the Bing sub-API is sourced from Microsoft Advertising. Unlike DataForSEO Labs (which uses DataForSEO's own clickstream-blended database), Keywords Data passes through the ad networks' own numbers, so it is the canonical source for paid-search planning signals: average monthly search volume, top-of-page bids, CPC, and competition. It supports both Live and Standard (Task POST / Tasks Ready / Task GET) methods.

## What it covers
Google Ads (`/v3/keywords_data/google_ads/`):
- **search_volume**: volume, competition, competition_index, CPC, and 12-month `monthly_searches` for up to 1,000 keywords.
- **keywords_for_site**: up to 2,000 keyword suggestions for a domain or page, with `keyword_annotations` concept groups.
- **keywords_for_keywords**: up to 20,000 suggestions from up to 20 seed keywords (max 80 chars each).
- **ad_traffic_by_keywords**: forecast of `average_cpc`, `cost`, and `clicks` for a given `bid` and `match` (exact/broad/phrase). Note `impressions` and `ctr` are deprecated and return null.

Bing Ads (`/v3/keywords_data/bing/`):
- **search_volume** and **search_volume_history** (monthly 24 months, weekly 15 weeks, daily 45 days).
- **keywords_for_site** (max 3,000 returned) and **keywords_for_keywords** (up to 200 seeds, 3,000 suggestions).
- **keyword_performance** (clicks, impressions, average_cpc, ctr by ad_position, previous month).
- **keyword_suggestions_for_url** (confidence_score 0.0-1.0) and **audience_estimation** (reach, est_impressions, suggested_bid using Microsoft/LinkedIn targeting dimensions).

## Key parameters / inputs
| field | notes |
|---|---|
| keywords | array; Google search_volume max 1000, keywords_for_keywords max 20 seeds; Bing up to 1000 |
| target | domain or URL for keywords_for_site / suggestions_for_url |
| location_* / language_* | targeting; Bing languages limited to English, French, German (en/fr/de) |
| bid / match | required for Google ad_traffic_by_keywords (exact/broad/phrase) |
| date_from / date_to | history window; Google 4 years, Bing 24 months |
| search_partners | include Google or Bing/Yahoo/AOL partner networks; default false |
| sort_by | relevance, search_volume, competition_index, bid metrics |

## Response / what you get back
Per-keyword results return `keyword`, `search_volume`, `competition` (Google: LOW/MEDIUM/HIGH; Bing: float 0.1/0.5/0.9), `competition_index` (0-100, Google), `cpc`, `low_top_of_page_bid` and `high_top_of_page_bid` (Google), and `monthly_searches[]` (year, month, search_volume). Google keywords_for_site adds `keyword_annotations`. Bing audience_estimation returns range objects (est_audience_size, est_clicks, est_spend, suggested_bid, suggested_budget).

## Cost & method notes
- Charged per request regardless of keyword count: the price for 1 or 1,000 keywords is the same. In the cost log, Google Ads search_volume and keywords_for_site each cost $0.075; Bing search_volume $0.075.
- Standard queue is cheaper than Live for bulk jobs. See [[cap-task-vs-live-execution]] and [[cap-queue-priority-cost-model]].

## When to use / how it fits
Keywords Data is step one of [[play-keyword-research-workflow]]: pull authoritative volume and bids, then expand and score ideas in [[cap-labs-keyword-research]]. Bing data feeds [[plat-bing-search]]. The Google Ads upstream is profiled in [[ent-google-ads-keyword-planner]]. For when to prefer cheaper pre-indexed Labs data over live ad-network calls, see [[dec-labs-vs-live-apis]] and the router in [[dec-which-api-for-which-job]].

## Gotchas / limits
- Google Ads Live endpoints are throttled to 12 requests per minute per account, far tighter than the platform-wide 2000 calls/min; Bing allows 2000 calls/min.
- Google Ads returns combined volume for groups of similar keywords and may return no data for some groups; certain UTF symbols and emojis are rejected.
- Bing supports only English, French, German on several endpoints; Bing performance data updates after the 3rd of each month.
- Bing `keyword_performance` docs quote both a 1,000 and a 2,500 keyword cap; treat 1,000 as the safe limit until the discrepancy is resolved.
- Google history spans 4 years; Bing spans 24 months.

## Related
- [[ent-clickstream-data]]
- [[cap-trends-and-clickstream]]
- [[cap-labs-keyword-research]]
- [[ent-google-ads-keyword-planner]]
- [[plat-bing-search]]
- [[play-keyword-research-workflow]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-platform-architecture]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/google_ads/ad_traffic_by_keywords/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/bing/search_volume/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/bing/audience_estimation/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/keywords_data/overview/ (retrieved 2026-06-26)
