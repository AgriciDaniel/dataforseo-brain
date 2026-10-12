"""Per-row endpoints priced per request alone, and live endpoints described as retired."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_endpoints as ve  # noqa: E402

PRICES = {"entries": [
    {"endpoint": "business_data/business_listings/search/live", "priority": "normal", "cost_type": "per_request", "cost": 0.012},
    {"endpoint": "business_data/business_listings/search/live", "priority": "normal", "cost_type": "per_result", "cost": 0.00036},
    {"endpoint": "on_page/instant_pages", "priority": "normal", "cost_type": "per_result", "cost": 0.00015},
]}


def write_note(vault, text):
    (vault / "wiki").mkdir(parents=True, exist_ok=True)
    (vault / "wiki" / "note.md").write_text(text, encoding="utf-8")


def test_per_request_only_price_flagged(tmp_path):
    prices = tmp_path / "live-prices-2026-10-02.json"
    prices.write_text(json.dumps(PRICES), encoding="utf-8")
    write_note(tmp_path, "| `business_data/business_listings/search/live` | **$0.012** |\n"
                         "| `/v3/business_data/business_listings/search/live` | $0.012 + $0.00036/row |\n"
                         "`on_page/instant_pages` costs $0.00015 a page.\n")
    out = ve.per_row_price_gaps(tmp_path, prices)
    assert len(out) == 1 and "note.md:1" in out[0]


def test_live_endpoint_called_retired_flagged(tmp_path):
    spec = tmp_path / ve.SPEC_REL
    spec.parent.mkdir(parents=True)
    spec.write_text("paths:\n  /v3/business_data/business_listings/search/live:\n"
                    "  /v3/business_data/social_media/pinterest/live:\n", encoding="utf-8")
    write_note(tmp_path, "- Retired, don't call: `/v3/business_data/business_listings/search/live`.\n"
                         "- Retired 2026-09-16: `/v3/business_data/social_media/pinterest/live`.\n"
                         "- Extended reviews: `/v3/business_data/business_listings/search/live` is live.\n")
    out = ve.false_retirements(tmp_path)
    assert len(out) == 1 and "note.md:1" in out[0]
