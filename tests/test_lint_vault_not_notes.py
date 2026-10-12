import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint_vault  # noqa: E402


def test_continuity_capsule_is_not_linted_as_a_note(tmp_path, capsys):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "CONTINUITY.md").write_text("# CONTINUITY - wiki\n\nNo frontmatter, a tool file.\n", encoding="utf-8")
    (wiki / "real-note.md").write_text("No frontmatter here either.\n", encoding="utf-8")

    lint_vault.main(["--vault", str(tmp_path)])

    err = capsys.readouterr().err
    assert "missing frontmatter: wiki" in err and "real-note.md" in err
    assert "CONTINUITY.md" not in err
