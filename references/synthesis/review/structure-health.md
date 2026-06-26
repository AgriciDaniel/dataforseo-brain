# Review: Structure & Health — DataForSEO Brain

Scope: dead wikilinks, orphan notes, frontmatter completeness, master `index.md` + folder `_index.md` MOC coverage, research-pack citation count, source-ledger refresh_due, em-dash policy, duplicate/contradictory content. Audited 80 wiki notes + 1 canvas, the research pack, `references/source-ledger.json`, and spot-checked the live docs at https://docs.dataforseo.com/v3/ on 2026-06-26.

## What passes (verified, not asserted)

- **Dead wikilinks: ZERO.** All 100+ distinct `[[link]]` targets resolve by path or basename (programmatic resolution over every `.md`/`.canvas`). Includes path-style links (`concepts/_index`, `meta/dashboard`, `sources/_index`, `dataforseo-platform-map`).
- **Frontmatter: 100% complete.** All 80 notes carry `type/title/domain/status/created/updated/tags`. No duplicate titles. Every `created`/`updated` is a valid ISO date and none is in the future (all <= 2026-06-26).
- **Master index coverage: complete.** `index.md` links all 68 content notes (33 cap + 7 dec + 8 ent + 10 plat + 10 play) plus `overview`, `hot`, `meta/dashboard`, `sources/_index`, `research-pack`, and the canvas.
- **Folder MOCs: complete.** concepts (33), decisions (7), entities (8), flows (10), platforms (10) — every `_index.md` links every note in its folder.
- **Research pack: 104 dated citations** (74 official + 30 external), each tagged `retrieved 2026-06-26`; the "104 dated citations" claim in `index.md` and the pack header is exact. Far exceeds the >=60 floor.
- **Source ledger:** `references/source-ledger.json` holds 12 sources (11 `official` + 1 `vendor`), every one with `refresh_due: 2026-07-26` (future). Exceeds the ">=2 official with future refresh_due" floor.
- **Canvas integrity:** all 29 `file` nodes + 1 `text` node resolve (paths relative to brain root).
- **No contradictions in key figures.** "12 modules" matches live docs (verified). The "200+ endpoints" (total surface) vs "39 endpoints" (live cost pass) vs "185 endpoint docs" (scrape) vs "20 endpoints" (Labs row) are distinct, correctly-scoped metrics, not conflicts. The "185 endpoint docs" claim matches the actual raw capture exactly (185 `.md` files under `.raw/.../dataforseo-research/` excluding `_research/`). Rate-limit figures (2000 calls/min, 30 simultaneous tasks) are consistent across all 13 notes that state them. The cap-serp / cap-labs / cap-backlinks splits are intentional decompositions, not duplicates.

## Findings

| Severity | Location | Issue | Recommended fix |
|---|---|---|---|
| MEDIUM | wiki-wide (22 of 80 files; ~275 em-dash occurrences) | Em-dash (`—`) policy violation against the vault standard "no em dashes." Concentrated in `sources/research-pack-2026-06-26.md` (106 lines / 183 occ.), `overview.md` (18), all 10 `platforms/plat-*.md` (4-6 each), the 6 `_index.md` MOCs (2 each), and `index/hot/log/meta-dashboard`. Most cap/dec/ent/flow note *bodies* are clean, so the brain is internally inconsistent. | Normalize: replace ` — ` separators with ` - ` (or restructure), and convert citation lines to `URL - retrieved 2026-06-26`. A single sed pass over the 22 files fixes the bulk; re-run `grep -rl '—' wiki/` to confirm zero. |
| LOW | CONTRIBUTING.md / AGENTS.md / docs/ | No em-dash / style rule is documented anywhere in the brain, so the "em-dash policy" being audited is implicit only. Cannot be enforced or tested. | Add one line to CONTRIBUTING.md ("Style: no em dashes; use `-` or `:`; no en-dash ranges") so the policy is explicit and lintable. |
| LOW | wiki/log.md | Orphan: zero inbound wikilinks and not linked from `index.md` (the only note in the vault with no inbound edge). It is the append-only run log, so convention tolerates it, but it is unreachable by navigation. | Add `[[log]]` to the `index.md` "Start here" line or to `meta/dashboard.md`. |
| LOW | wiki/sources/_index.md:19 | Redundant/odd relative path: `[[../sources/research-pack-2026-06-26]]` for a note in the *same* folder. Resolves (basename), but is sloppy and breaks if rendered outside Obsidian. | Change to `[[research-pack-2026-06-26]]`. |
| LOW | wiki/ (no `.obsidian`) + wiki/canvases/dataforseo-platform-map.canvas | Vault mount point is undocumented. The only `.obsidian` folders live in `assets/template-brain/` and `examples/sample-vault/`; `wiki/` has none. Canvas file nodes use `wiki/concepts/...md` prefixes, so they resolve ONLY if the vault is opened at the brain ROOT. If a user opens `wiki/` as the vault, all 29 canvas nodes break (bare-slug wikilinks still resolve). | Document the intended mount (brain root) in README, or re-root the canvas paths and ship a `.obsidian` so the deliverable opens deterministically. |
| LOW | wiki/meta/dashboard.md:37 | En-dash (`–`) used in a numeric range `~$0.0011–0.0105`. If the no-em-dash policy extends to en-dashes (vault convention), this is a stray. | Replace with `~$0.0011-0.0105` (hyphen) or "to". |

## Verdict

Structurally SOLID and market-ready: every hard gate passes (zero dead links, zero content orphans, 100% frontmatter, full index + MOC coverage, 104 dated citations, a 12-source ledger all future-dated, a healthy canvas, and live-verified module claims). The only open items are cosmetic/policy — pervasive em-dashes against the vault style rule (the one finding worth a batch fix), an unlinked `log.md`, a redundant link, and an undocumented vault root that could break the canvas. No BLOCKER or HIGH issues.
