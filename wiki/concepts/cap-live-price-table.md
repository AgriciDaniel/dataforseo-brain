---
type: concept
title: "Cap: Live Price Table (account-verified)"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-09-17
updated: 2026-09-17
tags: [dataforseo, cost, pricing, verified]
related:
  - "[[cap-queue-priority-cost-model]]"
  - "[[cap-account-usage-userdata]]"
  - "[[dec-cost-control-strategy]]"
  - "[[play-cost-optimized-pipeline]]"
---

# Cap: Live Price Table (account-verified)

> Exact per-endpoint prices pulled from this account on 2026-09-17, free, via
> `GET /v3/appendix/user_data`. Machine-readable copy:
> `references/live-prices-2026-09-17.json` (1,260 entries, 783 priced).
> Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Why this note exists
Every other cost figure in this brain was observed on 2026-06-26, before the
2026-07-01 pricing update. `user_data` returns the authoritative price list for
**your** account at **zero cost**, so it is the only figure worth trusting.
Re-pull it whenever spend matters; it is free and rate-limited to 6/min.

## What the 2026-07-01 increase actually hit
Verified live 2026-09-17. The rise was ~+20%, but **SERP was not included**:

| Endpoint | 2026-06-26 | 2026-09-17 | Delta |
|---|---|---|---|
| `serp/task_post` (Standard Normal) | $0.0006 | **$0.0006** | unchanged |
| `serp/task_post` (Standard High) | $0.0012 | **$0.0012** | unchanged |
| `serp/live/advanced` | $0.002 | **$0.002** | unchanged |
| `dataforseo_labs/*/live` | ~$0.0101 | **$0.012 + $0.00012/row** | +19% |
| `keywords_data/google_ads/search_volume/live` | $0.075 | **$0.09** | +20% |
| `keywords_data/clickstream_data/*/live` | $0.15 | **$0.18** | +20% |
| `domain_analytics/whois/overview/live` | $0.101 | **$0.12 + $0.0012/row** | +19% |
| `on_page/instant_pages` | $0.000125 | **$0.00015** | +20% |
| `business_data/business_listings/search/live` | $0.0103 | **$0.012 + $0.00036/row** | +17% |
| `backlinks/summary/live` | $0.02 | **$0.024 + $0.000036/row** | +20% |

## The cheapest paths (live figures)
- **SERP tiering is still the biggest single lever.** Standard Normal $0.0006 vs
  Live $0.002 - Live costs **3.33x**. Standard High $0.0012 is the scale
  compromise. Unchanged by the increase, so the old guidance holds exactly.
- **`on_page/instant_pages` at $0.00015 per result is the cheapest real call in
  the catalog** - 80x cheaper than a Live SERP. Use it for any single-page check.
- **Backlinks rows are near-free**: `backlinks/backlinks/live`,
  `bulk_backlinks/live` and `anchors/live` bill **$0.000036 per result**. A
  1,000-row pull is $0.036 plus the $0.024 request. Bulk endpoints take up to
  1,000 targets per billed request.
- **Labs is $0.012 per request plus $0.00012 per row returned** (an earlier version said "flat $0.012
  regardless of rows", which is wrong and invites oversized pulls). 50 rows cost $0.018; 1,000 rows
  cost $0.132. Still the cheapest keyword data under ~600 keywords: `keyword_overview` for 100 keywords
  is $0.024 against `keywords_data/google_ads/search_volume/live` at $0.09 flat. Always set `limit`.
- **`serp/task_get/*` is $0** - collecting a Standard result is free, and results
  are re-collectable for 30 days. Never pay twice for data you already pulled.

## Budget killers - avoid or gate these
| Endpoint | Cost | Note |
|---|---|---|
| `keywords_data/clickstream_data/*/live` | **$0.18/request** | most expensive call in the catalog; 300x a Standard SERP |
| `domain_analytics/whois/overview/live` | $0.12/request + $0.0012/row | also `dataforseo_labs/domain_whois_overview/live` |
| `dataforseo_labs/historical_rank_overview/live` | $0.12/request + $0.0012/row | historical Labs is 10x normal Labs |
| `dataforseo_labs/historical_bulk_traffic_estimation/live` | $0.12/request + $0.0012/row | |
| `ai_optimization/llm_mentions/top_pages/live` | $0.10/request | LLM Mentions family is uniformly pricey |
| `app_data/app_listings/search/live` | $0.10/request + $0.001/row | |
| `serp/ai_summary` | $0.01/result | 16x a Standard SERP; request deliberately |

Setting `include_clickstream_data: true` on a Labs call routes it into the $0.18
clickstream tier. That single boolean is the most expensive flag in the API.

## Gotchas / limits
- Prices are **per account**. This table is this account's; another key may differ.
- `user_data` itself costs $0 and returns `money.balance` and `money.limits` -
  set a daily cost limit so runaway jobs hit 40203 instead of draining balance.
- The JSON sidecar holds all three priority tiers; this note quotes `normal`.

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-queue-priority-cost-model]]
- [[cap-account-usage-userdata]]
- [[play-cost-optimized-pipeline]]
