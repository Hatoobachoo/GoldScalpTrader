"""Durable ManagedTrade storage with original strategy/R preservation."""
from __future__ import annotations

from datetime import datetime

from gold_scalp_trader.domain.enums import Direction, StrategyFamily
from gold_scalp_trader.persistence.store import StateStore
from .models import ManagedTrade

NS = "managed_trade"


def save(store: StateStore, scope: str, trade: ManagedTrade) -> None:
    store.put(
        NS,
        scope,
        {
            "trade_id": trade.trade_id,
            "ticket": trade.ticket,
            "symbol": trade.symbol,
            "direction": trade.direction.value,
            "volume": trade.volume,
            "entry": trade.entry,
            "original_sl": trade.original_sl,
            "current_sl": trade.current_sl,
            "primary_target": trade.primary_target,
            "expansion_target": trade.expansion_target,
            "family": trade.family.value,
            "policy_version": trade.policy_version,
            "original_r_price": trade.original_r_price,
            "opened_at": None if trade.opened_at is None else trade.opened_at.isoformat(),
        },
    )


def load(store: StateStore, scope: str) -> ManagedTrade | None:
    record = store.get(NS, scope)
    if record is None:
        return None
    payload = record.payload
    opened_raw = payload.get("opened_at")
    return ManagedTrade(
        str(payload["trade_id"]),
        int(payload["ticket"]),
        str(payload["symbol"]),
        Direction(payload["direction"]),
        float(payload["volume"]),
        float(payload["entry"]),
        float(payload["original_sl"]),
        float(payload["current_sl"]),
        float(payload["primary_target"]),
        None if payload["expansion_target"] is None else float(payload["expansion_target"]),
        StrategyFamily(payload["family"]),
        str(payload["policy_version"]),
        float(payload["original_r_price"]),
        None if opened_raw is None else datetime.fromisoformat(str(opened_raw)),
    )


def clear(store: StateStore, scope: str) -> None:
    store.delete(NS, scope)
