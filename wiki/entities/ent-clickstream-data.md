---
type: entity
title: "Clickstream data (providers & panels)"
domain: dataforseo
subdomain: keywords
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, keywords, clickstream, data-source]
related:
  - "[[cap-trends-and-clickstream]]"
  - "[[ent-google-ads-keyword-planner]]"
  - "[[ent-dataforseo]]"
---

# Clickstream data (providers & panels)

> The real-user behavior panels behind DataForSEO Trends and clickstream-refined search volume. Sits under [[index|DataForSEO Brain]] → [[entities/_index|Entities]].

## Overview
Clickstream data is anonymized real-user browsing/search behavior collected from device panels (own and partner). DataForSEO uses it as the refinement layer that re-distributes coarse Google Ads volume into per-keyword estimates, and as the signal behind DataForSEO Trends. It is one of the three data pillars behind [[ent-dataforseo]], alongside its own SERP scraping and the Google/Bing Ads keyword feeds from [[ent-google-ads-keyword-planner]].

## What it powers in DataForSEO
- The clickstream-refined "DataForSEO Search Volume": Google Ads SV is grouped per bucket, then re-distributed using clickstream event counts (or Bing Ads SV) - exposed via the `use_clickstream` / `include_clickstream_data` parameters.
- DataForSEO Trends and the Clickstream Data API endpoints ([[cap-trends-and-clickstream]]).
- Clickstream-derived enrichment fields on Labs keyword endpoints: `clickstream_keyword_info` (search volume, `gender_distribution`, `age_distribution`, `monthly_searches`) and `keyword_info_normalized_with_clickstream`.

## Observed cost signal (this brain's runs)
- `/v3/keywords_data/clickstream_data/dataforseo_search_volume/live` cost $0.15 for one result in the brain's own cost log - by far the priciest single keyword call recorded, versus $0.001 for a `dataforseo_trends/explore` call.
- Setting `include_clickstream_data: true` on Labs endpoints multiplies request cost by 2.
- This is why clickstream refinement is an opt-in, deliberate choice rather than a default - see [[dec-cost-control-strategy]].

## How the panels compare across vendors
- DataForSEO uses its own plus partner panels; [[ent-ahrefs]] leans on third-party clickstream panels; [[ent-semrush]] runs a panel of ~200 million devices; [[ent-moz]] uses clickstream-adjusted ranges.
- Because clickstream panels are samples, not censuses, no provider is "correct" in absolute terms - figures are best used as relative indicators.

## When to use / how it fits
- Opt into clickstream refinement when per-keyword granularity matters more than the ~2x cost, e.g. prioritization steps in [[play-keyword-research-workflow]].
- Choosing raw Google Ads vs Bing-normalized vs clickstream-refined volume is part of [[dec-which-api-for-which-job]].

## Gotchas / limits
- Doubled cost on clickstream-enabled requests; budget for it explicitly.
- Demographic splits (gender/age distributions) are estimates derived from the panel, not census data.
- Panel composition differs per vendor, so clickstream-refined numbers are not directly comparable across tools.

## Fields it surfaces
- `clickstream_keyword_info`: clickstream `search_volume`, `last_updated_time`, plus `gender_distribution` and `age_distribution` (18-24 through 55-64 buckets) and `monthly_searches`.
- `keyword_info_normalized_with_clickstream`: a clickstream-normalized search volume with an `is_normalized` flag and monthly rates.
- These sit alongside the Bing-normalized object so you can compare refinement models per keyword.

## Why it is the priciest signal
- Clickstream processing is compute- and panel-data-heavy, which is why the dedicated endpoint cost $0.15 per result in the brain's runs and why Labs clickstream doubles request cost.
- Reserve it for prioritization steps where per-keyword precision changes the decision, not for broad discovery.

## Providers behind the panels
- DataForSEO blends its own panels with partner panels; exact partner identities are not publicly itemized.
- Demographic and monthly-rate fields are modeled from the panel sample, so treat them as estimates.

## How to request it
- Labs endpoints: set `include_clickstream_data: true` (doubles request cost).
- Keywords Data: use the Clickstream Data API endpoints, or the `use_clickstream` path for DataForSEO Search Volume.

## Related
- [[index]]
- [[entities/_index]]
- [[ent-dataforseo]]
- [[ent-google-ads-keyword-planner]]
- [[ent-semrush]]
- [[ent-ahrefs]]
- [[cap-trends-and-clickstream]]
- [[cap-keywords-data-api]]
- [[cap-labs-keyword-research]]
- [[dec-cost-control-strategy]]

## Sources
- DataForSEO - Clickstream Data API - https://dataforseo.com/apis/clickstream-data-api - retrieved 2026-06-26
- DataForSEO - Search Volume precision methodology - https://dataforseo.com/blog/dataforseo-search-volume-precision-in-our-apis - retrieved 2026-06-26
- DataForSEO Labs - Google overview (clickstream double-charge) - https://docs.dataforseo.com/v3/dataforseo_labs-google-overview/ - retrieved 2026-06-26
- BloggersPassion - Where does Semrush get its data (2026) - https://bloggerspassion.com/semrush-data-sources/ - retrieved 2026-06-26
- Practical Ecommerce - Keyword Volume: Google vs Semrush vs Ahrefs - https://www.practicalecommerce.com/keyword-volume-google-vs-semrush-vs-ahrefs - retrieved 2026-06-26
