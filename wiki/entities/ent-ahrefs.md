---
type: entity
title: "Ahrefs (competitor data source)"
domain: dataforseo
subdomain: market
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, competitor, backlinks, market]
related:
  - "[[ent-dataforseo]]"
  - "[[dec-dataforseo-vs-ahrefs-semrush-moz]]"
  - "[[ent-semrush]]"
---

# Ahrefs (competitor data source)

> The backlink-led incumbent: largest link index, subscription-plus-units API, strong analyst UI. Sits under [[index|DataForSEO Brain]] → [[entities/_index|Entities]].

## Overview
Ahrefs is an all-in-one SEO suite evaluated here strictly as a programmatic data source competing with [[ent-dataforseo]]. It runs three data pipelines: its own crawler AhrefsBot (the second-most-active crawler after Googlebot, ~5 million pages/minute, ~6B pages/day), third-party clickstream panels, and Google Keyword Planner for keyword volume. Its differentiator is link-index depth and a trusted analyst dashboard, both of which DataForSEO does not try to match directly.

## Reported scale (official "Big Data")
- 35 trillion live backlinks, refreshed every 15-30 minutes.
- ~28.7 billion keywords; ~500.4 million referring domains; ~20.1 billion content pages; 217 locations.
- Runs on in-house hardware: ~662,000 CPU cores, 3 PB RAM, 504 PB SSD.
- Link-count methodology is documented officially (how Ahrefs counts links).

## API & pricing model
- Revamped API v3 (late 2025): plans from ~$500/mo to ~$10,000/mo, typically on top of a paid subscription seat.
- Unit model: base 50 units/request + per-row cost (1 unit/row standard, up to 5-10 for high-value fields); Standard plan ~150,000 units/mo; overage ~$0.35-$1.00 per 1,000 rows.
- Practitioner estimate of combined entry: ~$949/mo (Advanced subscription $449 + API). Treat the exact API floor as approximate (secondary aggregator sourced).
- Rate limit reported at ~60 requests/minute, versus DataForSEO's 2,000/minute.

## Keyword volume & AI coverage
- Search Volume leans on clickstream + own smoothing, then blends Keyword Planner. Ahrefs' own study found its volume "roughly accurate" for ~60% of tested keywords vs Search Console impressions, vs ~45% for Google Keyword Planner.
- Google-centric SERP coverage. AI Overviews / AI Mode / ChatGPT / Perplexity / Copilot / Gemini are tracked via the Brand Radar add-on (~243M prompts) at $199-$699/mo, a premium layer rather than raw API SERP scrapes.

## When to use / how it fits
- Best fit for agencies with backlink-led deliverables that need the largest, most-trusted link index and a strong UI for analysts ([[dec-dataforseo-vs-ahrefs-semrush-moz]]).
- Relevant to [[play-backlink-audit]] and [[play-competitor-gap-analysis]] as the incumbent benchmark against [[cap-backlinks-api]].
- DataForSEO wins on cost-per-request and breadth; Ahrefs wins on link depth and finished metrics - see [[dec-when-not-to-use-dataforseo]].

## Gotchas / limits
- Subscription seat plus metered units make Ahrefs costly as a pure programmatic data source.
- Lower rate limit (~60 req/min) constrains high-throughput pipelines vs DataForSEO.
- AI-search visibility sits behind paid add-ons, not the base API.

## As a programmatic source
- API v3 returns rows you pay for per request plus per row; high-value fields cost more units, so naive bulk pulls get expensive fast.
- The trusted link index and analyst UI are the product; raw cost-per-row is not where Ahrefs competes.

## Practical notes
- Brand Radar (AI-visibility) and the core API are separately priced add-ons on top of a subscription seat.
- For backlink-led deliverables where index depth is the headline, Ahrefs remains the benchmark this brain measures DataForSEO against ([[cap-backlinks-api]]).

## Coverage notes
- Google-centric SERP coverage; AI-search visibility is a Brand Radar add-on, not the base API.
- AhrefsBot is the second-most-active crawler after Googlebot, underpinning the index-freshness claim (links refreshed every 15-30 minutes).
- ~217 locations and in-house hardware (~662,000 CPU cores) support the scale figures.

## Related
- [[index]]
- [[entities/_index]]
- [[ent-dataforseo]]
- [[ent-semrush]]
- [[ent-moz]]
- [[ent-google-ads-keyword-planner]]
- [[cap-backlinks-api]]
- [[cap-data-collection-methodology]]
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]
- [[dec-when-not-to-use-dataforseo]]

## Sources
- Ahrefs - Big Data (official index figures) - https://ahrefs.com/big-data - retrieved 2026-06-26
- Ahrefs - About API v3 (units/rows model) - https://help.ahrefs.com/en/articles/6559232-about-api-v3 - retrieved 2026-06-26
- Ahrefs - Plans & Pricing - https://ahrefs.com/pricing - retrieved 2026-06-26
- Ahrefs - How accurate is keyword search volume - https://help.ahrefs.com/en/articles/72571-how-accurate-is-keyword-search-volume-in-ahrefs - retrieved 2026-06-26
- Ahrefs - How Ahrefs counts links - https://ahrefs.com/blog/how-ahrefs-counts-links/ - retrieved 2026-06-26
- SE Ranking - Ahrefs API alternatives - https://seranking.com/blog/ahrefs-api-alternatives/ - retrieved 2026-06-26
