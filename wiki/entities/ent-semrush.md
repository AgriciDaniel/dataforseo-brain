---
type: entity
title: "Semrush (competitor data source)"
domain: dataforseo
subdomain: market
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, competitor, keywords, market]
related:
  - "[[ent-dataforseo]]"
  - "[[dec-dataforseo-vs-ahrefs-semrush-moz]]"
  - "[[ent-ahrefs]]"
---

# Semrush (competitor data source)

> The all-in-one marketing SaaS: own crawler, large keyword/backlink DBs, Business-plan-gated API with per-line units. Sits under [[index|DataForSEO Brain]] → [[entities/_index|Entities]].

## Overview
Semrush is an all-in-one SEO + PPC + content + social platform, evaluated here as a programmatic data source against [[ent-dataforseo]]. It combines its own web crawler (~10 billion pages/day), the Google Ads API, third-party clickstream, and data-aggregator partnerships. Its strength is breadth of finished marketing metrics, white-label reporting, and a wide set of geo databases; like [[ent-ahrefs]] it gates API access behind a paid subscription seat.

## Reported scale & methodology
- Backlink index 43+ trillion; keyword database ~27.9 billion.
- Clickstream panel of ~200 million devices across desktop and mobile.
- Keyword volume blends Google Ads API + own clickstream; an internal 2022 study claimed Semrush volume was closest to Search Console data.
- 142+ geo databases; Google-centric SERP coverage with the Sensor + SERP-features filter.

## API & pricing model
- Standard API requires the Business plan ($499.95/mo) plus purchased units.
- Per-line units: organic keywords ~10 units/line live, ~50 units/line historical; units reset monthly with no rollover.
- The per-line unit counts are the stable, official-aligned figures; the $/unit conversion is inconsistent across sources (one estimate ~$0.00005/unit, another ~$0.01/unit) and should be treated as a range.

## AI-search coverage
- AI Overviews and related AI surfaces are tracked via the AI Visibility Toolkit ($99/mo add-on) and Semrush Sensor.
- Semrush's AIO study found AI Overview incidence oscillating from ~6.5% of keywords (Jan 2025) to ~25% (Jul) before settling ~15% (Nov 2025) - useful context for [[cap-geo-ai-search-optimization]].

## When to use / how it fits
- Best fit for a marketing team needing all-in-one tooling (SEO + PPC + social), white-label, and many geo databases ([[dec-dataforseo-vs-ahrefs-semrush-moz]]).
- The incumbent benchmark for [[cap-keywords-data-api]] and [[play-keyword-research-workflow]].
- DataForSEO undercuts it heavily as a pure data layer; reasons to choose Semrush instead are catalogued in [[dec-when-not-to-use-dataforseo]].

## Gotchas / limits
- Business-plan floor (~$500/mo) plus metered units make it expensive purely for programmatic access.
- Units reset monthly with no rollover (use-it-or-lose-it spend).
- Heavy variant grouping inflates head-term volumes relative to other tools, contributing to the well-known 30%-200% tool-to-tool volume discrepancies.

## As a programmatic source
- The Business-plan gate plus per-line units make Semrush costly for pure API consumption; live keyword lines (~10 units) are cheaper than historical (~50 units).
- Breadth (SEO + PPC + social + content), white-label reporting, and 142+ geo databases are the value, not raw per-call price.

## Practical notes
- The AI Visibility Toolkit and Sensor are add-ons layered on the suite, mirroring how DataForSEO exposes AI surfaces via [[cap-ai-optimization-api]].
- Use Semrush when a team wants finished, multi-channel marketing metrics in one place rather than a raw data feed.

## Coverage notes
- 142+ geo databases give strong international reach; SERP tracking is Google-centric via the Sensor.
- Backlink (43T+) and keyword (~27.9B) indexes are among the largest, a depth advantage over DataForSEO's raw index.
- The clickstream panel (~200M devices) underpins Semrush's claim of Search-Console-close volume.
- Like Ahrefs, its AI-search coverage is a paid add-on layered on the suite rather than a raw API surface.

## Related
- [[index]]
- [[entities/_index]]
- [[ent-dataforseo]]
- [[ent-ahrefs]]
- [[ent-moz]]
- [[ent-google-ads-keyword-planner]]
- [[cap-keywords-data-api]]
- [[cap-geo-ai-search-optimization]]
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]
- [[dec-when-not-to-use-dataforseo]]

## Sources
- Semrush - Data & Metrics (KB 997) - https://www.semrush.com/kb/997-semrush-data - retrieved 2026-06-26
- Semrush - API overview - https://developer.semrush.com/api/introduction/semrush-api-overview/ - retrieved 2026-06-26
- Semrush - API unit balance - https://developer.semrush.com/api/get-started/api-units-balance/ - retrieved 2026-06-26
- Semrush - SEO Toolkit pricing - https://www.semrush.com/pricing/seo/ - retrieved 2026-06-26
- Semrush - AI Overviews study (2025) - https://www.semrush.com/blog/semrush-ai-overviews-study/ - retrieved 2026-06-26
- That Marketing Buddy - Semrush API pricing analysis - https://thatmarketingbuddy.com/blog/semrush-api-pricing - retrieved 2026-06-26
