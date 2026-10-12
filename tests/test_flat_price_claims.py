import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_endpoints  # noqa: E402


def vault_with(tmp_path, body):
    note = tmp_path / "wiki" / "concepts" / "cap-x.md"
    note.parent.mkdir(parents=True)
    note.write_text(body, encoding="utf-8")
    return tmp_path


def test_catches_the_old_labs_claim(tmp_path):
    v = vault_with(tmp_path, "- **Labs is flat $0.012 per request** regardless of rows returned (up to 1,000).\n")
    assert validate_endpoints.flat_price_claims(v)


def test_accepts_the_per_row_statement(tmp_path):
    v = vault_with(tmp_path, "- Labs `keyword_overview` ($0.012 + $0.00012/keyword) beats Google Ads ($0.09 flat).\n")
    assert validate_endpoints.flat_price_claims(v) == []


def test_flat_google_ads_alone_is_fine(tmp_path):
    v = vault_with(tmp_path, "- Google Ads search volume is $0.09 flat per call.\n")
    assert validate_endpoints.flat_price_claims(v) == []
