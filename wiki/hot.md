---
type: hot
title: "DataForSEO Brain - Hot / Current Context"
domain: dataforseo
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, hot, context]
---

# DataForSEO Brain - Hot

> Current operating context for the brain. Most recent at the top. Hub: [[index|Master Index]].

## Currently true (2026-07-08)
- **Backlinks API and LLM Mentions API are now 100% pay-as-you-go.** On **2026-07-01** DataForSEO
  cancelled all remaining monthly commitments and dropped the **$100/mo minimums** on both modules;
  there is no subscription and no activation step. Re-verified live **2026-07-08**:
  `/v3/backlinks/summary/live`, `/v3/backlinks/bulk_ranks/live`, and
  `/v3/ai_optimization/llm_mentions/search/live` all now return `20000 Ok` with real data (previously
  `40204`). New fixtures + probe log under `.raw/sources/dataforseo-research/`
  (`_cost-log-2026-07-08-reprobe.json`). See [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]].
- `40204` ("subscription required") is now effectively **legacy** for these two modules; a pay-as-you-go
  account no longer receives it for Backlinks or LLM Mentions.
- The same 2026-07-01 update also **adjusted rates across selected APIs** (a broader repricing). Per-endpoint
  price figures in the brain are due a refresh and should not be treated as exact until re-audited.

## As built and first verified (2026-06-26)
- The brain was built and live-verified against the production API on **2026-06-26**. A $5-capped
  test pass spent **$0.86** across **43 endpoints** (incl. LLM Responses for ChatGPT/Claude/Gemini/Perplexity); the ledger is `.raw/sources/dataforseo-research/_cost-log.json`.
- Account access at build time: pay-as-you-go credit active; **Backlinks API** and **AI Optimization
  LLM Mentions** returned `40204` (then still gated). That gate was **removed 2026-07-01** (see the
  block above); both modules are now directly usable. LLM Responses (ChatGPT/Claude/Gemini/Perplexity)
  were already pay-as-you-go accessible. See [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]].
- The cheapest data tier is **DataForSEO Labs** (~$0.01/call). The biggest avoidable cost is using
  **Live** when **Standard** would do; see [[dec-live-vs-standard-vs-priority]] and [[dec-cost-control-strategy]].

## Recent platform changes (2026)
Newest first. Dates are the official DataForSEO update publication dates (source: https://dataforseo.com/updates, retrieved 2026-06-26; 2026-07-01 entry retrieved 2026-07-08).
- **2026-07-01 - All APIs moved to 100% pay-as-you-go.** The Backlinks + LLM Mentions **$100/mo minimums were cancelled** (existing subscriptions auto-cancelled, access retained), and **rates were adjusted across selected APIs**. See [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]]. Source: https://dataforseo.com/update/pricing-update-in-dataforseo-apis
- **2026-06-10 - Amazon Merchant API gains real-time Live endpoints** (previously task-based only); Live mode for ASIN/products/sellers. See [[cap-merchant-api]].
- **2026-05-28 - LLM Scraper (ChatGPT) returns ad results**, the sponsored placements shown inside ChatGPT responses. See [[cap-ai-optimization-api]].
- **2026-05-05 - DataForSEO API v2 fully closed**; no new v2 requests (task_get had a ~1-month grace window). v3 only.
- **2026-04-27 - OnPage Lighthouse API: seven new browser-simulation parameters** for device/network/browser emulation. See [[cap-onpage-api]].
- **2026-04-21 - OnPage uncrawlable-resources endpoint** plus expanded summary data. See [[cap-onpage-api]].

**Update 2026-07-01: the Backlinks + LLM Mentions $100/mo minimums WERE removed** (both moved to pay-as-you-go). This reverses the 2026-06-26 finding that they were "NOT removed / still 40204-gated"; that was correct on 2026-06-26 and became false on 2026-07-01. Re-verified live 2026-07-08. The old Make/n8n/Sheets connector waiver is now moot (no minimum left to waive). See [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]].

## Start here
- Command center: [[DataForSEO Brain Home]] (hub) and the `DataForSEO Brain Map` canvas (Obsidian vault)
- Router: [[dec-which-api-for-which-job]]
- Orientation: [[overview]]
- Platform shape: [[cap-platform-architecture]]
- Cost model: [[cap-queue-priority-cost-model]] and [[play-cost-optimized-pipeline]]
- Operator status: [[meta/dashboard]]

## Quick links by job
- Rank tracking: [[play-rank-tracking-pipeline]] using [[cap-serp-api]]
- Keyword research: [[play-keyword-research-workflow]] using [[cap-labs-keyword-research]] + [[cap-keywords-data-api]]
- Backlink audit: [[play-backlink-audit]] using [[cap-backlinks-api]]
- Site audit: [[play-technical-site-audit]] using [[cap-onpage-api]]
- Local SEO: [[play-local-seo-tracking]] using [[cap-business-data-api]]
- AI visibility (GEO): [[play-ai-visibility-tracking]] using [[cap-ai-optimization-api]] + [[cap-geo-ai-search-optimization]]
- E-commerce: [[play-ecommerce-product-research]] using [[cap-merchant-api]]

## Open questions / watch list
- AI Optimization (LLM Mentions) coverage is narrower than marketing implies and changes fast; re-verify monthly. See [[cap-ai-optimization-api]].
- Pricing and rate limits drift; the figures in [[cap-queue-priority-cost-model]] and the source-ledger `refresh_due` are set to 2026-07-26.
- Backlinks + LLM Mentions now have **authentic live fixtures** (captured 2026-07-08 after the pay-as-you-go move); the earlier "documented shapes only" caveat no longer applies. Broader per-endpoint repricing from 2026-07-01 is not yet fully re-audited.

## Recently added
- **SEOus dashboard coupling (2026-06-26):** new hub [[DataForSEO Brain Home]] + fan-out
  `DataForSEO Brain Map` canvas (Obsidian vault) + the route contract `references/dashboard-map.json`,
  wiring this brain to the self-hosted **SEOus** dashboard (forked from seo-playground, at `~/Desktop/Seous`).
- 68 content notes across [[concepts/_index|concepts]], [[platforms/_index|platforms]],
  [[entities/_index|entities]], [[flows/_index|flows]], and [[decisions/_index|decisions]].
- Research pack with 104 dated citations: [[research-pack-2026-06-26]].
- 42 authentic live response fixtures under `.raw/sources/dataforseo-research/*/fixtures/` (adds Backlinks summary + bulk_ranks and LLM Mentions search, captured 2026-07-08).
