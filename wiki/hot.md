---
type: hot
title: "DataForSEO Brain - Hot / Current Context"
domain: dataforseo
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, hot, context]
---

# DataForSEO Brain - Hot

> Current operating context for the brain. Most recent at the top. Hub: [[index|Master Index]].

## Currently true (2026-06-26)
- The brain was built and live-verified against the production API on **2026-06-26**. A $5-capped
  test pass spent **$0.86** across **43 endpoints** (incl. LLM Responses for ChatGPT/Claude/Gemini/Perplexity); the ledger is `.raw/sources/dataforseo-research/_cost-log.json`.
- Account access observed: pay-as-you-go credit is active; **Backlinks API** and **AI Optimization
  LLM Mentions** returned `40204` (need an add-on subscription). LLM Responses (ChatGPT/Claude/Gemini/Perplexity) ARE pay-as-you-go accessible and now have live fixtures; only LLM Mentions stays gated. Backlinks + LLM Mentions shapes are documented from the
  docs in [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]].
- The cheapest data tier is **DataForSEO Labs** (~$0.01/call). The biggest avoidable cost is using
  **Live** when **Standard** would do; see [[dec-live-vs-standard-vs-priority]] and [[dec-cost-control-strategy]].

## Recent platform changes (2026)
Newest first. Dates are the official DataForSEO update publication dates (source: https://dataforseo.com/updates, retrieved 2026-06-26).
- **2026-06-10 - Amazon Merchant API gains real-time Live endpoints** (previously task-based only); Live mode for ASIN/products/sellers. See [[cap-merchant-api]].
- **2026-05-28 - LLM Scraper (ChatGPT) returns ad results**, the sponsored placements shown inside ChatGPT responses. See [[cap-ai-optimization-api]].
- **2026-05-05 - DataForSEO API v2 fully closed**; no new v2 requests (task_get had a ~1-month grace window). v3 only.
- **2026-04-27 - OnPage Lighthouse API: seven new browser-simulation parameters** for device/network/browser emulation. See [[cap-onpage-api]].
- **2026-04-21 - OnPage uncrawlable-resources endpoint** plus expanded summary data. See [[cap-onpage-api]].

**Verified 2026-06-26: the Backlinks + LLM Mentions $100/mo subscriptions were NOT removed; still 40204-gated (waived only via Make/n8n/Sheets connectors).** See [[cap-backlinks-api]] and [[cap-llm-mentions-visibility]].

## Start here
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
- Backlinks/LLM-Mentions add-on subscriptions are not on the test account; live fixtures for those are unavailable (documented shapes only).

## Recently added
- 68 content notes across [[concepts/_index|concepts]], [[platforms/_index|platforms]],
  [[entities/_index|entities]], [[flows/_index|flows]], and [[decisions/_index|decisions]].
- Research pack with 104 dated citations: [[research-pack-2026-06-26]].
- 39 authentic live response fixtures under `.raw/sources/dataforseo-research/*/fixtures/`.
