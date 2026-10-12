"""The whole scheduled run, end to end, with every network call mocked: mentions, AI Mode, rank check,
price check, spec check, report, series, report index and the vault commit."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_prices  # noqa: E402
import dfs_safety  # noqa: E402
import refresh_prices  # noqa: E402
import run_baselines  # noqa: E402

CLIENT = {"name": "Acme", "location_code": 2840, "language_code": "en", "brand": "Acme",
          "domains": ["acme.example", "rival.example"], "probes": ["Best widget firm?"], "rank_checks": ["widget firm"]}


def fake_post(payload, url=run_baselines.URL):
    if url == run_baselines.URL:   # LLM Mentions multi_target_metrics
        items = [{"key": d, "total": {"mentions": 5, "ai_search_volume": 50}} for d in CLIENT["domains"]]
        return {"status_code": 20000, "cost": 0.102, "tasks": [{"status_code": 20000, "result": [{"items": items}]}]}
    if url == run_baselines.AI_MODE_URL:
        items = [{"type": "ai_overview", "markdown": "Try **Acme**.", "references": [{"url": "https://acme.example/"}]}]
        return {"status_code": 20000, "cost": 0.004, "tasks": [{"status_code": 20000, "result": [{"items": items}]}]}
    items = [{"type": "organic", "rank_group": 3, "url": "https://acme.example/widgets"}]   # rank check
    return {"status_code": 20000, "cost": 0.0035, "tasks": [{"status_code": 20000, "result": [{"items": items}]}]}


def test_full_run_writes_report_series_and_commit(monkeypatch, tmp_path):
    vault = tmp_path / "vault"
    (vault / "wiki" / "reports").mkdir(parents=True)
    (vault / "_attachments").mkdir()
    (vault / "clients.json").write_text(json.dumps({"clients": [CLIENT]}), encoding="utf-8")
    subprocess.run(["git", "-C", str(vault), "init", "-q"], check=True)

    monkeypatch.setattr(run_baselines, "post", fake_post)
    monkeypatch.setattr(dfs_safety, "preflight", lambda verbose=True: True)
    monkeypatch.setattr(dfs_safety, "guard", lambda est, cap, **kw: 10.0)
    monkeypatch.setattr(refresh_prices, "main", lambda: False)
    monkeypatch.setattr(check_prices, "check", lambda v: [])
    monkeypatch.setattr(run_baselines, "spec_check", lambda v: (["\nOpenAPI spec: current.\n"], False))
    monkeypatch.setattr(run_baselines, "changelog_check", lambda v: ([], False))
    monkeypatch.setattr(sys, "argv", ["run_baselines.py", "--vault", str(vault), "--max-spend", "0.5"])

    assert run_baselines.main() == 0

    report = next((vault / "wiki" / "reports").glob("rep-ai-visibility-*.md")).read_text(encoding="utf-8")
    assert "| acme.example **(client)** | 5 |" in report
    assert "Best widget firm?" in report and "| widget firm | 3 |" in report
    assert "Prices unchanged" in report and "OpenAPI spec: current" in report
    record = json.loads((vault / "_attachments" / "ai-visibility.jsonl").read_text(encoding="utf-8"))
    assert record["ranks"][0]["position"] == 3 and record["ai_mode"][0]["client_named"] is True
    log = subprocess.run(["git", "-C", str(vault), "log", "--format=%s"], capture_output=True, text=True).stdout
    assert log.startswith("run: AI visibility")


def test_price_alert_exits_3(monkeypatch, tmp_path):
    vault = tmp_path / "vault"
    (vault / "wiki" / "reports").mkdir(parents=True)
    (vault / "_attachments").mkdir()
    (vault / "clients.json").write_text(json.dumps({"clients": [dict(CLIENT, probes=[], rank_checks=[])]}), encoding="utf-8")
    monkeypatch.setattr(run_baselines, "post", fake_post)
    monkeypatch.setattr(dfs_safety, "preflight", lambda verbose=True: True)
    monkeypatch.setattr(dfs_safety, "guard", lambda est, cap, **kw: 10.0)
    monkeypatch.setattr(run_baselines, "price_check", lambda v: (["\n## Price check\n", "changed"], True))
    monkeypatch.setattr(run_baselines, "spec_check", lambda v: ([], False))
    monkeypatch.setattr(run_baselines, "changelog_check", lambda v: ([], False))
    monkeypatch.setattr(sys, "argv", ["run_baselines.py", "--vault", str(vault)])
    assert run_baselines.main() == 3
