"""The JSON-lines bridge and its Node client refuse a guarded call before any network request."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import dfs_bridge  # noqa: E402

UNBATCHED_ADS = {"path": "keywords_data/google_ads/search_volume/live",
                 "payload": [{"keywords": ["a", "b"], "location_code": 2840}]}


def test_bridge_reports_blocked(monkeypatch):
    monkeypatch.setenv("DATAFORSEO_LOGIN", "u")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "p")
    reply = dfs_bridge.handle(UNBATCHED_ADS)
    assert reply["ok"] is False and reply["kind"] == "blocked" and "Labs" in reply["error"]


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_node_client_throws_dfs_stop(tmp_path):
    script = tmp_path / "t.mjs"
    client = (SCRIPTS / "dfs_safety.mjs").as_uri()
    script.write_text(
        f'import {{ dfsCall, closeDfs, DfsStop }} from "{client}";\n'
        f'try {{ await dfsCall("{UNBATCHED_ADS["path"]}", {json.dumps(UNBATCHED_ADS["payload"])}, {{ source: "test" }}); '
        'console.log("BILLED"); } catch (e) { console.log(e instanceof DfsStop ? "STOP:" + e.kind : "ERR:" + e.message); }\n'
        "closeDfs();\n", encoding="utf-8")
    env = dict(os.environ, DATAFORSEO_LOGIN="u", DATAFORSEO_PASSWORD="p", DFS_PYTHON=sys.executable,
               DFS_GUARD_VAULT_LOG=str(tmp_path / "log.jsonl"))
    out = subprocess.run(["node", str(script)], capture_output=True, text=True, timeout=60, env=env)
    assert out.stdout.strip() == "STOP:blocked", out.stdout + out.stderr
