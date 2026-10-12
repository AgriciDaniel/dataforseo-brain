#!/usr/bin/env python3
"""Spend and guard report from one or more DataForSEO call logs.

    python spend_report.py --since 2026-10-02
    python spend_report.py --since 2026-10-02 --log server-calls.jsonl --balance

Default log: the vault's _attachments/dfs-calls.jsonl. Extra logs (e.g. a server's
~/.claude/dfs-guard/dfs-calls.jsonl, copied over) via --log or DFS_EXTRA_CALL_LOGS (comma separated).
REST lines carry the exact billed cost; connector lines carry the guard's estimate only, so a
balance delta (--balance, free) is the only true total.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dfs_safety  # noqa: E402

BURST_WINDOW_S = 60
BURST_MIN = 5       # this many calls to one endpoint inside the window looks unbatched


def read_logs(paths: list[Path], since: str) -> list[dict]:
    rows = []
    for p in paths:
        if not p.exists():
            print(f"missing log: {p}", file=sys.stderr)
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if str(r.get("ts", "")) >= since:
                r["_log"] = p.name if len(paths) > 1 else ""
                rows.append(r)
    return sorted(rows, key=lambda r: r.get("t") or 0)


def summarize(rows: list[dict]) -> dict:
    # task_get lines (logged before 2026-10-12) only echo the cost already billed at task_post
    rest = [r for r in rows if r.get("phase") == "rest" and "task_get" not in str(r.get("endpoint"))]
    pre = [r for r in rows if r.get("phase") == "pre"]
    by_day, by_source, by_endpoint = defaultdict(float), defaultdict(float), defaultdict(lambda: [0, 0.0])
    for r in rest:
        c = float(r.get("cost") or 0)
        by_day[str(r["ts"])[:10]] += c
        by_source[r.get("source") or "?"] += c
        ep = (r.get("endpoint") or "?").lstrip("/").removeprefix("v3/")   # older lines kept the /v3/ prefix
        by_endpoint[ep][0] += 1
        by_endpoint[ep][1] += c
    allowed = [r for r in pre if r.get("decision") in ("allow", "ask")]
    for r in allowed:
        e = by_endpoint["mcp:" + (r.get("endpoint") or "?")]
        e[0] += 1
        e[1] += float(r.get("est") or 0)
    decisions = Counter(r.get("decision") for r in pre)
    flagged = [r for r in pre if r.get("decision") in ("deny", "ask")]
    return {"rest_total": round(sum(by_day.values()), 4), "rest_calls": len(rest),
            "mcp_calls": len(allowed), "mcp_estimate": round(sum(float(r.get("est") or 0) for r in allowed), 4),
            "by_day": dict(sorted(by_day.items())), "by_source": dict(sorted(by_source.items(), key=lambda kv: -kv[1])),
            "by_endpoint": dict(sorted(by_endpoint.items(), key=lambda kv: -kv[1][1])),
            "decisions": dict(decisions), "flagged": flagged, "bursts": bursts(rest + allowed)}


def bursts(rows: list[dict]) -> list[tuple[str, str, int]]:
    """(first ts, endpoint, n) where one endpoint was called BURST_MIN+ times inside BURST_WINDOW_S."""
    by_ep = defaultdict(list)
    for r in rows:
        by_ep[r.get("endpoint") or "?"].append(r)
    out = []
    for ep, rs in by_ep.items():
        i = 0
        while i < len(rs):
            j = i
            while j + 1 < len(rs) and (rs[j + 1].get("t") or 0) - (rs[i].get("t") or 0) <= BURST_WINDOW_S:
                j += 1
            if j - i + 1 >= BURST_MIN:
                out.append((str(rs[i].get("ts")), ep, j - i + 1))
                i = j + 1
            else:
                i += 1
    return sorted(out)


def render(s: dict, since: str, balance: float | None) -> str:
    lines = [f"# DataForSEO spend since {since}", "",
             f"- REST (exact): **${s['rest_total']:.4f}** over {s['rest_calls']} calls",
             f"- Connector (guard estimate): ~${s['mcp_estimate']:.4f} over {s['mcp_calls']} calls",
             f"- Guard decisions: {', '.join(f'{k} {v}' for k, v in sorted(s['decisions'].items(), key=str)) or 'none'}"]
    if balance is not None:
        lines.append(f"- Balance now: ${balance:.2f} (a balance delta is the only true total)")
    lines += ["", "## By day (REST)", "| Day | $ |", "|---|---|"]
    lines += [f"| {d} | {c:.4f} |" for d, c in s["by_day"].items()]
    lines += ["", "## By source (REST)", "| Source | $ |", "|---|---|"]
    lines += [f"| {k} | {v:.4f} |" for k, v in s["by_source"].items()]
    lines += ["", "## Top endpoints", "| Endpoint | Calls | $ |", "|---|---|---|"]
    lines += [f"| `{k}` | {n} | {c:.4f} |" for k, (n, c) in list(s["by_endpoint"].items())[:15]]
    lines += ["", "## Guard blocks and asks (check for false blocks)"]
    lines += [f"- {r.get('ts')} `{r.get('endpoint')}` **{r.get('decision')}** (est ${float(r.get('est') or 0):.3f}) "
              f"{str(r.get('reason') or '')[:160]}" for r in s["flagged"]] or ["- none"]
    lines += ["", f"## Possible unbatched bursts ({BURST_MIN}+ calls to one endpoint within {BURST_WINDOW_S}s)"]
    lines += [f"- {ts} `{ep}` x{n}" for ts, ep, n in s["bursts"]] or ["- none"]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--since", required=True, help="YYYY-MM-DD (inclusive)")
    ap.add_argument("--log", action="append", default=[], type=Path)
    ap.add_argument("--balance", action="store_true", help="add the current balance (free call)")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)
    extra = [Path(p) for p in (os.environ.get("DFS_EXTRA_CALL_LOGS") or "").split(",") if p.strip()]
    logs = [Path(dfs_safety.VAULT_LOG)] + extra + args.log
    s = summarize(read_logs(logs, args.since))
    bal = dfs_safety.balance()[0] if args.balance else None
    text = render(s, args.since, bal)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
