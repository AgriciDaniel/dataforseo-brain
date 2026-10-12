"""dfs_safety.queue posts once, saves ids before polling, and never re-posts on a rerun."""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_safety  # noqa: E402


def test_queue_posts_once_and_collects(monkeypatch, tmp_path):
    monkeypatch.setattr(dfs_safety, "VAULT_LOG", str(tmp_path / "log.jsonl"))
    monkeypatch.setattr(dfs_safety, "_run_spent", 0.0)
    monkeypatch.setenv("DATAFORSEO_LOGIN", "u")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "p")
    posts = []

    def urlopen(req, timeout=None):
        if req.data:
            body = json.loads(req.data)
            posts.append(body)
            out = {"cost": 0.0006 * len(body), "tasks": [{"id": "id-" + t["tag"], "status_code": 20100} for t in body]}
        else:
            tid = req.full_url.rsplit("/", 1)[-1]
            out = {"cost": 0, "tasks": [{"id": tid, "status_code": 20000, "result": [{"keyword": tid}]}]}
        return io.BytesIO(json.dumps(out).encode())

    monkeypatch.setattr(dfs_safety.urllib.request, "urlopen", urlopen)
    tasks = [{"keyword": k, "location_code": 2840, "depth": 10, "tag": k} for k in ("a", "b")]
    ids = tmp_path / "ids.json"
    res = dfs_safety.queue("serp/google/organic/task_post", "serp/google/organic/task_get/advanced/{}", tasks, ids, poll_s=0)
    assert set(res) == {"a", "b"} and len(posts) == 1
    res2 = dfs_safety.queue("serp/google/organic/task_post", "serp/google/organic/task_get/advanced/{}", tasks, ids, poll_s=0)
    assert len(posts) == 1 and set(res2) == {"a", "b"}
