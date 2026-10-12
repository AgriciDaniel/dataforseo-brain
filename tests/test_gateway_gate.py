"""The gateway's gate(): guard decisions become refuse/run, asks need confirm_cost, and a daily cap holds."""
import sys
import time
from pathlib import Path

import pytest

pytest.importorskip("mcp")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gateway"))
import dfs_gateway as gw  # noqa: E402

NOW = time.time()


def test_truncating_google_ads_is_refused(monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    verdict, msg, _, rec = gw.gate("kw_data_google_ads_search_volume", {"keywords": ["k%d" % i for i in range(20)]}, "s", NOW, [])
    assert verdict == "refuse" and "nothing was billed" in msg and rec["decision"] == "deny"


def test_site_operator_needs_confirmation_then_runs(monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    args = {"keyword": "site:example.com/page", "location_name": "United States", "language_code": "en"}
    verdict, msg, _, rec = gw.gate("serp_organic_live_advanced", dict(args), "s", NOW, [])
    assert verdict == "refuse" and "confirm_cost" in msg and rec["decision"] == "ask-unconfirmed"
    verdict, _, fwd, rec = gw.gate("serp_organic_live_advanced", dict(args, confirm_cost=True), "s", NOW, [])
    assert verdict == "run" and "confirm_cost" not in fwd and rec["decision"] == "ask-confirmed"


def test_daily_cap(monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    monkeypatch.setattr(gw, "DAILY_CAP", 0.05)
    gw.add_spend(NOW, 0.049)
    verdict, msg, _, rec = gw.gate("dataforseo_labs_google_keyword_overview", {"keywords": ["a", "b"]}, "s", NOW, [])
    assert verdict == "refuse" and "budget" in msg and rec["decision"] == "deny-budget"


def test_limit_is_clamped_and_forwarded(monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    verdict, msg, fwd, rec = gw.gate("dataforseo_labs_google_ranked_keywords", {"target": "example.com", "limit": 500}, "s", NOW, [])
    assert verdict == "run" and fwd["limit"] == 25 and "guard fixed" in msg
