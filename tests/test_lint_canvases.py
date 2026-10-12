import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint_vault  # noqa: E402


def canvas(tmp_path, nodes, edges=()):
    (tmp_path / "wiki" / "canvases").mkdir(parents=True)
    (tmp_path / "wiki" / "hot.md").write_text("---\ntype: hot\n---\n", encoding="utf-8")
    path = tmp_path / "wiki" / "canvases" / "map.canvas"
    path.write_text(json.dumps({"nodes": list(nodes), "edges": list(edges)}), encoding="utf-8")
    return path


def test_flags_a_card_for_a_deleted_note_and_a_dangling_edge(tmp_path):
    c = canvas(tmp_path, [{"id": "a", "type": "file", "file": "wiki/hot.md"},
                          {"id": "b", "type": "file", "file": "wiki/meta/Deleted Template.md"}],
               [{"id": "e1", "fromNode": "a", "toNode": "zzz"}])
    issues = lint_vault.canvas_issues(tmp_path, c)
    assert len(issues) == 2 and "Deleted Template" in issues[0] and "e1" in issues[1]


def test_accepts_a_valid_canvas(tmp_path):
    c = canvas(tmp_path, [{"id": "a", "type": "file", "file": "wiki/hot.md"}, {"id": "t", "type": "text", "text": "x"}],
               [{"id": "e1", "fromNode": "a", "toNode": "t"}])
    assert lint_vault.canvas_issues(tmp_path, c) == []
