"""Research-only runtime evidence for management efficiency and shadow families.

This module never grants broker, Risk, Gate, Session or promotion authority.
It records causal observations so later governed research can compare actual
management paths with same-market shadow strategy evidence.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from typing import Any

from gold_scalp_trader.domain.enums import StrategyMode, Timeframe
from gold_scalp_trader.persistence.store import StateStore

MANAGEMENT_NS = "management_decision_evidence"
SHADOW_NS = "shadow_strategy_evidence"
SCHEMA_VERSION = 1


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
