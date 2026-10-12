#!/usr/bin/env python3
"""Validate every DataForSEO endpoint claim in a vault against the official OpenAPI spec.

Ground truth: .raw/sources/dataforseo-openapi/openapi_specification.yaml
(immutable, provenance in PROVENANCE.json). Cross-checks the account price
table so legacy-but-billable endpoints are reported rather than failed.

Exit 0 = clean, 1 = unknown endpoints referenced.
"""
import os
import argparse, json, pathlib, re, sys

DEFAULT_VAULT = pathlib.Path(os.environ.get("DFS_BRAIN_VAULT") or pathlib.Path.home() / "Documents" / "DataForSEO Brain" / "vault")
SPEC_REL = pathlib.Path(".raw/sources/dataforseo-openapi/openapi_specification.yaml")
_PRICE_DIRS = (DEFAULT_VAULT / "_attachments",
               pathlib.Path(__file__).resolve().parent.parent / "references")
PRICES = max((f for d in _PRICE_DIRS if d.is_dir() for f in d.glob("live-prices-*.json")),
             key=lambda f: f.name, default=pathlib.Path("missing-live-prices.json"))   # newest table wins

# /v3/... in prose, backticks, tables or code. Also bare module/endpoint forms.
ENDPOINT_RE = re.compile(r"/v3/[a-z0-9_]+(?:/[a-z0-9_{}]+)+")
RETIRED = {
    "/v3/ai_optimization/llm_mentions/search/live": "/v3/ai_optimization/llm_mentions/search_mentions/live",
    "/v3/ai_optimization/llm_mentions/top_domains/live": "/v3/ai_optimization/llm_mentions/top_mentioned_domains/live",
    "/v3/ai_optimization/llm_mentions/top_pages/live": "/v3/ai_optimization/llm_mentions/top_mentioned_pages/live",
    "/v3/ai_optimization/llm_mentions/aggregated_metrics/live": "/v3/ai_optimization/llm_mentions/target_metrics/live",
    "/v3/ai_optimization/llm_mentions/cross_aggregated_metrics/live": "/v3/ai_optimization/llm_mentions/multi_target_metrics/live",
}

# Costly endpoints with a cheap substitute. Calling one is allowed but must be
# a justified choice, not a reflex: google_ads/search_volume was 62% of all
# attributed spend with a ~84% cheaper Labs equivalent.
# See dec-google-ads-vs-labs-keyword-volume.
COSTLY = {
    "/v3/keywords_data/google_ads/search_volume/live": (
        0.09, "/v3/dataforseo_labs/google/keyword_ideas/live", 0.012,
        "only when you need advertiser-reported volume, CPC/competition, or current-month freshness"),
    "/v3/dataforseo_labs/google/historical_rank_overview/live": (
        0.12, "/v3/dataforseo_labs/google/domain_rank_overview/live", 0.012,
        "only when you need the historical series, not the current snapshot"),
}
# llm_responses (the API model, $0.03-0.09 with web search) vs llm_scraper (what users see, $0.004).
# The lead engine spent $1.62 on 21 of these on 2026-09-25; the scraper would have cost $0.08.
# (~$0.0006 with web_search off on a small model, so the flag is about web-search runs.)
_SCRAPER = {"chat_gpt": "/v3/ai_optimization/chat_gpt/llm_scraper/live/advanced",
            "gemini": "/v3/ai_optimization/gemini/llm_scraper/live/advanced"}
for _eng in ("chat_gpt", "gemini", "perplexity", "claude"):
    COSTLY[f"/v3/ai_optimization/{_eng}/llm_responses/live"] = (
        0.077, _SCRAPER.get(_eng, "(no scraper for this engine)"), 0.004,
        "only for the API model's answer, or with web_search off on a small model (~$0.0006)")
CODE_GLOBS = ("*.py", "*.mjs", "*.js", "*.ts")
SKIP_DIRS = {"node_modules", ".venv", "venv", "__pycache__", ".git", "dist", "build"}


def code_files(roots):
    for root in roots:
        files = [root] if root.is_file() else (f for g in CODE_GLOBS for f in root.rglob(g))
        for f in sorted(set(files)):
            if not SKIP_DIRS & set(f.parts) and f.name != pathlib.Path(__file__).name:
                yield f


def mentions(body, ep):
    """Code often drops the /v3/ prefix (BASE_URL + 'ai_optimization/...')."""
    return ep in body or ep[len("/v3/"):] in body

MODULES = ("serp","keywords_data","dataforseo_labs","ai_optimization","business_data",
           "on_page","app_data","merchant","backlinks","domain_analytics",
           "content_analysis","appendix")
ACK_RE = re.compile(r"not in the current OpenAPI spec|returned? `?task_status_code 40402|returns 40402|v1 names \(retired")
# Retired upstream after the spec snapshot was taken (dataforseo.com/updates), so the spec can't flag them.
RETIRED_FAMILIES = {
    "/v3/serp/google/events": "Google Events SERP, deprecated 2026-09-15",
    "/v3/business_data/social_media": "Pinterest / Social Media API, retired 2026-09-16",
}
RETIRED_ACK_RE = re.compile(r"retired|deprecated|removed|ended|discontinued|don't call|do not call", re.I)


ROUTING_RULES = [  # (pattern, qualifiers that make the line acceptable, why)
    (re.compile(r"llm_responses"), re.compile(r"scraper|perplexity|sonar|only|API model|raw|avoid|instead|not |\$0\.0[0-9]|13x|superseded|claude", re.I),
     "llm_responses for routine answers costs ~$0.08 with web search; ChatGPT/Gemini answers belong on llm_scraper ($0.004)"),
    (re.compile(r"google_ads/search_volume|kw_data_google_ads_search_volume"),
     re.compile(r"600|1,000|only|metro|city|DMA|advertiser|\$0\.09|not |avoid|instead|blocked|pricey|costly|reserve", re.I),
     "Google Ads volume is $0.09 a call; under ~600 keywords Labs keyword_overview is cheaper"),
]


def routing_issues(vault):
    """Playbook/decision lines that send agents to the two historically costliest routes without a qualifier."""
    out = []
    base = pathlib.Path(vault).joinpath("wiki")
    for folder in ("flows", "decisions"):
        for md in sorted(base.joinpath(folder).glob("*.md")):
            rel = md.relative_to(vault).as_posix()
            lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
            for i, line in enumerate(lines):
                text = re.sub(r"https?://\S+", "", line)
                window = " ".join(lines[max(0, i - 1):i + 2])   # sentences wrap across lines
                for pat, ok, why in ROUTING_RULES:
                    if pat.search(text) and not ok.search(window):
                        out.append(f"{rel}:{i + 1} {why}")
    return out


def retired_refs(vault):
    """Lines in notes that mention a retired family without saying it is retired."""
    out = []
    for md in sorted(pathlib.Path(vault).joinpath("wiki").rglob("*.md")):
        rel = md.relative_to(vault).as_posix()
        if "/sources/" in rel or rel.endswith(("log.md", "lesson-log.md")) or "archive" in rel:
            continue   # dated records may describe the past
        for no, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            text = re.sub(r"https?://\S+", "", line)
            for fam, why in RETIRED_FAMILIES.items():
                short = fam[len("/v3/"):]
                if (fam in text or short in text) and not RETIRED_ACK_RE.search(line):
                    out.append(f"{rel}:{no} mentions {short} ({why}) without marking it retired")
    return out


PER_ROW_RE = re.compile(r"\b(labs|keyword_overview|keyword_ideas|ranked_keywords|business listings|listings search|backlinks|content analysis|llm mentions)\b", re.I)
FLAT_RE = re.compile(r"\bflat\b|regardless of (?:rows|results|the number of rows)", re.I)
PER_ROW_ACK_RE = re.compile(r"per (?:row|result|keyword returned)|/row|\+ ?\$0\.000|corrected|used to say|said \"flat", re.I)


def flat_price_claims(vault, files=None):
    """Lines that call a per-row endpoint flat-priced. Labs, listings, backlinks, content analysis and LLM Mentions
    all bill a request fee PLUS a per-row fee; "flat" invites oversized pulls (a note said so until 2026-10-04)."""
    out = []
    for md, rel in _notes(vault, files):
        for no, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if PER_ROW_RE.search(line) and FLAT_RE.search(line) and not PER_ROW_ACK_RE.search(line):
                out.append(f"{rel}:{no} calls a per-row endpoint flat-priced")
    return out


TICKED_EP_RE = re.compile(r"`(?:/v3/)?([a-z0-9_]+(?:/[a-z0-9_]+)+)`")


def _notes(vault, files=None):
    """(path, label) pairs: the vault's wiki notes (minus logs, archives, reports), or an explicit file list."""
    if files is not None:
        return [(pathlib.Path(f), str(f)) for f in files]
    out = []
    for md in sorted(pathlib.Path(vault).joinpath("wiki").rglob("*.md")):
        rel = md.relative_to(vault).as_posix()
        if not (rel.endswith(("log.md", "lesson-log.md")) or "archive" in rel or "/reports/" in rel):
            out.append((md, rel))
    return out


def per_row_price_gaps(vault, prices=None, files=None):
    """Lines that price an endpoint by the request alone when it also bills per row (whois and historical Labs
    add $0.0012/row, listings $0.00036/row). The table said "$0.012" for listings while a frame pull paid $0.37."""
    path = pathlib.Path(prices) if prices else PRICES
    if not path.exists():
        return []
    types = {}
    for e in json.loads(path.read_text(encoding="utf-8"))["entries"]:
        if e.get("cost", 0) > 0:
            types.setdefault(e["endpoint"], set()).add(e.get("cost_type"))
    both = {ep for ep, t in types.items() if {"per_request", "per_result"} <= t}
    out = []
    for md, rel in _notes(vault, files):
        for no, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "$" in line and not PER_ROW_ACK_RE.search(line):
                out.extend(f"{rel}:{no} prices `{ep}` per request only; it also bills per row"
                           for ep in TICKED_EP_RE.findall(line) if ep in both)
    return out


RETIRED_CLAIM_RE = re.compile(r"\b(?:retired|deprecated)\b|\bdo(?:n't| not) call\b", re.I)


def false_retirements(vault):
    """Lines that call an endpoint retired or off-limits while the current spec still serves it. A note listed
    Business Listings search as retired; an agent reading it would have routed around a working, cheap API."""
    spec_path = pathlib.Path(vault) / SPEC_REL
    if not spec_path.exists():
        return []
    spec = load_spec(spec_path)
    out = []
    for md in sorted(pathlib.Path(vault).joinpath("wiki").rglob("*.md")):
        rel = md.relative_to(vault).as_posix()
        if rel.endswith(("log.md", "lesson-log.md")) or "archive" in rel:
            continue
        for no, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not RETIRED_CLAIM_RE.search(line):
                continue
            out.extend(f"{rel}:{no} calls {ep} retired, but the OpenAPI spec still serves it"
                       for ep in (e.rstrip("/") for e in ENDPOINT_RE.findall(line))
                       if ep in spec and ep not in RETIRED and not ep.startswith(tuple(RETIRED_FAMILIES)))
    return out


ITEM_TYPE_RE = re.compile(r"`((?:chat_gpt|gemini|perplexity|ai_overview|ai_mode)_[a-z_]+|[a-z_]+_element)`")


def item_type_issues(vault):
    """AI answer item types (`gemini_text`, `ai_overview_shopping`...) that the OpenAPI spec does not define.
    Parsers match on these names, so an invented one means a parser that silently finds nothing."""
    spec_path = pathlib.Path(vault) / SPEC_REL
    if not spec_path.exists():
        return []
    spec = spec_path.read_text(encoding="utf-8")
    out = []
    for md in sorted(pathlib.Path(vault).joinpath("wiki").rglob("*.md")):
        rel = md.relative_to(vault).as_posix()
        if rel.endswith(("log.md", "lesson-log.md")) or "archive" in rel:
            continue
        for no, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            out.extend(f"{rel}:{no} `{t}` is not an item type in the OpenAPI spec"
                       for t in ITEM_TYPE_RE.findall(line) if t not in spec)
    return out
BARE_RE =re.compile(r"`((?:%s)/[a-z0-9_]+(?:/[a-z0-9_]+)*)`" % "|".join(MODULES))


def load_spec(path):
    return {l[2:].rstrip(":\n") for l in path.open(encoding="utf-8") if l.startswith("  /v3/")}


def load_prices():
    if not PRICES.exists():
        return {}, {}
    d = json.loads(PRICES.read_text(encoding="utf-8"))
    billable, known = {}, set()
    for e in d["entries"]:
        ep = "/v3/" + e["endpoint"]
        known.add(ep)
        if e.get("cost", 0) > 0:
            billable[ep] = max(billable.get(ep, 0), e["cost"])
    return known, billable


ENGINES = ("google", "amazon", "bing", "youtube", "apple", "yahoo", "baidu",
           "naver", "seznam", "app_store", "google_play")


def normalise(ep):
    # spec uses {id} style params; claims usually use a literal. Collapse both.
    return re.sub(r"\{[a-z0-9_]+\}", "{}", ep.rstrip("/"))


def resolve(ep, spec_n):
    """Map a written reference onto spec paths.

    The account price table and our prose are engine-agnostic
    (`dataforseo_labs/keyword_ideas/live`) while the spec enumerates every
    engine (`dataforseo_labs/google/keyword_ideas/live`). Billing is per
    endpoint family, not per engine, so a shorthand reference is valid if it
    resolves to one or more concrete spec paths.
    """
    if ep in spec_n:
        return [ep], "exact"
    parts = ep.split("/")            # ['', 'v3', module, ...rest]
    if len(parts) > 3:
        head, rest = parts[:3], parts[3:]
        hits = ["/".join(head + [eng] + rest) for eng in ENGINES
                if "/".join(head + [eng] + rest) in spec_n]
        if hits:
            return hits, "engine-shorthand"
    # trailing _live written as /live (price-table style)
    if ep.endswith("_live"):
        alt = ep[: -len("_live")] + "/live"
        if alt in spec_n:
            return [alt], "suffix-variant"
    # prose often drops the trailing /live
    if not ep.endswith(("/live", "/task_post")):
        hits, how = resolve(ep + "/live", spec_n) if "/live/" not in ep else ([], "")
        if hits:
            return hits, "missing-/live"
    # the spec snapshot lists only the POST side of task endpoints (0 task_get paths);
    # a task_get / tasks_ready / tasks_fixed reference is valid if its task_post exists
    m = re.match(r"(.*)/(task_get(?:/[a-z]+)?(?:/\{\})?|tasks_ready|tasks_fixed)$", ep)
    if m:
        post, _ = resolve(m.group(1) + "/task_post", spec_n)
        if post:
            return post, "task-get (POST side in spec)"
    # docs pages (".../overview") are not endpoints
    if ep.endswith("/overview") and not ep.endswith("whois/overview"):
        return [ep], "docs-page"
    # a module or family prefix (e.g. /v3/serp/youtube) is valid if real endpoints sit under it
    under = [p for p in spec_n if p.startswith(ep + "/")]
    if under:
        return sorted(under), "family-prefix"
    return [], "unresolved"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", type=pathlib.Path, default=DEFAULT_VAULT)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--scripts", type=pathlib.Path, nargs="+",
                    default=[pathlib.Path(__file__).resolve().parent],
                    help="code files or directories to scan for retired/costly endpoint CALLS (py, mjs, js, ts)")
    args = ap.parse_args()

    spec_path = args.vault / SPEC_REL
    if not spec_path.exists():
        sys.exit(f"missing spec: {spec_path}\nrun the OpenAPI ingest first")

    spec = load_spec(spec_path)
    spec_n = {normalise(p) for p in spec}
    priced, billable = load_prices()
    priced_n = {normalise(p) for p in priced}

    refs = {}   # endpoint -> set(files)
    for md in sorted(args.vault.rglob("*.md")):
        if ".raw" in md.parts or ".obsidian" in md.parts:
            continue
        if md.name in ("log.md", "lesson-log.md") or "archive" in md.name or md.name.startswith("reference-hot"):
            continue   # dated records describe past states, not current claims
        text = md.read_text(encoding="utf-8", errors="replace")
        # docs URLs are citations, not endpoint claims; templated paths ({}/{a,b}) are illustrative
        text = re.sub(r"https?://\S+", "", text)
        # lines that already flag a path as invalid, absent or retired are acknowledged, not claims
        text = "\n".join(l for l in text.splitlines() if not (ACK_RE.search(l) or RETIRED_ACK_RE.search(l)))
        found = set(ENDPOINT_RE.findall(text))
        found |= {"/v3/" + m for m in BARE_RE.findall(text)}
        for ep in found:
            if "{" in ep and not re.search(r"/\{(id|task_id)\}$", ep):   # pattern, not a path
                continue
            refs.setdefault(normalise(ep), set()).add(md.relative_to(args.vault).as_posix())

    ok, shorthand, legacy, unknown = [], [], [], []
    for ep, files in sorted(refs.items()):
        hits, how = resolve(ep, spec_n)
        if how == "exact":
            ok.append(ep)
        elif hits:
            shorthand.append((ep, how, len(hits)))
        elif ep in priced_n:
            legacy.append((ep, sorted(files)))
        else:
            unknown.append((ep, sorted(files)))

    costly_used = []
    for src in code_files(args.scripts):
        body = src.read_text(encoding="utf-8", errors="replace")
        for ep, (cost, alt, altcost, when) in COSTLY.items():
            if mentions(body, ep) and "COSTLY-OK" not in body:
                costly_used.append((str(src), ep, cost, alt, altcost, when))

    called_retired = []
    for src in code_files(args.scripts):
        body = src.read_text(encoding="utf-8", errors="replace")
        for old, new in RETIRED.items():
            if mentions(body, old):
                called_retired.append((str(src), old, new))

    if args.json:
        print(json.dumps({"spec_endpoints": len(spec), "referenced": len(refs),
                          "valid": len(ok), "shorthand": shorthand,
                          "legacy": legacy, "unknown": unknown,
                          "retired_in_code": called_retired,
                          "costly_in_code": costly_used}, indent=2))
    else:
        print(f"spec: {len(spec)} endpoints | vault references: {len(refs)} distinct")
        print(f"  valid (exact spec match)  : {len(ok)}")
        print(f"  valid (engine shorthand)  : {len(shorthand)}")
        print(f"  LEGACY (billable, no spec): {len(legacy)}")
        print(f"  UNKNOWN                   : {len(unknown)}")
        for ep, how, n in shorthand:
            print(f"    ok  {ep}  -> {n} spec paths ({how})")
        for ep, files in legacy:
            cost = billable.get(ep)
            tag = f" ${cost}/req" if cost else ""
            print(f"\n  LEGACY {ep}{tag}")
            for f in files:
                print(f"         {f}")
        for ep, files in unknown:
            print(f"\n  UNKNOWN {ep}")
            for f in files:
                print(f"          {f}")

    if not args.json:
        print("")
        if called_retired:
            print("  RETIRED ENDPOINT IN CODE (%d):" % len(called_retired))
            for name, old, new in called_retired:
                print("    %s: %s" % (name, old))
                print("      -> use %s" % new)
        else:
            print("  retired endpoints in code: none")
        if costly_used:
            print("")
            print("  COSTLY ENDPOINT IN CODE (%d) - justify or switch:" % len(costly_used))
            for name, ep, cost, alt, altcost, when in costly_used:
                print("    %s: %s ($%s/req)" % (name, ep, cost))
                if alt.startswith("/v3/"):
                    print("      cheaper: %s ($%s/req, %.0f%% less)" % (alt, altcost, (1-altcost/cost)*100))
                else:
                    print("      cheaper: %s" % alt)
                print("      keep it %s" % when)
                print("      add a COSTLY-OK comment in the file to acknowledge")

    stale = retired_refs(args.vault)
    if not args.json:
        print("  retired families described as live in notes: %d" % len(stale))
        for s in stale:
            print("    " + s)
    return 1 if (unknown or called_retired or stale) else 0


if __name__ == "__main__":
    sys.exit(main())
