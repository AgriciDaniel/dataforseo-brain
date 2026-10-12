#!/usr/bin/env python3
"""Free daily drift watch: DataForSEO's updates feed, its OpenAPI spec and the account price table.

Runs the same three free checks as run_baselines.py, without any paid call, so watching for new
endpoints, retirements and price changes doesn't depend on a paid client run being scheduled.

Exit codes (the .cmd wrapper turns them into popups):
  0  nothing new
  3  something new to record (only when it differs from what the last run already reported)
  4  a check has failed on FAIL_ALERT_AFTER consecutive runs (the site blocked us, the network is down...)
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_baselines as rb  # noqa: E402

FAIL_ALERT_AFTER = 2
FAIL_MARKERS = ("skipped", "failed")


def run_checks(vault):
    """[(name, lines, needs_attention)] for the three free checks."""
    out = []
    for name, fn in (("updates", rb.changelog_check), ("spec", rb.spec_check), ("prices", rb.price_check)):
        try:
            lines, attention = fn(vault)
        except Exception as exc:   # one broken check must not hide the others
            lines, attention = [f"{name} check failed: {exc}"], False
        out.append((name, lines, attention))
    return out


def failed(lines):
    text = " ".join(lines).lower()
    return any(m in text for m in FAIL_MARKERS)


def decide(results, state):
    """(exit code, new state). Attention alerts fire once per distinct finding; failures after N in a row."""
    attention = [ln for _, lines, att in results if att for ln in lines if ln.strip()]
    fingerprint = hashlib.sha1("\n".join(attention).encode()).hexdigest()[:12] if attention else ""
    fails = dict(state.get("fails", {}))
    for name, lines, _ in results:
        fails[name] = fails.get(name, 0) + 1 if failed(lines) else 0
    new_state = {"fingerprint": fingerprint, "fails": fails}
    if any(n >= FAIL_ALERT_AFTER for n in fails.values()):
        return 4, new_state
    if fingerprint and fingerprint != state.get("fingerprint"):
        return 3, new_state
    return 0, new_state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", type=pathlib.Path, default=rb.DEFAULT_VAULT)
    args = ap.parse_args()
    state_path = args.vault / "_attachments" / "drift-watch-state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    results = run_checks(args.vault)
    code, new_state = decide(results, state)
    print(f"drift watch {datetime.datetime.now():%Y-%m-%d %H:%M}")
    for name, lines, att in results:
        print(f"[{name}]{' ATTENTION' if att else ''}" + "".join(lines).rstrip())
    print(f"consecutive failures: {new_state['fails']}  exit={code}")
    state_path.write_text(json.dumps(new_state), encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
