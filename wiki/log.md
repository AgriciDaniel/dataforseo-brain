---
type: log
title: "DataForSEO Brain - Build & Change Log"
domain: dataforseo
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, log, changelog]
---

# DataForSEO Brain - Build & Change Log

> Append-only; newest on top. Hub: [[index|Master Index]].

## 2026-07-08 - Backlinks + LLM Mentions pay-as-you-go correction
Corrected the cross-cutting brain state after DataForSEO's 2026-07-01 pricing update moved all endpoints to pay-as-you-go and cancelled the Backlinks and LLM Mentions monthly commitments.

- **Access correction:** Backlinks and LLM Mentions were gated through 2026-06-26, but the gate was removed 2026-07-01. Live re-probe on 2026-07-08 returned `20000 Ok` for `/v3/backlinks/summary/live`, `/v3/backlinks/bulk_ranks/live`, and `/v3/ai_optimization/llm_mentions/search/live`.
- **40204:** kept in [[cap-status-error-codes]] as a defined code, reframed as legacy for these modules.
- **Evidence:** official pricing update plus fixtures under `.raw/sources/dataforseo-research/` and `_cost-log-2026-07-08-reprobe.json`.

## 2026-06-26 - Mega review + gap-fill (v1.0.1)
A full review pass: an ultracode 7-reviewer Workflow + 4 deep-dives (currency, Backlinks, AI Optimization) + a claude-obsidian wiki-lint.

- **Findings:** 37 (0 blockers, 4 HIGH). All applied. Verdict: brain was already solid; fixes were narrow.
- **HIGH fixes:** radius meters -> km in [[cap-business-data-api]]; MCP 2.9.9 / Node >=20 in [[cap-mcp-server-integration]]; Apple depth 100/700/per-100 in [[cap-app-data-api]]; added AI Summary + Screenshot to [[cap-serp-api]].
- **Enrichment:** Backlinks subscription + ~2T index + rank/spam in [[cap-backlinks-api]]; live `/models` truth + LLM Mentions $100/mo gate in [[cap-ai-optimization-api]] and [[cap-llm-mentions-visibility]]; API v2 closure (2026-05-05) in [[cap-task-vs-live-execution]].
- **New live data:** LLM Responses fixtures for all 4 model providers. Em dashes removed vault-wide.
- **Re-verified:** Brainstein SSS+ 100/100 held; wiki-lint 0 critical/0 warnings; 0 dead links.

## 2026-06-26 - Initial build to market-ready
Built the brain as an orchestrated run: a watcher thread plus parallel secretaries.

- **Scrape:** 6 parallel WebFetch secretaries captured 185 endpoint docs across all 12 modules
  into `.raw/sources/dataforseo-research/`, with per-module citation manifests (226 unique doc URLs).
- **Live test:** a $5-capped harness tested 39 endpoints against the production API for $0.85,
  capturing authentic response fixtures. Backlinks and LLM Mentions returned 40204 (add-on required).
  See [[cap-queue-priority-cost-model]] and `_cost-log.json`.
- **Research:** four fact-checked reports (competitive/market, AI-GEO practice, cost-and-lifecycle,
  MCP-and-integration) with ~86 trustworthy external sources, feeding
  [[dec-dataforseo-vs-ahrefs-semrush-moz]], [[cap-geo-ai-search-optimization]], and [[dec-cost-control-strategy]].
- **Synthesis:** 68 content notes across [[concepts/_index|concepts]], [[platforms/_index|platforms]],
  [[entities/_index|entities]], [[flows/_index|flows]], and [[decisions/_index|decisions]],
  every note >= 80 lines and >= 8 wikilinks, every claim traced to [[research-pack-2026-06-26|the research pack]].
- **Cost model captured:** cheapest is OnPage instant_pages (~$0.0001) and Labs (~$0.01); the main
  cost lever is [[dec-live-vs-standard-vs-priority|Live vs Standard]].

Entry point: [[index]] · [[overview]] · [[hot]] · [[meta/dashboard]].
