"""Silent zeros (domain target on a query-side LLM Mentions endpoint) and known parameter traps are denied."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_guard as g  # noqa: E402

NOW = time.time()


def decide(tool, inp):
    return g.decide(tool, inp, "s", NOW, [])


def test_domain_target_on_query_side_endpoint_is_denied():
    inp = {"path": "/v3/ai_optimization/llm_mentions/historical/live",
           "data": [{"target": [{"domain": "example.ca"}], "location_code": 2840}]}
    d, reason, _ = decide("api_request", inp)
    assert d == "deny" and "keyword" in reason and "zeros" in reason


def test_keyword_target_on_query_side_endpoint_passes_the_kind_check():
    inp = {"path": "/v3/ai_optimization/llm_mentions/historical/live",
           "data": [{"target": [{"keyword": "payment processing"}], "location_code": 2840}]}
    d, reason, _ = decide("api_request", inp)
    assert d == "ask"            # LLM Mentions still asks for the price, but not denied


def test_connector_top_domains_with_domain_target_is_denied():
    d, _, _ = decide("mcp__x__ai_opt_llm_ment_top_domains", {"target": [{"domain": "a.com"}]})
    assert d == "deny"


def test_entity_side_endpoint_accepts_domains():
    inp = {"path": "/v3/ai_optimization/llm_mentions/multi_target_metrics/live",
           "data": [{"targets": [{"key": "a", "target": [{"domain": "a.com"}]}]}]}
    d, _, _ = decide("api_request", inp)
    assert d == "ask"


def test_israel_google_ads_with_language_is_denied():
    inp = {"path": "/v3/keywords_data/google_ads/search_volume/live",
           "data": [{"keywords": ["k%d" % i for i in range(700)], "location_code": 2376, "language_code": "he"}]}
    d, reason, _ = decide("api_request", inp)
    assert d == "deny" and "language" in reason


def test_duplicate_tags_type_is_checked():
    inp = {"path": "/v3/on_page/duplicate_tags", "data": [{"id": "x", "type": "duplicate_h1"}]}
    d, reason, _ = decide("api_request", inp)
    assert d == "deny" and "duplicate_title" in reason
