import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_endpoints  # noqa: E402


def vault_with(tmp_path, body, folder="flows"):
    note = tmp_path / "wiki" / folder / "play-x.md"
    note.parent.mkdir(parents=True)
    note.write_text(body, encoding="utf-8")
    return tmp_path


def test_catches_the_old_keyword_research_step(tmp_path):
    v = vault_with(tmp_path, "## Endpoints\n- `POST /v3/keywords_data/google_ads/search_volume/live` (ground-truth volume/CPC for the seeds).\n")
    assert any("Google Ads" in f for f in validate_endpoints.routing_issues(v))


def test_catches_the_old_provenance_step(tmp_path):
    v = vault_with(tmp_path, "## Steps\n2. `ai_optimization/{surface}/llm_responses/live` with `web_search: true`.\n")
    assert any("llm_scraper" in f for f in validate_endpoints.routing_issues(v))


def test_accepts_qualified_lines_including_wrapped_sentences(tmp_path):
    v = vault_with(tmp_path, "> Reserve\n> `keywords_data/google_ads/search_volume/live` for cases that\n> need advertiser numbers.\n"
                             "- Perplexity via `llm_responses` (sonar).\n", folder="decisions")
    assert validate_endpoints.routing_issues(v) == []
