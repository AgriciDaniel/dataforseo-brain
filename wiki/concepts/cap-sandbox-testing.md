---
type: concept
title: "Sandbox & Testing"
domain: dataforseo
subdomain: platform
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, platform, sandbox]
related:
 - "[[cap-platform-architecture]]"
 - "[[cap-queue-priority-cost-model]]"
 - "[[cap-webhooks-pingback-postback]]"
---

# Sandbox & Testing

> A free environment at `sandbox.dataforseo.com` that returns structurally identical dummy data, letting you validate request shape and integration logic at $0 before spending on production. Sits under [[index|DataForSEO Brain]] → [[concepts/_index|Concepts]].

## Overview
The sandbox is "a technical environment for developers where DataForSEO API can be used without unnecessary expenses." It mirrors production exactly in structure and fields but returns generic dummy data, so you can build and CI-test integration logic (parsing, retries, webhook handling) without consuming credits. It is free for any registered user and shares production rate limits, so it also lets you exercise throughput handling safely.

## What it covers
- Base URL: `https://sandbox.dataforseo.com/v3/`.
- Cost: completely free - "Your account will not be charged for using Sandbox endpoints."
- Identical response contract: "The structure and fields of the sandbox response are identical to that of the actual API response."
- Coverage: works with all DataForSEO APIs (SERP, Keywords Data, Domain Analytics, Labs, Backlinks, OnPage, Content Analysis, Merchant, App Data, Business Data).
- Supports `pingback_url` and `postback_url`, and both Standard task-based and Live endpoints.

## Key parameters / inputs
- Switch hosts only: replace `api.dataforseo.com/v3/` with `sandbox.dataforseo.com/v3/`; no other code changes needed.
- Example paths: `https://sandbox.dataforseo.com/v3/serp/google/organic/task_post`, `https://sandbox.dataforseo.com/v3/serp/google/organic/task_get/advanced/$id`.
- All normal task fields apply (location_code, language_code, tag, webhook URLs).

## Response / what you get back
- Generic, auto-generated dummy data with production-identical JSON shape and field names.
- Standard envelope and status codes behave as in production (20000/20100 on success).
- Error 40404 - "Sandbox missing prepared data" - when the sandbox lacks prepared data for a given request.

## Cost & method notes
The sandbox is the zero-cost foundation of the cost-optimization playbook: build and test against it, then flip the host to production. Separately, new accounts also get a $1 free credit (unlimited validity) for real endpoints. Combine sandbox development with the spend levers in [[cap-queue-priority-cost-model]] and the money-saving flow [[play-cost-optimized-pipeline]].

## When to use / how it fits
Use during development and CI to validate request shape, parse logic, and webhook receivers before any billed call. It is step one of [[dec-cost-control-strategy]] and [[play-cost-optimized-pipeline]], and the safest way to learn [[cap-task-vs-live-execution]] and [[cap-webhooks-pingback-postback]].

## Gotchas / limits
- Same rate limits as production: 2000 API calls/min, 100 tasks/POST (1 for Live). See [[cap-rate-limits-throughput]].
- Data is dummy: validate structure and plumbing, not data accuracy or business logic that depends on real values.
- 40404 means no prepared sandbox data exists for that exact request - adjust the request or test that path in production with the $1 credit.
- Webhook testing works in sandbox, but real result payloads differ from dummy ones.

- Base host swap is the only change: `api.dataforseo.com/v3/` becomes `sandbox.dataforseo.com/v3/`.
- Works with all modules: SERP, Keywords Data, Domain Analytics, Labs, Backlinks, OnPage, Content Analysis, Merchant, App Data, Business Data.
- Supports both Standard task-based and Live endpoints, plus `pingback_url` and `postback_url`.
- Response structure and field names are production-identical; only the data is dummy.
- Same auth credentials as production. See [[cap-authentication-security]].
- Same rate limits as production: 2000 calls/min, 100 tasks/POST (1 for Live). See [[cap-rate-limits-throughput]].
- Status codes behave as in production (20000/20100 on success). See [[cap-status-error-codes]].
- 40404 ("Sandbox missing prepared data") signals no prepared data for that exact request.
- Use it to learn execution modes before paying. See [[cap-task-vs-live-execution]].
- New accounts also get a $1 free credit (unlimited validity) for real endpoints. See [[cap-queue-priority-cost-model]].
- It is step one of the cost playbook. See [[dec-cost-control-strategy]] and [[play-cost-optimized-pipeline]].
- Test webhook receivers here before production. See [[cap-webhooks-pingback-postback]].

## Related
- [[index]]
- [[concepts/_index]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[cap-webhooks-pingback-postback]]
- [[cap-task-vs-live-execution]]
- [[cap-rate-limits-throughput]]
- [[cap-status-error-codes]]
- [[cap-authentication-security]]
- [[dec-cost-control-strategy]]
- [[play-cost-optimized-pipeline]]

## Sources
- https://docs.dataforseo.com/v3/appendix/sandbox/ (retrieved 2026-06-26)
- https://dataforseo.com/help-center/how-does-your-free-unlimited-trial-work (retrieved 2026-06-26)
- https://docs.dataforseo.com/v3/appendix/errors/ (retrieved 2026-06-26)
