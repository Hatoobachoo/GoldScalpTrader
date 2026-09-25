"""Collect read-only connected Exness DEMO certification evidence.

This tool intentionally performs NO broker write. It can run while the governed
DEMO bot is stopped for a checkpoint/read audit, or separately when safe for the
operator. It records only facts actually observed from MT5 + the local durable
StateStore. Missing lifecycle drills remain PENDING rather than being invented.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from gold_scalp_trader.app.startup import mt5_session
from gold_scalp_trader.config import load_settings
from gold_scalp_trader.domain.enums import IntentState, RuntimeMode
from gold_scalp_trader.execution.intent_store import NS as INTENT_NS, unresolved
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
    return any(str(record.payload.get("action")) == action and str(record.payload.get("state")) == state for record in records)


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
            "verified_open": False,
            "verified_modify": False,
            "verified_close": False,
        }
    store = StateStore(path)
    try:
        intents = store.list_records(INTENT_NS)
        unresolved_rows = unresolved(store)
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
            "verified_open": _intent_observed(intents, "OPEN"),
            "verified_modify": _intent_observed(intents, "MODIFY"),
            "verified_close": _intent_observed(intents, "CLOSE"),
        }
    finally:
        store.close()


def collect() -> dict[str, object]:
    settings = load_settings()
    if settings.mode is not RuntimeMode.DEMO:
        raise RuntimeError("connected DEMO certification requires MODE=DEMO")
    if not settings.demo_write_enabled:
        raise RuntimeError("DEMO_TRADING_CONFIRM must explicitly approve DEMO")

    captured = datetime.now(tz=UTC)
    with mt5_session() as mt5:
        is_demo = demo_account_verified(mt5)
        if not is_demo:
            raise RuntimeError("MT5 account does not positively report DEMO mode")
        result = Mt5Reader(settings, mt5).read(captured_at=captured)

    snapshot = result.snapshot
    spec = snapshot.symbol_spec
    state = _state_evidence(Path(settings.state_db_path))
    positions = None if snapshot.positions is None else len(snapshot.positions)
    quality = {tf.value: value.value for tf, value in snapshot.quality.items()}

    lifecycle = {
        "connected_demo_identity": "PASS",
        "symbol_spec_observed": "PASS",
        "fresh_quote_observed": _status(snapshot.quote.age_seconds <= settings.max_quote_age_seconds and snapshot.quote.age_seconds >= -2.0),
        "state_integrity": state.get("integrity", "NOT_AVAILABLE"),
        "verified_open_observed": _status(bool(state.get("verified_open"))),
        "verified_modify_observed": _status(bool(state.get("verified_modify"))),
        "verified_close_observed": _status(bool(state.get("verified_close"))),
        "actual_learning_observed": _status(int(state.get("learning_observations", 0)) > 0),
        "unresolved_intent_clear": _status(int(state.get("unresolved_intents", 0)) == 0),
        "manual_known_trade_close_drill": "PENDING_OPERATOR_DRILL",
        "ambiguous_ack_no_duplicate_drill": "PENDING_SAFE_CONNECTED_DRILL",
        "restart_during_active_lifecycle": "PENDING_CONNECTED_DRILL",
        "fresh_machine_restore_handoff": "PENDING_CONNECTED_DRILL",
        "broker_schedule_preclose_dst_holiday": "PENDING_OBSERVATION",
        "spread_slippage_deviation_distribution": "PENDING_SAMPLE",
        "latency_distribution": "PENDING_SAMPLE",
    }

    full_complete = all(
        value == "PASS"
        for value in (
            lifecycle["connected_demo_identity"],
            lifecycle["symbol_spec_observed"],
            lifecycle["fresh_quote_observed"],
            lifecycle["state_integrity"],
            lifecycle["verified_open_observed"],
            lifecycle["verified_modify_observed"],
            lifecycle["verified_close_observed"],
            lifecycle["actual_learning_observed"],
            lifecycle["unresolved_intent_clear"],
        )
    ) and all(
        not str(value).startswith("PENDING")
        for key, value in lifecycle.items()
        if key not in {
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
    )

    return {
        "schema_version": 1,
        "captured_at_utc": captured.isoformat(),
        "mode": settings.mode.value,
        "broker_write_performed_by_this_tool": False,
        "real_release_enabled": False,
        "account_scope_sha256": _scope_hash(snapshot.account.login, snapshot.account.server, result.resolved_symbol),
        "server": snapshot.account.server,
        "currency": snapshot.account.currency,
        "symbol": result.resolved_symbol,
        "quote": {
            "bid": snapshot.quote.bid,
            "ask": snapshot.quote.ask,
            "spread": snapshot.quote.spread,
            "age_seconds": snapshot.quote.age_seconds,
        },
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
        "data_quality": quality,
        "positions_verified_count": positions,
        "positions_quality": snapshot.positions_quality.value,
        "durable_state": state,
        "phase15": lifecycle,
        "full_connected_certification": "PASS" if full_complete else "INCOMPLETE",
        "profitability_claim": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runtime/evidence"))
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    report = collect()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    target = args.output_dir / f"connected-demo-{stamp}.json"
    if target.exists():
        raise FileExistsError(target)
    target.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")

    print("GoldScalpTrader — Connected DEMO evidence")
    print(f"Evidence file: {target}")
    print(f"Symbol: {report['symbol']}")
    print(f"Quote age: {report['quote']['age_seconds']:.3f}s")
    for key, value in report["phase15"].items():
        print(f"  {key:<42} {value}")
    print(f"FULL CONNECTED CERTIFICATION: {report['full_connected_certification']}")
    print("This tool performed NO broker write.")

    if args.require_complete and report["full_connected_certification"] != "PASS":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
