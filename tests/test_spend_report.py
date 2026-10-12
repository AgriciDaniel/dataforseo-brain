"""spend_report: merges logs, separates exact REST spend from connector estimates, flags blocks and bursts."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import spend_report as sr  # noqa: E402


def write(p, rows):
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def test_merge_totals_flags_and_bursts(tmp_path):
    a, b = tmp_path / "vault.jsonl", tmp_path / "server.jsonl"
    write(a, [{"phase": "rest", "t": 100, "ts": "2026-10-04T10:00:00", "source": "scan", "endpoint": "serp/x", "cost": 0.002},
              {"phase": "pre", "t": 200, "ts": "2026-10-04T10:01:00", "endpoint": "kw_data_google_ads_search_volume",
               "decision": "deny", "est": 0.09, "reason": "truncates"},
              {"phase": "rest", "t": 50, "ts": "2026-10-01T10:00:00", "source": "old", "endpoint": "serp/x", "cost": 9}])
    write(b, [{"phase": "pre", "t": 300 + i, "ts": "2026-10-05T09:00:0%d" % i, "endpoint": "serp_organic_live_advanced",
               "decision": "allow", "est": 0.002} for i in range(6)])
    rows = sr.read_logs([a, b], "2026-10-02")
    s = sr.summarize(rows)
    assert s["rest_total"] == 0.002 and s["rest_calls"] == 1          # the 10-01 row is before --since
    assert s["mcp_calls"] == 6 and abs(s["mcp_estimate"] - 0.012) < 1e-9
    assert s["decisions"] == {"deny": 1, "allow": 6} and s["flagged"][0]["endpoint"] == "kw_data_google_ads_search_volume"
    assert s["bursts"] == [("2026-10-05T09:00:00", "serp_organic_live_advanced", 6)]
    text = sr.render(s, "2026-10-02", None)
    assert "**deny**" in text and "x6" in text


def test_v3_prefix_does_not_split_an_endpoint():
    rows = [{"phase": "rest", "ts": "2026-10-02T00:00:00", "t": 1, "endpoint": "/v3/serp/google/organic/live/advanced", "cost": 0.002},
            {"phase": "rest", "ts": "2026-10-02T00:00:00", "t": 2, "endpoint": "serp/google/organic/live/advanced", "cost": 0.002}]
    s = sr.summarize(rows)
    assert s["by_endpoint"]["serp/google/organic/live/advanced"][0] == 2


def test_task_get_echo_rows_are_ignored():
    rows = [{"phase": "rest", "ts": "2026-10-12T00:00:00", "t": 1, "endpoint": "serp/google/organic/task_post", "cost": 0.0945},
            {"phase": "rest", "ts": "2026-10-12T00:00:01", "t": 2, "endpoint": "serp/google/organic/task_get/advanced/x", "cost": 0.0021}]
    assert sr.summarize(rows)["rest_total"] == 0.0945
