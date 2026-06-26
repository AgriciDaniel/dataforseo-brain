#!/usr/bin/env python3
"""Synthesize a deterministic cost summary from one or more DataForSEO responses.

Read-only. No credentials, no network. Usage:
    python scripts/synthesize_cost_summary.py tests/fixtures/sample-dataforseo-response.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dataforseo_brain.adapters import load_response, normalize_records, synthesize_cost_summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize DataForSEO response costs.")
    parser.add_argument("responses", nargs="+", help="one or more response JSON files")
    args = parser.parse_args(argv)
    records: list[dict] = []
    for path in args.responses:
        records.extend(normalize_records(load_response(path)))
    summary = synthesize_cost_summary(records)
    json.dump(summary, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
