# Product Boundaries

DataForSEO Brain is an advisory, read-only Obsidian brain for DataForSEO v3 API mastery - 12 modules and ~200+ endpoints (SERP, Keywords Data, AI Optimization, Domain Analytics, DataForSEO Labs, OnPage, Backlinks, Content Analysis, Merchant, App Data, Business Data, Databases), the task/live queue execution model, and the per-call cost model.

## It Does

- Preserve raw sources under `.raw/`.
- Synthesize source-cited notes and deliverables.
- Maintain action queues, reports, and next actions.
- Keep decisions auditable through source links and rollback notes.
- Gate maturity through `references/source-ledger.json`,
  `references/adapter-manifest.json`, and `scripts/audit_brain.py`.

## It Does Not

- No endpoint, parameter, cost, or auth claim without a current official docs citation
- No credentials, tokens, or .env values in any repo artifact; secrets stay in ~/Desktop/Keys
- No live billable API call beyond the operator-approved $5 cap; track spend via the user_data endpoint and hard-stop
- No irreversible recommendation without owner, confidence, source, and rollback note

## Safety Risks

- Stale pricing, rate limits, or endpoint parameters
- Credential or PII leakage in captured response fixtures
- Overconfident cost estimates leading to budget overrun
- Generated reports leaking local filesystem paths

## Maturity Boundary

This repo starts as `scaffolded`. Market-ready quality requires current
research, domain adapters, deterministic demo verification, source citations,
Obsidian graph hygiene, and release scans. The audit score is capped below 90
until those stages are complete.
