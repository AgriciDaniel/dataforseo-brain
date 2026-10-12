"""dfs_safety.call applies the guard to REST: blocks before billing, stops on 402, caps a run, tags the source."""
import io
import json
import sys
import urllib.error
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_safety  # noqa: E402

SERP = "/v3/serp/google/organic/live/advanced"


@pytest.fixture
def api(monkeypatch, tmp_path):
    log = tmp_path / "dfs-calls.jsonl"
    monkeypatch.setattr(dfs_safety, "VAULT_LOG", str(log))
    monkeypatch.setattr(dfs_safety, "_run_spent", 0.0)
    monkeypatch.setenv("DATAFORSEO_LOGIN", "user")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "pass")
    monkeypatch.delenv("DFS_RUN_CAP", raising=False)
    state = {"calls": [], "body": {"status_code": 20000, "cost": 0.002, "tasks_error": 0}, "http": None}

    def urlopen(req, timeout=None):
        state["calls"].append((req.full_url, json.loads(req.data) if req.data else None))
        if state["http"]:
            raise urllib.error.HTTPError(req.full_url, state["http"], "Payment Required", {}, io.BytesIO(b"{}"))
        return io.BytesIO(json.dumps(state["body"]).encode())

    monkeypatch.setattr(dfs_safety.urllib.request, "urlopen", urlopen)
    state["log"] = log
    return state


def test_search_operator_is_blocked_unless_confirmed(api):
    with pytest.raises(dfs_safety.Blocked, match="5x"):
        dfs_safety.call(SERP, [{"keyword": "site:example.com", "location_code": 2840, "depth": 10}])
    assert api["calls"] == []
    dfs_safety.call(SERP, [{"keyword": "site:example.com", "location_code": 2840, "depth": 10}], confirm_cost=True)
    assert len(api["calls"]) == 1


def test_guard_deny_blocks_before_billing(api):
    with pytest.raises(dfs_safety.Blocked, match="Labs"):
        dfs_safety.call("/v3/keywords_data/google_ads/search_volume/live", [{"keywords": ["a", "b"], "location_code": 2840}])
    assert api["calls"] == []


def test_missing_serp_depth_is_set_to_10(api):
    dfs_safety.call(SERP, [{"keyword": "pain relief cream", "location_code": 2840}])
    assert api["calls"][0][1][0]["depth"] == 10


def test_identical_call_within_an_hour_is_blocked(api):
    task = [{"keyword": "pain relief cream", "location_code": 2840, "depth": 10}]
    dfs_safety.call(SERP, task)
    with pytest.raises(dfs_safety.Blocked, match="Identical"):
        dfs_safety.call(SERP, task)
    dfs_safety.call(SERP, task, allow_repeat=True)
    assert len(api["calls"]) == 2


def test_402_stops_the_run(api):
    api["http"] = 402
    with pytest.raises(dfs_safety.OutOfBalance):
        dfs_safety.call(SERP, [{"keyword": "x", "location_code": 2840, "depth": 10}])


def test_run_cap(api, monkeypatch):
    monkeypatch.setenv("DFS_RUN_CAP", "0.003")
    api["body"]["cost"] = 0.002
    dfs_safety.call(SERP, [{"keyword": "a", "location_code": 2840, "depth": 10}])
    with pytest.raises(dfs_safety.Blocked, match="run cap"):
        dfs_safety.call(SERP, [{"keyword": "b", "location_code": 2840, "depth": 10}])
    assert len(api["calls"]) == 1


def test_source_tag_is_logged(api):
    dfs_safety.call(SERP, [{"keyword": "a", "location_code": 2840, "depth": 10}], source="weekly-report")
    rec = json.loads(api["log"].read_text(encoding="utf-8").strip())
    assert rec["source"] == "weekly-report" and rec["hash"]


def test_trailing_slash_is_stripped(api):
    dfs_safety.call("/v3/ai_optimization/llm_mentions/multi_target_metrics/live/",
                    [{"targets": [{"key": "a", "target": [{"domain": "a.com"}]}]}])
    assert not api["calls"][0][0].endswith("/")


def test_task_get_is_never_blocked(api):
    api["body"]["cost"] = 0
    dfs_safety.call("/v3/serp/google/organic/task_get/advanced/abc")
    dfs_safety.call("/v3/serp/google/organic/task_get/advanced/abc")
    assert len(api["calls"]) == 2


def test_task_get_cost_echo_is_not_logged_or_counted(api):
    api["body"]["cost"] = 0.0021      # task_get repeats the task's cost; nothing new is billed
    dfs_safety.call("/v3/serp/google/organic/task_get/advanced/abc")
    assert not api["log"].exists() and dfs_safety._run_spent == 0
