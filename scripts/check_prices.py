#!/usr/bin/env python3
"""Flag DataForSEO prices in vault notes that disagree with the live price table.

Ground truth: the newest `_attachments/live-prices-*.json` in the vault
(captured from the account's price table). A line is checked when it names
exactly one priced endpoint function; every dollar amount on it must be one of
that function's current prices or a whole multiple of its per-call price
(call totals). Lines that mark a price as historical ("June", "before
2026-07-01", "was ~$x") are skipped, as are dated snapshots (log, reports,
sources, archives) and the price table note that compares old and new.

Exit 0 = no drift, 1 = drift found.
"""
from __future__ import annotations
import os

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_VAULT = Path(os.environ.get("DFS_BRAIN_VAULT") or Path.home() / "Documents" / "DataForSEO Brain" / "vault")
SKIP_PARTS = {"reports", "sources", ".raw"}
SKIP_NAMES = {"log.md", "lesson-log.md", "cap-live-price-table.md"}
SKIP_STEM_PREFIXES = ("hot-archive", "reference-hot")
HISTORICAL_RE = re.compile(
    r"June|pre-2026-07-01|before (?:the )?2026-07-01|since 2026-07-01|\(was |\bwas ~?\$|"
    r"\bran \$|old price|historical",
    re.I,
)
PRICE_RE = re.compile(r"\$(\d*\.\d+)")
# generic words that are endpoint functions but also ordinary prose
AMBIGUOUS = {"live", "summary", "search", "explore", "overview", "categories", "locations", "languages"}
REL_TOL = 0.02


def latest_prices(vault: Path) -> Path | None:
    files = sorted((vault / "_attachments").glob("live-prices-*.json"))
    return files[-1] if files else None


def load_table(path: Path) -> dict[str, dict[str, set[float]]]:
    """function name -> {'request': {...}, 'result': {...}} across engines and priorities."""
    table: dict[str, dict[str, set[float]]] = {}
    for entry in json.loads(path.read_text(encoding="utf-8"))["entries"]:
        cost = float(entry.get("cost") or 0)
        if cost <= 0:
            continue
        parts = [p for p in entry["endpoint"].split("/") if p not in {"live", "advanced", "html", "regular", "task_post"}]
        if len(parts) < 2:
            continue
        kind = "result" if entry.get("cost_type") == "per_result" else "request"
        keys = {parts[-1], "/".join(parts[-2:])}
        if parts[0] == "keywords_data" and len(parts) == 2:
            keys.add("google_ads/" + parts[1])   # the account table drops the engine on Google Ads tasks ($0.06 queued)
        for key in keys:
            table.setdefault(key, {"request": set(), "result": set()})[kind].add(cost)
    return table


def is_current(value: float, prices: dict[str, set[float]]) -> bool:
    allowed = prices["request"] | prices["result"]
    if any(abs(value - p) <= p * REL_TOL for p in allowed):
        return True
    for per_call in prices["request"]:
        n = round(value / per_call)
        if n >= 2 and abs(value - n * per_call) <= value * REL_TOL:
            return True    # a total for n calls
        if prices["result"] and per_call <= value <= per_call + 1000 * max(prices["result"]):
            return True    # one call plus its rows
    return False


def mentioned(line: str, table: dict) -> dict[str, dict[str, set[float]]]:
    found = {}
    for key in table:
        if key in AMBIGUOUS:
            continue
        if re.search(r"(?<![a-z_])" + re.escape(key) + r"(?![a-z_])", line):
            found[key] = table[key]
    # prefer the most specific form: drop "search_volume" when "google_ads/search_volume" matched
    return {k: v for k, v in found.items() if not any(o != k and o.endswith("/" + k) for o in found)}


def scan(vault: Path, table: dict) -> list[str]:
    findings = []
    for path in sorted((vault / "wiki").rglob("*.md")):
        if SKIP_PARTS & set(path.parts) or path.name in SKIP_NAMES or path.stem.startswith(SKIP_STEM_PREFIXES):
            continue
        for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "$" not in line or HISTORICAL_RE.search(line):
                continue
            hits = mentioned(line, table)
            if len(hits) != 1:
                continue      # comparison lines and prose without an endpoint are out of scope
            (name, prices), = hits.items()
            bad = [v for v in map(float, PRICE_RE.findall(line)) if v < 1 and not is_current(v, prices)]
            if bad:
                now = sorted(prices["request"])[:1] + sorted(prices["result"])[:1]
                findings.append(f"{path.relative_to(vault).as_posix()}:{no} {name} says "
                                f"{', '.join('$%g' % b for b in bad)}; live: {' + '.join('$%g' % p for p in now)}")
    return findings


def check(vault: Path) -> list[str]:
    path = latest_prices(vault)
    return scan(vault, load_table(path)) if path else []


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vault", type=Path, default=DEFAULT_VAULT)
    args = ap.parse_args(argv)
    findings = check(args.vault.expanduser().resolve())
    for f in findings:
        print(f"PRICE DRIFT {f}")
    print(f"price drift: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
