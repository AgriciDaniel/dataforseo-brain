"""Parameters the OpenAPI spec says multiply the price are held for approval and priced in the estimate."""
import io
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_guard  # noqa: E402

T = "mcp__dataforseo__"


def decide(tool, inp):
    return dfs_guard.decide(T + tool, inp, "s", 0, [])


def test_site_operator_is_held_and_priced_5x():
    inp = {"keyword": "site:example.com", "language_code": "en", "depth": 10}
    decision, reason, _ = decide("serp_organic_live_advanced", inp)
    assert decision == "ask" and "5x" in reason
    assert dfs_guard.estimate("serp_organic_live_advanced", inp) == pytest.approx(0.01)


@pytest.mark.parametrize("keyword", ["website: design ideas", "best site builders", "intitle"])
def test_plain_keywords_are_not_operators(keyword):
    decision, _, _ = decide("serp_organic_live_advanced", {"keyword": keyword, "language_code": "en", "depth": 10})
    assert decision == "allow"


def test_clickstream_flag_is_held_and_doubles_the_estimate():
    inp = {"keywords": ["a"], "limit": 50, "include_clickstream_data": True}
    decision, reason, _ = decide("dataforseo_labs_google_keyword_ideas", inp)
    assert decision == "ask" and "doubles" in reason
    plain = dfs_guard.estimate("dataforseo_labs_google_keyword_ideas", dict(inp, include_clickstream_data=False))
    assert dfs_guard.estimate("dataforseo_labs_google_keyword_ideas", inp) == pytest.approx(2 * plain)


def test_javascript_on_instant_pages_is_held_but_not_on_lighthouse():
    assert decide("on_page_instant_pages", {"url": "https://a.com", "enable_javascript": True})[0] == "ask"
    assert decide("on_page_lighthouse", {"url": "https://a.com", "enable_javascript": True})[0] == "allow"


def test_youtube_block_depth_over_20_is_held():
    decision, reason, _ = decide("serp_youtube_organic_live_advanced",
                                 {"keyword": "a", "location_name": "United States", "language_code": "en", "block_depth": 60})
    assert decision == "ask" and "3 result pages" in reason


def test_people_also_ask_clicks_are_added_to_the_estimate():
    inp = {"keyword": "a", "depth": 10, "people_also_ask_click_depth": 2}
    assert dfs_guard.estimate("serp_organic_live_advanced", inp) == pytest.approx(0.002 + 2 * 0.00015)


def test_an_approved_ask_still_runs_trimmed(monkeypatch, tmp_path):
    """LLM Mentions search at limit 100 asks for approval; the limit-50 trim must ride along as updatedInput."""
    monkeypatch.setattr(dfs_guard, "LOG", str(tmp_path / "log.jsonl"))
    monkeypatch.setattr(dfs_guard, "VAULT_LOG", str(tmp_path / "vault.jsonl"))
    monkeypatch.setattr(sys, "argv", ["dfs_guard.py", "pre"])
    payload = {"session_id": "s", "tool_name": T + "ai_opt_llm_ment_search", "tool_input": {"target": [{"domain": "a.com"}], "limit": 100}}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    out = io.StringIO()
    monkeypatch.setattr(sys, "stdout", out)
    dfs_guard.main()
    hook = json.loads(out.getvalue())["hookSpecificOutput"]
    assert hook["permissionDecision"] == "ask"
    assert hook["updatedInput"]["limit"] == 50 and "limit=50" in hook["permissionDecisionReason"]


@pytest.mark.parametrize("depth,cost", [(10, 0.002), (20, 0.0035), (30, 0.005), (100, 0.0155)])
def test_serp_pages_after_the_first_bill_at_the_measured_rate(depth, cost):
    assert dfs_guard.estimate("serp_organic_live_advanced", {"keyword": "a", "depth": depth}) == pytest.approx(cost)
