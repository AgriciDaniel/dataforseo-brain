"""DFS_BRAIN_VAULT points every script at a vault outside ~/Documents (server runs)."""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def test_env_moves_vault_and_call_log(monkeypatch, tmp_path):
    monkeypatch.setenv("DFS_BRAIN_VAULT", str(tmp_path))
    monkeypatch.delenv("DFS_GUARD_VAULT_LOG", raising=False)
    import dfs_safety, run_baselines, validate_endpoints, check_prices  # noqa: E401
    for m in (dfs_safety, run_baselines, validate_endpoints, check_prices):
        importlib.reload(m)
    assert run_baselines.DEFAULT_VAULT == tmp_path and validate_endpoints.DEFAULT_VAULT == tmp_path
    assert check_prices.DEFAULT_VAULT == tmp_path
    assert Path(dfs_safety.VAULT_LOG) == tmp_path / "_attachments" / "dfs-calls.jsonl"
    monkeypatch.delenv("DFS_BRAIN_VAULT")
    for m in (dfs_safety, run_baselines, validate_endpoints, check_prices):
        importlib.reload(m)
