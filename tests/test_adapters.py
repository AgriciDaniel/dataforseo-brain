"""Tests for the DataForSEO response adapters (importer, synthesis, renderer)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from dataforseo_brain.adapters import (  # noqa: E402
    DataForSEOFormatError,
    load_response,
    normalize_records,
    render_report,
    synthesize_cost_summary,
)

FIXTURE = ROOT / "tests" / "fixtures" / "sample-dataforseo-response.json"


def test_load_and_normalize():
    resp = load_response(FIXTURE)
    records = normalize_records(resp)
    assert len(records) == 1
    rec = records[0]
    assert rec["endpoint"] == "keyword_overview"
    assert rec["task_status_code"] == 20000
    assert rec["cost"] == pytest.approx(0.0105)
    assert rec["target"] == "seo tools"


def test_cost_summary_is_deterministic():
    records = normalize_records(load_response(FIXTURE))
    a = synthesize_cost_summary(records)
    b = synthesize_cost_summary(records)
    assert a == b
    assert a["schema"] == "dataforseo.cost-summary-v1"
    assert a["calls"] == 1
    assert a["ok_calls"] == 1
    assert a["total_cost_usd"] == pytest.approx(0.0105)
    assert a["by_endpoint"]["keyword_overview"] == pytest.approx(0.0105)


def test_render_report_has_wikilinks_and_rollback():
    records = normalize_records(load_response(FIXTURE))
    md = render_report(synthesize_cost_summary(records), records)
    assert "# DataForSEO Cost Scorecard" in md
    assert "[[cap-queue-priority-cost-model]]" in md
    assert "## Rollback" in md
    assert "## Sources" in md
    assert "https://docs.dataforseo.com" in md


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_response(ROOT / "tests" / "fixtures" / "does-not-exist.json")


def test_malformed_envelope_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"not": "a dataforseo envelope"}), encoding="utf-8")
    with pytest.raises(DataForSEOFormatError):
        load_response(bad)


def test_invalid_json_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(DataForSEOFormatError):
        load_response(bad)
