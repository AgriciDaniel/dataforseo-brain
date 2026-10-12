import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_safety  # noqa: E402


def fake_api(monkeypatch, tmp_path, body):
    log = tmp_path / "dfs-calls.jsonl"
    monkeypatch.setattr(dfs_safety, "VAULT_LOG", str(log))
    monkeypatch.setenv("DATAFORSEO_LOGIN", "user")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "pass")
    seen = {}

    def urlopen(req, timeout=None):
        seen["url"] = req.full_url
        return io.BytesIO(json.dumps(body).encode())

    monkeypatch.setattr(dfs_safety.urllib.request, "urlopen", urlopen)
    return log, seen


def test_billed_call_is_logged_with_its_exact_cost(monkeypatch, tmp_path):
    log, seen = fake_api(monkeypatch, tmp_path, {"status_code": 20000, "cost": 0.004, "tasks_error": 0})

    dfs_safety.call("https://api.dataforseo.com/v3/serp/google/ai_mode/live/advanced", [{"keyword": "x"}])

    rec = json.loads(log.read_text(encoding="utf-8").strip())
    assert seen["url"].endswith("/v3/serp/google/ai_mode/live/advanced")
    assert rec["phase"] == "rest" and rec["endpoint"] == "serp/google/ai_mode/live/advanced"
    assert rec["cost"] == 0.004 and rec["tasks"] == 1


def test_free_call_is_not_logged(monkeypatch, tmp_path):
    log, _ = fake_api(monkeypatch, tmp_path, {"status_code": 20000, "cost": 0})

    dfs_safety.call(dfs_safety.USER_DATA)

    assert not log.exists()
