"""The guard's messages are what agents read at call time; they must pass the same price-model lint as the wiki."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_endpoints as ve  # noqa: E402

SCRIPTS = sorted((Path(__file__).resolve().parents[1] / "scripts").glob("*.py"))
SKIP = {"validate_endpoints.py"}   # holds the rule's own patterns


def test_scripts_make_no_flat_price_claims_for_per_row_endpoints():
    bad = [f"{f.name}:{no}: {line.strip()[:100]}"
           for f in SCRIPTS if f.name not in SKIP
           for no, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1)
           if ve.PER_ROW_RE.search(line) and ve.FLAT_RE.search(line) and not ve.PER_ROW_ACK_RE.search(line)]
    assert not bad, bad
