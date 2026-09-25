"""Aggregate read-only connected DEMO certification observations.

This module has no MT5 dependency and no broker authority. It combines already
captured certification reports so a long-running DEMO session can accumulate
OPEN/MODIFY/CLOSE/learning evidence without turning missing drills into PASS.
"""
from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from statistics import fmean
from typing import Any

CORE_ANY_KEYS = (
    "verified_open_observed",
    "verified_modify_observed",
    "verified_close_observed",
    "actual_learning_observed",
)
ALWAYS_PASS_KEYS = (
    "connected_demo_identity",
    "symbol_spec_observed",
    "fresh_quote_observed",
    "state_integrity",
)
EXTERNAL_DRILL_KEYS = (
    "manual_known_trade_close_drill",
    "ambiguous_ack_no_duplicate_drill",
    "restart_during_active_lifecycle",
    "fresh_machine_restore_handoff",
    "broker_schedule_preclose_dst_holiday",
    "spread_slippage_deviation_distribution",
    "latency_distribution",
)


def _all_pass(reports: Sequence[dict[str, Any]], key: str) -> bool:
    return all(str(report["phase15"].get(key)) == "PASS" for report in reports)


def _any_pass(reports: Sequence[dict[str, Any]], key: str) -> bool:
    return any(str(report["phase15"].get(key)) == "PASS" for report in reports)


def _latest_status(reports: Sequence[dict[str, Any]], key: str) -> str:
    return str(reports[-1]["phase15"].get(key, "PENDING"))


def _validate_identity(reports: Sequence[dict[str, Any]]) -> None:
    if not reports:
        raise ValueError("at least one connected DEMO report is required")
    scopes = {str(report.get("account_scope_sha256")) for report in reports}
    symbols = {str(report.get("symbol")) for report in reports}
    modes = {str(report.get("mode")) for report in reports}
    if len(scopes) != 1 or len(symbols) != 1:
        raise ValueError("connected DEMO observations span different account/symbol scopes")
    if modes != {"DEMO"}:
        raise ValueError("connected DEMO evidence may contain DEMO mode only")
    if any(bool(report.get("broker_write_performed_by_this_tool")) for report in reports):
        raise ValueError("read-only certification evidence reports an unexpected broker write")
    if any(bool(report.get("real_release_enabled")) for report in reports):
        raise ValueError("REAL release must remain disabled during DEMO certification")


def aggregate_connected_demo_reports(reports: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Return a truthful accumulated Phase-15 summary for one broker scope.

    Normal lifecycle observations are cumulative: once a verified OPEN/MODIFY/
    CLOSE or actual learning record has been observed, later flat snapshots do
    not erase that evidence. Current-health facts such as unresolved Intents use
    the latest sample. External/manual drills remain pending until an input
    report explicitly records them as PASS.
    """

    _validate_identity(reports)
    spreads = [float(report["quote"]["spread"]) for report in reports]
    quote_ages = [float(report["quote"]["age_seconds"]) for report in reports]
    captured = [datetime.fromisoformat(str(report["captured_at_utc"])) for report in reports]
    positions = [report.get("positions_verified_count") for report in reports]
    known_positions = [int(value) for value in positions if value is not None]

    phase15: dict[str, str] = {}
    for key in ALWAYS_PASS_KEYS:
        phase15[key] = "PASS" if _all_pass(reports, key) else "DEGRADED"
    for key in CORE_ANY_KEYS:
        phase15[key] = "PASS" if _any_pass(reports, key) else "PENDING"
    phase15["unresolved_intent_clear"] = _latest_status(reports, "unresolved_intent_clear")
    for key in EXTERNAL_DRILL_KEYS:
        phase15[key] = "PASS" if _any_pass(reports, key) else _latest_status(reports, key)

    core_complete = all(phase15[key] == "PASS" for key in CORE_ANY_KEYS) and all(
        phase15[key] == "PASS" for key in ALWAYS_PASS_KEYS
    ) and phase15["unresolved_intent_clear"] == "PASS"
    full_complete = core_complete and all(phase15[key] == "PASS" for key in EXTERNAL_DRILL_KEYS)

    return {
        "schema_version": 1,
        "scope_sha256": str(reports[0]["account_scope_sha256"]),
        "symbol": str(reports[0]["symbol"]),
        "mode": "DEMO",
        "sample_count": len(reports),
        "first_captured_at_utc": min(captured).isoformat(),
        "last_captured_at_utc": max(captured).isoformat(),
        "quote": {
            "spread_min": min(spreads),
            "spread_mean": fmean(spreads),
            "spread_max": max(spreads),
            "quote_age_max_seconds": max(quote_ages),
        },
        "positions": {
            "known_sample_count": len(known_positions),
            "min_verified_count": min(known_positions) if known_positions else None,
            "max_verified_count": max(known_positions) if known_positions else None,
        },
        "phase15": phase15,
        "core_demo_lifecycle_observed": "PASS" if core_complete else "INCOMPLETE",
        "full_connected_certification": "PASS" if full_complete else "INCOMPLETE",
        "broker_write_performed_by_monitor": False,
        "real_release_enabled": False,
        "profitability_claim": "NONE",
    }
