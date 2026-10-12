#!/usr/bin/env python3
"""JSON-lines bridge to dfs_safety.call for non-Python callers (Node, PHP CLI, shell).

One long-lived process per run, so the run cap and repeat checks span every call:
  stdin : {"id": 1, "path": "serp/google/organic/live/advanced", "payload": [...], "source": "x",
           "confirm_cost": false, "allow_repeat": false}
  stdout: {"id": 1, "ok": true, "data": {...}}
          {"id": 1, "ok": false, "kind": "blocked" | "out_of_balance" | "error", "error": "..."}
A "blocked" or "out_of_balance" reply means nothing was billed and the caller must stop, not retry.
Node client: scripts/dfs_safety.mjs.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dfs_safety  # noqa: E402


def handle(req):
    try:
        data = dfs_safety.call(req["path"], req.get("payload"), timeout=req.get("timeout", 120),
                               source=req.get("source"), confirm_cost=bool(req.get("confirm_cost")),
                               allow_repeat=bool(req.get("allow_repeat")))
        return {"ok": True, "data": data}
    except dfs_safety.Blocked as exc:
        return {"ok": False, "kind": "blocked", "error": str(exc)}
    except dfs_safety.OutOfBalance as exc:
        return {"ok": False, "kind": "out_of_balance", "error": str(exc)}
    except Exception as exc:   # reported to the caller, never swallowed
        return {"ok": False, "kind": "error", "error": f"{type(exc).__name__}: {exc}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
        except ValueError as exc:
            reply = {"id": None, "ok": False, "kind": "error", "error": f"bad JSON: {exc}"}
        else:
            reply = dict(handle(req), id=req.get("id"))
        sys.stdout.write(json.dumps(reply) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
