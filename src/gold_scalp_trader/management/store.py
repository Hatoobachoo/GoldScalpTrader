"""Durable ManagedTrade storage with original strategy/R and timing lineage preservation."""
from __future__ import annotations

from datetime import datetime

from gold_scalp_trader.domain.enums import Direction, StrategyFamily
from gold_scalp_trader.persistence.store import StateStore
from .models import ManagedTrade

NS = "managed_trade"


def _dt(value):
    return None if value is None else datetime.fromisoformat(str(value))


def _opt_float(value):
    return None if value is None else float(value)


def _opt_int(value):
    return None if value is None else int(value)


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
            "opportunity_id": trade.opportunity_id,
            "episode_id": trade.episode_id,
            "trade_plan_id": trade.trade_plan_id,
            "entry_reference": trade.entry_reference,
            "m5_source_event_ids": list(trade.m5_source_event_ids),
            "m5_event_time": None if trade.m5_event_time is None else trade.m5_event_time.isoformat(),
            "timing_profile": trade.timing_profile,
            "timing_policy_version": trade.timing_policy_version,
            "timing_trigger_time": None if trade.timing_trigger_time is None else trade.timing_trigger_time.isoformat(),
            "m5_event_age_seconds": trade.m5_event_age_seconds,
            "m5_event_age_bars": trade.m5_event_age_bars,
            "trigger_age_seconds": trade.trigger_age_seconds,
            "chase_atr": trade.chase_atr,
            "micro_extension_atr": trade.micro_extension_atr,
        },
    )


def load(store: StateStore, scope: str) -> ManagedTrade | None:
    record = store.get(NS, scope)
    if record is None:
        return None
    p = record.payload
    return ManagedTrade(
        trade_id=str(p["trade_id"]),
        ticket=int(p["ticket"]),
        symbol=str(p["symbol"]),
        direction=Direction(p["direction"]),
        volume=float(p["volume"]),
        entry=float(p["entry"]),
        original_sl=float(p["original_sl"]),
        current_sl=float(p["current_sl"]),
        primary_target=float(p["primary_target"]),
        expansion_target=_opt_float(p.get("expansion_target")),
        family=StrategyFamily(p["family"]),
        policy_version=str(p["policy_version"]),
        original_r_price=float(p["original_r_price"]),
        opened_at=_dt(p.get("opened_at")),
        opportunity_id=None if p.get("opportunity_id") is None else str(p["opportunity_id"]),
        episode_id=None if p.get("episode_id") is None else str(p["episode_id"]),
        trade_plan_id=None if p.get("trade_plan_id") is None else str(p["trade_plan_id"]),
        entry_reference=_opt_float(p.get("entry_reference")),
        m5_source_event_ids=tuple(str(x) for x in p.get("m5_source_event_ids", ())),
        m5_event_time=_dt(p.get("m5_event_time")),
        timing_profile=None if p.get("timing_profile") is None else str(p["timing_profile"]),
        timing_policy_version=None if p.get("timing_policy_version") is None else str(p["timing_policy_version"]),
        timing_trigger_time=_dt(p.get("timing_trigger_time")),
        m5_event_age_seconds=_opt_float(p.get("m5_event_age_seconds")),
        m5_event_age_bars=_opt_int(p.get("m5_event_age_bars")),
        trigger_age_seconds=_opt_float(p.get("trigger_age_seconds")),
        chase_atr=_opt_float(p.get("chase_atr")),
        micro_extension_atr=_opt_float(p.get("micro_extension_atr")),
    )


def clear(store: StateStore, scope: str) -> None:
    store.delete(NS, scope)
