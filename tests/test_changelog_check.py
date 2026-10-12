import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_baselines  # noqa: E402


def vault(tmp_path, checked="2026-10-01"):
    note = tmp_path / "wiki" / "sources" / "dfs-changelog.md"
    note.parent.mkdir(parents=True)
    note.write_text(f"**URL:** https://dataforseo.com/updates · **Checked:** {checked}\n", encoding="utf-8")
    return tmp_path


def posts(monkeypatch, *dated):
    body = json.dumps([{"date": d + "T10:00:00", "title": {"rendered": t}, "link": "https://dataforseo.com/update/x/"}
                       for d, t in dated]).encode()
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: io.BytesIO(body))


def test_nothing_new_is_quiet(monkeypatch, tmp_path):
    posts(monkeypatch, ("2026-09-29", "Keywords for Site supports pages"))
    lines, alert = run_baselines.changelog_check(vault(tmp_path))
    assert alert is False and "nothing new" in lines[0]


def test_new_update_alerts_and_lists_it(monkeypatch, tmp_path):
    posts(monkeypatch, ("2026-10-08", "Bing Shopping API retired"), ("2026-09-29", "older"))
    lines, alert = run_baselines.changelog_check(vault(tmp_path))
    text = "\n".join(lines)
    assert alert is True and "Bing Shopping API retired" in text and "older" not in text


def test_network_failure_is_quiet(monkeypatch, tmp_path):
    def boom(req, timeout=None):
        raise OSError("offline")
    monkeypatch.setattr("urllib.request.urlopen", boom)
    lines, alert = run_baselines.changelog_check(vault(tmp_path))
    assert alert is False and "skipped" in lines[0]


def test_same_day_post_counts_unless_recorded(monkeypatch, tmp_path):
    posts(monkeypatch, ("2026-10-01", "Posted later on the checked day"))
    v = vault(tmp_path)
    lines, alert = run_baselines.changelog_check(v)
    assert alert is True and "Posted later" in "\n".join(lines)
    note = v / "wiki" / "sources" / "dfs-changelog.md"
    note.write_text(note.read_text(encoding="utf-8") + "\n- [x](https://dataforseo.com/update/x/)\n", encoding="utf-8")
    lines, alert = run_baselines.changelog_check(v)
    assert alert is False
