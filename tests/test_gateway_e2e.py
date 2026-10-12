"""The whole gateway over HTTP against a stub upstream: handshake, tools/list, a refused call, a fixed call."""
import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("mcp")
from starlette.testclient import TestClient  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "gateway"))
import dfs_gateway as gw  # noqa: E402

TOKEN = "t" * 32
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}


def rpc(client, id_, method, params=None):
    r = client.post(f"/mcp/{TOKEN}/", headers=HEADERS,
                    json={"jsonrpc": "2.0", "id": id_, "method": method, "params": params or {}})
    assert r.status_code == 200, r.text
    return r.json()["result"]


def test_gateway_end_to_end(monkeypatch, tmp_path):
    monkeypatch.setenv("DFS_GATEWAY_TOKEN", TOKEN)
    monkeypatch.setenv("DFS_GATEWAY_ALLOWED_HOSTS", "testserver")
    monkeypatch.setenv("DFS_GATEWAY_UPSTREAM", f'"{sys.executable}" "{ROOT / "tests" / "fixtures" / "stub_dfs_server.py"}"')
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    monkeypatch.setattr(gw.guard, "VAULT_LOG", str(tmp_path / "vault-calls.jsonl"))
    with TestClient(gw.make_app()) as client:
        assert client.get(f"/health/{TOKEN}").json() == {"ok": True, "tools": 2}
        assert client.get("/health/wrong").status_code == 404
        assert client.get("/mcp/" + "x" * 32 + "/").status_code == 404
        r = client.post(f"/mcp/{TOKEN}", headers=HEADERS, json={"jsonrpc": "2.0", "id": 9, "method": "tools/list"},
                        follow_redirects=False)
        assert r.status_code == 200 and "location" not in r.headers   # no slash redirect leaking the token
        bad = client.post(f"/mcp/{TOKEN}/", headers=dict(HEADERS, Host="evil.example"),
                          json={"jsonrpc": "2.0", "id": 8, "method": "tools/list"})
        assert bad.status_code in (400, 403, 421)   # DNS-rebinding protection
        rpc(client, 1, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                      "clientInfo": {"name": "test", "version": "1"}})
        tools = rpc(client, 2, "tools/list")["tools"]
        assert {t["name"] for t in tools} == {"kw_data_google_ads_search_volume", "dataforseo_labs_google_ranked_keywords"}
        assert all("confirm_cost" in t["inputSchema"]["properties"] for t in tools)

        refused = rpc(client, 3, "tools/call", {"name": "kw_data_google_ads_search_volume",
                                                "arguments": {"keywords": ["k%d" % i for i in range(20)]}})
        assert "nothing was billed" in refused["content"][0]["text"]

        fixed = rpc(client, 4, "tools/call", {"name": "dataforseo_labs_google_ranked_keywords",
                                              "arguments": {"target": "example.com", "limit": 500}})
        assert "Third-party data" in fixed["content"][0]["text"]
        assert json.loads(fixed["content"][1]["text"])["limit"] == 25
    logged = [json.loads(l) for l in (tmp_path / "vault-calls.jsonl").read_text().splitlines()]
    assert [r["decision"] for r in logged if r["phase"] == "pre"] == ["deny", "modify"]
    assert all(r["source"] == "gateway" for r in logged)


def test_two_upstreams_are_merged_and_routed(monkeypatch, tmp_path):
    stub1 = f'"{sys.executable}" "{ROOT / "tests" / "fixtures" / "stub_dfs_server.py"}"'
    stub2 = f'"{sys.executable}" "{ROOT / "tests" / "fixtures" / "stub_dfs_docs_server.py"}"'
    monkeypatch.setenv("DFS_GATEWAY_TOKEN", TOKEN)
    monkeypatch.setenv("DFS_GATEWAY_ALLOWED_HOSTS", "testserver")
    monkeypatch.setenv("DFS_GATEWAY_UPSTREAM", stub1 + " ;; " + stub2)
    monkeypatch.setattr(gw.guard, "LOG", str(tmp_path / "calls.jsonl"))
    monkeypatch.setattr(gw.guard, "VAULT_LOG", str(tmp_path / "vault-calls.jsonl"))
    with TestClient(gw.make_app()) as client:
        assert client.get(f"/health/{TOKEN}").json() == {"ok": True, "tools": 3}
        rpc(client, 1, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                      "clientInfo": {"name": "test", "version": "1"}})
        names = {t["name"] for t in rpc(client, 2, "tools/list")["tools"]}
        assert names == {"kw_data_google_ads_search_volume", "dataforseo_labs_google_ranked_keywords", "docs_search"}
        docs = rpc(client, 3, "tools/call", {"name": "docs_search", "arguments": {"query": "serp"}})
        assert '"docs_search"' in docs["content"][1]["text"]
        ranked = rpc(client, 4, "tools/call", {"name": "dataforseo_labs_google_ranked_keywords",
                                               "arguments": {"target": "example.com", "limit": 10}})
        assert "SHADOWED" not in ranked["content"][1]["text"]      # the first upstream wins a name clash
