---
type: overview
title: "DataForSEO Brain - Overview"
domain: dataforseo
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, overview, orientation]
---

# DataForSEO Brain - Overview

> What DataForSEO is, how it is shaped, and how to navigate this brain. Live-verified against the
> production API on 2026-06-26 (a $5-capped test pass spending $0.85 across 39 endpoints).

## What DataForSEO is
DataForSEO is a **raw SEO-data API provider**, not a dashboard. You send REST requests and get back
structured JSON: SERPs, keyword metrics, backlinks, on-page audits, e-commerce data, business data,
and AI-answer visibility. It is sold **pay-as-you-go** (a $50 minimum deposit, no seats), which is the
structural difference from seat-and-subscription tools like [[ent-ahrefs|Ahrefs]] and [[ent-semrush|Semrush]]. See
[[ent-dataforseo|the vendor entity]] and [[dec-dataforseo-vs-ahrefs-semrush-moz|the competitive decision]].

## The platform in one screen
The API is `https://api.dataforseo.com/v3/{module}/{function}`. Every response carries a `cost`, a
`status_code`, and a `tasks[]` array. The shape is documented in [[cap-platform-architecture]].

The **12 modules**:
- [[cap-serp-api|SERP API]] - Google + Bing + YouTube + Baidu + Yahoo + Seznam + Naver results.
- [[cap-keywords-data-api|Keywords Data API]] - search volume, keyword ideas, ad traffic.
- [[cap-labs-keyword-research|DataForSEO Labs]] - pre-indexed keyword, competitor, and market data.
- [[cap-backlinks-api|Backlinks API]] - link profiles from DataForSEO's own crawler.
- [[cap-onpage-api|OnPage API]] - crawler + technical SEO audit + Lighthouse.
- [[cap-domain-analytics|Domain Analytics]] - technology detection + WHOIS.
- [[cap-content-analysis-api|Content Analysis]] - citation search + sentiment.
- [[cap-merchant-api|Merchant API]] - Amazon + Google Shopping.
- [[cap-app-data-api|App Data API]] - Google Play + Apple App Store.
- [[cap-business-data-api|Business Data API]] - Google Business, reviews, listings.
- [[cap-ai-optimization-api|AI Optimization API]] - LLM responses, scrapers, and brand mentions in AI answers.
- [[cap-databases|Databases]] - bulk pre-indexed data delivery.

## The two execution models
Most endpoints offer two ways to run, and choosing wrong is the main cost mistake:
- **Standard (task-based):** `task_post` → poll `tasks_ready` → fetch `task_get`. Cheapest; async.
- **Live:** one synchronous call. Convenient but priced higher. The full lifecycle is in
  [[cap-task-vs-live-execution]]; the cost trade is in [[dec-live-vs-standard-vs-priority]].

DataForSEO **Labs** and **Databases** are pre-indexed and cheaper still when you don't need
last-24h freshness - covered in [[dec-labs-vs-live-apis]].

## The cost mental model
Billing is per-result or per-request, with priority levels and a `cost` field on every response.
The levers (Standard vs Live, bulk endpoints, Labs vs live, the free [[cap-sandbox-testing|sandbox]],
[[cap-webhooks-pingback-postback|webhooks]] over polling, depth tuning) are collected in
[[dec-cost-control-strategy]] and the [[play-cost-optimized-pipeline|cost-optimized pipeline]].
Throughput limits (2000 calls/min, 30 simultaneous) are in [[cap-rate-limits-throughput]].

## Who it is for (and who it isn't)
Best for SaaS builders and in-house engineers who want raw data at scale and will write code.
Less suitable when you need a UI, have tiny volume, or lack engineering - see
[[dec-when-not-to-use-dataforseo]]. Agents can reach it through the official
[[cap-mcp-server-integration|MCP server]] or [[dec-mcp-vs-raw-rest|raw REST]].

## The SEOus dashboard
DataForSEO ships no UI of its own, so this brain is paired with **SEOus** — a minimalistic,
self-hosted dashboard (Next.js + local SQLite cache) that turns the modules above into clickable
tools, governed by a cost-control spine (Standard-vs-Live, Labs-first, result caching, a live cost
ledger). The brain is its knowledge layer: the hub [[DataForSEO Brain Home]] groups every capability
into the eight SEOus tool groups, the `DataForSEO Brain Map` canvas (Obsidian vault) draws the
fan-out, and `references/dashboard-map.json` is the route ↔ capability ↔ playbook contract both sides
read. Backlinks and LLM Mentions appear as graceful "subscription required" tools until their add-ons
are activated.

## How to navigate this brain
- Start with the router: [[dec-which-api-for-which-job]].
- Command center: [[DataForSEO Brain Home]] (hub) and the `DataForSEO Brain Map` canvas (Obsidian vault).
- Mechanics live in [[concepts/_index|Concepts]]; surfaces in [[platforms/_index|Platforms]];
  competitors and sources in [[entities/_index|Entities]].
- End-to-end recipes are in [[flows/_index|Flows]]; the judgment calls in [[decisions/_index|Decisions]].
- Every claim traces to [[research-pack-2026-06-26|the research pack]] (104 dated citations).
- Operator status: [[meta/dashboard|Dashboard]] · [[hot|Hot]].

## Sources
- DataForSEO API v3 documentation - https://docs.dataforseo.com/v3/ - retrieved 2026-06-26
- DataForSEO pricing - https://dataforseo.com/pricing - retrieved 2026-06-26
