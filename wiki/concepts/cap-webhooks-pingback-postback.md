---
type: concept
title: "Webhooks: Pingback, Postback & Resend"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, webhooks]
related:
 - "[[cap-task-vs-live-execution]]"
 - "[[cap-platform-architecture]]"
 - "[[cap-rate-limits-throughput]]"
---

# Webhooks: Pingback, Postback & Resend

> Push task completion to your server instead of polling: pingback sends a GET notification, postback POSTs gzip-compressed results, and the Webhook Resend endpoint recovers missed deliveries. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
For the Standard (task-based) method, you would otherwise poll `tasks_ready` then `task_get`. Webhooks remove that polling: register a `pingback_url` (a completion ping) or `postback_url` (the actual results pushed to you). This "eliminates constant polling of the Tasks Ready endpoint, reducing API calls and associated costs" and is the recommended pattern above ~100,000 tasks/day. A Resend endpoint recovers deliveries your server missed.

## What it covers
- Pingback (callback/notification): set `pingback_url`; on completion DataForSEO sends a GET to that URL. A file is created on your server with the completed task ID(s) and your `tag`.
- Postback (webhook/HTTP push): set `postback_url`; on completion DataForSEO sends a POST with results "compressed in the gzip format." `postback_data` is required and sets the datatype returned ("advanced", "html", and for some APIs "regular").
- `$id` and `$tag` URL variables: `?id=$id` substitutes the completed task id; `&tag=$tag` substitutes the `tag` field for your own routing.
- Webhook Resend endpoint: `POST https://api.dataforseo.com/v3/appendix/webhook_resend`.

## Key parameters / inputs
- `pingback_url`, `postback_url` (both support `$id` and `$tag`).
- `postback_data`: datatype to return ("advanced"/"html"/"regular").
- `tag`: arbitrary label carried into `$tag` for routing/labeling.
- Webhook Resend body: array of task objects, each with `id` (string UUID), up to 100 IDs per call.

## Response / what you get back
- Pingback: only the task ID(s) and `tag` - you then call `task_get` to fetch results.
- Postback: full gzip-compressed result payload delivered to your endpoint.
- Resend: re-delivers pingbacks/postbacks for up to 100 specified tasks.

## Cost & method notes
Webhooks themselves add no charge and cut billable polling calls. The Webhook Resend endpoint carries zero charge, and "Your account will not be double-charged for resending a webhook." Pingback (ID only) is the lightest; postback delivers full results in one push. Pairs with [[cap-task-vs-live-execution]] and the cost model in [[cap-queue-priority-cost-model]].

## When to use / how it fits
Use for any scaled Standard pipeline: official guidance says pingbacks/postbacks "enable you to work with more than 1000 tasks per minute or 100,000 tasks a day." Core to [[play-rank-tracking-pipeline]] and [[play-cost-optimized-pipeline]], and a key lever in [[dec-cost-control-strategy]] and [[dec-live-vs-standard-vs-priority]].

## Gotchas / limits
- Webhooks apply to the Standard method (Live returns results inline, so no callback).
- Whitelist DataForSEO's sending IPs (e.g. 144.76.154.130, 144.76.153.113) so your server accepts deliveries.
- If your server/database missed a delivery, use Webhook Resend (≤100 IDs) - do not re-run the task and pay again.
- Keep `tasks_ready` polling only as a fallback for missed deliveries.
- Test webhook receivers in the free sandbox first. See [[cap-sandbox-testing]].

- Webhooks apply to the Standard method only; Live returns results inline with no callback. See [[cap-task-vs-live-execution]].
- Pingback creates a file on your server with the completed task ID(s) and your `tag`.
- Postback delivers the full result payload gzip-compressed in one POST.
- `postback_data` is required with `postback_url` and sets the datatype ("advanced"/"html"/sometimes "regular"). See [[cap-result-tiers-regular-advanced-html]].
- Both URLs support `$id` and `$tag` substitution for routing.
- Webhook Resend handles up to 100 task IDs per call with no double-charge.
- Official guidance: webhooks enable more than 1000 tasks/min or 100,000 tasks/day. See [[cap-rate-limits-throughput]].
- Whitelist DataForSEO sending IPs (e.g. 144.76.154.130, 144.76.153.113) inbound. See [[cap-authentication-security]].
- Keep `tasks_ready` polling only as a fallback for missed deliveries.
- Test receivers for free in the sandbox first. See [[cap-sandbox-testing]].
- This is a primary cost lever versus polling. See [[cap-queue-priority-cost-model]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-task-vs-live-execution]]
- [[cap-platform-architecture]]
- [[cap-rate-limits-throughput]]
- [[cap-queue-priority-cost-model]]
- [[cap-status-error-codes]]
- [[cap-sandbox-testing]]
- [[dec-cost-control-strategy]]
- [[play-rank-tracking-pipeline]]
- [[play-cost-optimized-pipeline]]

## Sources
- https://dataforseo.com/help-center/pingbacks-postbacks-with-dataforseo-api (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix-webhook_resend/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/errors-and-webhook-resend-endpoints (retrieved 2026-06-26)
- https://dataforseo.com/help-center/collect-serp-data-from-dataforseo-api (retrieved 2026-06-26)
