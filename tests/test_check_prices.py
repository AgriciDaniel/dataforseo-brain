import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_prices  # noqa: E402

PRICES = {"entries": [
    {"endpoint": "keywords_data/google_ads/search_volume/live", "priority": "normal", "cost_type": "per_request", "cost": 0.09},
    {"endpoint": "dataforseo_labs/keyword_ideas/live", "priority": "normal", "cost_type": "per_request", "cost": 0.012},
    {"endpoint": "dataforseo_labs/keyword_ideas/live", "priority": "normal", "cost_type": "per_result", "cost": 0.00012},
    {"endpoint": "on_page/instant_pages", "priority": "normal", "cost_type": "per_result", "cost": 0.00015},
]}


def make_vault(tmp_path, body, folder="concepts"):
    (tmp_path / "_attachments").mkdir()
    (tmp_path / "_attachments" / "live-prices-2026-10-02.json").write_text(json.dumps(PRICES), encoding="utf-8")
    note = tmp_path / "wiki" / folder / "note.md"
    note.parent.mkdir(parents=True)
    note.write_text(body, encoding="utf-8")
    return tmp_path


def test_flags_old_price_stated_as_current(tmp_path):
    vault = make_vault(tmp_path, "- `google_ads/search_volume` costs $0.075 per call.\n")
    findings = check_prices.check(vault)
    assert len(findings) == 1 and "$0.075" in findings[0] and "$0.09" in findings[0]


def test_accepts_current_price_call_totals_and_rows(tmp_path):
    vault = make_vault(tmp_path, "\n".join([
        "- `google_ads/search_volume` is $0.09; 42 calls cost $3.78.",
        "- `keyword_ideas` $0.012 + $0.00012/row; 340 rows came to $0.053.",
        "- `instant_pages` $0.00015 per page.",
    ]))
    assert check_prices.check(vault) == []


def test_skips_historical_lines_and_dated_reports(tmp_path):
    vault = make_vault(tmp_path, "- `keyword_ideas` was ~$0.0105 in June.\n")
    assert check_prices.check(vault) == []
    report = vault / "wiki" / "reports" / "rep.md"
    report.parent.mkdir()
    report.write_text("- `instant_pages` $0.000125\n", encoding="utf-8")
    assert check_prices.check(vault) == []


def test_skips_lines_comparing_two_endpoints(tmp_path):
    vault = make_vault(tmp_path, "- `google_ads/search_volume` $0.09 vs `keyword_ideas` $0.012\n")
    assert check_prices.check(vault) == []


def test_engineless_keywords_data_task_maps_to_google_ads(tmp_path):
    """The account table lists queued Google Ads volume as keywords_data/search_volume/task_post ($0.06)."""
    import json as _json
    t = tmp_path / "live-prices-2026-10-02.json"
    t.write_text(_json.dumps({"entries": [
        {"endpoint": "keywords_data/google_ads/search_volume/live", "cost_type": "per_request", "cost": 0.09},
        {"endpoint": "keywords_data/search_volume/task_post", "cost_type": "per_request", "cost": 0.06}]}), encoding="utf-8")
    table = check_prices.load_table(t)
    assert 0.06 in table["google_ads/search_volume"]["request"]
