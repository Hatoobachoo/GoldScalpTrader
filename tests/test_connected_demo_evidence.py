from __future__ import annotations

from copy import deepcopy

import pytest

from gold_scalp_trader.diagnostics.connected_demo import aggregate_connected_demo_reports


def _report(*, spread: float = 0.20, age: float = 0.10, open_: str = "PENDING", modify: str = "PENDING", close: str = "PENDING", learning: str = "PENDING", unresolved: str = "PASS") -> dict[str, object]:
    return {
        "captured_at_utc": "2026-09-25T12:00:00+00:00",
        "mode": "DEMO",
        "broker_write_performed_by_this_tool": False,
        "real_release_enabled": False,
        "account_scope_sha256": "scope-a",
        "symbol": "XAUUSDm",
        "quote": {"spread": spread, "age_seconds": age},
        "positions_verified_count": 0,
        "phase15": {
            "connected_demo_identity": "PASS",
            "symbol_spec_observed": "PASS",
            "fresh_quote_observed": "PASS",
            "state_integrity": "PASS",
            "verified_open_observed": open_,
            "verified_modify_observed": modify,
            "verified_close_observed": close,
            "broker_side_close_visibility": "PENDING",
            "actual_learning_observed": learning,
            "unresolved_intent_clear": unresolved,
            "manual_known_trade_close_drill": "PENDING_OPERATOR_DRILL",
            "ambiguous_ack_no_duplicate_drill": "PENDING_SAFE_CONNECTED_DRILL",
            "restart_during_active_lifecycle": "PENDING_CONNECTED_DRILL",
            "fresh_machine_restore_handoff": "PENDING_CONNECTED_DRILL",
            "broker_schedule_preclose_dst_holiday": "PENDING_OBSERVATION",
            "spread_slippage_deviation_distribution": "PENDING_SAMPLE",
            "latency_distribution": "PENDING_SAMPLE",
        },
    }


def test_accumulator_keeps_lifecycle_evidence_without_false_full_pass() -> None:
    first = _report(open_="PASS", modify="PASS")
    second = _report(close="PASS", learning="PASS", spread=0.30, age=0.20)
    second["captured_at_utc"] = "2026-09-25T12:01:00+00:00"

    summary = aggregate_connected_demo_reports([first, second])

    assert summary["sample_count"] == 2
    assert summary["phase15"]["verified_open_observed"] == "PASS"
    assert summary["phase15"]["verified_modify_observed"] == "PASS"
    assert summary["phase15"]["verified_close_observed"] == "PASS"
    assert summary["phase15"]["actual_learning_observed"] == "PASS"
    assert summary["core_demo_lifecycle_observed"] == "PASS"
    assert summary["full_connected_certification"] == "INCOMPLETE"
    assert summary["quote"]["spread_min"] == pytest.approx(0.20)
    assert summary["quote"]["spread_max"] == pytest.approx(0.30)


def test_external_drills_accumulate_only_after_explicit_pass() -> None:
    first = _report()
    second = _report()
    second["captured_at_utc"] = "2026-09-25T12:01:00+00:00"
    second["phase15"]["broker_side_close_visibility"] = "PASS"
    second["phase15"]["manual_known_trade_close_drill"] = "PASS"

    summary = aggregate_connected_demo_reports([first, second])

    assert summary["phase15"]["broker_side_close_visibility"] == "PASS"
    assert summary["phase15"]["manual_known_trade_close_drill"] == "PASS"
    assert summary["phase15"]["restart_during_active_lifecycle"].startswith("PENDING")


def test_latest_unresolved_intent_state_is_not_laundered() -> None:
    first = _report(open_="PASS", modify="PASS", close="PASS", learning="PASS", unresolved="PASS")
    second = _report(unresolved="PENDING")
    second["captured_at_utc"] = "2026-09-25T12:01:00+00:00"

    summary = aggregate_connected_demo_reports([first, second])

    assert summary["phase15"]["unresolved_intent_clear"] == "PENDING"
    assert summary["core_demo_lifecycle_observed"] == "INCOMPLETE"


def test_scope_mismatch_is_rejected() -> None:
    first = _report()
    second = deepcopy(first)
    second["account_scope_sha256"] = "scope-b"

    with pytest.raises(ValueError, match="different account/symbol scopes"):
        aggregate_connected_demo_reports([first, second])


def test_monitor_evidence_cannot_claim_real_or_broker_write() -> None:
    report = _report()
    report["real_release_enabled"] = True
    with pytest.raises(ValueError, match="REAL release"):
        aggregate_connected_demo_reports([report])

    report = _report()
    report["broker_write_performed_by_this_tool"] = True
    with pytest.raises(ValueError, match="unexpected broker write"):
        aggregate_connected_demo_reports([report])
