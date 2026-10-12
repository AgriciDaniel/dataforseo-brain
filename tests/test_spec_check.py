import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_baselines  # noqa: E402


def vault(tmp_path, commit="65aa53af6ce3"):
    prov = tmp_path / ".raw" / "sources" / "dataforseo-openapi" / "PROVENANCE.json"
    prov.parent.mkdir(parents=True)
    prov.write_text(json.dumps({"commit": commit}), encoding="utf-8")
    return tmp_path


def upstream(monkeypatch, sha):
    body = json.dumps([{"sha": sha, "commit": {"committer": {"date": "2026-10-10T00:00:00Z"}}}]).encode()
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: io.BytesIO(body))


def test_current_spec_is_quiet(monkeypatch, tmp_path):
    upstream(monkeypatch, "65aa53af6ce3" + "0" * 28)
    lines, alert = run_baselines.spec_check(vault(tmp_path))
    assert alert is False and "current" in lines[0]


def test_newer_upstream_spec_alerts(monkeypatch, tmp_path):
    upstream(monkeypatch, "abcdef123456" + "0" * 28)
    lines, alert = run_baselines.spec_check(vault(tmp_path))
    assert alert is True and "abcdef123456" in lines[0]


def test_network_failure_never_alerts_or_raises(monkeypatch, tmp_path):
    def boom(req, timeout=None):
        raise OSError("offline")
    monkeypatch.setattr("urllib.request.urlopen", boom)
    lines, alert = run_baselines.spec_check(vault(tmp_path))
    assert alert is False and "skipped" in lines[0]
