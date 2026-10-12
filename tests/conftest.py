import pytest


@pytest.fixture(autouse=True)
def _isolated_operator_home(tmp_path_factory, monkeypatch):
    """lint_vault also lints the operator's rules/agents/skills; tests must not read the real home folder."""
    monkeypatch.setenv("DFS_OPERATOR_HOME", str(tmp_path_factory.mktemp("home")))
