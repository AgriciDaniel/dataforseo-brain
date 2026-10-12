#!/usr/bin/env python3
"""DataForSEO call guard (Claude Code PreToolUse / PostToolUse hook).

Every rule here comes from a measured mistake in 689 DataForSEO calls (2026-09-01..10-02):
  - Google Ads search_volume called 109 times with 1-77 keywords (Labs is ~7x cheaper below ~600)
  - 40 calls rate-limited (40202) by 22 calls/minute from parallel subagents
  - 63 results too large to read (Labs/listings limits 40-1000) but billed per result
  - 75 byte-identical repeat calls
  - 12 calls rejected for arrays/numbers passed as strings
  - SERP depth 100 (10 billed pages, $0.0155) where 10 would do; llm_responses where scrapers cost 1/10
  - price multipliers the OpenAPI spec states: SERP search operators (site:, intitle:...) x5,
    Labs include_clickstream_data x2, OnPage JavaScript rendering (measured 12x), YouTube block_depth
Decisions: deny (always wrong, model gets the fix), ask (costly but sometimes right, user decides; any
auto-fix rides along as updatedInput, so an approved call still runs trimmed).
Disable entirely with env DFS_GUARD_OFF=1. Log: ~/.claude/dfs-guard/calls.jsonl (+ brain vault copy).
"""
import hashlib
import json
import math
import os
import re
import sys
import time

STATE = os.environ.get("DFS_GUARD_STATE") or os.path.join(os.path.expanduser("~"), ".claude", "dfs-guard")
LOG = os.path.join(STATE, "calls.jsonl")
VAULT_LOG = os.environ.get("DFS_GUARD_VAULT_LOG") or os.path.join(os.environ.get("DFS_BRAIN_VAULT") or os.path.join(os.path.expanduser("~"), "Documents", "DataForSEO Brain", "vault"), "_attachments", "dfs-calls.jsonl")

CARD = "~/Documents/DataForSEO Brain/vault/wiki/concepts/cap-live-price-table.md"   # cheapest-correct endpoint per job
CONNECTOR_ADS_ITEMS = 10            # the claude.ai connector's Google Ads tool truncates its result to 10 items
GOOGLE_ADS_MIN_KEYWORDS = 600       # below this, Labs keyword_overview is cheaper
RATE_WINDOW_S = 60
RATE_MAX_GOOGLE_ADS, RATE_MAX_OTHER = 10, 30   # Google Ads is rate-limited at 12/min by DataForSEO
REPEAT_DENY_S, REPEAT_ASK_S = 3600, 86400
SESSION_ASK_STEP = 0.50             # ask each time a session's estimated spend crosses another $0.50
SERP_MAX_DEPTH = 20
LIMIT_CAPS = {                      # per-result endpoints; caps keep results readable and cheap
    "ranked_keywords": 25, "domain_intersection": 25, "page_intersection": 25,
    "keyword_suggestions": 50, "keyword_ideas": 50, "related_keywords": 50, "relevant_pages": 50,
    "competitors_domain": 50, "serp_competitors": 50, "subdomains": 50, "historical_serps": 20,
    "business_listings_search": 25, "backlinks_referring_domains": 50, "backlinks_backlinks": 50,
    "backlinks_anchors": 50, "backlinks_domain_pages": 50, "backlinks_competitors": 50,
    "llm_ment_search": 50, "content_analysis_search": 50, "whois_overview": 25,
}
AI_ANSWER_KEYS = ("scraper", "llm_response", "llm_responses")   # repeated runs are deliberate (variance)
LIST_DEFAULT_LIMIT = 100            # what the API returns when limit is omitted
SERP_OPERATOR_RE = re.compile(   # the spec: a keyword with one of these "multiplies the charge per task by 5"
    r"(?:^|\s)(?:allinanchor|allintext|allintitle|allinurl|define|filetype|id|inanchor|info|intext|intitle|inurl|link|related|site):", re.I)
JS_RENDER_ENDPOINTS = ("instant_pages", "content_parsing", "on_page/task_post", "on_page_task_post")   # spec: enable_javascript adds charges
ARRAY_FIELDS = ("keywords", "targets")
NUMBER_FIELDS = ("limit", "depth", "offset", "location_code")


def bare(tool):
    """mcp__<server>__<tool> -> <tool>; api_request is resolved by its path."""
    return tool.split("__")[-1] if tool.startswith("mcp__") else tool


def endpoint_of(tool, inp):
    name = bare(tool)
    if name == "api_request":
        return "api:" + str(inp.get("path", "")).strip("/").replace("/v3/", "").replace("v3/", "")
    return name


def payload(tool, inp):
    """The request body: api_request nests it in data (sometimes a list or a JSON string)."""
    if bare(tool) != "api_request":
        return inp or {}
    data = inp.get("data") or {}
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except ValueError:
            return {}
    if isinstance(data, list):
        data = data[0] if data else {}
    return data if isinstance(data, dict) else {}


def num(v, default=None):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def matches(ep, *keys):
    return any(k in ep for k in keys)


def norm(ep):
    """Tool name or API path -> underscore form without the live/advanced suffix, for suffix matching."""
    e = ep.replace("api:", "").replace("/live/advanced", "").replace("/live", "").replace("/", "_")
    return e.replace("dataforseo_labs_google_", "dataforseo_labs_").replace("business_data_business_listings", "business_listings")


def cap_for(ep):
    if "bulk" in ep:
        return None
    e = norm(ep)
    for key, cap in LIMIT_CAPS.items():
        if e.endswith(key):
            return cap
    return None


def serp_live_cost(pages):
    """Live Google organic: $0.002 for the first 10 results, $0.0015 per further 10 (measured 10-03: 20 = $0.0035, 30 = $0.005)."""
    return 0.002 + 0.0015 * (max(1, pages) - 1)


def is_true(v):
    return v is True or str(v).lower() == "true"


def uses_serp_operator(ep, p):
    return matches(ep, "serp_organic", "serp/google/organic", "serp/google/news", "serp/google/images") \
        and bool(SERP_OPERATOR_RE.search(str(p.get("keyword", ""))))


def renders_js(ep, p):
    return matches(ep, *JS_RENDER_ENDPOINTS) and any(
        is_true(p.get(f)) for f in ("enable_javascript", "enable_browser_rendering", "load_resources", "calculate_keyword_density"))


def multiplier_warning(ep, p):
    """Ask before a parameter that the OpenAPI spec says multiplies the price (spec scan, 2026-10-02)."""
    if uses_serp_operator(ep, p):
        return ("A search operator (site:, inurl:, intitle:...) bills this SERP call 5x: $0.01 instead of $0.002 a page. "
                "For your own sites, Search Console's index data is free. Approve if you need the operator query.")
    if is_true(p.get("include_clickstream_data")):
        return "include_clickstream_data doubles the price of this Labs call. Approve only if you need clickstream-normalised volumes."
    if renders_js(ep, p):
        return ("JavaScript rendering, resource loading and keyword density add charges on OnPage (a rendered crawl measured 12x: "
                "$0.0018 against $0.00015 a page). Approve only for a site that needs JavaScript to show its content.")
    block_depth = num(p.get("block_depth"), 20) or 20
    if matches(ep, "serp_youtube_organic", "serp/youtube/organic") and block_depth > 20:
        pages = math.ceil(block_depth / 20)
        return f"YouTube block_depth={block_depth} bills {pages} result pages of 20 blocks (${0.002 * pages:.3f}). The default 20 covers most checks."
    return None


QUERY_SIDE_LLM_RE = re.compile(r"llm_ment.*(historical|timeseries|top_mentioned|top_domains|top_pages)")
DUPLICATE_TAG_TYPES = ("duplicate_title", "duplicate_description")


def target_elements(p):
    """Every element of target / targets[].target, flattened."""
    out = list(p.get("target") or []) if isinstance(p.get("target"), list) else []
    for t in p.get("targets") or [] if isinstance(p.get("targets"), list) else []:
        if isinstance(t, dict) and isinstance(t.get("target"), list):
            out += t["target"]
    return [e for e in out if isinstance(e, dict)]


def target_kind_problem(ep, p):
    """Query-side LLM Mentions endpoints fed a domain return 20000 Ok, all zeros, fully billed (2026-09-17, $0.20)."""
    if not QUERY_SIDE_LLM_RE.search(ep):
        return None
    els = target_elements(p)
    if els and any("domain" in e for e in els) and not any("keyword" in e for e in els):
        return ("This LLM Mentions endpoint is query-side: it takes a keyword target. A domain target returns "
                "20000 Ok with all zeros and is still billed. Use {'keyword': '...'} here, or multi_target_metrics "
                "(ai_opt_llm_ment_cross_agg_metrics) to measure a domain.")
    return None


def param_gotcha(ep, p):
    """Parameter traps found in past runs; each one failed or returned nothing."""
    israel = p.get("location_code") == 2376 or "israel" in str(p.get("location_name") or "").lower()
    if matches(ep, "google_ads") and israel and (p.get("language_code") or p.get("language_name")):
        return "Google Ads volume for Israel rejects a language; omit language_code/language_name for location 2376."
    if matches(ep, "duplicate_tags") and p.get("type") not in DUPLICATE_TAG_TYPES:
        return f"on_page/duplicate_tags only accepts type {' or '.join(DUPLICATE_TAG_TYPES)}."
    return None


def estimate(ep, p):
    """Rough USD from the 2026-10-02 account price table; used for budget prompts, not billing.
    tests/test_dfs_guard_prices.py compares these against the newest live-prices JSON in the vault.
    Multipliers are the ones the OpenAPI spec states (scan of 2026-10-02)."""
    cost = base_estimate(ep, p)
    if is_true(p.get("include_clickstream_data")):
        cost *= 2
    if renders_js(ep, p):
        cost *= 12     # measured on a 300-page crawl, 2026-09-18 (cap-onpage-hidden-js-cost)
    if uses_serp_operator(ep, p):
        cost *= 5
    return cost + 0.00015 * (num(p.get("people_also_ask_click_depth"), 0) or 0)


FREE_HELPER_RE = re.compile(r"(?:^|[/_])(?:categories|locations|languages|available_filters|filters|llm_models|loc_and_lang)(?:/[a-z]{2})?$")


def is_free_helper(ep):
    """Lookup lists cost nothing. Paid endpoints also contain these words (categories_for_domain is $0.012 + rows,
    top_mentioned_brand_categories $0.10 + rows), so match only a path that ENDS in one and isn't a live call."""
    return "docs_" in ep or (bool(FREE_HELPER_RE.search(ep)) and "/live" not in ep and "brand_categories" not in ep)


def below_country(p):
    """A city, metro (DMA) or state location. Labs is country-only, so Google Ads is the only source of
    local volume there and the 600-keyword Labs rule doesn't apply (it blocked a 4-city market scan, 2026-10-04)."""
    name = str(p.get("location_name") or "")
    code = p.get("location_code")
    return "," in name or (isinstance(code, (int, float)) and code >= 10000)   # country codes are 4 digits (US 2840)


def base_estimate(ep, p):
    n_kw = len(p.get("keywords") or []) if isinstance(p.get("keywords"), list) else 1
    limit = num(p.get("limit"), LIST_DEFAULT_LIMIT)
    if is_free_helper(ep):
        return 0.0
    if matches(ep, "google_ads"):
        per = 0.06 if "task_post" in ep else 0.09     # Standard queue is a third cheaper (measured 2026-10-04)
        return per * max(1, math.ceil(n_kw / 1000))
    if matches(ep, "keywords_data/bing", "kw_data_bing"):
        return 0.09
    if matches(ep, "top_mentioned_brand_categories"):
        return 0.10 + 0.001 * limit
    if matches(ep, "clickstream"):
        return 0.012 + 0.00012 * n_kw if "bulk" in ep else 0.18
    if matches(ep, "llm_ment", "llm_mentions"):
        return 0.10 + 0.001 * limit
    if matches(ep, "llm_response", "llm_responses"):
        return 0.05            # $0.0006 base + model tokens; ~$0.01 small models, ~$0.10 with web search on large ones
    if matches(ep, "scraper"):
        return 0.0012 if "task_post" in ep else 0.004
    if matches(ep, "ai_mode"):
        return 0.0012 if "task_post" in ep else 0.004
    if matches(ep, "serp_competitors"):          # a Labs endpoint; the SERP rule below would price it at $0.002
        return 0.012 + 0.00012 * limit
    if matches(ep, "serp_youtube_organic", "serp/youtube/organic"):
        return 0.002 * max(1, math.ceil((num(p.get("block_depth"), 20) or 20) / 20))   # billed per 20 blocks
    if matches(ep, "serp_organic", "serp/", "serp_"):
        return serp_live_cost(math.ceil((num(p.get("depth"), 10) or 10) / 10))
    if matches(ep, "whois"):
        return 0.12 + 0.0012 * limit          # default 100 rows: $0.24, double the request fee
    if matches(ep, "historical_bulk_traffic_estimation", "domain_metrics_by_categories"):
        n = len(p.get("targets") or []) if isinstance(p.get("targets"), list) else limit
        return 0.12 + 0.0012 * n
    if matches(ep, "app_listings"):
        return 0.10 + 0.001 * limit
    if matches(ep, "historical_rank_overview"):
        return 0.12 + 0.0012 * 10             # no limit field; one row per month returned
    if matches(ep, "keyword_overview", "bulk_keyword_difficulty", "search_intent", "bulk_search_volume"):
        return 0.012 + 0.00012 * n_kw
    if matches(ep, "labs", "dataforseo_labs"):
        return 0.012 + 0.00012 * limit
    if matches(ep, "business_listings"):
        return 0.012 + 0.00036 * limit
    if matches(ep, "backlinks", "content_analysis"):
        return 0.024 + 0.000036 * limit
    if matches(ep, "domains_by_technology", "domains_by_html_terms", "technologies_summary", "aggregation_technologies",
               "technology_stats"):
        return 0.012 + 0.0012 * limit
    if matches(ep, "technologies"):
        return 0.012
    if matches(ep, "merchant_amazon_asin", "merchant/amazon/asin"):
        return 0.0015 if "task_post" in ep else 0.005
    if matches(ep, "merchant_amazon", "merchant/amazon"):
        return 0.0015 if "task_post" in ep else 0.0033
    if matches(ep, "dfs_trends_explore", "dataforseo_trends/explore"):
        return 0.0012
    if matches(ep, "dataforseo_trends/merged_data", "dfs_trends_merged"):
        return 0.006
    if matches(ep, "dfs_trends", "dataforseo_trends"):
        return 0.0024
    if matches(ep, "instant_pages", "content_parsing"):
        return 0.00015
    if matches(ep, "lighthouse"):
        return 0.005
    if matches(ep, "on_page"):
        return 0.00015 * (num(p.get("max_crawl_pages"), 100) or 100)
    return 0.01


def read_log(max_lines=2000):
    try:
        with open(LOG, encoding="utf-8") as f:
            lines = f.readlines()[-max_lines:]
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def append(path, rec):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def call_hash(ep, p):
    return hashlib.sha1((ep + json.dumps(p, sort_keys=True, default=str)).encode()).hexdigest()[:16]


def check(tool, inp, session, now, log):
    """Return (decision, reason) with decision in allow/deny/ask."""
    ep = endpoint_of(tool, inp)
    p = payload(tool, inp)
    if ep.startswith("docs_") or ep.endswith(("locations", "languages", "filters")):
        return "allow", ""

    for f in ARRAY_FIELDS:
        v = p.get(f)
        if isinstance(v, str) and v.strip().startswith("["):
            return "deny", f"`{f}` was sent as a string ('{v[:40]}...'). Pass a JSON array, not a quoted string."
    for f in NUMBER_FIELDS:
        v = p.get(f)
        if isinstance(v, str) and v.strip().lstrip("-").isdigit():
            return "deny", f"`{f}` was sent as the string '{v}'. Pass a number."
    problem = target_kind_problem(ep, p) or param_gotcha(ep, p)
    if problem:
        return "deny", problem

    if matches(ep, "google_ads_search_volume", "google_ads/search_volume"):
        kws = p.get("keywords") if isinstance(p.get("keywords"), list) else []
        if "kw_data_google_ads_search_volume" in ep and len(kws) > CONNECTOR_ADS_ITEMS:
            return "deny", (f"The connector's Google Ads tool returns only {CONNECTOR_ADS_ITEMS} of the {len(kws)} keywords "
                            "but bills the whole call (measured 2026-10-04: 95 sent, 10 back). Use REST: "
                            "dfs_safety.call('/v3/keywords_data/google_ads/search_volume/live', "
                            "[{'keywords': [...], 'location_code': ..., 'language_code': 'en'}]) returns every keyword; "
                            "through the gateway, use api_request with path /v3/keywords_data/google_ads/search_volume/live.")
        if len(kws) < GOOGLE_ADS_MIN_KEYWORDS and not below_country(p):
            return "deny", (f"Google Ads search_volume costs a flat $0.09 per call; with {len(kws)} keywords Labs ($0.012 + $0.00012/keyword) is cheaper. "
                            "Use dataforseo_labs_google_keyword_overview ($0.012 + $0.00012/keyword, up to 700 keywords per call). "
                            f"Use Google Ads only for {GOOGLE_ADS_MIN_KEYWORDS}+ keywords in ONE call (max 1,000). Collect all keywords first, then make one call.")

    patch = {}
    cap = cap_for(ep)
    if cap is not None:
        limit = num(p.get("limit"))
        if limit is None or limit > cap:
            patch["limit"] = cap   # billed per row; 63 oversized results at limits 40-1000 were paid for and unreadable

    if patch:
        p = dict(p, **patch)
    if matches(ep, "serp_organic", "serp/google/organic"):
        if "depth" not in p:
            patch["depth"] = 10    # API default is 100 results = 10 billed pages ($0.0155)
            p = dict(p, depth=10)
        depth = num(p.get("depth"), 10)
        if depth > SERP_MAX_DEPTH:
            return "ask", f"SERP depth={depth} bills {math.ceil(depth / 10)} pages (${serp_live_cost(math.ceil(depth / 10)):.4f}). Top 10-20 is enough for most checks.", patch

    warning = multiplier_warning(ep, p)
    if warning:
        return "ask", warning, patch

    if matches(ep, "llm_response", "llm_responses"):
        return "ask", llm_response_advice(ep, p), patch

    if matches(ep, "llm_ment", "llm_mentions"):
        return "ask", ("LLM Mentions is $0.10 per call plus $0.001 per row. Put several targets in one call (connector: ai_opt_llm_ment_cross_agg_metrics, 2-10 targets; REST: multi_target_metrics) and know which question each call answers."), patch

    if matches(ep, "historical_rank_overview", "whois"):
        return "ask", f"{ep} costs ~${estimate(ep, p):.2f} per call. Approve if needed.", patch

    h = call_hash(ep, p)
    for rec in ([] if matches(ep, *AI_ANSWER_KEYS) else reversed(log)):
        if rec.get("hash") == h and rec.get("phase") == "pre":
            age = now - rec.get("t", 0)
            if age < REPEAT_DENY_S:
                return "deny", (f"Identical {ep} call already made {int(age // 60)} min ago (session {rec.get('session', '?')[:8]}). "
                                "Reuse that result instead of paying again.")
            if age < REPEAT_ASK_S:
                return "ask", f"Identical {ep} call was made {age / 3600:.1f} h ago. Approve only if fresh data is needed.", patch
            break

    is_ads = matches(ep, "google_ads")
    recent = [r for r in log if r.get("phase") == "pre" and now - r.get("t", 0) < RATE_WINDOW_S
              and matches(r.get("endpoint", ""), "google_ads") == is_ads]
    limit_now = RATE_MAX_GOOGLE_ADS if is_ads else RATE_MAX_OTHER
    if len(recent) >= limit_now:
        return "deny", (f"{len(recent)} {'Google Ads' if is_ads else 'DataForSEO'} calls in the last minute (limit {limit_now}/min here; "
                        "DataForSEO rate-limits Google Ads at 12/min). Batch inputs into fewer calls, or have the parent agent make one combined call.")

    spent = sum(r.get("est", 0) for r in log if r.get("phase") == "pre" and r.get("session") == session)
    est = estimate(ep, p)
    if math.floor((spent + est) / SESSION_ASK_STEP) > math.floor(spent / SESSION_ASK_STEP):
        return "ask", f"This session's estimated DataForSEO spend reaches ${spent + est:.2f} with this call (~${est:.3f}). Approve to continue.", patch
    if patch:
        return "modify", "set " + ", ".join(f"{k}={v}" for k, v in patch.items()) + " (per-row billing and readable results; page with `offset` if more rows are truly needed)", patch
    return "allow", ""


def llm_response_advice(ep, p):
    """Name the cheaper route that exists for this model. The per-endpoint connector has a ChatGPT
    scraper tool but no Gemini one, so 'use the scraper' alone sent agents back to llm_responses."""
    model = str(p.get("llm_type") or ep).lower()
    msg = "llm_responses costs ~$0.03-0.09 per answer with web search (~$0.01 without, on a small model). "
    if "gemini" in model:
        return msg + ("For what Gemini users see, the Gemini scraper costs $0.004 but has no tool in the per-endpoint connector: "
                      "POST /v3/ai_optimization/gemini/llm_scraper/live/advanced with scripts/dfs_safety.call (it logs the cost), "
                      "or through api_request where that tool exists.")
    if "chat_gpt" in model or "chatgpt" in model:
        return msg + "For what ChatGPT users see, use the ai_optimization_chat_gpt_scraper tool ($0.004)."
    return msg + "No scraper exists for this model, so this is the only route. Approve if you need the answer."


def decide(tool, inp, session, now, log):
    """check() with a uniform (decision, reason, patch) result."""
    r = check(tool, inp, session, now, log)
    return (r[0], r[1], r[2] if len(r) > 2 else {})


def apply_patch(tool, inp, patch):
    """Write patched fields back into the tool input (api_request keeps them inside data)."""
    if bare(tool) != "api_request":
        return dict(inp, **patch)
    data = inp.get("data")
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except ValueError:
            return inp
    if isinstance(data, list) and data and isinstance(data[0], dict):
        data = [dict(data[0], **patch)] + data[1:]
    elif isinstance(data, dict):
        data = dict(data, **patch)
    return dict(inp, data=data)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"
    if os.environ.get("DFS_GUARD_OFF") == "1":
        return 0
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    tool, inp = data.get("tool_name", ""), data.get("tool_input") or {}
    session, now = data.get("session_id", ""), time.time()
    ep, p = endpoint_of(tool, inp), payload(tool, inp)

    if mode == "post":
        resp = data.get("tool_response")
        text = resp if isinstance(resp, str) else json.dumps(resp, default=str)
        # A large result is replaced by the harness note "Error: result (...) exceeds maximum allowed tokens.
        # Output has been saved to ..." - the API call succeeded (and was billed), so that is not an error.
        saved = "exceeds maximum allowed tokens" in text[:400] and "saved to" in text[:600]
        rec = {"phase": "post", "t": now, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "session": session, "endpoint": ep,
               "hash": call_hash(ep, p), "chars": len(text), "saved_to_file": saved,
               "error": not saved and ('"status_code": 4' in text or "Error" in text[:300])}
        append(LOG, rec)
        append(VAULT_LOG, rec)
        return 0

    decision, reason, patch = decide(tool, inp, session, now, read_log())
    if patch:
        inp = apply_patch(tool, inp, patch)
        p = payload(tool, inp)
    rec = {"phase": "pre", "t": now, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "session": session, "endpoint": ep,
           "hash": call_hash(ep, p), "est": round(estimate(ep, p), 5), "decision": decision,
           "input": {k: (v if not isinstance(v, list) else f"[{len(v)} items]") for k, v in p.items()}}
    if decision != "allow":
        rec["reason"] = (reason or "")[:300]   # kept for the weekly review of false blocks
    if decision != "deny":
        append(LOG, rec)        # denied calls never ran: keep them out of spend and rate counts
    append(VAULT_LOG, rec)
    if decision == "allow":
        return 0
    if decision == "ask" and patch:
        reason += " Approving runs it with " + ", ".join(f"{k}={v}" for k, v in patch.items()) + "."
    if decision in ("deny", "ask"):
        reason += f" Quick card: {CARD}"
    out = {"hookEventName": "PreToolUse", "permissionDecisionReason": "DataForSEO guard: " + reason}
    if decision == "modify":
        out.update(permissionDecision="allow", updatedInput=inp)
    else:
        out["permissionDecision"] = decision
        if decision == "ask" and patch:
            out["updatedInput"] = inp   # without this an approved call ran untrimmed (e.g. LLM Mentions at limit 100, not 50)
    print(json.dumps({"hookSpecificOutput": out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
