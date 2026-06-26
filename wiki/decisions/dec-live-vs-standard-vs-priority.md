---
type: decision
title: "Live vs Standard vs Priority"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, decision, cost, latency]
related:
  - "[[cap-task-vs-live-execution]]"
  - "[[cap-queue-priority-cost-model]]"
  - "[[dec-cost-control-strategy]]"
---

# Live vs Standard vs Priority

> The single biggest cost lever: pay for synchronous Live, or queue Standard at Normal or High priority. Sits under [[index|DataForSEO Brain]] → [[decisions/_index|Decisions]].

## Overview
DataForSEO offers two execution methods and, within Standard, two priority levels. Live is synchronous (results in the same request); Standard is asynchronous (`task_post` → `tasks_ready`/webhook → `task_get`). The choice trades latency for cost and is the dominant variable in any spend model. Mechanics are detailed in [[cap-task-vs-live-execution]] and [[cap-queue-priority-cost-model]].

## The matrix (official Google Organic, base 10 results)
| Mode / Priority | Price per SERP | Per 1M SERPs | Turnaround |
|---|---|---|---|
| Standard, Normal (priority 1) | $0.0006 | $600 | ~5 min |
| Standard, High (priority 2) | $0.0012 | $1,200 | ~1 min |
| Live | $0.002 | $2,000 | ~6 sec |

Net: Live costs ~3.3x Standard-Normal; High priority is ~2x Normal.

## Decision rules
- Need instant/real-time results (per-user lookup, interactive UI) → Live, and pay the premium.
- Scaling large volumes → Standard, ideally High priority: DataForSEO explicitly recommends it because it avoids holding a persistent open connection per request and collects asynchronously. "Large-scale companies working with SERP API usually find the Standard mode with High priority a better fit."
- Planned, non-urgent bulk collection → Standard Normal for the cheapest rate.
- Do NOT engineer concurrency to beat the 30-simultaneous Live cap; prefer the Standard queue "whenever available."

## Mode availability by API
- SERP, Merchant, Business Data support both Live and Standard (with priority options).
- DataForSEO Labs is Live-only.
- OnPage is Standard-based, with cost/speed set by crawl parameters.

## When to use / how it fits
- This decision underpins [[play-rank-tracking-pipeline]], [[play-cost-optimized-pipeline]], and every high-volume flow.
- Combine with webhooks ([[cap-webhooks-pingback-postback]]) so Standard does not require constant polling.
- It is the headline lever inside [[dec-cost-control-strategy]] and a row-level qualifier on [[dec-which-api-for-which-job]].

## Gotchas / limits
- Accidental Live usage is the classic footgun: ~3.3x the Standard-Normal rate for data you did not need in real time.
- Live results are not stored (capture from the response); Standard results are retained 30 days, re-collectable at no extra charge ([[cap-task-vs-live-execution]]).
- Live SERP has a 120-second timeout (set your client timeout to 120s) and a 30-simultaneous-request ceiling on database/Live APIs ([[cap-rate-limits-throughput]]).
- Raising `depth` above the default ~doubles price per extra 100 results, independent of mode.

## Worked sizing
- 10,000 SERPs, not time-critical: Standard Normal ~$6 vs Live ~$20 - prefer Standard.
- 10,000 SERPs needed within the hour: Standard High (~1 min turnaround, ~$12) beats holding 10,000 open Live connections.
- A single per-user lookup in a UI: Live is correct despite the premium, because latency is the product.

## Collection cadence
- Up to ~100,000 tasks/day: Standard + `tasks_ready` polled ~once/minute.
- Above 100,000/day: postback/pingback architecture, which "enables you to work with more than 1000 tasks per minute or 100,000 tasks a day."

## Related
- [[index]]
- [[decisions/_index]]
- [[cap-task-vs-live-execution]]
- [[cap-queue-priority-cost-model]]
- [[cap-webhooks-pingback-postback]]
- [[cap-rate-limits-throughput]]
- [[cap-serp-api]]
- [[dec-cost-control-strategy]]
- [[dec-labs-vs-live-apis]]
- [[dec-which-api-for-which-job]]
- [[play-cost-optimized-pipeline]]

## Sources
- What is the difference between Live and Standard modes? - https://dataforseo.com/help-center/live-vs-standard-method - retrieved 2026-06-26
- serp/overview - https://docs.dataforseo.com/v3/serp-overview/ - retrieved 2026-06-26
- SERP API pricing - https://dataforseo.com/apis/serp-api/pricing - retrieved 2026-06-26
- Best practices for handling live endpoints - https://dataforseo.com/help-center/best-practices-live-endpoints-in-dataforseo-api - retrieved 2026-06-26
