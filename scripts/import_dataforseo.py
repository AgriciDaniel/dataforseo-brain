#!/usr/bin/env python3
"""Import a DataForSEO v3 response envelope and print normalized records.

Read-only. No credentials, no network. Usage:
    python scripts/import_dataforseo.py --response tests/fixtures/sample-dataforseo-response.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dataforseo_brain.adapters import load_response, normalize_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize a DataForSEO response.")
    parser.add_argument("--response", required=True, help="path to a DataForSEO response JSON")
    args = parser.parse_args(argv)
    records = normalize_records(load_response(args.response))
    json.dump(records, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
