# Market Research - DataForSEO as a programmatic SEO data provider

Captured 2026-06-26 from a multi-source, fact-checked research pass (see
`.raw/sources/dataforseo-research/_research/competitive-market.md`, 35 cited sources).

## Buyer Hypothesis
SEO engineers, agencies, and AI/GEO builders who need a source-cited operating memory of the
DataForSEO API: endpoints, parameters, request lifecycle, costs, and adapters.

## Demand Questions
- Who pays for this workflow? Teams that build SEO tooling or run SEO at scale and want raw data, not a dashboard.
- What raw materials do they already have? API credentials, target domains/keywords, and an engineering stack.
- What output saves time or reduces risk? A reliable endpoint+cost map so they avoid the Live-queue cost footgun and pick the cheapest data tier.
- What would they screenshot in a sales page? The cost-per-1000-SERPs comparison and the which-API router.
- What monthly loop brings them back? Pricing/endpoint drift re-verification and AI-visibility (GEO) tracking.

## Competitive positioning (the market structure)
| Provider | Pricing model | Data sourcing | Best buyer fit |
|---|---|---|---|
| DataForSEO | Pay-as-you-go, per-request/per-result, no seats, $50 min | Own SERP scraper + own backlink crawler + Google/Bing Ads + clickstream | SaaS builders, in-house engineers (cheapest at scale, raw JSON) |
| SerpApi | Pay-as-you-go searches, no rollover | Real-time SERP scraping only (no keyword/backlink DB) | Real-time SERP + legal cover; ~15-40x DFS per-SERP cost |
| Ahrefs | Subscription seat + API units/rows | Largest link index (own AhrefsBot) + clickstream + Keyword Planner | Backlink-led agencies |
| Semrush | Subscription seat + API units | Own crawler + third-party + 200M-device clickstream | All-in-one marketing teams |
| Moz | Bundled with Moz Pro, rows-based | Link Explorer index, DA/PA ML model | Budget DA/PA scoring |

## Evidence Log
| Evidence | Source | Retrieved | Confidence | Notes |
|---|---|---:|---|---|
| DataForSEO SERP cost ~$0.60/$1.20/$2.00 per 1,000 (Standard/Priority/Live) | https://dataforseo.com/pricing | 2026-06-26 | high | live-confirmed ~$0.0020/query |
| DataForSEO is pay-as-you-go with a $50 minimum deposit | https://dataforseo.com/pricing | 2026-06-26 | high | no seats |
| DataForSEO runs its own SERP scraping and backlink crawler infrastructure | https://docs.dataforseo.com/v3/backlinks/overview/ | 2026-06-26 | high | self-sourced index |
| SerpApi offers real-time SERP scraping only, no keyword/backlink database | https://serpapi.com/ | 2026-06-26 | medium | narrower scope |
| Ahrefs gates API access behind subscription + per-row units | https://ahrefs.com/api | 2026-06-26 | medium | seat + units |
| Semrush exposes API on Business plan with unit-based metering | https://www.semrush.com/api-analytics/ | 2026-06-26 | medium | seat + units |
| Keyword volume across all tools derives from Google Ads buckets; tool-to-tool variance 30-200% | https://www.searchenginejournal.com/ | 2026-06-26 | medium | treat as relative |
| DataForSEO has an official 10-module MCP server for agent integration | https://github.com/dataforseo/mcp-server-typescript | 2026-06-26 | high | agent-native |

## Where DataForSEO wins / loses
- Wins: cost at scale, breadth (12 modules), raw structured data, 2000 req/min throughput, no UI tax, agent-native MCP, dedicated AI Optimization (GEO) endpoints.
- Loses: no dashboard (raw JSON requires engineering), default keyword volume is Google-Ads-average unless clickstream-refined, smaller backlink index than Ahrefs/Semrush, the Live-queue cost premium is easy to trigger accidentally.
