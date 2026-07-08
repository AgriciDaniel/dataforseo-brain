---
type: concept
title: "Backlinks API (Capability)"
domain: dataforseo
subdomain: backlinks
status: stable
created: 2026-06-26
updated: 2026-07-08
tags: [dataforseo, backlinks, link-intelligence]
related:
  - "[[cap-backlinks-bulk-metrics]]"
  - "[[cap-labs-competitor-research]]"
  - "[[play-backlink-audit]]"
  - "[[cap-data-collection-methodology]]"
---

# Backlinks API (Capability)

> The Backlinks API serves link intelligence from DataForSEO's own backlink crawler and index: summary metrics, full backlink lists, anchors, referring domains and networks, competitors, intersections, per-page data, and new/lost time series for any domain, subdomain, or URL. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
This module is DataForSEO's answer to Ahrefs and Majestic: a continuously crawled backlink index queried by REST. You pass a `target` (a domain, a subdomain, or a full URL) and get aggregate link metrics, the actual backlinks, anchor-text breakdowns, the referring domains and their IP networks, link gaps against competitors, and the new-versus-lost dynamics over time. Endpoints are Live POST calls under `/v3/backlinks/{function}/live` (the one exception is the free `GET /v3/backlinks/index`). As of 2026-07-01, Backlinks is plain pay-as-you-go with no subscription and no activation step; the 2026-06-26 `40204` gate was removed, and live probes on 2026-07-08 returned `20000 Ok` for `summary/live` and `bulk_ranks/live` with real data. See [[cap-status-error-codes]].

## What it covers
- `GET /v3/backlinks/index` - **free, no charge**; returns the live index volume (backlinks, pages, domains) plus 12-month growth history. The current live index is **~1.96-2.0 trillion live backlinks across ~198-208 billion pages** (the docs' 800.6B backlinks / 80.8B pages / 770.7M domains figure is a stale example snapshot, not the live count). Use it to verify index scale before running paid live pulls.
- `/v3/backlinks/summary/live` - headline counts: backlinks, referring domains, spam score, attribute distributions.
- `/v3/backlinks/history/live` - monthly historical metrics from January 2019 to present; the `new_backlinks` / `lost_backlinks` and new/lost referring-domain fields only populate from May 2021 onward.
- `/v3/backlinks/backlinks/live` - the detailed backlink list with per-link metadata.
- `/v3/backlinks/anchors/live` - anchor-text aggregation with per-anchor metrics.
- `/v3/backlinks/referring_domains/live` and `/v3/backlinks/referring_networks/live` - linking domains and their IP/subnet groupings.
- `/v3/backlinks/competitors/live`, `/v3/backlinks/domain_intersection/live`, `/v3/backlinks/page_intersection/live` - competitor profiles and link-gap analysis.
- `/v3/backlinks/domain_pages/live` and `/v3/backlinks/domain_pages_summary/live` - per-page backlink data for a target.
- `/v3/backlinks/timeseries_summary/live` and `/v3/backlinks/timeseries_new_lost_summary/live` - metrics and new/lost links and domains grouped by interval.

## Key parameters / inputs
| field | notes |
|---|---|
| target | required; a domain, subdomain, or absolute URL |
| mode | as_is / one_per_domain / one_per_anchor grouping (backlinks endpoint) |
| backlinks_status_type | all / live / lost; default live |
| include_subdomains | include subdomains in the search; default true |
| include_indirect_links | include redirects and canonical links; default true |
| exclude_internal_backlinks | drop links from the target's own subdomains; default true |
| internal_list_limit | cap on nested arrays (TLDs, types, attributes); default 10, max 1000 |
| rank_scale | one_hundred or one_thousand; default one_thousand |
| backlinks_filters | `summary` endpoint only - filters the backlinks behind the headline counts; summary has no order_by/limit/offset |
| filters / order_by / limit / offset | list endpoints (`backlinks`, `anchors`, `referring_domains`): max 8 filters, max 3 sort rules, limit up to 1000, offset up to 20000 |

## Response / what you get back
Summary-style responses carry `rank`, `backlinks`, `referring_domains`, `referring_main_domains`, `referring_pages`, `backlinks_spam_score`, and `broken_backlinks`. Distribution objects include `referring_links_tld`, `referring_links_types`, `referring_links_attributes`, and `referring_links_platform_types`. Individual backlinks expose `anchor`, `dofollow`, `first_seen`, and `lost_date` (null while live). Rank is a PageRank-style 0-100 or 0-1000 score depending on `rank_scale`.

**Rank methodology.** Rank is DataForSEO's Domain-Rating analog, built on Google's original PageRank formula but with a **damping factor of 0.5** (vs Google's 0.85). A domain's rank is the log-compressed normalized sum of the PageRanks of its indexed pages, so each higher point needs exponentially more links. Three distinct fields appear: `rank` (the target's own rank, or the rank a backlink passes), `domain_from_rank` (rank of the referring domain), and `page_from_rank` (rank of the referring page). Scale is 0-1000 by default, or 0-100 with `rank_scale: one_hundred` (conversion `sin(rank / 636.62) * 100`).

**Spam score.** `backlinks_spam_score` (group) / `target_spam_score` (domain) is a proprietary 0-100% estimate, not a Google signal, computed from **18 page-level signals** - for example insecure HTTP (+30%), contact info present (-20%), social meta tags present (-15%), plus domain length, TLD reputation, and external/internal link ratios. Bands are **0-30 low, 31-60 medium, 61-100 high**; a group or domain score is the average of its per-page scores.

## Cost & method notes
- Endpoints are Live/synchronous; per-request billing. Since 2026-07-01, Backlinks live endpoints are pay-as-you-go and no separate add-on subscription is required.
- **Access mechanics:** gated through 2026-06-26; removed 2026-07-01 when DataForSEO moved all APIs to pay-as-you-go. Existing Backlinks subscriptions were auto-cancelled and accounts keep access without a monthly minimum. The old Make.com, n8n, and Google Sheets connector waiver is historical and now moot because there is no minimum left to waive; see [[cap-llm-mentions-visibility]] for the parallel LLM Mentions change.
- **Per-call pricing (flat across the pay-as-you-go endpoints):** $0.02 per request + $0.00003 per returned row, max 1,000 rows per request - roughly **$0.05 per 1,000 backlinks** (1 request + 1,000 rows = $0.05). That headline figure undercuts Ahrefs (~$5.00/1k) and Semrush (~$2.00/1k); see [[dec-dataforseo-vs-ahrefs-semrush-moz]].
- In the 2026-06-26 live cost log, `summary`, `referring_domains`, and `anchors` returned task status `40204` with `cost: 0.0`. Re-probed live on 2026-07-08, `/v3/backlinks/summary/live` and `/v3/backlinks/bulk_ranks/live` returned `20000 Ok` with real data; fixtures: `.raw/sources/dataforseo-research/backlinks/fixtures/summary-live.json` and `.raw/sources/dataforseo-research/backlinks/fixtures/bulk_ranks-live.json`.
- The data comes from DataForSEO's own backlink crawler and index, sourced and refreshed independently. See [[cap-data-collection-methodology]] and [[cap-queue-priority-cost-model]].

## When to use / how it fits
This module drives [[play-backlink-audit]] (summary -> referring domains -> new/lost -> bulk spam -> cleanup) and the link side of [[play-competitor-gap-analysis]] (domain/page intersection alongside Labs intersections). For headline metrics across many targets at once, prefer [[cap-backlinks-bulk-metrics]]. Route jobs through [[dec-which-api-for-which-job]] and weigh build-vs-buy against rivals via [[dec-dataforseo-vs-ahrefs-semrush-moz]].

## Gotchas / limits
- **Access status timeline:** gated through 2026-06-26; removed 2026-07-01 when DataForSEO moved all APIs to pay-as-you-go. The earlier 2026-06-26 note that the subscription was NOT removed was accurate then, but became false after the published pricing update. Treat `40204` for Backlinks as historical and legacy; a pay-as-you-go account no longer receives it for Backlinks live endpoints verified 2026-07-08. See [[cap-status-error-codes]].
- No $100/month Backlinks add-on remains; budget for per-request and per-row usage before building on this module.
- 2000 API calls/min, max 30 simultaneous requests; `offset` past 20000 should switch to a search-after token.
- Spam score and rank are model estimates, not Google signals; compare against [[ent-ahrefs]] and [[ent-moz]] metrics rather than treating them as authoritative.
- Historical depth starts January 2019; older link history is not available. The `new_backlinks` / `lost_backlinks` and new/lost referring-domain fields are a narrower window: they only populate from May 2021 onward, so velocity metrics before that date are blank.

## Related
- [[cap-backlinks-bulk-metrics]]
- [[cap-labs-competitor-research]]
- [[cap-data-collection-methodology]]
- [[cap-domain-analytics]]
- [[cap-llm-mentions-visibility]]
- [[cap-status-error-codes]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[ent-ahrefs]]
- [[ent-moz]]
- [[play-backlink-audit]]
- [[play-competitor-gap-analysis]]
- [[dec-which-api-for-which-job]]
- [[dec-dataforseo-vs-ahrefs-semrush-moz]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/backlinks/index/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/summary/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/backlinks/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/referring_domains/live/ (retrieved 2026-06-26)
- https://dataforseo.com/update/pricing-update-in-dataforseo-apis (retrieved 2026-07-08)
- https://dataforseo.com/help-center/backlinks-api-pricing-explained (retrieved 2026-06-26; subscription mechanics superseded by the 2026-07-01 pricing update)
- https://dataforseo.com/pricing/backlinks/backlinks (retrieved 2026-06-26)
- https://app.dataforseo.com/backlinks-subscription (retrieved 2026-06-26)
- https://dataforseo.com/updates (retrieved 2026-06-26 - no Backlinks subscription removal announced)
- https://dataforseo.com/help-center/what_is_rank_in_backlinks_api (retrieved 2026-06-26)
- https://dataforseo.com/help-center/what-is-spam-score-and-how-is-it-calculated (retrieved 2026-06-26)
