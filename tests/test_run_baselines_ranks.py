import sys

import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_baselines  # noqa: E402

CLIENT = {"name": "Acme Studio", "domains": ["acme-studio.example", "rival-agency.example"], "location_code": 2840,
          "rank_checks": ["aeo agency"]}


def serp(*urls):
    items = [{"type": "organic", "rank_group": n, "url": u} for n, u in enumerate(urls, 1)]
    return {"cost": 0.004, "tasks": [{"status_code": 20000, "result": [{"items": items}]}]}


def test_finds_the_clients_own_position_not_a_competitors():
    row = run_baselines.score_rank(CLIENT, "aeo agency", serp("https://rival-agency.example/", "https://www.acme-studio.example/services/aeo-agency"))
    assert row["position"] == 2 and row["url"].endswith("/aeo-agency")


def test_not_ranking_is_none():
    assert run_baselines.score_rank(CLIENT, "aeo agency", serp("https://rival-agency.example/"))["position"] is None


def test_estimate_includes_rank_checks():
    base = dict(CLIENT, rank_checks=[])
    assert run_baselines.estimate([CLIENT], ai_mode=False) - run_baselines.estimate([base], ai_mode=False) == pytest.approx(run_baselines.RANK_COST)


def test_payload_asks_for_two_pages():
    assert run_baselines.rank_payload(CLIENT, "aeo agency")[0]["depth"] == 20
