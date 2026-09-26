"""Research-only runtime evidence for timing/management efficiency and shadow families.

This module never grants broker, Risk, Gate, Session or promotion authority.
It records causal observations and derives only metrics supported by durable
runtime evidence. Post-trade analytics explicitly distinguish polling-observed
path statistics from true intrabar extrema.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any

from gold_scalp_trader.domain.enums import Direction, StrategyMode, Timeframe
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.timing_learning import NS as TIMING_NS

MANAGEMENT_NS = "management_decision_evidence"
SHADOW_NS = "shadow_strategy_evidence"
SCHEMA_VERSION = 2
READY_OUTCOMES = {"READY_BUY", "READY_SELL"}


@dataclass(frozen=True, slots=True)
class TradeEfficiency:
    initial_risk_money: float | None = None
    realized_r: float | None = None
    entry_reference_drift_r: float | None = None
    observed_mfe_r: float | None = None
    observed_mae_r: float | None = None
    observed_capture_efficiency: float | None = None
    observed_giveback_r: float | None = None
    opportunity_to_entry_seconds: float | None = None
    ready_to_entry_seconds: float | None = None
    trigger_to_entry_seconds: float | None = None
    m5_event_to_entry_seconds: float | None = None
    time_to_first_protect_seconds: float | None = None
    time_to_first_trail_seconds: float | None = None
    time_to_observed_primary_target_seconds: float | None = None
    time_to_observed_expansion_target_seconds: float | None = None
    time_to_observed_mfe_seconds: float | None = None
    management_samples: int = 0

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def _value(value: Any) -> str | None:
    if value is None:
        return None
    return str(getattr(value, "value", value))


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    method = getattr(value, "isoformat", None)
    return method() if callable(method) else str(value)


def _num(value: Any) -> float | None:
    return None if value is None else round(float(value), 8)


def _key(prefix: str, payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return f"{prefix}-{sha256(raw.encode('utf-8')).hexdigest()}"


def _open_r(trade: Any, market: Any) -> float | None:
    r = getattr(trade, "original_r_price", None)
    if r is None or float(r) <= 0:
        return None
    direction = _value(getattr(trade, "direction", None))
    price = market.quote.bid if direction == "BUY" else market.quote.ask if direction == "SELL" else None
    if price is None:
        return None
    entry = float(trade.entry)
    return (float(price) - entry) / float(r) if direction == "BUY" else (entry - float(price)) / float(r)


def _initial_risk_money(trade: Any, market: Any) -> float | None:
    """Observed initial monetary R from broker symbol economics when available."""
    spec = getattr(market, "symbol_spec", None)
    if spec is None:
        return None
    tick_size = getattr(spec, "tick_size", None)
    tick_value = getattr(spec, "tick_value", None)
    volume = getattr(trade, "volume", None)
    r_price = getattr(trade, "original_r_price", None)
    values = (tick_size, tick_value, volume, r_price)
    if any(value is None for value in values):
        return None
    tick_size = float(tick_size)
    tick_value = float(tick_value)
    volume = float(volume)
    r_price = float(r_price)
    if tick_size <= 0 or tick_value <= 0 or volume <= 0 or r_price <= 0:
        return None
    return (r_price / tick_size) * tick_value * volume


def record_management(store: StateStore, result: Any) -> str | None:
    trade = getattr(result, "managed_trade", None)
    action = getattr(result, "management_action", None)
    cycle = getattr(result, "cycle", None)
    if trade is None or action is None or cycle is None:
        return None
    intelligence = getattr(cycle, "intelligence", None)
    market = getattr(intelligence, "market", None)
    if market is None:
        return None
    bars = 0
    if trade.opened_at is not None:
        bars = sum(1 for candle in market.series(Timeframe.M5) if candle.close_time > trade.opened_at)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "trade_id": trade.trade_id,
        "position_ticket": trade.ticket,
        "family": _value(trade.family),
        "policy_version": trade.policy_version,
        "direction": _value(trade.direction),
        "captured_at_utc": _iso(market.captured_at),
        "action": _value(action),
        "reason": str(getattr(cycle, "reason", "")),
        "open_r": _num(_open_r(trade, market)),
        "initial_risk_money": _num(_initial_risk_money(trade, market)),
        "bars_in_trade": bars,
        "spread": _num(market.quote.spread),
        "current_sl": _num(trade.current_sl),
        "original_sl": _num(trade.original_sl),
        "primary_target": _num(trade.primary_target),
        "expansion_target": _num(trade.expansion_target),
        "opportunity_id": trade.opportunity_id,
        "episode_id": trade.episode_id,
        "trade_plan_id": trade.trade_plan_id,
        "timing_profile": trade.timing_profile,
        "timing_policy_version": trade.timing_policy_version,
    }
    event_key = _key("MGT", payload)
    store.append_event(MANAGEMENT_NS, event_key, payload)
    return event_key


def record_shadows(store: StateStore, result: Any) -> tuple[str, ...]:
    cycle = getattr(result, "cycle", None)
    if cycle is None:
        return ()
    intelligence = getattr(cycle, "intelligence", None)
    market = getattr(intelligence, "market", None)
    isolation = getattr(cycle, "isolation", None)
    if market is None or isolation is None:
        return ()
    candidates = getattr(isolation, "candidates", None)
    if candidates is None:
        return ()
    active = getattr(isolation, "active_family", None)
    keys: list[str] = []
    for isolated in candidates:
        if getattr(isolated, "mode", None) is not StrategyMode.SHADOW_ONLY:
            continue
        candidate = getattr(isolated, "candidate", None)
        if candidate is None:
            continue
        payload = {
            "schema_version": SCHEMA_VERSION,
            "captured_at_utc": _iso(getattr(market, "captured_at", None)),
            "active_family": _value(active),
            "shadow_family": _value(getattr(candidate, "family", None)),
            "candidate_id": getattr(candidate, "candidate_id", None),
            "qualification": _value(getattr(candidate, "qualification", None)),
            "direction": _value(getattr(candidate, "direction", None)),
            "qualified": bool(getattr(candidate, "qualified", False)),
            "score": _num(getattr(candidate, "score", None)),
            "coverage": _num(getattr(candidate, "coverage", None)),
            "source_event_ids": sorted(str(x) for x in getattr(candidate, "source_event_ids", ()) or ()),
            "m5_event_time": _iso(getattr(candidate, "m5_event_time", None)),
            "preferred_m1_profile": getattr(candidate, "preferred_m1_profile", None),
            "policy_version": getattr(candidate, "policy_version", None),
            "spread": _num(getattr(getattr(market, "quote", None), "spread", None)),
            "bid": _num(getattr(getattr(market, "quote", None), "bid", None)),
            "ask": _num(getattr(getattr(market, "quote", None), "ask", None)),
        }
        event_key = _key("SHD", payload)
        store.append_event(SHADOW_NS, event_key, payload)
        keys.append(event_key)
    return tuple(keys)


def record_runtime_research(store: StateStore, result: Any) -> dict[str, Any]:
    management_key = record_management(store, result)
    shadow_keys = record_shadows(store, result)
    return {"management_event": management_key, "shadow_events": shadow_keys}


def trade_path_summary(store: StateStore, trade_id: str) -> dict[str, Any]:
    rows = [event.payload for event in store.list_events(MANAGEMENT_NS) if event.payload.get("trade_id") == trade_id]
    open_rs = [float(row["open_r"]) for row in rows if row.get("open_r") is not None]
    actions = Counter(str(row.get("action", "UNKNOWN")) for row in rows)
    return {
        "trade_id": trade_id,
        "samples": len(rows),
        "max_favorable_r": max(open_rs) if open_rs else None,
        "max_adverse_r": min(open_rs) if open_rs else None,
        "by_action": dict(sorted(actions.items())),
    }


def summarize_runtime_evidence(store: StateStore) -> dict[str, Any]:
    management = store.list_events(MANAGEMENT_NS)
    shadows = store.list_events(SHADOW_NS)
    return {
        "management_samples": len(management),
        "shadow_samples": len(shadows),
        "management_by_action": dict(sorted(Counter(str(e.payload.get("action", "UNKNOWN")) for e in management).items())),
        "shadow_by_family": dict(sorted(Counter(str(e.payload.get("shadow_family", "UNKNOWN")) for e in shadows).items())),
        "qualified_shadow_samples": sum(1 for e in shadows if e.payload.get("qualified") is True),
    }


def _dt(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _seconds(start: datetime | None, end: datetime | None) -> float | None:
    if start is None or end is None:
        return None
    value = (end - start).total_seconds()
    return value if value >= 0 else None


def _target_r(trade: ManagedTrade, target: float | None) -> float | None:
    if target is None or trade.original_r_price <= 0:
        return None
    move = float(target) - trade.entry if trade.direction is Direction.BUY else trade.entry - float(target)
    return move / trade.original_r_price if move > 0 else None


def _first_time_at_or_above(rows: list[dict[str, Any]], threshold: float | None) -> datetime | None:
    if threshold is None:
        return None
    for row in rows:
        value = row.get("open_r")
        when = _dt(row.get("captured_at_utc"))
        if value is not None and when is not None and float(value) >= threshold:
            return when
    return None


def _first_action_time(rows: list[dict[str, Any]], action: str) -> datetime | None:
    for row in rows:
        if str(row.get("action", "")).upper() == action:
            when = _dt(row.get("captured_at_utc"))
            if when is not None:
                return when
    return None


def measure_trade_efficiency(
    store: StateStore,
    trade: ManagedTrade,
    *,
    closed_at: datetime,
    net_money: float,
) -> TradeEfficiency:
    """Derive causal metrics without pretending sampled observations are complete path truth."""
    management = [event.payload for event in store.list_events(MANAGEMENT_NS) if str(event.payload.get("trade_id") or "") == trade.trade_id]
    management.sort(key=lambda row: str(row.get("captured_at_utc") or ""))

    timing: list[dict[str, Any]] = []
    if trade.opportunity_id:
        timing = [event.payload for event in store.list_events(TIMING_NS) if str(event.payload.get("opportunity_id") or "") == trade.opportunity_id]
        timing.sort(key=lambda row: str(row.get("timing_decision_at") or ""))

    initial_risk_values = [float(row["initial_risk_money"]) for row in management if row.get("initial_risk_money") is not None and float(row["initial_risk_money"]) > 0]
    initial_risk_money = initial_risk_values[0] if initial_risk_values else None
    realized_r = None if initial_risk_money is None else float(net_money) / initial_risk_money

    drift_r = None
    if trade.entry_reference is not None and trade.original_r_price > 0:
        drift = trade.entry - trade.entry_reference if trade.direction is Direction.BUY else trade.entry_reference - trade.entry
        drift_r = drift / trade.original_r_price

    open_samples: list[tuple[datetime, float]] = []
    for row in management:
        when = _dt(row.get("captured_at_utc"))
        value = row.get("open_r")
        if when is not None and value is not None:
            open_samples.append((when, float(value)))
    observed_mfe_r = max((value for _, value in open_samples), default=None)
    observed_mae_r = min((value for _, value in open_samples), default=None)
    observed_capture = None
    observed_giveback = None
    # A sparse sampled path can miss the closing spike. If verified realized R is
    # above the sampled MFE, the sampled path cannot support capture/giveback.
    if realized_r is not None and observed_mfe_r is not None and observed_mfe_r > 0 and realized_r <= observed_mfe_r + 1e-9:
        observed_giveback = observed_mfe_r - realized_r
        if realized_r >= 0:
            observed_capture = realized_r / observed_mfe_r

    first_mfe_at = None
    if observed_mfe_r is not None:
        first_mfe_at = next((when for when, value in open_samples if value == observed_mfe_r), None)

    opportunity_created = next((_dt(row.get("opportunity_created_at")) for row in timing if _dt(row.get("opportunity_created_at")) is not None), None)
    first_ready_at = next((
        _dt(row.get("timing_decision_at"))
        for row in timing
        if str(row.get("timing_outcome")) in READY_OUTCOMES and _dt(row.get("timing_decision_at")) is not None
    ), None)
    protect_at = _first_action_time(management, "PROTECT")
    trail_at = _first_action_time(management, "TRAIL")
    primary_at = _first_time_at_or_above(management, _target_r(trade, trade.primary_target))
    expansion_at = _first_time_at_or_above(management, _target_r(trade, trade.expansion_target))

    return TradeEfficiency(
        initial_risk_money=initial_risk_money,
        realized_r=realized_r,
        entry_reference_drift_r=drift_r,
        observed_mfe_r=observed_mfe_r,
        observed_mae_r=observed_mae_r,
        observed_capture_efficiency=observed_capture,
        observed_giveback_r=observed_giveback,
        opportunity_to_entry_seconds=_seconds(opportunity_created, trade.opened_at),
        ready_to_entry_seconds=_seconds(first_ready_at, trade.opened_at),
        trigger_to_entry_seconds=_seconds(trade.timing_trigger_time, trade.opened_at),
        m5_event_to_entry_seconds=_seconds(trade.m5_event_time, trade.opened_at),
        time_to_first_protect_seconds=_seconds(trade.opened_at, protect_at),
        time_to_first_trail_seconds=_seconds(trade.opened_at, trail_at),
        time_to_observed_primary_target_seconds=_seconds(trade.opened_at, primary_at),
        time_to_observed_expansion_target_seconds=_seconds(trade.opened_at, expansion_at),
        time_to_observed_mfe_seconds=_seconds(trade.opened_at, first_mfe_at),
        management_samples=len(management),
    )
