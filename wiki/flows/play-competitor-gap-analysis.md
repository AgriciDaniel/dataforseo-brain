---
type: flow
title: "Play: Competitor Gap Analysis"
domain: dataforseo
subdomain: labs
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, labs, backlinks, competitive]
related:
  - "[[cap-labs-competitor-research]]"
  - "[[cap-backlinks-api]]"
  - "[[dec-labs-vs-live-apis]]"
---

# Play: Competitor Gap Analysis

> Find keyword and link gaps against competitors: Labs domain/keyword intersection, ranked keywords, Backlinks domain intersection, and tech-stack fingerprinting. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
This analysis maps where competitors win and you do not, across two axes: search (which keywords they rank for that you do not) and links (which domains link to them but not to you). It leans on DataForSEO Labs (pre-indexed, cheap) for the keyword side and the Backlinks API for the link gap, with Domain Analytics Technologies adding a stack fingerprint for context.

## Trigger
A team needs a competitive content/link roadmap: a market-entry plan, a quarterly competitor review, or a link-building campaign. Inputs are your domain plus 1-20 competitor domains, with `location_code` and `language_code`.

## Endpoints used (in order)
- `POST /v3/dataforseo_labs/google/competitors_domain/live` (discover SERP competitors).
- `POST /v3/dataforseo_labs/google/ranked_keywords/live` (each domain's keyword footprint).
- `POST /v3/dataforseo_labs/google/domain_intersection/live` (shared-SERP keyword overlap).
- `POST /v3/dataforseo_labs/google/page_intersection/live` (page-level overlap).
- `POST /v3/backlinks/domain_intersection/live` (link gap: who links to them, not you).
- `POST /v3/backlinks/competitors/live` and `POST /v3/domain_analytics/technologies/domain_technologies/live`.

## Pipeline
1. Confirm the competitor set: run `competitors_domain` on your domain to surface the domains that share SERPs with you, then finalize the comparison list.
2. Profile each domain's footprint with `ranked_keywords` (returns the keywords a domain ranks for, with `keyword_data`, `ranked_serp_element`, and aggregate `metrics` position distribution; updates weekly). Set `item_types` to include `organic`, `featured_snippet`, `local_pack`, `ai_overview_reference`.
3. Find keyword gaps with `domain_intersection` (`target1` = competitor, `target2` = you, `intersections: true`): each item gives the shared keyword plus `first_domain_serp_element` and `second_domain_serp_element`, so you see who holds the position. Invert/filter to isolate keywords the competitor ranks for where you are absent or weaker.
4. Localize the gap with `page_intersection` to find the specific competitor pages capturing shared keywords, giving concrete content targets.
5. Find the link gap with Backlinks `domain_intersection`: supply your domain and up to 20 competitors in `targets`, set `exclude_targets` to your own domain (or use `intersection_mode`), and read the referring domains that link to competitors but not you, scored by `rank` and `backlinks_spam_score`. Cross-check with Backlinks `competitors`.
6. Fingerprint the stack with `domain_technologies` (returns the `technologies` object: CMS, frameworks, analytics, CDN, etc.) to understand competitor platforms and migration signals.
7. Synthesize a roadmap: a prioritized keyword-gap list (volume x difficulty x intent) plus a ranked link-prospect list, both tied to the competitor pages that earn them.

## Cost & cadence
- Labs competitive endpoints bill about $0.0105 per request (cost-log: `domain_intersection`, `ranked_keywords`, `competitors_domain`, `serp_competitors`, `relevant_pages` all $0.0105; `domain_rank_overview` $0.0101).
- Backlinks `domain_intersection` is Live-only and billed per request under pay-as-you-go; no Backlinks subscription is required as of 2026-07-01.
- Domain Analytics `domain_technologies` bills about $0.01 per request (cost-log: $0.01); Whois overview is pricier at about $0.101.
- `include_clickstream_data: true` doubles Labs request cost; leave it off for gap work.
- Cadence: full gap analysis quarterly; ranked-keyword refresh monthly (Labs updates weekly).

## Output
A competitive gap pack: keyword-gap table (competitor ranks, you do not), page-level content targets, a link-prospect list (referring domains linking to competitors but not you), and a competitor tech-stack fingerprint.

## Pitfalls / limits
- Labs returns pre-indexed estimates, not live SERPs; for a few high-stakes terms confirm against a live SERP query.
- `domain_intersection` takes exactly two targets (`target1`, `target2`); to compare many competitors, run pairwise or use `competitors_domain` first.
- Backlinks `domain_intersection` allows up to 20 targets and up to 10 `exclude_targets`; mind `intersection_mode` (`all` vs `partial`) which changes what counts as a gap.
- Labs limits: max 1,000 results/page, 8 filters, 3 sort rules, 30 simultaneous requests, 2,000 calls/min.
- Tech detection is best-effort fingerprinting and can miss server-side or obfuscated stacks.

## Decisions in play
- [[dec-labs-vs-live-apis]]: the keyword gap runs entirely on pre-indexed Labs (cheap, slightly stale); confirm only a few high-stakes terms against live SERP.
- [[dec-which-api-for-which-job]]: Labs for the keyword/page gap, Backlinks for the link gap, Domain Analytics for the tech fingerprint.
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]: build-your-own gap analysis on raw data versus a packaged competitor tool; DataForSEO wins on cost at scale and white-labeling.

## Related
- [[cap-labs-competitor-research]]
- [[cap-labs-keyword-research]]
- [[cap-backlinks-api]]
- [[cap-backlinks-bulk-metrics]]
- [[cap-domain-analytics]]
- [[ent-ahrefs]]
- [[ent-semrush]]
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]
- [[dec-which-api-for-which-job]]
- [[dec-labs-vs-live-apis]]
- [[play-backlink-audit]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/domain_intersection/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/domain_analytics/technologies/domain_technologies/live/ (retrieved 2026-06-26)
- https://dataforseo.com/update/pricing-update-in-dataforseo-apis (retrieved 2026-07-08)
