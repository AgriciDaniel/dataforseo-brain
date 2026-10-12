---
type: flow
title: "Play: AI Visibility Tracker"
domain: dataforseo
subdomain: ai-optimization
status: stable
created: 2026-09-17
updated: 2026-09-17
tags: [dataforseo, ai-optimization, llm-mentions, cost, retainer]
related:
  - "[[cap-llm-mentions-visibility]]"
  - "[[cap-live-price-table]]"
  - "[[cap-queue-priority-cost-model]]"
---

# Play: AI Visibility Tracker

> Track a client and its competitor set across LLM answers for about **$0.11 a
> run**, using one `multi_target_metrics` call instead of N per-domain calls.
> Sits under [[index|DataForSEO Brain]] -> [[flows/_index|Flows]].

## Overview
`multi_target_metrics` bills **one request per task regardless of target count**.
That single fact turns AI-visibility reporting from a manual audit line item
into a near-zero-COGS recurring deliverable.

## Trigger
Any client who asks "are we showing up in ChatGPT / AI Overviews?", any
competitive pitch, and any retainer that needs a monthly movement number.

## Endpoints used
- `POST /v3/ai_optimization/llm_mentions/multi_target_metrics/live` - the tracker.
- `POST /v3/ai_optimization/llm_mentions/timeseries_delta/live` - period-over-period movement.
- `POST /v3/ai_optimization/llm_mentions/top_mentioned_brands/live` - category share of voice.
- `GET /v3/appendix/user_data` - free spend check.

## Pipeline
1. Build the target set: the client plus 2-9 competitors, `key` labelled by domain.
   Max 10 sets per call, each holding up to 10 entities.
2. Set `location_code` and `language_code` to the client's market. **Do not leave
   the 2840 (US) default in place for a non-US client** - it silently answers the
   wrong question.
3. Post to the bare path, no trailing slash.
4. Read `items[].total.{mentions, ai_search_volume}` per target; the
   `aggregated_metrics.sources_domain` block names which domains the LLM cites.
5. Store the run with its date. The value is the series, not the snapshot.
6. Add `timeseries_delta` once two runs exist.

## Cost & cadence
Verified live 2026-09-17: **5 targets, one call, $0.105.**

| Cadence | Per client / year |
|---|---|
| Weekly | 52 x $0.105 = **$5.46** |
| Monthly | 12 x $0.105 = **$1.26** |

Five separate `target_metrics` calls cost ~$0.505 - **4.8x** more for the same
data. `_lite` variants are the same price, so they save response size, not money.

## Output
A dated table of mentions and AI search volume per domain, plus the citation
source domains. Example, a Canadian law-firm set (`location_code` 2124), 2026-09-17:

| Target | mentions | ai_search_volume |
|---|---|---|
| competitor-d.example | 670 | 167,440 |
| competitor-a.example | 338 | 111,870 |
| competitor-c.example | 99 | 35,860 |
| competitor-b.example | 13 | 1,160 |
| **client.example** | **1** | **70** |

## Pitfalls / limits
- `location_code` defaults to **2840 (US)**. Wrong market = wrong answer, billed.
- 2-10 target sets per call; a larger roster needs a second billed request.
- Live method only, so it counts against the 30-simultaneous-request ceiling.
- `ai_search_volume` is DataForSEO's modelled figure, not a Google-published
  metric. Present it as relative share of voice, not absolute traffic.
- Snapshots are not retained for you - persist each run or the series is lost.

## Decisions in play
- [[dec-google-ads-vs-labs-keyword-volume]]: same principle - pick the endpoint
  that bills once for work you would otherwise pay for N times.

## Related
- [[index]]
- [[flows/_index]]
- [[cap-llm-mentions-visibility]]
- [[cap-live-price-table]]
