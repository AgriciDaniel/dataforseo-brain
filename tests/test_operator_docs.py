"""lint_vault lints the rules and agent briefs agents read before calling DataForSEO."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint_vault  # noqa: E402
import validate_endpoints as ve  # noqa: E402


def test_flat_claim_in_operator_rule_is_caught(tmp_path):
    rules = tmp_path / ".claude" / "rules"
    rules.mkdir(parents=True)
    (rules / "dataforseo-spend.md").write_text("- LLM Mentions is $0.10 a call, flat.\n", encoding="utf-8")
    skills = tmp_path / ".claude" / "skills" / "seo-x"
    skills.mkdir(parents=True)
    (skills / "SKILL.md").write_text("Use DataForSEO Labs, flat $0.012 regardless of rows.\n", encoding="utf-8")
    (skills / "other.md").write_text("Unrelated skill, Labs flat.\n", encoding="utf-8")   # no 'dataforseo': skipped
    docs = lint_vault.operator_docs(tmp_path)
    assert len(docs) == 2
    assert len(ve.flat_price_claims(tmp_path, files=docs)) == 2
