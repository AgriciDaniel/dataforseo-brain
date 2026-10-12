#!/usr/bin/env python3
"""Pull account-verified DataForSEO prices from /v3/appendix/user_data (free).

Writes references/live-prices-<date>.json and prints the biggest cost levers.
Credentials come from DATAFORSEO_LOGIN (or DATAFORSEO_USERNAME) + DATAFORSEO_PASSWORD.
"""
import base64, datetime, json, os, pathlib, sys, urllib.request

URL = "https://api.dataforseo.com/v3/appendix/user_data"


def fetch() -> dict:
    login = os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DATAFORSEO_USERNAME")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        sys.exit("set DATAFORSEO_LOGIN (or DATAFORSEO_USERNAME) and DATAFORSEO_PASSWORD")
    token = base64.b64encode(f"{login}:{password}".encode()).decode()
    request = urllib.request.Request(URL, headers={"Authorization": f"Basic {token}"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def flatten(node, path, rows):
    if not isinstance(node, dict):
        return
    if any(key.startswith("priority_") for key in node):
        for priority, entries in node.items():
            if not priority.startswith("priority_"):
                continue
            for entry in entries or []:
                rows.append({
                    "endpoint": "/".join(path),
                    "priority": priority.replace("priority_", ""),
                    "cost_type": entry.get("cost_type"),
                    "cost": entry.get("cost"),
                })
        return
    for key, value in node.items():
        flatten(value, path + [key], rows)


def newest_entries(folder: pathlib.Path):
    files = sorted(folder.glob("live-prices-*.json"))
    return json.loads(files[-1].read_text(encoding="utf-8"))["entries"] if files else None


def main() -> bool:
    """Write a dated price table only when prices changed. Returns True if they changed."""
    payload = fetch()
    if payload.get("status_code") != 20000:
        sys.exit(f"user_data failed: {payload.get('status_code')} {payload.get('status_message')}")
    result = payload["tasks"][0]["result"][0]
    rows: list[dict] = []
    flatten(result["price"], [], rows)

    today = datetime.date.today().isoformat()
    body = json.dumps({
        "captured": today,
        "source": "GET /v3/appendix/user_data (free)",
        "account_balance_usd": result["money"]["balance"],
        "entries": rows,
    }, indent=2) + "\n"
    refs = pathlib.Path(__file__).resolve().parent.parent / "references"
    # The vault's lint (check_prices) and the guard's price test read the vault copy; keep both in step.
    vault_dir = pathlib.Path(os.environ.get("DFS_BRAIN_VAULT") or os.environ.get("DFS_VAULT") or pathlib.Path.home() / "Documents" / "DataForSEO Brain" / "vault") / "_attachments"
    previous = newest_entries(vault_dir) if vault_dir.is_dir() else newest_entries(refs)
    if previous == rows:
        print(f"prices unchanged since the last table ({len(rows)} entries); nothing written")
        return False
    out = refs / f"live-prices-{today}.json"
    out.write_text(body, encoding="utf-8")
    if vault_dir.is_dir():
        (vault_dir / out.name).write_text(body, encoding="utf-8")
        print(f"also wrote {vault_dir / out.name}")

    priced = [r for r in rows if r["priority"] == "normal" and (r["cost"] or 0) > 0]
    priced.sort(key=lambda r: r["cost"], reverse=True)
    print(f"balance ${result['money']['balance']} | {len(rows)} entries -> {out.name}")
    print("\npriciest calls:")
    for row in priced[:8]:
        print(f"  ${row['cost']:<9} {row['cost_type']:<13} {row['endpoint']}")
    print("\ncheapest priced calls:")
    for row in reversed(priced[-8:]):
        print(f"  ${row['cost']:<9} {row['cost_type']:<13} {row['endpoint']}")
    return True


if __name__ == "__main__":
    main()
