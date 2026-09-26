"""Collect read-only connected Exness DEMO certification evidence.

This tool intentionally performs NO broker write. Explicit operator drill PASS
records must be artifact-backed, scope-bound and validated before contributing
to full Phase-15 certification.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from gold_scalp_trader.app.session_authority import resolve as resolve_session
from gold_scalp_trader.app.startup import mt5_session
from gold_scalp_trader.config import load_settings
from gold_scalp_trader.diagnostics.connected_demo import (
    EXTERNAL_DRILL_KEYS,
    SCHEDULE_EVIDENCE_KEY,
    apply_operator_drill_evidence,
)
from gold_scalp_trader.diagnostics.connected_runtime_evidence import (
    session_payload,
    summarize_local_research,
)
from gold_scalp_trader.domain.enums import IntentState, RuntimeMode
from gold_scalp_trader.execution.intent_store import NS as INTENT_NS, unresolved
from gold_scalp_trader.management.closure import RECEIPT_NS
from gold_scalp_trader.management.store import NS as MANAGED_TRADE_NS
from gold_scalp_trader.market_data.account_mode import demo_account_verified
from gold_scalp_trader.market_data.mt5_reader import Mt5Reader
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.episode_journal import NS as EPISODE_NS
from gold_scalp_trader.research.learning import NS as LEARNING_NS

UTC = timezone.utc


def _status(value: bool) -> str:
    return "PASS" if value else "PENDING"


def _scope_hash(login: int, server: str, symbol: str) -> str:
    return hashlib.sha256(f"{login}|{server}|{symbol}".encode("utf-8")).hexdigest()


def _intent_observed(records, action: str, state: str = IntentState.ACCEPTED_VERIFIED.value) -> bool:
    return any(
        str(record.payload.get("action")) == action
        and str(record.payload.get("state")) == state
        for record in records
    )


def _empty_local_research() -> dict[str, int]:
    return {
        "timing_samples": 0,
        "timing_broker_write_associated_samples": 0,
        "management_samples": 0,
        "shadow_samples": 0,
        "qualified_shadow_samples": 0,
    }


def _state_evidence(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {
            "database_present": False,
            "integrity": "NOT_AVAILABLE",
            "intents": 0,
            "unresolved_intents": 0,
            "managed_trades": 0,
            "learning_observations": 0,
            "research_episodes": 0,
            "closure_receipts": 0,
            "closure_origins": {},
            "verified_open": False,
            "verified_modify": False,
            "verified_close": False,
            "broker_side_close_observed": False,
            "manual_known_close_observed": False,
            "runtime_research": _empty_local_research(),
        }

    store = StateStore(path)
    try:
        intents = store.list_records(INTENT_NS)
        unresolved_rows = unresolved(store)
        receipts = store.list_records(RECEIPT_NS)
        origins = Counter(str(row.payload.get("close_origin", "UNKNOWN")) for row in receipts)
        return {
            "database_present": True,
            "integrity": "PASS" if store.integrity_check() else "FAIL",
            "intents": len(intents),
            "intent_states": dict(Counter(str(row.payload.get("state", "UNKNOWN")) for row in intents)),
            "intent_actions": dict(Counter(str(row.payload.get("action", "UNKNOWN")) for row in intents)),
            "unresolved_intents": len(unresolved_rows),
            "managed_trades": len(store.list_records(MANAGED_TRADE_NS)),
            "learning_observations": len(store.list_records(LEARNING_NS)),
            "research_episodes": len(store.list_events(EPISODE_NS)),
            "closure_receipts": len(receipts),
            "closure_origins": dict(origins),
            "verified_open": _intent_observed(intents, "OPEN"),
            "verified_modify": _intent_observed(intents, "MODIFY"),
            "verified_close": _intent_observed(intents, "CLOSE"),
            "broker_side_close_observed": any(
                row.payload.get("close_intent_id") in {None, ""} for row in receipts
            ),
            "manual_known_close_observed": any(
                str(row.payload.get("close_origin", "UNKNOWN")) in {"EXTERNAL", "MIXED"}
                for row in receipts
            ),
            "runtime_research": summarize_local_research(store),
        }
    finally:
        store.close()


def _load_operator_evidence(directory: Path | None) -> list[dict[str, Any]]:
    if directory is None or not directory.exists():
        return []
    if not directory.is_dir():
        raise ValueError("operator evidence path must be a directory")
    out: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"operator evidence must be an object: {path}")
        out.append(payload)
    return out


def _base_connected_snapshot():
    settings = load_settings()
    if settings.mode is not RuntimeMode.DEMO:
        raise RuntimeError("connected DEMO certification requires MODE=DEMO")
    captured = datetime.now(tz=UTC)
    with mt5_session() as mt5:
        if not demo_account_verified(mt5):
            raise RuntimeError("MT5 account does not positively report DEMO mode")
        result = Mt5Reader(settings, mt5).read(captured_at=captured)
    return settings, captured, result


def collect(operator_evidence_dir: Path | None = None) -> dict[str, object]:
    settings, captured, result = _base_connected_snapshot()
    snapshot = result.snapshot
    spec = snapshot.symbol_spec
    state = _state_evidence(Path(settings.state_db_path))
    positions = None if snapshot.positions is None else len(snapshot.positions)
    provider = resolve_session(settings, snapshot)
    session = session_payload(provider)
    local_research = dict(state.get("runtime_research", _empty_local_research()))

    lifecycle = {
        "connected_demo_identity": "PASS",
        "symbol_spec_observed": "PASS",
        "fresh_quote_observed": _status(
            -2.0 <= snapshot.quote.age_seconds <= settings.max_quote_age_seconds
        ),
        "state_integrity": state.get("integrity", "NOT_AVAILABLE"),
        "verified_open_observed": _status(bool(state.get("verified_open"))),
        "verified_modify_observed": _status(bool(state.get("verified_modify"))),
        "verified_close_observed": _status(bool(state.get("verified_close"))),
        "broker_side_close_visibility": _status(bool(state.get("broker_side_close_observed"))),
        "actual_learning_observed": _status(int(state.get("learning_observations", 0)) > 0),
        "unresolved_intent_clear": _status(int(state.get("unresolved_intents", 0)) == 0),
        "manual_known_trade_close_drill": _status(bool(state.get("manual_known_close_observed")))
        if state.get("database_present")
        else "PENDING_OPERATOR_DRILL",
        "ambiguous_ack_no_duplicate_drill": "PENDING_SAFE_CONNECTED_DRILL",
        "restart_during_active_lifecycle": "PENDING_CONNECTED_DRILL",
        "fresh_machine_restore_handoff": "PENDING_CONNECTED_DRILL",
        "broker_schedule_preclose_dst_holiday": "PENDING_OBSERVATION",
        "spread_slippage_deviation_distribution": "PENDING_SAMPLE",
        "latency_distribution": "PENDING_SAMPLE",
        "protect_trail_modify_drill": "PENDING_CONNECTED_DRILL",
        "broker_side_tp_sl_close_drill": "PENDING_CONNECTED_DRILL",
        "strategy_isolation_attribution": "PENDING_CONNECTED_DRILL",
        # Durable timing/shadow samples are exposed below but do not auto-certify
        # the canonical connected drill; explicit connected evidence remains required.
        "m1_refinement_timing": "PENDING_SAMPLE",
        "three_loss_cooldown_persistence": "PENDING_CONNECTED_DRILL",
        "shadow_learning_report": "PENDING_SAMPLE",
    }

    report = {
        "schema_version": 4,
        "captured_at_utc": captured.isoformat(),
        "mode": settings.mode.value,
        "broker_write_performed_by_this_tool": False,
        "real_release_enabled": False,
        "account_scope_sha256": _scope_hash(
            snapshot.account.login, snapshot.account.server, result.resolved_symbol
        ),
        "server": snapshot.account.server,
        "currency": snapshot.account.currency,
        "symbol": result.resolved_symbol,
        "quote": {
            "bid": snapshot.quote.bid,
            "ask": snapshot.quote.ask,
            "spread": snapshot.quote.spread,
            "age_seconds": snapshot.quote.age_seconds,
        },
        "session": session,
        "symbol_spec": {
            "digits": spec.digits,
            "point": spec.point,
            "tick_size": spec.tick_size,
            "tick_value": spec.tick_value,
            "volume_min": spec.volume_min,
            "volume_max": spec.volume_max,
            "volume_step": spec.volume_step,
            "stops_level_points": spec.stops_level_points,
            "freeze_level_points": spec.freeze_level_points,
            "trade_mode": spec.trade_mode,
            "filling_mode": spec.filling_mode,
        },
        "data_quality": {tf.value: value.value for tf, value in snapshot.quality.items()},
        "positions_verified_count": positions,
        "positions_quality": snapshot.positions_quality.value,
        "durable_state": state,
        "runtime_research": local_research,
        "phase15": lifecycle,
        "full_connected_certification": "INCOMPLETE",
        "profitability_claim": "NONE",
    }

    evidence = _load_operator_evidence(operator_evidence_dir)
    if evidence:
        report = apply_operator_drill_evidence(report, evidence)

    core = {
        "connected_demo_identity",
        "symbol_spec_observed",
        "fresh_quote_observed",
        "state_integrity",
        "verified_open_observed",
        "verified_modify_observed",
        "verified_close_observed",
        "actual_learning_observed",
        "unresolved_intent_clear",
    }
    phase15 = report["phase15"]
    complete = all(phase15[key] == "PASS" for key in core) and all(
        phase15[key] == "PASS" for key in EXTERNAL_DRILL_KEYS
    )
    report["full_connected_certification"] = "PASS" if complete else "INCOMPLETE"
    return report


def _record_drill(
    *,
    drill: str,
    artifact: Path,
    output_dir: Path,
    valid_until_utc: str | None,
    note: str,
) -> Path:
    if drill not in EXTERNAL_DRILL_KEYS:
        raise ValueError(f"unsupported Phase-15 drill: {drill}")
    if not artifact.is_file():
        raise FileNotFoundError(artifact)
    settings, observed, result = _base_connected_snapshot()
    snapshot = result.snapshot
    if drill == SCHEDULE_EVIDENCE_KEY and not valid_until_utc:
        raise ValueError("broker schedule evidence requires --valid-until-utc")
    valid_until = None
    if valid_until_utc:
        parsed = datetime.fromisoformat(valid_until_utc.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("--valid-until-utc must be timezone-aware")
        if parsed.astimezone(UTC) < observed:
            raise ValueError("--valid-until-utc must be in the future")
        valid_until = parsed.astimezone(UTC).isoformat()
    payload = {
        "schema_version": 1,
        "mode": settings.mode.value,
        "account_scope_sha256": _scope_hash(
            snapshot.account.login, snapshot.account.server, result.resolved_symbol
        ),
        "symbol": result.resolved_symbol,
        "drill": drill,
        "result": "PASS",
        "observed_at_utc": observed.isoformat(),
        "artifact_name": artifact.name,
        "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "valid_until_utc": valid_until,
        "note": note,
        "broker_write_performed_by_this_tool": False,
        "real_release_enabled": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{drill}-{observed.strftime('%Y%m%dT%H%M%SZ')}.json"
    if target.exists():
        raise FileExistsError(target)
    target.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runtime/evidence"))
    parser.add_argument(
        "--operator-evidence-dir",
        type=Path,
        default=Path("runtime/evidence/operator-drills"),
    )
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--record-drill", choices=EXTERNAL_DRILL_KEYS)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--valid-until-utc")
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    if args.record_drill:
        if args.artifact is None:
            parser.error("--record-drill requires --artifact")
        target = _record_drill(
            drill=args.record_drill,
            artifact=args.artifact,
            output_dir=args.operator_evidence_dir,
            valid_until_utc=args.valid_until_utc,
            note=args.note,
        )
        print(f"Evidence record: {target}")
        print("Artifact hash captured; no broker write was performed by this tool.")
        return 0

    report = collect(args.operator_evidence_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / f"connected-demo-{datetime.now(tz=UTC).strftime('%Y%m%dT%H%M%SZ')}.json"
    if target.exists():
        raise FileExistsError(target)
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Evidence file: {target}")
    print(f"Symbol: {report['symbol']}")
    print(f"Quote age: {report['quote']['age_seconds']:.3f}s")
    session = report["session"]
    print(
        "Session: "
        f"{session['state']} verified={session['schedule_verified']} "
        f"tradeable={session['tradeable']} reason={session['reason']}"
    )
    research = report["runtime_research"]
    print(
        "Runtime research: "
        f"timing={research['timing_samples']} "
        f"timing+write={research['timing_broker_write_associated_samples']} "
        f"management={research['management_samples']} "
        f"shadow={research['shadow_samples']}"
    )
    for key, value in report["phase15"].items():
        print(f"  {key:<42} {value}")
    print(f"FULL CONNECTED CERTIFICATION: {report['full_connected_certification']}")
    print("This tool performed NO broker write.")
    return 2 if args.require_complete and report["full_connected_certification"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
