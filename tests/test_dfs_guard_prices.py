"""The guard's cost estimates must track the live price table (catches the next price change)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_guard  # noqa: E402

VAULT_PRICES = (sorted((Path.home() / "Documents" / "DataForSEO Brain" / "vault" / "_attachments").glob("live-prices-*.json"))
                or sorted((Path(__file__).resolve().parents[1] / "references").glob("live-prices-*.json")))

# (tool or api path, payload, price-table endpoint, rows billed)
CASES = [
    ("mcp__x__kw_data_google_ads_search_volume", {"keywords": ["a"] * 700}, "keywords_data/google_ads/search_volume/live", 0),
    ("mcp__x__dataforseo_labs_google_keyword_overview", {"keywords": ["a"] * 100}, "dataforseo_labs/keyword_overview/live", 100),
    ("mcp__x__dataforseo_labs_google_keyword_ideas", {"limit": 50}, "dataforseo_labs/keyword_ideas/live", 50),
    ("mcp__x__business_data_business_listings_search", {"limit": 25}, "business_data/business_listings/search/live", 25),
    ("mcp__x__backlinks_backlinks", {"limit": 50}, "backlinks/backlinks/live", 50),
    ("mcp__x__content_analysis_search", {"limit": 50}, "content_analysis/search/live", 50),
    ("mcp__x__on_page_lighthouse", {}, "on_page/lighthouse/live", 0),
    ("mcp__x__dataforseo_labs_google_historical_rank_overview", {}, "dataforseo_labs/historical_rank_overview/live", 0),
    ("api_request", {"path": "/v3/domain_analytics/technologies/domains_by_technology/live", "data": [{"limit": 100}]},
     "domain_analytics/technologies/domains_by_technology/live", 100),
    ("mcp__x__ai_opt_llm_ment_search", {"limit": 10}, "ai_optimization/llm_mentions/search_mentions/live", 10),
    ("mcp__x__domain_analytics_whois_overview", {"limit": 100}, "domain_analytics/whois/overview/live", 100),
    ("mcp__x__dataforseo_labs_google_serp_competitors", {"limit": 50}, "dataforseo_labs/serp_competitors/live", 50),
    ("api_request", {"path": "/v3/dataforseo_labs/google/categories_for_domain/live", "data": [{"limit": 100}]},
     "dataforseo_labs/categories_for_domain/live", 100),
    ("api_request", {"path": "/v3/app_data/apple/app_listings/search/live", "data": [{"limit": 100}]},
     "app_data/app_listings/search/live", 100),
]


def live_price(table, endpoint, rows):
    req = max((e["cost"] for e in table if e["endpoint"] == endpoint and e["cost_type"] == "per_request"), default=0)
    per = max((e["cost"] for e in table if e["endpoint"] == endpoint and e["cost_type"] == "per_result"), default=0)
    return req + per * rows


@pytest.mark.skipif(not VAULT_PRICES, reason="vault price table not on this machine")
@pytest.mark.parametrize("tool,inp,endpoint,rows", CASES)
def test_estimate_matches_live_price(tool, inp, endpoint, rows):
    table = json.loads(VAULT_PRICES[-1].read_text(encoding="utf-8"))["entries"]
    expected = live_price(table, endpoint, rows)
    ep = dfs_guard.endpoint_of(tool, inp)
    got = dfs_guard.estimate(ep, dfs_guard.payload(tool, inp))
    assert expected > 0, f"{endpoint} missing from the price table"
    assert abs(got - expected) <= max(0.0015, expected * 0.15), f"{ep}: guard ${got:.4f} vs live ${expected:.4f}"


def test_ai_mode_is_priced_above_organic_serp():
    ai = dfs_guard.estimate(dfs_guard.endpoint_of("api_request", {"path": "/v3/serp/google/ai_mode/live/advanced"}), {})
    organic = dfs_guard.estimate("serp_organic_live_advanced", {"depth": 10})
    assert ai == pytest.approx(0.004) and organic == pytest.approx(0.002)


def test_clickstream_global_volume_is_expensive():
    ep = dfs_guard.endpoint_of("api_request", {"path": "/v3/keywords_data/clickstream_data/global_search_volume/live"})
    assert dfs_guard.estimate(ep, {}) == pytest.approx(0.18)


def test_whois_overview_limit_capped():
    """Whois bills $0.0012 a row, the highest per-row rate, and defaults to 100 rows."""
    assert dfs_guard.cap_for("mcp__x__domain_analytics_whois_overview") == 25


def test_lookup_helpers_free_and_paid_lookalikes_not():
    for tool in ("mcp__x__ai_opt_llm_ment_loc_and_lang", "mcp__x__kw_data_google_trends_categories",
                 "mcp__x__serp_locations", "mcp__x__dataforseo_labs_available_filters"):
        assert dfs_guard.base_estimate(tool, {}) == 0.0, tool
    for path in ("/v3/dataforseo_labs/google/categories_for_domain/live",
                 "/v3/ai_optimization/llm_mentions/top_mentioned_brand_categories/live"):
        assert dfs_guard.base_estimate(path, {}) > 0.01, path


def test_no_endpoint_underestimated_by_half():
    """Every billed endpoint in the price table, at 50 rows: the guard may overestimate, never under by 2x+
    (a $0 or SERP-rate estimate on a $0.12 call means the budget ask never fires)."""
    if not VAULT_PRICES:
        pytest.skip("no price table")
    rates = {}
    for e in json.loads(VAULT_PRICES[-1].read_text(encoding="utf-8"))["entries"]:
        if e.get("priority") in ("normal", None) and e.get("cost", 0) > 0:
            r = rates.setdefault(e["endpoint"], {})
            r[e["cost_type"]] = max(r.get(e["cost_type"], 0), e["cost"])
    low = []
    for ep, r in rates.items():
        if not ep.endswith(("live", "live/advanced", "task_post")):
            continue
        if ep.startswith("keywords_data/") and ep.endswith("task_post") and ep.count("/") == 2:
            ep = ep.replace("keywords_data/", "keywords_data/google_ads/")   # the table drops the engine on Google Ads tasks
        true = r.get("per_request", 0) + r.get("per_result", 0) * (50 if r.get("per_request") else 1)
        if dfs_guard.base_estimate("/v3/" + ep, {"limit": 50}) < true / 2:
            low.append(ep)
    assert not low, low


def test_google_ads_small_batch_allowed_below_country():
    """Labs has no city volume; a city-level Google Ads call must not be blocked for being small."""
    assert dfs_guard.below_country({"location_name": "Springfield,Illinois,United States"})
    assert dfs_guard.below_country({"location_code": 1014221})
    assert not dfs_guard.below_country({"location_name": "United States"})
    assert not dfs_guard.below_country({"location_code": 2840})


def test_connector_google_ads_over_ten_keywords_denied():
    """The connector returns 10 items of a Google Ads call and bills all of it."""
    inp = {"keywords": ["k%d" % i for i in range(11)], "location_name": "Springfield,Illinois,United States"}
    decision, msg = dfs_guard.check("mcp__x__kw_data_google_ads_search_volume", inp, {}, 0, [])[:2]
    assert decision == "deny" and "REST" in msg


def test_google_ads_queued_cheaper_than_live():
    """Standard-queue Google Ads volume bills $0.06 a task against $0.09 live (30 tasks billed $1.80, 2026-10-04)."""
    assert dfs_guard.base_estimate("/v3/keywords_data/google_ads/search_volume/task_post", {"keywords": ["a"]}) == 0.06
    assert dfs_guard.base_estimate("/v3/keywords_data/google_ads/search_volume/live", {"keywords": ["a"]}) == 0.09
