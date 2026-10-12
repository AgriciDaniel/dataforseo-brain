"""Security fixes from the pre-exposure review: api_request shape limits, ask ceiling, daily counter."""
import sys
import time
from pathlib import Path

import pytest

pytest.importorskip("mcp")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gateway"))
import dfs_gateway as gw  # noqa: E402

NOW = time.time()


@pytest.mark.parametrize("args,needle", [
    ({"url": "https://attacker.example/", "method": "POST"}, "`url` is not accepted"),
    ({"path": "/v3/serp/google/organic/live/advanced", "method": "DELETE"}, "method DELETE"),
    ({"path": "/v3/../../etc/passwd"}, "must look like"),
    ({"path": "/v3/serp/google/organic/live/advanced?x=1"}, "must look like"),
    ({"path": "/v3/appendix/webhook_resend"}, "module `appendix`"),
    ({"path": "/v3/serp/google/organic/task_post", "data": [{"keyword": "a"}, {"keyword": "b"}]}, "one task per call"),
    ({"path": "/v3/serp/google/organic/task_post", "data": [{"keyword": "a", "postback_url": "https://x.example"}]}, "callback"),
])
def test_api_request_shapes_refused(args, needle, monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    verdict, msg, _, rec = gw.gate("api_request", dict(args), "s", NOW, [])
    assert verdict == "refuse" and needle in msg and rec["decision"] == "deny-shape"


def test_free_balance_call_allowed(monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    verdict, _, _, _ = gw.gate("api_request", {"path": "/v3/appendix/user_data", "method": "GET"}, "s", NOW, [])
    assert verdict == "run"


def test_costly_ask_refused_even_when_confirmed(monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    args = {"path": "/v3/ai_optimization/llm_mentions/search/live", "data": [{"target": [{"domain": "a.com"}], "limit": 50}],
            "confirm_cost": True}
    verdict, msg, _, rec = gw.gate("api_request", args, "s", NOW, [])
    assert verdict == "refuse" and rec["decision"] == "deny-ask-too-costly"


def test_daily_counter_file(monkeypatch, tmp_path):
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    monkeypatch.setattr(gw, "DAILY_CAP", 0.05)
    gw.add_spend(NOW, 0.049)
    verdict, msg, _, rec = gw.gate("api_request", {"path": "/v3/dataforseo_labs/google/keyword_overview/live",
                                                   "data": [{"keywords": ["a", "b"]}]}, "s", NOW, [])
    assert verdict == "refuse" and rec["decision"] == "deny-budget"
