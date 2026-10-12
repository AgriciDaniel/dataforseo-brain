"""market_scan: plan math, ids saved before polling, re-runs never re-post, and the scoring."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dfs_safety  # noqa: E402
import market_scan as ms  # noqa: E402

CFG = {"areas": {"a": {"ads": 200001, "city": "A,State,United States", "lat": 1, "lng": 2},
                 "b": {"ads": 200002, "city": "B,State,United States", "lat": 3, "lng": 4}},
       "services": {"septic": ["septic pumping", "septic tank pumping"], "roofing": ["roofer"]},
       "econ": {"septic": 4.13}, "top_per_area": 1, "min_searches": 40, "buyer_pairs": 2,
       "buyer_categories": {"septic": ["septic_system_service"]}}


def cfg(tmp_path):
    p = tmp_path / "scan.json"
    p.write_text(json.dumps({**CFG, "out": str(tmp_path / "out")}), encoding="utf-8")
    return ms.load_config(p)


def test_plan_uses_queued_prices(tmp_path):
    steps = ms.plan(cfg(tmp_path))
    assert steps["volume (queued Google Ads, 1 task per area)"] == 0.12
    assert any(k.startswith("buyer counts") and v == round(2 * 0.01236, 4) for k, v in steps.items())


def test_ids_saved_and_rerun_does_not_repost(tmp_path, monkeypatch):
    out = tmp_path / "out"
    out.mkdir()
    posts = []

    def fake_call(path, payload=None):
        if "task_post" in path:
            posts.append(len(payload))
            return {"tasks": [{"status_code": 20100, "id": f"id-{t['tag']}", "data": {"tag": t["tag"]}} for t in payload]}
        return {"tasks": [{"status_code": 20000, "result": []}]}

    monkeypatch.setattr(dfs_safety, "call", fake_call)
    tasks = [{"tag": "a"}, {"tag": "b"}]
    ids = ms.post_once(out, "volume", "/v3/x/task_post", tasks)
    assert json.loads((out / "volume_ids.json").read_text()) == ids
    ms.post_once(out, "volume", "/v3/x/task_post", tasks)
    assert posts == [2]                       # second run posted nothing
    got = ms.collect(out, "volume", "/v3/x/task_get", ids, sleep=lambda s: None)
    assert set(got) == {"a", "b"}


def test_picks_keep_economics_trades_beyond_top_n(tmp_path):
    c = cfg(tmp_path)
    rows = [{"area": "a", "service": "roofing", "vol": 500, "value": 9000, "query": "roofer"},
            {"area": "a", "service": "septic", "vol": 100, "value": 800, "query": "septic pumping"}]
    assert {r["service"] for r in ms.picks(c, rows)} == {"roofing", "septic"}


def test_score_soft_market(tmp_path):
    c = cfg(tmp_path)
    serp = {"result": [{"items": [
        {"type": "local_pack", "rating": {"votes_count": 2}}, {"type": "local_pack", "rating": {"votes_count": 11}},
        {"type": "local_pack", "rating": {"votes_count": 50}},
        {"type": "organic", "domain": "www.yelp.com"}, {"type": "organic", "domain": "weakseptic.com"}]}]}
    rows = [{"area": "a", "service": "septic", "vol": 510, "value": 8700, "query": "septic pumping"}]
    out = ms.score(c, rows, {ms.tag("a", "septic pumping"): serp}, {"weakseptic.com": 40})
    assert out[0]["soft"] is True and out[0]["directories"] == 1 and out[0]["pack"] == [2, 11, 50]


def test_plan_counts_economics_trades_in_serps(tmp_path):
    steps = ms.plan(cfg(tmp_path))
    assert any(k.startswith("SERPs") and v == round(2 * (1 + 1) * 0.0006, 4) for k, v in steps.items())
