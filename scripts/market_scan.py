#!/usr/bin/env python3
"""Lead-gen market scan: which town x trade pairs a landing page + Business Profile can win.

    python market_scan.py plan --config scan.json            # cost of every step, nothing billed
    python market_scan.py run  --config scan.json --max-spend 2.50

Everything billable goes through the Standard queue where one exists, task ids are saved before
polling (a re-run collects, never re-buys), and buyer counts are bought only for the top pairs.
Spend rules: fix the full keyword list first (Google Ads bills per location, not per keyword), queue
everything, and buy buyer counts only for pairs you will act on.

Config (JSON):
  out: output folder
  areas: {key: {"ads": google_ads_location_code, "city": "Name,State,United States",
                "lat": .., "lng": ..}}            # ads code: DMA or county for small towns
  services: {service: [keywords...]}              # all keywords go in every area's task
  buyer_categories: {service: [business listing categories...]}   # optional
  econ: {service: weight}                         # optional trade economics, 1-5
  top_per_area: 8, min_searches: 40, buyer_pairs: 25, radius_km: 40
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dfs_safety  # noqa: E402

ADS_TASK, SERP_TASK, COUNT, RANKS_REQ, RANKS_ROW = 0.06, 0.0006, 0.01236, 0.024, 0.000036
LABS_REQ, LABS_ROW = 0.012, 0.00012
DIRECTORIES = ("yelp", "angi", "homeadvisor", "thumbtack", "bbb.org", "houzz", "homeguide", "nextdoor", "facebook",
               "yellowpages", "porch", "networx", "fixr", "forbes", "mapquest", "reddit", "youtube", "wikipedia",
               "indeed", "lowes", "homedepot", "bark.com", "instagram", "linkedin", "superpages", "manta")


def load_config(path: pathlib.Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg.setdefault("top_per_area", 8)
    cfg.setdefault("min_searches", 40)
    cfg.setdefault("buyer_pairs", 25)
    cfg.setdefault("radius_km", 40)
    cfg["out"] = pathlib.Path(cfg.get("out") or path.with_suffix("")).expanduser()
    return cfg


def keywords(cfg: dict) -> list[str]:
    seen = []
    for ks in cfg["services"].values():
        seen += [k for k in ks if k not in seen]
    return seen


def plan(cfg: dict) -> dict[str, float]:
    """Upper-bound cost per step. SERPs assume every service x area clears the demand floor."""
    n_areas, n_kw = len(cfg["areas"]), len(keywords(cfg))
    if n_kw > 1000:
        raise SystemExit("more than 1,000 keywords: split the services list")
    serps = n_areas * (cfg["top_per_area"] + len(cfg.get("econ") or {}))   # picks add every economics trade
    steps = {
        "volume (queued Google Ads, 1 task per area)": n_areas * ADS_TASK,
        "national CPC fallback (Labs keyword_overview)": LABS_REQ + LABS_ROW * n_kw,
        f"SERPs (queued, up to {serps})": serps * SERP_TASK,
        "domain strength (bulk_ranks, ~6 domains per SERP)": RANKS_REQ + RANKS_ROW * serps * 6,
        f"buyer counts (top {cfg['buyer_pairs']} pairs)": cfg["buyer_pairs"] * COUNT if cfg.get("buyer_categories") else 0.0,
    }
    return {k: round(v, 4) for k, v in steps.items()}


# ---- queue helpers -------------------------------------------------------------------------------
def post_once(out: pathlib.Path, name: str, path: str, tasks: list[dict]) -> dict[str, str]:
    ids_file = out / f"{name}_ids.json"
    ids = json.loads(ids_file.read_text(encoding="utf-8")) if ids_file.exists() else {}
    todo = [t for t in tasks if t["tag"] not in ids]
    for i in range(0, len(todo), 100):
        data = dfs_safety.call(path, todo[i:i + 100])
        for t in data.get("tasks") or []:
            tag = (t.get("data") or {}).get("tag")
            if t.get("status_code") == 20100 and tag:
                ids[tag] = t["id"]
            else:
                print(f"post failed {tag}: {t.get('status_code')} {t.get('status_message')}", file=sys.stderr)
        ids_file.write_text(json.dumps(ids, indent=1), encoding="utf-8")   # saved before any polling
    return ids


def collect(out: pathlib.Path, name: str, get_path: str, ids: dict[str, str], wait_s: int = 1800,
            sleep=time.sleep) -> dict[str, dict]:
    d = out / name
    d.mkdir(parents=True, exist_ok=True)
    pending = {t: i for t, i in ids.items() if not (d / f"{t}.json").exists()}
    deadline = time.time() + wait_s
    while pending and time.time() < deadline:
        for tag, tid in list(pending.items()):
            task = (dfs_safety.call(f"{get_path}/{tid}").get("tasks") or [{}])[0]
            if task.get("status_code") == 20000:
                (d / f"{tag}.json").write_text(json.dumps(task), encoding="utf-8")
                del pending[tag]
            elif task.get("status_code") not in (40601, 40602):
                print(f"{tag}: {task.get('status_code')} {task.get('status_message')}", file=sys.stderr)
                del pending[tag]
        if pending:
            sleep(30)
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in d.glob("*.json")}


# ---- analysis --------------------------------------------------------------------------------------
def service_rows(cfg: dict, volume: dict[str, dict], national_cpc: dict[str, float]) -> list[dict]:
    service_of = {k: s for s, ks in cfg["services"].items() for k in ks}
    rows = []
    for area, task in volume.items():
        agg = {}
        for it in task.get("result") or []:
            kw, vol = it["keyword"], it.get("search_volume") or 0
            cpc = it.get("cpc") or national_cpc.get(kw, 0)
            a = agg.setdefault(service_of[kw], {"vol": 0, "value": 0.0, "best": (0, kw)})
            a["vol"] += vol
            a["value"] += vol * cpc
            a["best"] = max(a["best"], (vol, kw))
        rows += [{"area": area, "service": s, "vol": a["vol"], "value": round(a["value"]), "query": a["best"][1]}
                 for s, a in agg.items()]
    return rows


def picks(cfg: dict, rows: list[dict]) -> list[dict]:
    """Top services per area by value, plus every economics-listed trade above the demand floor
    (ranking by click value alone missed septic, wells and excavation on the first run)."""
    out, econ = [], cfg.get("econ") or {}
    for area in cfg["areas"]:
        mine = [r for r in rows if r["area"] == area and r["vol"] >= cfg["min_searches"]]
        top = sorted(mine, key=lambda r: -r["value"])[:cfg["top_per_area"]]
        out += top + [r for r in mine if r["service"] in econ and r not in top]
    return out


def parse_serp(task: dict) -> dict:
    items = ((task.get("result") or [{}])[0].get("items")) or []
    organic = [i for i in items if i.get("type") == "organic"]
    local = [o["domain"].removeprefix("www.") for o in organic
             if not any(d in (o.get("domain") or "") for d in DIRECTORIES)]
    packs = [i for i in items if i.get("type") == "local_pack"][:3]
    return {"local": local, "dirs": len(organic) - len(local),
            "pack": sorted(((p.get("rating") or {}).get("votes_count") or 0) for p in packs)}


def score(cfg: dict, rows: list[dict], serps: dict[str, dict], ranks: dict[str, int]) -> list[dict]:
    econ, out = cfg.get("econ") or {}, []
    for r in rows:
        task = serps.get(tag(r["area"], r["query"]))
        if not task:
            continue
        s = parse_serp(task)
        pack_med = statistics.median(s["pack"]) if s["pack"] else 0
        org = [ranks.get(d, 0) for d in s["local"]]
        org_med = statistics.median(org) if org else 0
        difficulty = max(1 + pack_med / 25 + org_med / 100 - 0.05 * s["dirs"], 0.5)
        weight = (econ.get(r["service"], 4) / 4) ** 3
        out.append({**r, "pack": s["pack"], "organic_median": org_med, "directories": s["dirs"],
                    "soft": pack_med < 30 and org_med < 250, "score": round(r["value"] / difficulty * weight)})
    return sorted(out, key=lambda x: -x["score"])


def tag(area: str, kw: str) -> str:
    return f"{area}__{kw.replace(' ', '_')}"


# ---- run -------------------------------------------------------------------------------------------
def run(cfg: dict, max_spend: float) -> list[dict]:
    out = cfg["out"]
    out.mkdir(parents=True, exist_ok=True)
    est = sum(plan(cfg).values())
    dfs_safety.guard(est, max_spend)
    kws = keywords(cfg)

    nat_file = out / "labs_national.json"
    if not nat_file.exists():
        data = dfs_safety.call("/v3/dataforseo_labs/google/keyword_overview/live",
                               [{"keywords": kws, "location_code": 2840, "language_code": "en"}])
        nat_file.write_text(json.dumps(data), encoding="utf-8")
    items = json.loads(nat_file.read_text(encoding="utf-8"))["tasks"][0]["result"][0]["items"] or []
    national = {i["keyword"]: (i.get("keyword_info") or {}).get("cpc") or 0 for i in items}

    ids = post_once(out, "volume", "/v3/keywords_data/google_ads/search_volume/task_post",
                    [{"keywords": kws, "location_code": a["ads"], "language_code": "en", "tag": k}
                     for k, a in cfg["areas"].items()])
    volume = collect(out, "volume", "/v3/keywords_data/google_ads/search_volume/task_get", ids)
    chosen = picks(cfg, service_rows(cfg, volume, national))

    ids = post_once(out, "serp", "/v3/serp/google/organic/task_post",
                    [{"keyword": r["query"], "location_name": cfg["areas"][r["area"]]["city"], "language_code": "en",
                      "depth": 10, "tag": tag(r["area"], r["query"])} for r in chosen])
    serps = collect(out, "serp", "/v3/serp/google/organic/task_get/advanced", ids)

    ranks_file = out / "ranks.json"
    ranks = json.loads(ranks_file.read_text(encoding="utf-8")) if ranks_file.exists() else {}
    todo = sorted({d for t in serps.values() for d in parse_serp(t)["local"]} - set(ranks))
    for i in range(0, len(todo), 1000):
        data = dfs_safety.call("/v3/backlinks/bulk_ranks/live", [{"targets": todo[i:i + 1000]}])
        ranks.update({it["target"]: it.get("rank") or 0 for it in data["tasks"][0]["result"][0]["items"]})
        ranks_file.write_text(json.dumps(ranks), encoding="utf-8")

    scored = score(cfg, chosen, serps, ranks)
    if cfg.get("buyer_categories"):
        buyers(cfg, out, scored[:cfg["buyer_pairs"]])
    (out / "scores.json").write_text(json.dumps(scored, indent=1), encoding="utf-8")
    return scored


def buyers(cfg: dict, out: pathlib.Path, rows: list[dict]) -> None:
    """Contractors per trade near each top pair: one search count per pair (aggregation is not a substitute)."""
    d = out / "counts"
    d.mkdir(exist_ok=True)
    for r in rows:
        cats = cfg["buyer_categories"].get(r["service"])
        f = d / f"{r['area']}__{r['service'].replace(' ', '_').replace('/', '_')}.json"
        if not cats or f.exists():
            continue
        a = cfg["areas"][r["area"]]
        task = dfs_safety.call("/v3/business_data/business_listings/search/live",
                               [{"categories": cats, "location_coordinate": f"{a['lat']},{a['lng']},{cfg['radius_km']}",
                                 "limit": 1}])["tasks"][0]
        f.write_text(json.dumps(task), encoding="utf-8")
    for r in rows:
        f = d / f"{r['area']}__{r['service'].replace(' ', '_').replace('/', '_')}.json"
        if f.exists():
            r["buyers"] = ((json.loads(f.read_text(encoding="utf-8")).get("result") or [{}])[0] or {}).get("total_count")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", choices=["plan", "run"])
    ap.add_argument("--config", type=pathlib.Path, required=True)
    ap.add_argument("--max-spend", type=float, default=0.0)
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    steps = plan(cfg)
    for k, v in steps.items():
        print(f"  ${v:>7.3f}  {k}")
    print(f"  ${sum(steps.values()):>7.3f}  total upper bound ({len(cfg['areas'])} areas, {len(keywords(cfg))} keywords)")
    if args.command == "plan":
        return 0
    if args.max_spend <= 0:
        raise SystemExit("run needs --max-spend (the plan total above is the upper bound)")
    for r in run(cfg, args.max_spend)[:20]:
        print(f"{r['score']:>6}  {r['area']:<16} {r['query']:<28} {r['vol']:>5}/mo ${r['value']:>6}  pack {r['pack']}"
              f"  org {r['organic_median']:.0f}  buyers {r.get('buyers', '-')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
