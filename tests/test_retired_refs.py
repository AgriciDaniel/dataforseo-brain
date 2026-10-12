import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_endpoints  # noqa: E402


def make_vault(tmp_path, text, folder="concepts"):
    note = tmp_path / "wiki" / folder / "note.md"
    note.parent.mkdir(parents=True)
    note.write_text(text, encoding="utf-8")
    return tmp_path


def test_flags_retired_family_described_as_live(tmp_path):
    vault = make_vault(tmp_path, "- Use `/v3/serp/google/events/live/advanced` for local events.\n")
    found = validate_endpoints.retired_refs(vault)
    assert len(found) == 1 and "Google Events" in found[0]


def test_accepts_lines_that_mark_it_retired(tmp_path):
    vault = make_vault(tmp_path, "- `business_data/social_media/pinterest/live`: retired 2026-09-16, don't call.\n")
    assert validate_endpoints.retired_refs(vault) == []


def test_dated_sources_may_describe_the_past(tmp_path):
    vault = make_vault(tmp_path, "- serp/google/events was available in June.\n", folder="sources")
    assert validate_endpoints.retired_refs(vault) == []
