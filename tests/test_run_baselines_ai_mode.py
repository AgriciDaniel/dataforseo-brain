import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_baselines  # noqa: E402

CLIENT = {"name": "acme-law.example", "brand": "Acme", "location_code": 2124, "language_code": "en",
          "domains": ["acme-law.example", "rival-law.example"], "probes": ["Best charity lawyers in Canada?"]}


def ai_mode_response(markdown, urls, cost=0.002):
    item = {"type": "ai_overview", "markdown": markdown, "references": [{"url": u} for u in urls]}
    return {"status_code": 20000, "cost": cost,
            "tasks": [{"status_code": 20000, "result": [{"items": [{"type": "organic"}, item]}]}]}


def test_ai_mode_payload_uses_client_location():
    assert run_baselines.ai_mode_payload(CLIENT, "q") == [
        {"keyword": "q", "location_code": 2124, "language_code": "en"}]


def test_score_answer_separates_cited_and_named():
    data = ai_mode_response("Consider **Acme** or Rival LLP.",
                            ["https://www.rival-law.example/charity", "https://cra.gc.ca/x"])
    row = run_baselines.score_ai_mode(CLIENT, "q", data)
    assert row == {"probe": "q", "answered": True, "client_named": True, "client_cited": False,
                   "cited": ["rival-law.example"], "cost": 0.002}


def test_citations_found_in_sections_links_and_markdown():
    answer = {"type": "ai_overview", "markdown": "See [Acme](https://acme-law.example/team).", "references": [],
              "items": [{"type": "ai_overview_element", "references": [{"url": "https://rival-law.example/a"}],
                         "links": [{"url": "https://www.acme-law.example/x"}]}]}
    data = {"status_code": 20000, "cost": 0.004,
            "tasks": [{"status_code": 20000, "result": [{"items": [answer]}]}]}
    row = run_baselines.score_ai_mode(CLIENT, "q", data)
    assert row["client_cited"] is True and row["cited"] == ["acme-law.example", "rival-law.example"]


def test_no_ai_answer_is_recorded_as_unanswered():
    data = {"status_code": 20000, "cost": 0.002,
            "tasks": [{"status_code": 20000, "result": [{"items": [{"type": "organic"}]}]}]}
    row = run_baselines.score_ai_mode(CLIENT, "q", data)
    assert row["answered"] is False and row["cited"] == [] and row["client_named"] is False


def test_estimate_counts_ai_mode_probes():
    assert abs(run_baselines.estimate([CLIENT], ai_mode=True) - (0.10 + 0.002 + 0.004)) < 1e-9
    assert abs(run_baselines.estimate([CLIENT], ai_mode=False) - 0.102) < 1e-9
