# DataForSEO Brain - note template + authoring rules (for synthesis agents)

Every content note in `wiki/` (concepts/, platforms/, entities/, flows/, decisions/) MUST follow
this template. Targets that the audit enforces:
- **≥ 80 lines** per note (the section skeleton below clears this when each section has real content).
- **≥ 8 `[[wikilinks]]`** per note (frontmatter `related` + the `## Related` block guarantee this).
- Frontmatter present on EVERY note: `type, title, domain, status, created, updated, tags`.
- Every note ends with a `## Sources` block citing the REAL `docs.dataforseo.com` URL(s) from the
  matching `.raw/sources/dataforseo-research/<module>/<endpoint>.md` (`## Sources` / frontmatter `url`)
  or the `_research/*.md` report. Never invent a URL or an API field.

## Exact skeleton

```
---
type: <concept|platform|entity|flow|decision>
title: "<Human Title>"
domain: dataforseo
subdomain: <serp|labs|keywords|ai-optimization|backlinks|domain-analytics|onpage|content-analysis|merchant|app-data|business-data|databases|platform|market>
status: stable
created: 2026-06-26
updated: 2026-06-26
tags: [dataforseo, <module-or-facet>, <facet2>]
related:
  - "[[<slug-1>]]"
  - "[[<slug-2>]]"
  - "[[<slug-3>]]"
---

# <Human Title>

> One-sentence definition. Sits under [[index|DataForSEO Brain]] → [[<folder>/_index|<Folder>]].

## Overview
3-6 sentences: what this is, why it matters, where it fits in the DataForSEO platform.

## What it covers
Bullets mapping to the REAL endpoints/fields from the raw docs (name them precisely).

## Key parameters / inputs
A short table or bullets of the most important request parameters (from the raw `## Request parameters`).

## Response / what you get back
The key response fields or result item types (from the raw `## Response fields`).

## Cost & method notes
Live vs Standard vs Priority, per-result vs per-request, Advanced/HTML, limits - link
[[cap-queue-priority-cost-model]] and [[cap-task-vs-live-execution]] where relevant.

## When to use / how it fits
Tie to at least one workflow ([[play-...]]) and one decision ([[dec-...]]).

## Gotchas / limits
Rate limits, retention, subscription gates, accuracy caveats (cite raw / research).

## Related
- [[<module hub or index>]]
- [[<sibling 1>]]
- [[<sibling 2>]]
- [[<sibling 3>]]
- [[cap-platform-architecture]]
- [[cap-queue-priority-cost-model]]
- [[dec-which-api-for-which-job]]
- [[<one flow or decision>]]

## Sources
- <real doc/research URL> - retrieved 2026-06-26
- <second real URL if available> - retrieved 2026-06-26
```

## Rules
1. Use ONLY slugs that exist in `references/synthesis/page-registry.md` for `[[wikilinks]]` (so links resolve - no dead links).
2. `## Related` must contain ≥ 8 distinct wikilinks; `related:` frontmatter adds 3 more (dups across the two are fine, both count).
3. Pull params/fields/costs from the matching `.raw/.../<module>/*.md` - quote real names; do not fabricate.
4. Decisions/entities/flows that synthesize market or practitioner knowledge cite the `_research/*.md` reports' URLs.
5. Keep prose tight and factual; no marketing fluff, no em dashes.
6. File names = the registry slug + `.md`, placed in the registry's folder.
