# Wiki Lint Report - DataForSEO Brain

**Date:** 2026-06-26
**Vault root:** `wiki/`
**Scope:** Full wiki (80 .md files, 5 .canvas files)
**DragonScale:** Not adopted (DRAGONSCALE_ADDR=0, DRAGONSCALE_TILE=0)

---

## Summary

- Pages scanned: 80 .md files + 5 .canvas files
- Issues found: 6 (0 critical, 0 warnings, 6 suggestions)

The brain passes the Brainstein SSS+ audit independently. Zero dead links, zero frontmatter gaps, zero orphan pages, zero empty headings, zero stale seeds, zero em/en-dashes, no MOC gaps. All six issues below are unlinked entity mentions in body prose - the entity pages exist and are linked elsewhere in the vault; these are within-page cross-reference gaps only.

---

## Critical (must fix)

None.

---

## Warnings (should fix)

None.

---

## Suggestions (worth considering)

### 1. `wiki/overview.md:20` - "Ahrefs and Semrush" without entity links

**Problem:** The opening description reads "seat-and-subscription tools like Ahrefs and Semrush" with neither name linked to its entity page. The decision page `[[dec-dataforseo-vs-ahrefs-semrush-moz]]` is linked on line 21, but `[[ent-ahrefs]]` and `[[ent-semrush]]` are never linked anywhere in this file.

**Fix:** Change `like Ahrefs and Semrush` to `like [[ent-ahrefs|Ahrefs]] and [[ent-semrush|Semrush]]` at line 20.

---

### 2. `wiki/concepts/cap-geo-ai-search-optimization.md:52,57,59` - "Ahrefs" cited three times with no entity link

**Problem:** "Ahrefs" is cited three times in the body prose (lines 52, 57, 59) as a data source for AI visibility research. No link to `[[ent-ahrefs]]` exists anywhere in this file, despite the entity page profiling Ahrefs' methodology and pricing.

**Fix:** Add `[[ent-ahrefs]]` to the Related section (lines 62-73) or convert the first inline citation at line 52 to `[[ent-ahrefs|Ahrefs]]`.

---

### 3. `wiki/concepts/cap-keywords-data-api.md:21` - "clickstream" in intro without entity link

**Problem:** Line 21 reads "DataForSEO Labs (which uses DataForSEO's own clickstream-blended database)" without linking `[[ent-clickstream-data]]`. The file links `[[ent-google-ads-keyword-planner]]` and `[[cap-trends-and-clickstream]]`, but the clickstream entity page is absent.

**Fix:** Add `- [[ent-clickstream-data]]` to the Related section at the bottom of the file.

---

### 4. `wiki/concepts/cap-trends-and-clickstream.md:46` - "Google Ads API" without entity link

**Problem:** Line 46 reads "misspelled keywords auto-correct via Google Ads API validation" without linking `[[ent-google-ads-keyword-planner]]`. The file links `[[ent-clickstream-data]]` but not the Google Ads entity.

**Fix:** Add `[[ent-google-ads-keyword-planner]]` to the Related section of this file.

---

### 5. `wiki/decisions/dec-cost-control-strategy.md:35-36` - "clickstream" and "Google Ads" without entity links

**Problem:** Lines 35-36 of the lesson block name "clickstream" and "Google Ads keyword calls" as the priciest tiers without linking `[[ent-clickstream-data]]` or `[[ent-google-ads-keyword-planner]]`. Line 45 does link `[[ent-ahrefs]]` and `[[ent-semrush]]`, so the omission is inconsistent.

**Fix:** Add `[[ent-clickstream-data]]` and `[[ent-google-ads-keyword-planner]]` to the Related section of this file.

---

### 6. `wiki/meta/dashboard.md:40,42` - Cost cheat-sheet table rows without entity links

**Problem:** The cost cheat-sheet table at lines 40 and 42 names "Keywords Data Google Ads" and "Clickstream search volume" as plain text. These are the two highest-cost tiers and directly correspond to `[[ent-google-ads-keyword-planner]]` and `[[ent-clickstream-data]]`.

**Fix:** Convert the table cell text on line 40 to `Keywords Data [[ent-google-ads-keyword-planner\|Google Ads]]` and line 42 to `[[ent-clickstream-data\|Clickstream]] search volume`.

---

## Checks that passed clean

| Check | Result |
|---|---|
| Frontmatter completeness (type, title, domain, status, created, updated, tags) | PASS - all 80 files complete |
| Dead wikilinks | PASS - 0 broken links across all files |
| Canvas references (`dataforseo-platform-map`) | PASS - file exists at `wiki/canvases/` |
| Orphan pages (zero inbound wikilinks, excl. log.md) | PASS - every file is linked from at least one other |
| Empty/stub headings | PASS - all ## headings have content beneath them |
| Em-dash / en-dash in note bodies | PASS - none found |
| Stale seed pages (status=seed, updated > 30 days ago) | PASS - no seed-status pages |
| MOC/index completeness (index.md + all folder _index.md) | PASS - all notes accounted for |
| Numeric claim consistency (rate limits, deposit, storage) | PASS - all consistent (endpoint-specific limits are correctly labelled: 2000/min global, 12/min Google Ads Live, 6/min user_data, 60/min Ahrefs - no contradictions) |
| Substance gate on 69 content notes (avg lines, avg links) | PASS - avg 83.1 lines (gate >=80), avg 26.8 links (gate >=8) |

---

## Index cross-check

`wiki/index.md` references `[[dataforseo-platform-map|Platform Map canvas]]` - verified present at `wiki/canvases/dataforseo-platform-map.canvas`. No stale index entries found.

---

## Notes on numeric claims

The apparent "contradiction" in calls-per-minute figures is expected and correct:
- **2000/min** - platform-wide global ceiling
- **12/min** - Google Ads Live endpoint-specific cap (Keywords Data)
- **6/min** - `appendix/user_data` endpoint-specific cap
- **60/min** - Ahrefs competitor API rate (used in comparison context only)
- **10/min** - `appendix/errors` endpoint-specific cap

These are not contradictions; each figure is scoped to its context in every occurrence.
