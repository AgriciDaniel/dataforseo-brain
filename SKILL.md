---
name: dataforseo-brain
description: >
  Scaffold and operate DataForSEO Brain, a source-cited Obsidian brain for DataForSEO v3 API mastery — 12 modules and ~200+ endpoints (SERP, Keywords Data, AI Optimization, Domain Analytics, DataForSEO Labs, OnPage, Backlinks, Content Analysis, Merchant, App Data, Business Data, Databases), the task/live queue execution model, and the per-call cost model..
  Use when the user says "dataforseo-brain", "DataForSEO Brain", "create a DataForSEO v3 API mastery — 12 modules and ~200+ endpoints (SERP, Keywords Data, AI Optimization, Domain Analytics, DataForSEO Labs, OnPage, Backlinks, Content Analysis, Merchant, App Data, Business Data, Databases), the task/live queue execution model, and the per-call cost model. brain",
  "import sources", "synthesize plan", "render report", or wants a persistent
  vault-backed operating system for DataForSEO v3 API mastery — 12 modules and ~200+ endpoints (SERP, Keywords Data, AI Optimization, Domain Analytics, DataForSEO Labs, OnPage, Backlinks, Content Analysis, Merchant, App Data, Business Data, Databases), the task/live queue execution model, and the per-call cost model..
argument-hint: "new | ingest | synthesize | report | visuals | lint | next"
license: Custom license
---

# DataForSEO Brain

Operate the vault first. Read `CODEX.md`, `wiki/hot.md`, and `wiki/index.md`
before changing notes.

## Commands

```bash
/dataforseo-brain new <client-slug> --owner <name>
/dataforseo-brain ingest --vault <path> --file <source>
/dataforseo-brain synthesize --vault <path>
/dataforseo-brain report --vault <path>
/dataforseo-brain visuals --vault <path>
/dataforseo-brain lint --vault <path>
/dataforseo-brain next --vault <path>
```

Source checkout equivalent:

```bash
dataforseo-brain new <client-slug> --owner <name>
dataforseo-brain ingest --vault <path> --file <source>
dataforseo-brain synthesize --vault <path>
dataforseo-brain report --vault <path> --html-only
```

## Required Operating Rules

1. Read `<vault>/CODEX.md`.
2. Read `<vault>/wiki/hot.md`.
3. Read `<vault>/wiki/index.md`.
4. Preserve `.raw/` as immutable source material.
5. Never store credentials in the vault.
6. Never make domain-specific claims without dated trustworthy sources.
7. Keep `hot`, `index`, `overview`, and `log` current.
8. Record research evidence in `references/source-ledger.json`.
9. Record domain adapter completion in `references/adapter-manifest.json`.

## Script Mapping

- `new` -> `python scripts/scaffold_vault.py`
- `ingest` -> `python scripts/ingest_source.py`
- `synthesize` -> `python scripts/synthesize_brain.py`
- `report` -> `python scripts/render_brain_report.py`
- `visuals` -> `python scripts/generate_vault_visuals.py`
- `lint` -> `python scripts/lint_vault.py`
- `next` -> `python scripts/guide_next_action.py`

## Quality Gates

- No endpoint, parameter, cost, or auth claim without a current official docs citation
- No credentials, tokens, or .env values in any repo artifact; secrets stay in ~/Desktop/Keys
- No live billable API call beyond the operator-approved $5 cap; track spend via the user_data endpoint and hard-stop
- No irreversible recommendation without owner, confidence, source, and rollback note

Do not call this brain market-ready unless `scripts/audit_brain.py --require
market-ready` passes. A scaffold is not a finished brain.

## Research Refresh

monthly for endpoint, parameter, and pricing drift; before every release for cost and authentication claims

## Community

Built and maintained inside the AI Marketing Hub Pro community: https://www.skool.com/ai-marketing-hub-pro
