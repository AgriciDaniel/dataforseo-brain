#!/usr/bin/env python3
"""Render a sourced markdown cost scorecard from DataForSEO responses.

Read-only. No credentials, no network. Usage:
    python scripts/render_dataforseo_report.py tests/fixtures/sample-dataforseo-response.json
Writes markdown to stdout (or --out FILE).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dataforseo_brain.adapters import (
    load_response,
    normalize_records,
    render_report,
    synthesize_cost_summary,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a DataForSEO cost scorecard.")
    parser.add_argument("responses", nargs="+", help="one or more response JSON files")
    parser.add_argument("--out", help="write markdown to this file instead of stdout")
    args = parser.parse_args(argv)
    records: list[dict] = []
    for path in args.responses:
        records.extend(normalize_records(load_response(path)))
    md = render_report(synthesize_cost_summary(records), records)
    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
