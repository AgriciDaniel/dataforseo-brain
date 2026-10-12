import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_prices  # noqa: E402
import refresh_prices  # noqa: E402
import run_baselines  # noqa: E402

PRICE = {"serp": {"live": {"advanced": {"priority_normal": [{"cost_type": "per_request", "cost": 0.002}]}}}}


def fake_fetch(cost):
    price = json.loads(json.dumps(PRICE))
    price["serp"]["live"]["advanced"]["priority_normal"][0]["cost"] = cost
    return lambda: {"status_code": 20000, "tasks": [{"result": [{"price": price, "money": {"balance": 1.0}}]}]}


def setup(monkeypatch, tmp_path, cost):
    vault = tmp_path / "vault"
    (vault / "_attachments").mkdir(parents=True)
    monkeypatch.setenv("DFS_VAULT", str(vault))
    monkeypatch.setattr(refresh_prices, "fetch", fake_fetch(cost))
    monkeypatch.setattr(refresh_prices.pathlib.Path, "resolve", lambda self: tmp_path / "repo" / "scripts" / "x.py", raising=False)
    (tmp_path / "repo" / "references").mkdir(parents=True)
    return vault


def test_unchanged_prices_write_nothing(monkeypatch, tmp_path):
    vault = setup(monkeypatch, tmp_path, 0.002)
    assert refresh_prices.main() is True
    assert refresh_prices.main() is False
    assert len(list((vault / "_attachments").glob("live-prices-*.json"))) == 1


def test_run_alerts_on_changed_prices_or_drift(monkeypatch, tmp_path):
    monkeypatch.setattr(refresh_prices, "main", lambda: False)
    monkeypatch.setattr(check_prices, "check", lambda vault: [])
    lines, alert = run_baselines.price_check(tmp_path)
    assert alert is False and "unchanged" in "".join(lines)

    monkeypatch.setattr(check_prices, "check", lambda vault: ["wiki/x.md:3 serp says $0.003; live: $0.002"])
    lines, alert = run_baselines.price_check(tmp_path)
    assert alert is True and "disagree" in "".join(lines)


def test_a_failed_refresh_never_raises(monkeypatch, tmp_path):
    def boom():
        raise SystemExit("set DATAFORSEO_LOGIN")
    monkeypatch.setattr(refresh_prices, "main", boom)
    lines, alert = run_baselines.price_check(tmp_path)
    assert alert is True and "failed" in "".join(lines)
