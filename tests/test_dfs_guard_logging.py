"""The guard's log must not count saved-to-file results as errors, and must keep the reason for non-allow decisions."""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_guard  # noqa: E402


def run(monkeypatch, tmp_path, mode, payload):
    log, vault = tmp_path / "log.jsonl", tmp_path / "vault.jsonl"
    monkeypatch.setattr(dfs_guard, "LOG", str(log))
    monkeypatch.setattr(dfs_guard, "VAULT_LOG", str(vault))
    monkeypatch.setattr(sys, "argv", ["dfs_guard.py", mode])
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    dfs_guard.main()
    return [json.loads(l) for l in vault.read_text(encoding="utf-8").splitlines()]


def test_saved_to_file_is_not_an_error(monkeypatch, tmp_path):
    note = ("Error: result (223,760 characters across 8,076 lines) exceeds maximum allowed tokens. "
            "Output has been saved to C:\\x\\tool-results\\a.txt.")
    rec = run(monkeypatch, tmp_path, "post", {"session_id": "s", "tool_name": "mcp__x__dataforseo_labs_google_keyword_overview",
                                              "tool_input": {"keywords": ["a"]}, "tool_response": note})[-1]
    assert rec["saved_to_file"] is True and rec["error"] is False


def test_api_error_is_still_an_error(monkeypatch, tmp_path):
    rec = run(monkeypatch, tmp_path, "post", {"session_id": "s", "tool_name": "mcp__x__serp_organic_live_advanced",
                                              "tool_input": {"keyword": "a"}, "tool_response": '{"status_code": 40501}'})[-1]
    assert rec["error"] is True


def test_deny_keeps_its_reason(monkeypatch, tmp_path):
    rec = run(monkeypatch, tmp_path, "pre", {"session_id": "s", "tool_name": "mcp__x__kw_data_google_ads_search_volume",
                                             "tool_input": {"keywords": ["a", "b"]}})[-1]
    assert rec["decision"] == "deny" and "Labs" in rec["reason"]
