#!/usr/bin/env python3
"""Automate the qualitative AI-visibility probe protocol.

llm_mentions counts how often a domain is named. These probes capture what the
answer actually SAYS and which link is served - that is how a dead served host
gets caught. Both are needed; this automates the half that was hand-tabulated
and therefore stopped being run.

Cost: llm_scraper/live/advanced $0.004, llm_responses/live $0.0006 per probe.
A full 5-probe client protocol is about $0.017.

  python scripts/ai_probes.py --client acme --probes probes/acme.json
"""
import argparse, datetime, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dfs_safety

SCRAPER = "/v3/ai_optimization/chat_gpt/llm_scraper/live/advanced"
RESPONSE = "/v3/ai_optimization/chat_gpt/llm_responses/live"  # COSTLY-OK: web_search off on a small model, ~$0.0006 a probe


def run_scraper(keyword, location_code, language_code="en"):
    body = {"keyword": keyword, "location_code": location_code,
            "language_code": language_code, "force_web_search": True}
    d = dfs_safety.call(SCRAPER, [body], timeout=300)
    return d


def run_response(prompt, model_name, web_search=False):
    body = {"user_prompt": prompt, "model_name": model_name, "web_search": web_search}
    d = dfs_safety.call(RESPONSE, [body], timeout=300)
    return d


def _walk_strings(obj, keys, out):
    """Collect every string stored under `keys`, at any depth."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, str) and v.strip():
                out.append(v)
            else:
                _walk_strings(v, keys, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk_strings(v, keys, out)


def answer_text(data):
    """Pull the answer text out of any llm_scraper / llm_responses shape.

    The scraper nests the answer in `markdown` on each item, and items nest
    further items. An earlier version looked only at flat text/answer/content
    keys and silently returned "" for every scraper response, which made every
    "mentioned" check vacuously False. Walk the whole tree instead.
    """
    try:
        result = data["tasks"][0]["result"]
    except (KeyError, IndexError, TypeError):
        return ""
    out = []
    _walk_strings(result, {"markdown", "text", "answer", "content", "message"}, out)
    seen, uniq = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return chr(10).join(uniq)


def sources_of(data):
    try:
        items = (data["tasks"][0]["result"] or [{}])[0].get("items") or []
    except (KeyError, IndexError, TypeError):
        return []
    urls = []
    for it in items:
        for key in ("sources", "citations", "references", "search_results"):
            for s in it.get(key) or []:
                u = s.get("url") or s.get("link") if isinstance(s, dict) else None
                if u:
                    urls.append(u)
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", required=True)
    ap.add_argument("--probes", type=pathlib.Path, required=True,
                    help="JSON: {domain, location_code, queries[], base_model_prompt, model_name}")
    ap.add_argument("--vault", type=pathlib.Path,
                    default=pathlib.Path(dfs_safety.__file__).resolve().parent.parent)
    ap.add_argument("--max-spend", type=float, default=0.10)
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    cfg = json.loads(args.probes.read_text(encoding="utf-8"))
    queries = cfg["queries"]
    estimate = 0.004 * len(queries) + (0.0006 if cfg.get("base_model_prompt") else 0)

    dfs_safety.preflight()
    dfs_safety.guard(estimate, args.max_spend)

    domain = cfg["domain"]
    stamp = datetime.date.today().isoformat()
    spent, rows = 0.0, []

    for q in queries:
        if spent >= args.max_spend:
            print("HARD STOP at $%.4f" % spent, file=sys.stderr)
            break
        d = run_scraper(q, cfg.get("location_code", 2840))
        spent += d.get("cost") or 0
        text = answer_text(d)
        srcs = sources_of(d)
        mentioned = bool(re.search(re.escape(domain.split(".")[0]), text, re.I))
        served = [u for u in srcs if domain.split(".")[0] in u.lower()]
        rows.append({"probe": q, "mentioned": mentioned,
                     "served_links": served[:3], "n_sources": len(srcs),
                     "cost": d.get("cost")})
        print("  %-58s mentioned=%s  sources=%d" % (q[:58], mentioned, len(srcs)))

    base = None
    if cfg.get("base_model_prompt") and spent < args.max_spend:
        d = run_response(cfg["base_model_prompt"], cfg.get("model_name", "gpt-4o-mini"))
        spent += d.get("cost") or 0
        base = {"prompt": cfg["base_model_prompt"], "answer": answer_text(d)[:1500],
                "cost": d.get("cost")}
        print("  base-model probe: %d chars" % len(base["answer"]))

    out = args.out or (args.vault / "wiki" / "reports" /
                       f"rep-ai-probes-{stamp}-{re.sub('[^a-z0-9]+','-',args.client.lower())}.md")
    lines = [f"---\ntype: report\ntitle: \"Report: AI Probes {args.client} {stamp}\"\n"
             f"status: stable\ncreated: {stamp}\nupdated: {stamp}\n"
             f"tags: [dataforseo, ai-optimization, probes]\n---\n",
             f"# AI Probes - {args.client} ({stamp})\n",
             f"Domain `{domain}` - qualitative companion to the llm_mentions series. "
             f"Total spend this run: **${spent:.4f}**.\n",
             "| Probe | Mentioned | Own links served | Sources |", "|---|---|---|---|"]
    for r in rows:
        lines.append("| %s | %s | %s | %d |" % (
            r["probe"], "yes" if r["mentioned"] else "**no**",
            ", ".join(r["served_links"]) or "-", r["n_sources"]))
    if base:
        lines += ["", "## Base model (no web search)", "", "> " +
                  base["answer"].replace("\n", "\n> ")[:1200]]
    lines += ["", "## Related", "- [[lesson-log]]", ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\ntotal $%.4f -> %s" % (spent, out.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
