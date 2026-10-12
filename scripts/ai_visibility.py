#!/usr/bin/env python3
"""AI-visibility tracker: one billed request for a whole competitor set.

  python scripts/ai_visibility.py --location 2840 client.example competitor-a.example competitor-b.example

Bills one request per run regardless of target count (verified 2026-09-17:
5 targets = $0.105). Credentials from DATAFORSEO_LOGIN (or DATAFORSEO_USERNAME)
and DATAFORSEO_PASSWORD. Appends each run to a JSONL so the series accumulates.
"""
import argparse, datetime, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dfs_safety  # noqa: E402

URL = "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/multi_target_metrics/live"


def post(payload: list) -> dict:
    return dfs_safety.call(URL, payload, timeout=180)   # logs the exact cost to the vault call log


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("domains", nargs="+", help="2-10 domains; the first is the client")
    ap.add_argument("--location", type=int, default=2840, help="location_code (default 2840 US)")
    ap.add_argument("--language", default="en")
    ap.add_argument("--platform", choices=["chat_gpt", "google"], help="omit for both")
    ap.add_argument("--client", help="series label; defaults to the first domain. Must match "
                                     "clients.json for run_baselines.py to compute deltas")
    ap.add_argument("--out", default="ai-visibility.jsonl")
    args = ap.parse_args()

    if not 2 <= len(args.domains) <= 10:
        sys.exit("multi_target_metrics takes 2-10 targets per request")

    body = {
        "language_code": args.language,
        "location_code": args.location,
        "internal_list_limit": 5,
        "targets": [{"key": d, "target": [{"domain": d, "search_filter": "include"}]}
                    for d in args.domains],
    }
    if args.platform:
        body["platform"] = args.platform

    data = post([body])
    if data.get("status_code") != 20000:
        sys.exit(f"request failed: {data.get('status_code')} {data.get('status_message')}")
    task = data["tasks"][0]
    if task.get("status_code") != 20000:
        sys.exit(f"task failed: {task.get('status_code')} {task.get('status_message')}")

    items = (task.get("result") or [{}])[0].get("items") or []
    rows = sorted(
        ((i.get("key"), (i.get("total") or {}).get("mentions") or 0,
          (i.get("total") or {}).get("ai_search_volume") or 0) for i in items),
        key=lambda r: r[2], reverse=True)

    stamp = datetime.date.today().isoformat()
    print(f"{stamp}  location {args.location}  cost ${data.get('cost')}\n")
    print("%-30s %10s %18s" % ("target", "mentions", "ai_search_volume"))
    for key, mentions, volume in rows:
        mark = " <-- client" if key == args.domains[0] else ""
        print("%-30s %10d %18d%s" % (key, mentions, volume, mark))

    out = pathlib.Path(args.out)
    with out.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"date": stamp, "client": args.client or args.domains[0],
                             "location_code": args.location,
                             "language_code": args.language, "cost": data.get("cost"),
                             "rows": [{"target": k, "mentions": m, "ai_search_volume": v}
                                      for k, m, v in rows]}) + "\n")
    print(f"\nappended to {out}")


if __name__ == "__main__":
    main()
