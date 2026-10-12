import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint_vault  # noqa: E402

FRONT = b"---\ntype: note\n---\n"


def lint_one(tmp_path, capsys, body: bytes) -> str:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "n.md").write_bytes(FRONT + body)
    lint_vault.main(["--vault", str(tmp_path)])
    return capsys.readouterr().err


@pytest.mark.parametrize("body", [
    "See `D:\\Acme Studio\neports\x826-10-02`.\n".encode(),   # \r and \2026 mangled by shell escaping
    b"pattern \x08clinic\x08\n",                                     # \b turned into a backspace
    b"line one\r\r\nline two\r\r\n",                                 # doubled CRLF conversion
])
def test_escape_damage_fails_the_lint(tmp_path, capsys, body):
    assert "control character" in lint_one(tmp_path, capsys, body)


def test_plain_crlf_and_tabs_pass(tmp_path, capsys):
    assert "control character" not in lint_one(tmp_path, capsys, b"a\r\nb\tc\r\n")
