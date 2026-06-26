---
type: meta
title: "DataForSEO Brain - Operator Dashboard"
domain: dataforseo
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, meta, dashboard, health]
---

# DataForSEO Brain - Operator Dashboard

> Coverage, health, and the substance-gate status. Hub: [[index|Master Index]] · [[hot|Hot]].

## Module coverage matrix
Every module has a capability concept note, raw endpoint docs, and (where accessible) a live fixture.

| Module | Concept note | Live-tested 2026-06-26 |
|---|---|---|
| SERP | [[cap-serp-api]], [[cap-serp-google-verticals]], [[cap-serp-non-google-engines]] | yes (organic/maps/bing/youtube/news/images) |
| Keywords Data | [[cap-keywords-data-api]], [[cap-trends-and-clickstream]] | yes (Ads volume, Trends, clickstream) |
| DataForSEO Labs | [[cap-labs-keyword-research]], [[cap-labs-competitor-research]], [[cap-labs-market-analysis]] | yes (20 endpoints) |
| Backlinks | [[cap-backlinks-api]], [[cap-backlinks-bulk-metrics]] | no - needs add-on subscription (40204) |
| OnPage | [[cap-onpage-api]] | yes (instant_pages) |
| Domain Analytics | [[cap-domain-analytics]] | yes (technologies, whois) |
| Content Analysis | [[cap-content-analysis-api]] | yes (search, summary) |
| Merchant | [[cap-merchant-api]] | partial (Shopping is Standard-only) |
| App Data | [[cap-app-data-api]] | documented |
| Business Data | [[cap-business-data-api]] | yes (business listings) |
| AI Optimization | [[cap-ai-optimization-api]], [[cap-llm-mentions-visibility]] | LLM Responses live (4 models); LLM Mentions needs add-on (40204) |
| Databases | [[cap-databases]] | documented (bulk delivery) |

## Cost cheat-sheet (live-observed 2026-06-26)
| Tier | Example | Cost |
|---|---|---|
| Cheapest | OnPage instant_pages | ~$0.0001 |
| Cheap | DataForSEO Labs | ~$0.0011-0.0105 |
| Cheap | SERP Live Advanced (depth 10) | ~$0.0020 |
| Medium | Content Analysis | ~$0.020 |
| Higher | Keywords Data Google Ads ([[ent-google-ads-keyword-planner]]) | ~$0.075 |
| Higher | Whois overview | ~$0.101 |
| Highest tested | Clickstream search volume ([[ent-clickstream-data]]) | ~$0.150 |

Full ledger: `.raw/sources/dataforseo-research/_cost-log.json`. Strategy: [[dec-cost-control-strategy]].

## Substance-gate status (targets the audit enforces)
- Wiki notes: 68 content notes + hubs, every note >= 80 lines and >= 8 wikilinks. Gate: avg >= 80 lines, >= 8 links.
- Research pack: [[research-pack-2026-06-26]] with 104 dated citations. Gate: >= 60.
- Sources ledger: 12 official/vendor sources, refresh_due 2026-07-26. Gate: >= 2 official.

## Navigation
[[concepts/_index]] · [[platforms/_index]] · [[entities/_index]] · [[flows/_index]] · [[decisions/_index]] · [[sources/_index]]

## Refresh
Monthly for endpoint, parameter, and pricing drift; re-verify cost and auth before release.
Most volatile: [[cap-ai-optimization-api]] and SERP feature coverage in [[cap-serp-google-verticals]].
