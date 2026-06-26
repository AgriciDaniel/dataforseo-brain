#!/usr/bin/env python3
"""DataForSEO live-test harness — cost-governed authentic fixture capture.

Reads credentials from the environment (DATAFORSEO_USERNAME / DATAFORSEO_PASSWORD),
makes the cheapest representative call per endpoint family, records the real `cost`
returned by the API into a running ledger, and HARD-STOPS at a cumulative cap.

Fixtures are written to .raw/sources/dataforseo-research/<ns>/fixtures/<slug>.json.
Responses contain only public SEO data (no credentials).
"""
from __future__ import annotations
import base64, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

BASE = "https://api.dataforseo.com"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / ".raw" / "sources" / "dataforseo-research"
LEDGER = RAW / "_cost-log.json"
CAP = float(os.environ.get("DFS_COST_CAP", "5.00"))

USER = os.environ.get("DATAFORSEO_USERNAME")
PW = os.environ.get("DATAFORSEO_PASSWORD")
if not USER or not PW:
    print("MISSING credentials in env", file=sys.stderr); sys.exit(2)
AUTH = base64.b64encode(f"{USER}:{PW}".encode()).decode()

US = 2840  # location_code United States
EN = "en"

# (namespace, slug, http_method, path, payload-or-None)  — POST payloads are wrapped in a list.
TESTS = [
    # --- Labs (pre-indexed, cheapest, highest value) ---
    ("labs", "google-keyword-ideas", "POST", "/v3/dataforseo_labs/google/keyword_ideas/live", {"keywords": ["seo tools"], "location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-keyword-suggestions", "POST", "/v3/dataforseo_labs/google/keyword_suggestions/live", {"keyword": "seo", "location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-related-keywords", "POST", "/v3/dataforseo_labs/google/related_keywords/live", {"keyword": "seo", "location_code": US, "language_code": EN, "limit": 5, "depth": 1}),
    ("labs", "google-keyword-overview", "POST", "/v3/dataforseo_labs/google/keyword_overview/live", {"keywords": ["seo tools"], "location_code": US, "language_code": EN}),
    ("labs", "google-bulk-keyword-difficulty", "POST", "/v3/dataforseo_labs/google/bulk_keyword_difficulty/live", {"keywords": ["seo tools"], "location_code": US, "language_code": EN}),
    ("labs", "google-search-intent", "POST", "/v3/dataforseo_labs/google/search_intent/live", {"keywords": ["seo tools"], "language_code": EN}),
    ("labs", "google-ranked-keywords", "POST", "/v3/dataforseo_labs/google/ranked_keywords/live", {"target": "dataforseo.com", "location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-serp-competitors", "POST", "/v3/dataforseo_labs/google/serp_competitors/live", {"keywords": ["seo tools"], "location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-competitors-domain", "POST", "/v3/dataforseo_labs/google/competitors_domain/live", {"target": "dataforseo.com", "location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-domain-rank-overview", "POST", "/v3/dataforseo_labs/google/domain_rank_overview/live", {"target": "dataforseo.com", "location_code": US, "language_code": EN}),
    ("labs", "google-domain-intersection", "POST", "/v3/dataforseo_labs/google/domain_intersection/live", {"target1": "dataforseo.com", "target2": "ahrefs.com", "location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-relevant-pages", "POST", "/v3/dataforseo_labs/google/relevant_pages/live", {"target": "dataforseo.com", "location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-categories-for-domain", "POST", "/v3/dataforseo_labs/google/categories_for_domain/live", {"target": "dataforseo.com", "language_code": EN, "limit": 5}),
    ("labs", "google-top-searches", "POST", "/v3/dataforseo_labs/google/top_searches/live", {"location_code": US, "language_code": EN, "limit": 5}),
    ("labs", "google-bulk-traffic-estimation", "POST", "/v3/dataforseo_labs/google/bulk_traffic_estimation/live", {"targets": ["dataforseo.com"], "location_code": US, "language_code": EN}),
    ("labs", "amazon-related-keywords", "POST", "/v3/dataforseo_labs/amazon/related_keywords/live", {"keyword": "laptop", "location_code": US, "language_code": EN, "limit": 5, "depth": 1}),
    # --- SERP (live advanced, minimal depth) ---
    ("serp", "google-organic", "POST", "/v3/serp/google/organic/live/advanced", {"keyword": "seo tools", "location_code": US, "language_code": EN, "depth": 10}),
    ("serp", "google-maps", "POST", "/v3/serp/google/maps/live/advanced", {"keyword": "coffee shop", "location_code": US, "language_code": EN, "depth": 10}),
    ("serp", "bing-organic", "POST", "/v3/serp/bing/organic/live/advanced", {"keyword": "seo tools", "location_code": US, "language_code": EN, "depth": 10}),
    ("serp", "youtube-organic", "POST", "/v3/serp/youtube/organic/live/advanced", {"keyword": "seo tutorial", "location_code": US, "language_code": EN, "depth": 10}),
    # --- Keywords Data ---
    ("keywords-data", "google-ads-search-volume", "POST", "/v3/keywords_data/google_ads/search_volume/live", {"keywords": ["seo tools", "keyword research"], "location_code": US, "language_code": EN}),
    ("keywords-data", "google-trends-explore", "POST", "/v3/keywords_data/google_trends/explore/live", {"keywords": ["seo"], "location_code": US}),
    ("keywords-data", "dataforseo-trends-explore", "POST", "/v3/keywords_data/dataforseo_trends/explore/live", {"keywords": ["seo"], "location_code": US}),
    ("keywords-data", "clickstream-dfs-search-volume", "POST", "/v3/keywords_data/clickstream_data/dataforseo_search_volume/live", {"keywords": ["seo tools"], "location_code": US, "language_code": EN}),
    # --- Backlinks (live) ---
    ("backlinks", "backlinks-summary", "POST", "/v3/backlinks/summary/live", {"target": "dataforseo.com", "internal_list_limit": 1, "backlinks_status_type": "live"}),
    ("backlinks", "referring-domains", "POST", "/v3/backlinks/referring_domains/live", {"target": "dataforseo.com", "limit": 5, "backlinks_status_type": "live"}),
    ("backlinks", "anchors", "POST", "/v3/backlinks/anchors/live", {"target": "dataforseo.com", "limit": 5, "backlinks_status_type": "live"}),
    ("backlinks", "bulk-ranks", "POST", "/v3/backlinks/bulk_ranks/live", {"targets": ["dataforseo.com"]}),
    ("backlinks", "bulk-spam-score", "POST", "/v3/backlinks/bulk_spam_score/live", {"targets": ["dataforseo.com"]}),
    # --- Domain Analytics ---
    ("domain-analytics", "domain-technologies", "POST", "/v3/domain_analytics/technologies/domain_technologies/live", {"target": "dataforseo.com"}),
    ("domain-analytics", "whois-overview", "POST", "/v3/domain_analytics/whois/overview/live", {"limit": 1, "filters": [["domain", "=", "dataforseo.com"]]}),
    # --- Content Analysis ---
    ("content-analysis", "search", "POST", "/v3/content_analysis/search/live", {"keyword": "dataforseo", "page_type": ["ecommerce", "news", "blogs", "message-boards", "organization"], "limit": 5}),
    ("content-analysis", "summary", "POST", "/v3/content_analysis/summary/live", {"keyword": "dataforseo"}),
    # --- AI Optimization (cheaper endpoints; LLM responses skipped to bound cost) ---
    ("ai-optimization", "ai-keyword-data-search-volume", "POST", "/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live", {"keywords": ["seo tools"], "location_code": US, "language_code": EN}),
    ("ai-optimization", "llm-mentions-search", "POST", "/v3/ai_optimization/llm_mentions/search/live", {"target": {"keyword": "best seo api"}, "limit": 5}),
    # --- Merchant (Google Shopping live) ---
    ("merchant", "google-shopping-products", "POST", "/v3/merchant/google/products/live/advanced", {"keyword": "laptop", "location_code": US, "language_code": EN, "depth": 10}),
    # --- Business Data (indexed listings live) ---
    ("business-data", "business-listings-search", "POST", "/v3/business_data/business_listings/search/live", {"categories": ["restaurant"], "location_coordinate": "40.7128,-74.0060,10", "limit": 1}),
    # --- OnPage (instant single page — cheapest non-crawl) ---
    ("onpage", "instant-pages", "POST", "/v3/on_page/instant_pages", {"url": "https://dataforseo.com/"}),
]


def call(method: str, path: str, payload):
    url = BASE + path
    data = None
    if method == "POST":
        data = json.dumps([payload]).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode())


def main():
    ledger = []
    spent = 0.0
    ok = skipped = failed = 0
    print(f"CAP = ${CAP:.2f}\n")
    for ns, slug, method, path, payload in TESTS:
        if spent >= CAP - 0.05:
            print(f"[CAP] stopping before {ns}/{slug} (spent ${spent:.4f})")
            ledger.append({"ns": ns, "slug": slug, "status": "skipped-cap", "cumulative": round(spent, 6)})
            skipped += 1
            continue
        try:
            resp = call(method, path, payload)
        except Exception as e:  # noqa: BLE001
            print(f"  FAIL {ns}/{slug}: {type(e).__name__} {str(e)[:80]}")
            ledger.append({"ns": ns, "slug": slug, "status": "error", "error": str(e)[:120], "cumulative": round(spent, 6)})
            failed += 1
            continue
        cost = float(resp.get("cost") or 0.0)
        sc = resp.get("status_code")
        t0 = (resp.get("tasks") or [{}])[0]
        tsc = t0.get("status_code")
        spent += cost
        rc = t0.get("result_count")
        # write fixture only on a usable success
        if sc == 20000 and tsc == 20000:
            fx = RAW / ns / "fixtures"
            fx.mkdir(parents=True, exist_ok=True)
            (fx / f"{slug}.json").write_text(json.dumps(resp, indent=1)[:200000], encoding="utf-8")
            ok += 1
            mark = "OK "
        else:
            failed += 1
            mark = "BAD"
        print(f"  {mark} {ns}/{slug:32s} cost=${cost:.4f} cum=${spent:.4f} task_sc={tsc} results={rc}")
        ledger.append({"ns": ns, "slug": slug, "url": path, "status_code": sc, "task_status_code": tsc,
                       "result_count": rc, "cost": round(cost, 6), "cumulative": round(spent, 6)})
    summary = {"cap": CAP, "total_spent": round(spent, 6), "ok": ok, "failed": failed,
               "skipped": skipped, "calls": ledger}
    LEDGER.write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"\n=== DONE ok={ok} failed={failed} skipped={skipped} | TOTAL SPENT ${spent:.4f} / ${CAP:.2f} ===")
    print(f"ledger -> {LEDGER}")


if __name__ == "__main__":
    main()
