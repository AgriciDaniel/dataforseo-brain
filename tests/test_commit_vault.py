import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_baselines  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout.strip()


def test_commits_new_output_in_a_git_vault(tmp_path):
    git(tmp_path, "init", "-q")
    (tmp_path / "report.md").write_text("x", encoding="utf-8")

    run_baselines.commit_vault(tmp_path, "run: AI visibility test")

    assert git(tmp_path, "log", "--format=%s") == "run: AI visibility test"
    assert git(tmp_path, "status", "--porcelain") == ""


def test_nothing_to_commit_is_quiet(tmp_path, capsys):
    git(tmp_path, "init", "-q")
    run_baselines.commit_vault(tmp_path, "empty")
    assert "WARNING" not in capsys.readouterr().err


def test_vault_without_git_is_left_alone(tmp_path):
    run_baselines.commit_vault(tmp_path, "x")
    assert not (tmp_path / ".git").exists()
