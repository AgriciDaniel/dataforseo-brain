import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_endpoints  # noqa: E402

SPEC = """paths:
  /v3/ai_optimization/gemini/llm_scraper/live/advanced:
components:
  mapping:
    gemini_text: '#/x'
    ai_overview_shopping: '#/y'
"""


def vault_with(tmp_path, body):
    spec = tmp_path / validate_endpoints.SPEC_REL
    spec.parent.mkdir(parents=True)
    spec.write_text(SPEC, encoding="utf-8")
    note = tmp_path / "wiki" / "concepts" / "cap-x.md"
    note.parent.mkdir(parents=True)
    note.write_text(body, encoding="utf-8")
    return tmp_path


def test_flags_an_invented_item_type(tmp_path):
    v = vault_with(tmp_path, "Items: `gemini_text`, `gemini_source`.\n")
    issues = validate_endpoints.item_type_issues(v)
    assert len(issues) == 1 and "gemini_source" in issues[0]


def test_accepts_the_spec_names(tmp_path):
    v = vault_with(tmp_path, "AI Mode carries `ai_overview_shopping`; Gemini returns `gemini_text`.\n")
    assert validate_endpoints.item_type_issues(v) == []


def test_flags_a_wrong_element_suffix(tmp_path):
    v = vault_with(tmp_path, "AI Mode carries `ai_overview_shopping_element`.\n")
    assert validate_endpoints.item_type_issues(v)
