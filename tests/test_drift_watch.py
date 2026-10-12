"""drift_watch alerts once per new finding and only after repeated check failures."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drift_watch as dw  # noqa: E402

QUIET = [("updates", ["nothing new"], False), ("spec", ["current"], False), ("prices", ["unchanged"], False)]
NEW_POST = [("updates", ["- 2026-10-13: [New thing](x)"], True)] + QUIET[1:]
BLOCKED = [("updates", ["DataForSEO changelog check skipped: HTTP 403"], False)] + QUIET[1:]


def test_quiet_run_exits_0():
    code, _ = dw.decide(QUIET, {})
    assert code == 0


def test_new_finding_alerts_once():
    code, state = dw.decide(NEW_POST, {})
    assert code == 3
    code, _ = dw.decide(NEW_POST, state)
    assert code == 0                      # same finding again: no second popup


def test_failure_alerts_only_after_two_in_a_row():
    code, state = dw.decide(BLOCKED, {})
    assert code == 0 and state["fails"]["updates"] == 1
    code, state = dw.decide(BLOCKED, state)
    assert code == 4
    code, state = dw.decide(QUIET, state)
    assert code == 0 and state["fails"]["updates"] == 0
