"""Aggregate read-only connected DEMO certification observations.

This module has no MT5 dependency and no broker authority. It combines already
captured certification reports and validates explicit operator drill evidence.
Missing drills never become PASS merely because time elapsed or a monitor ran.
"""
from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timezone
from statistics import fmean
from typing import Any

UTC = timezone.utc
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
    "broker_side_close_visibility",
    "manual_known_trade_close_drill",
    "ambiguous_ack_no_duplicate_drill",
    "restart_during_active_lifecycle",
    "fresh_machine_restore_handoff",
    "broker_schedule_preclose_dst_holiday",
    "spread_slippage_deviation_distribution",
    "latency_distribution",
    "protect_trail_modify_drill",
    "broker_side_tp_sl_close_drill",
    "strategy_isolation_attribution",
    "m1_refinement_timing",
    "three_loss_cooldown_persistence",
    "shadow_learning_report",
)
SCHEDULE_EVIDENCE_KEY = "broker_schedule_preclose_dst_holiday"


def _parse_aware(value: object, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {name}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return parsed.astimezone(UTC)


def _valid_sha256(value: object) -> bool:
    text = str(value).lower()
    return len(text) == 64 and all(ch in "0123456789abcdef" for ch in text)


def apply_operator_drill_evidence(report: dict[str, Any], records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Apply artifact-backed, scope-bound operator drill evidence."""
    if str(report.get("mode")) != "DEMO":
        raise ValueError("operator drill evidence may apply to DEMO reports only")
    scope = str(report.get("account_scope_sha256"))
    symbol = str(report.get("symbol"))
    captured = _parse_aware(report.get("captured_at_utc"), "captured_at_utc")
    phase15 = dict(report.get("phase15", {}))
    accepted: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict) or record.get("schema_version") != 1:
            raise ValueError("unsupported operator drill evidence schema")
        if bool(record.get("broker_write_performed_by_this_tool")):
            raise ValueError("operator drill evidence reports an unexpected broker write")
        if bool(record.get("real_release_enabled")):
            raise ValueError("REAL release must remain disabled during DEMO drill evidence")
        if str(record.get("account_scope_sha256")) != scope or str(record.get("symbol")) != symbol:
            raise ValueError("operator drill evidence scope/symbol mismatch")
        if str(record.get("mode")) != "DEMO":
            raise ValueError("operator drill evidence must be DEMO scoped")
        drill = str(record.get("drill"))
        if drill not in EXTERNAL_DRILL_KEYS:
            raise ValueError(f"unknown Phase-15 drill evidence key: {drill}")
        if str(record.get("result")) != "PASS":
            raise ValueError("operator drill evidence result must be PASS")
        observed = _parse_aware(record.get("observed_at_utc"), "observed_at_utc")
        if observed > captured:
            raise ValueError("operator drill evidence cannot come from the future")
        artifact_name = str(record.get("artifact_name", "")).strip()
        artifact_sha256 = record.get("artifact_sha256")
        if not artifact_name or not _valid_sha256(artifact_sha256):
            raise ValueError("operator drill PASS requires artifact_name and valid artifact_sha256")
        if drill == SCHEDULE_EVIDENCE_KEY:
            valid_until = _parse_aware(record.get("valid_until_utc"), "valid_until_utc")
            if valid_until < captured:
                continue
        phase15[drill] = "PASS"
        accepted.append({
            "drill": drill,
            "observed_at_utc": observed.isoformat(),
            "artifact_name": artifact_name,
            "artifact_sha256": str(artifact_sha256).lower(),
            "valid_until_utc": record.get("valid_until_utc"),
            "note": str(record.get("note", "")),
        })
    out = dict(report)
    out["phase15"] = phase15
    out["operator_drill_evidence"] = accepted
    return out


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
    _validate_identity(reports)
    spreads = [float(report["quote"]["spread"]) for report in reports]
    quote_ages = [float(report["quote"]["age_seconds"]) for report in reports]
    captured = [_parse_aware(report["captured_at_utc"], "captured_at_utc") for report in reports]
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
    accepted_operator_records = [item for report in reports for item in report.get("operator_drill_evidence", ()) if isinstance(item, dict)]
    return {
        "schema_version": 3,
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
        "operator_drill_evidence_count": len(accepted_operator_records),
        "core_demo_lifecycle_observed": "PASS" if core_complete else "INCOMPLETE",
        "full_connected_certification": "PASS" if full_complete else "INCOMPLETE",
        "broker_write_performed_by_monitor": False,
        "real_release_enabled": False,
        "profitability_claim": "NONE",
    }
