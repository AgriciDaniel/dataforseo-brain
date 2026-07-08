---
type: meta
title: "DataForSEO Brain - Operator Dashboard"
domain: dataforseo
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, meta, dashboard, health]
---

# DataForSEO Brain - Operator Dashboard

> Coverage, health, and the substance-gate status. Hub: [[index|Master Index]] · [[DataForSEO Brain Home|Brain Home]] · [[hot|Hot]].

## SEOus dashboard route map
The brain is wired to the **SEOus** dashboard. Each tool group maps to capability notes and a playbook;
the machine-readable contract is `references/dashboard-map.json`.

| SEOus route | Module(s) | Capabilities | Status |
|---|---|---|---|
| `/dashboard/serp` | SERP | [[cap-serp-api]], [[cap-serp-google-verticals]], [[cap-serp-non-google-engines]] | live |
| `/dashboard/keyword-overview` | Keywords + Labs | [[cap-keywords-data-api]], [[cap-labs-keyword-research]] | live |
| `/dashboard/backlinks` | Backlinks | [[cap-backlinks-api]], [[cap-backlinks-bulk-metrics]] | pay-as-you-go |
| `/dashboard/on-page` | OnPage + Content + Domain | [[cap-onpage-api]], [[cap-content-analysis-api]], [[cap-domain-analytics]] | live |
| `/dashboard/local-finder` | Business Data | [[cap-business-data-api]] | live |
| `/dashboard/ai-optimization` | AI Optimization | [[cap-ai-optimization-api]], [[cap-llm-mentions-visibility]] | live (Mentions pay-as-you-go) |
| `/dashboard/merchant` | Merchant + App Data | [[cap-merchant-api]], [[cap-app-data-api]] | planned |
| `/dashboard/ledger` | Platform + Databases | [[cap-queue-priority-cost-model]], [[cap-databases]] | planned |
| `/dashboard/autocomplete` | Free (no cost) | [[cap-keywords-data-api]] | planned |

## Module coverage matrix
Every module has a capability concept note, raw endpoint docs, and (where accessible) a live fixture.

| Module | Concept note | Live-tested status |
|---|---|---|
| SERP | [[cap-serp-api]], [[cap-serp-google-verticals]], [[cap-serp-non-google-engines]] | yes (organic/maps/bing/youtube/news/images) |
| Keywords Data | [[cap-keywords-data-api]], [[cap-trends-and-clickstream]] | yes (Ads volume, Trends, clickstream) |
| DataForSEO Labs | [[cap-labs-keyword-research]], [[cap-labs-competitor-research]], [[cap-labs-market-analysis]] | yes (20 endpoints) |
| Backlinks | [[cap-backlinks-api]], [[cap-backlinks-bulk-metrics]] | yes (summary + bulk_ranks re-probed 2026-07-08) |
| OnPage | [[cap-onpage-api]] | yes (instant_pages) |
| Domain Analytics | [[cap-domain-analytics]] | yes (technologies, whois) |
| Content Analysis | [[cap-content-analysis-api]] | yes (search, summary) |
| Merchant | [[cap-merchant-api]] | partial (Shopping is Standard-only) |
| App Data | [[cap-app-data-api]] | documented |
| Business Data | [[cap-business-data-api]] | yes (business listings) |
| AI Optimization | [[cap-ai-optimization-api]], [[cap-llm-mentions-visibility]] | LLM Responses live (4 models); LLM Mentions search live 2026-07-08 |
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

Full ledger: `.raw/sources/dataforseo-research/_cost-log.json`; 2026-07-08 Backlinks and LLM Mentions re-probe ledger: `.raw/sources/dataforseo-research/_cost-log-2026-07-08-reprobe.json`. Strategy: [[dec-cost-control-strategy]].

## Substance-gate status (targets the audit enforces)
- Wiki notes: 68 content notes + hubs, every note >= 80 lines and >= 8 wikilinks. Gate: avg >= 80 lines, >= 8 links.
- Research pack: [[research-pack-2026-06-26]] with 104 dated citations. Gate: >= 60.
- Sources ledger: 13 official/vendor sources, refresh_due 2026-07-26. Gate: >= 2 official.

## Navigation
[[concepts/_index]] · [[platforms/_index]] · [[entities/_index]] · [[flows/_index]] · [[decisions/_index]] · [[sources/_index]]

## Refresh
Monthly for endpoint, parameter, and pricing drift; re-verify cost and auth before release.
Most volatile: [[cap-ai-optimization-api]] and SERP feature coverage in [[cap-serp-google-verticals]].
