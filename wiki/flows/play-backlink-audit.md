---
type: flow
title: "Play: Backlink Audit"
domain: dataforseo
subdomain: backlinks
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, backlinks, audit]
related:
  - "[[cap-backlinks-api]]"
  - "[[cap-backlinks-bulk-metrics]]"
  - "[[dec-which-api-for-which-job]]"
---

# Play: Backlink Audit

> Profile a domain's link graph, find toxic and lost links, and produce a cleanup/outreach list from DataForSEO's own backlink index. Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
This audit reads a target's backlink profile end-to-end: the headline metrics, the referring-domain roster, anchor distribution, link velocity (new vs lost), and spam scoring. All endpoints are Live-only and draw on DataForSEO's proprietary backlink crawler/index, so the numbers are vendor-native rather than Google-sourced. The output is a disavow/cleanup candidate list plus a baseline for ongoing monitoring.

## Trigger
A domain needs a link-health review: a penalty investigation, an M&A due-diligence check, a quarterly health snapshot, or a competitor link comparison. Input is a single `target` (domain, subdomain, or full page URL).

## Endpoints used (in order)
- `POST /v3/backlinks/summary/live` (profile overview).
- `POST /v3/backlinks/referring_domains/live` (the referring-domain roster).
- `POST /v3/backlinks/anchors/live` (anchor-text distribution).
- `POST /v3/backlinks/bulk_new_lost_backlinks/live` (link velocity / churn).
- `POST /v3/backlinks/bulk_spam_score/live` (spam score for up to 1,000 targets).
- `POST /v3/backlinks/history/live` and `/timeseries_summary/live` (trend context).

## Pipeline
1. Run `summary` on the `target`. Read `backlinks`, `referring_domains`, `referring_main_domains`, `rank`, `backlinks_spam_score`, `broken_backlinks`, and the distribution objects (`referring_links_types`, `referring_links_attributes`, `referring_links_tld`, `referring_links_countries`). Set `backlinks_status_type` to `live`, `lost`, or `all` depending on scope.
2. Pull the referring-domain roster with `referring_domains` (default 100, max 1,000 per request; page with `offset`). Sort by `rank` and `backlinks_spam_score`; use `filters` (max 8) to isolate high-spam or nofollow-only domains.
3. Audit anchors with `anchors` to spot over-optimized or spammy anchor patterns (money-keyword stuffing is a manual-action signal).
4. Measure velocity with `bulk_new_lost_backlinks` to see whether the profile is gaining or shedding links; sudden loss spikes flag a problem, sudden gains may flag a negative-SEO attack.
5. Score toxicity: feed the suspect referring domains/pages (up to 1,000 per call) into `bulk_spam_score` to get the 0-100 `spam_score` per target in one billed request.
6. Build the cleanup list: domains/pages above your spam threshold with low `rank` become disavow candidates; broken backlinks pointing at the target become reclamation candidates.
7. Add trend context with `history`/`timeseries_summary` for a month-over-month chart, and re-run on a schedule to monitor.

## Cost & cadence
- Backlinks endpoints are Live-only and billed per request; pricing is on the Backlinks API page (per-row plus per-request components).
- Bulk endpoints are the cost lever: `bulk_spam_score` scores up to 1,000 targets in one billed request rather than 1,000 separate calls. The same applies to bulk ranks and bulk new/lost.
- Since 2026-07-01, the Backlinks API is pay-as-you-go with no subscription or activation step. The `backlinks_subscription_expiry_date` field in `user_data` is legacy and irrelevant for access; 2026-07-08 probes returned `20000 Ok` for `summary/live` and `bulk_ranks/live`.
- Cadence: full audit on demand; monitoring (summary + new/lost) weekly or monthly.

## Output
A backlink audit pack: profile summary metrics, ranked referring-domain table, anchor distribution, new/lost velocity chart, and a prioritized disavow + reclamation list. Feeds [[play-competitor-gap-analysis]] for link-gap work.

## Pitfalls / limits
- No Backlinks API subscription is required. Check `user_data` for balance and limits before running, not for access.
- `include_subdomains`, `include_indirect_links`, and `exclude_internal_backlinks` all default to true and materially change counts; set them deliberately and keep them consistent across runs.
- `rank_scale` defaults to `one_thousand`; switch to `one_hundred` if your reporting expects 0-100.
- Rate ceiling is 2,000 calls/min and max 30 simultaneous Live requests; max 1,000 items per page and 1,000 targets per bulk call.
- Spam score is DataForSEO's own metric, not Google's; treat it as a triage signal, not a verdict.

## Decisions in play
- [[dec-which-api-for-which-job]]: Backlinks API summary/referring_domains/anchors for the profile, bulk endpoints for spam scoring at scale.
- [[dec-cost-control-strategy]]: prefer the bulk endpoints (up to 1,000 targets per billed request) over per-target calls.
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]: DataForSEO's index is its own crawler, so counts differ from Ahrefs/Moz; keep one source of truth per report.

## Related
- [[cap-backlinks-api]]
- [[cap-backlinks-bulk-metrics]]
- [[cap-task-vs-live-execution]]
- [[cap-data-collection-methodology]]
- [[cap-account-usage-userdata]]
- [[ent-ahrefs]]
- [[ent-moz]]
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]
- [[dec-which-api-for-which-job]]
- [[play-competitor-gap-analysis]]
- [[index]]
- [[flows/_index]]

## Sources
- https://docs.dataforseo.com/v3/backlinks/summary/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/referring_domains/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/bulk_spam_score/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/domain_intersection/live/ (retrieved 2026-06-26)
- https://dataforseo.com/update/pricing-update-in-dataforseo-apis (retrieved 2026-07-08)
- .raw/sources/dataforseo-research/backlinks/fixtures/summary-live.json (captured 2026-07-08)
- .raw/sources/dataforseo-research/backlinks/fixtures/bulk_ranks-live.json (captured 2026-07-08)
