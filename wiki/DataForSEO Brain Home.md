---
type: meta
title: "DataForSEO Brain Home"
domain: dataforseo
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, moc, home]
---

# 🧠 DataForSEO Brain - Home

Your command center for the **DataForSEO v3 API** - 12 modules, ~200+ endpoints, the task/live queue
model, and the per-call cost model - wired to **SEOus**, a minimalistic self-hosted dashboard.
Live-verified 2026-06-26. Full catalog: [[index]] · the eight capability groups below map 1:1 to the SEOus dashboard sidebar (run SEOus locally; the route contract is `references/dashboard-map.json`).

## 🔎 Search & SERP - 4 capabilities · 1 playbook
- [[cap-serp-api]] - live + queued SERPs across seven engines; the spine of rank tracking
- [[cap-serp-google-verticals]] - AI Overview, Maps, News, Images, Jobs, Shopping verticals
- [[cap-serp-non-google-engines]] - Bing, YouTube, Baidu, Yahoo, Seznam, Naver
- [[cap-result-tiers-regular-advanced-html]] - regular vs advanced vs html result depth
- Surfaces: [[plat-google-search]] · [[plat-bing-search]] · [[plat-youtube]] · [[plat-other-search-engines]]
- Playbook: [[play-rank-tracking-pipeline]]  ·  Decision: [[dec-live-vs-standard-vs-priority]]

## 🧮 Keywords, Competitors & Research - 5 capabilities · 3 playbooks
- [[cap-keywords-data-api]] - search volume, keyword ideas, ad-traffic metrics
- [[cap-trends-and-clickstream]] - Google Trends plus clickstream-blended volume
- [[cap-labs-keyword-research]] - pre-indexed keyword ideas and difficulty (cheapest tier)
- [[cap-labs-competitor-research]] - competitor and ranked-keyword intelligence
- [[cap-labs-market-analysis]] - market and category share analysis
- Playbooks: [[play-keyword-research-workflow]] · [[play-competitor-gap-analysis]] · [[play-content-strategy-brief]]
- Decision: [[dec-labs-vs-live-apis]]

## 🔗 Links & Authority - 2 capabilities · 1 playbook
- [[cap-backlinks-api]] - link profiles from DataForSEO's own crawler *(add-on gated - 40204)*
- [[cap-backlinks-bulk-metrics]] - bulk rank, referring-domain, and spam metrics
- Playbook: [[play-backlink-audit]]

## 🛠️ Technical & On-Page - 3 capabilities · 1 playbook
- [[cap-onpage-api]] - crawler, technical audit, and Lighthouse browser simulation
- [[cap-content-analysis-api]] - citation search plus sentiment summary
- [[cap-domain-analytics]] - technology detection and WHOIS
- Playbook: [[play-technical-site-audit]]

## 📍 Local & Maps - 1 capability · 1 playbook
- [[cap-business-data-api]] - Google Business, reviews, listings, and geo-grid tracking
- Surfaces: [[plat-google-maps-local]] · [[plat-review-platforms]]
- Playbook: [[play-local-seo-tracking]]

## 🤖 AI / GEO visibility - 3 capabilities · 1 playbook
- [[cap-ai-optimization-api]] - LLM responses, LLM scraper, and AI keyword data
- [[cap-llm-mentions-visibility]] - share-of-voice across AI answers *(add-on gated - 40204)*
- [[cap-geo-ai-search-optimization]] - the GEO / answer-engine optimization surface
- Surface: [[plat-ai-assistants]]  ·  Playbook: [[play-ai-visibility-tracking]]

## 🛒 E-commerce & Apps - 2 capabilities · 1 playbook
- [[cap-merchant-api]] - Amazon plus Google Shopping product and seller data
- [[cap-app-data-api]] - Google Play and Apple App Store listings and reviews
- Surfaces: [[plat-amazon-marketplace]] · [[plat-google-shopping]] · [[plat-app-stores]]
- Playbook: [[play-ecommerce-product-research]]

## 💵 Cost & Platform mechanics - 13 capabilities · 1 playbook · 5 decisions
- [[cap-platform-architecture]] · [[cap-task-vs-live-execution]] · [[cap-queue-priority-cost-model]] · [[cap-rate-limits-throughput]]
- [[cap-status-error-codes]] · [[cap-authentication-security]] · [[cap-sandbox-testing]] · [[cap-webhooks-pingback-postback]]
- [[cap-locations-languages-targeting]] · [[cap-account-usage-userdata]] · [[cap-data-collection-methodology]] · [[cap-databases]] · [[cap-mcp-server-integration]]
- Router: [[dec-which-api-for-which-job]]  ·  Cost: [[dec-cost-control-strategy]]  ·  Pipeline: [[play-cost-optimized-pipeline]]
- More decisions: [[dec-mcp-vs-raw-rest]] · [[dec-when-not-to-use-dataforseo]] · [[dec-dataforseo-vs-ahrefs-semrush-moz]]

---

The eight groups above map one-to-one onto the SEOus sidebar; the route ↔ capability ↔ playbook
contract lives in `references/dashboard-map.json`. The same fan-out is drawn as the [brain relationship map](_attachments/brain-relationship-map.svg) on the site, and as the `DataForSEO Brain Map` canvas in the Obsidian vault.

See [[overview]] · [[index]] · [[dashboard|Operator Dashboard]] · [[hot|Hot / current context]]
