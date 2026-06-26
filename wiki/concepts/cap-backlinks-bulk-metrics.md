---
type: concept
title: "Backlinks Bulk Metrics (Capability)"
domain: dataforseo
subdomain: backlinks
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, backlinks, bulk]
related:
  - "[[cap-backlinks-api]]"
  - "[[play-backlink-audit]]"
  - "[[dec-cost-control-strategy]]"
  - "[[cap-queue-priority-cost-model]]"
---

# Backlinks Bulk Metrics (Capability)

> The Backlinks bulk endpoints return headline link metrics (rank, spam score, backlink count, referring domains, new/lost, and a full page summary) for up to 1000 targets in a single request, so you can score a whole list of domains in one call instead of one call per target. Sits under [[index|DataForSEO Brain]] -> [[concepts/_index|Concepts]].

## Overview
The bulk family is the cost-efficient sibling of the detailed [[cap-backlinks-api]]. Instead of a deep profile for one target, each bulk endpoint takes a `targets` array (up to 1000 entries) and returns one row of metrics per target. This is the right tool for screening a large prospect list, scoring all competitors at once, or refreshing a dashboard of tracked domains. All endpoints are Live POST calls under `/v3/backlinks/bulk_{metric}/live` and, like the rest of the module, sit behind the paid Backlinks add-on.

## What it covers
- `/v3/backlinks/bulk_ranks/live` - PageRank-style `rank` (0-1000 or 0-100) per target.
- `/v3/backlinks/bulk_spam_score/live` - `spam_score` (0-100) per target.
- `/v3/backlinks/bulk_backlinks/live` - total `backlinks` count per target.
- `/v3/backlinks/bulk_referring_domains/live` - referring domains with nofollow and main-domain breakdowns.
- `/v3/backlinks/bulk_new_lost_backlinks/live` - new and lost backlinks over a time period (up to a 365-day window).
- `/v3/backlinks/bulk_new_lost_referring_domains/live` - new and lost referring domains, with main-domain breakdowns.
- `/v3/backlinks/bulk_pages_summary/live` - a full per-URL metric block (rank, counts, TLDs, link types, platform types, countries) for up to 1000 items but max 100 distinct domains.

## Key parameters / inputs
| field | notes |
|---|---|
| targets | required array; up to 1000 targets per call; domains/subdomains without https://, pages as absolute URLs |
| rank_scale | one_hundred or one_thousand (bulk_ranks, bulk_pages_summary) |
| date_from | yyyy-mm-dd for new/lost endpoints; default 30 days prior; minimum 365 days prior |
| include_subdomains | include subdomains; default true (bulk_pages_summary) |
| tag | user-defined task identifier, max 255 chars |

## Response / what you get back
Each endpoint returns a compact, target-keyed row. `bulk_ranks` returns `target` and `rank`; `bulk_spam_score` returns `type`, `target`, `spam_score`; `bulk_backlinks` returns `target`, `backlinks`, `items_count`. `bulk_referring_domains` adds `referring_domains`, `referring_domains_nofollow`, `referring_main_domains`, `referring_main_domains_nofollow`. The new/lost endpoints return `new_backlinks` / `lost_backlinks` or `new_referring_domains` / `lost_referring_domains` (plus main-domain variants). `bulk_pages_summary` is the richest, returning `url`, `rank`, `main_domain_rank`, `backlinks`, `first_seen`, `lost_date`, `backlinks_spam_score`, `broken_backlinks`, `referring_domains`, `referring_ips`, `referring_subnets`, `referring_links_tld`, `referring_links_types`, `referring_links_platform_types`, and `referring_links_countries`.

## Cost & method notes
- Live/synchronous; the whole module needs the Backlinks add-on. In the cost log, `bulk_ranks` and `bulk_spam_score` returned status 40204 with `cost: 0.0` because the test account lacks the add-on.
- The economic case: one bulk call covers up to 1000 targets, versus 1000 separate per-target calls. At the 2000 calls/min and 30-simultaneous ceiling, bulk keeps you well under rate limits and cuts request count by up to 1000x. See [[cap-queue-priority-cost-model]] and [[dec-cost-control-strategy]].

## When to use / how it fits
Reach for bulk metrics when you have a list and want a score, not a deep profile: prospect screening, competitor scoreboards, and the early "score everything" step of [[play-backlink-audit]] and [[play-competitor-gap-analysis]]. When a single target then needs a deep dive, switch to [[cap-backlinks-api]]. This pattern is a worked example in [[play-cost-optimized-pipeline]]; route jobs via [[dec-which-api-for-which-job]].

A typical sequence is: run `bulk_ranks` and `bulk_spam_score` across the full candidate list to triage, drop low-rank or high-spam targets, then run `bulk_referring_domains` and `bulk_new_lost_referring_domains` on the survivors to judge link velocity. Only the shortlist that clears those gates is worth a per-target `backlinks` pull. The `targets` array accepts a mix of domains, subdomains, and page URLs in one call, so a single request can score competitors and individual landing pages together.

## Gotchas / limits
- The 1000-target cap is per call, but `bulk_pages_summary` additionally caps at 100 distinct domains even when 1000 items are submitted.
- New/lost windows cannot exceed 365 days; the default lookback is 30 days.
- Same add-on gate as the rest of the module: no data without the subscription.
- Metrics are DataForSEO model estimates; benchmark against [[ent-ahrefs]] and [[ent-semrush]] before treating thresholds as absolute.
- `rank_scale` defaults differ from what a dashboard might show; set `one_hundred` or `one_thousand` explicitly so scores are comparable across runs.
- Bulk endpoints return one summary row per target, not the underlying links, so a target flagged by `bulk_spam_score` still needs the per-target `backlinks` endpoint to see which links drive the score.

## Related
- [[cap-backlinks-api]]
- [[cap-data-collection-methodology]]
- [[cap-labs-competitor-research]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[ent-ahrefs]]
- [[ent-semrush]]
- [[play-backlink-audit]]
- [[play-cost-optimized-pipeline]]
- [[dec-cost-control-strategy]]
- [[dec-which-api-for-which-job]]
- [[index]]
- [[concepts/_index]]

## Sources
- https://docs.dataforseo.com/v3/backlinks/bulk_ranks/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/bulk_spam_score/live/ (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/backlinks/bulk_pages_summary/live/ (retrieved 2026-06-26)
