import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint_vault  # noqa: E402

REPO_GUARD = Path(lint_vault.__file__).resolve().parent / "dfs_guard.py"


def test_identical_copy_is_fine(tmp_path):
    installed = tmp_path / "dfs_guard.py"
    installed.write_bytes(REPO_GUARD.read_bytes())
    assert lint_vault.stale_hook_copy(installed) is None


def test_stale_copy_is_flagged(tmp_path):
    installed = tmp_path / "dfs_guard.py"
    installed.write_bytes(REPO_GUARD.read_bytes() + b"\n# old\n")
    assert "differs" in lint_vault.stale_hook_copy(installed)


def test_no_installed_hook_is_fine(tmp_path):
    assert lint_vault.stale_hook_copy(tmp_path / "missing.py") is None
