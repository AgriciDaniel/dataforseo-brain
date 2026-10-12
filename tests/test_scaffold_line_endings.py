import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import scaffold_vault  # noqa: E402


def test_crlf_templates_are_written_with_lf(tmp_path):
    src, dest = tmp_path / "src", tmp_path / "dest"
    src.mkdir()
    (src / "README.md").write_bytes(b"# {{name}}\r\n\r\nOpen this folder.\r\n")

    scaffold_vault.copy_template(src, dest, {"{{name}}": "Vault"})

    assert (dest / "README.md").read_bytes() == b"# Vault\n\nOpen this folder.\n"
