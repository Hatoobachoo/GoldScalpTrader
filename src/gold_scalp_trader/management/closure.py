"""Crash-safe close proof and archive helpers for known bot ManagedTrades."""
from __future__ import annotations
from gold_scalp_trader.market_data.activity import DealFacts
from gold_scalp_trader.persistence.store import StateStore, StateIntegrityError
from gold_scalp_trader.research.live_learning import enqueue
from .models import ManagedTrade
from .store import clear

RECEIPT_NS = "managed_trade_closure_receipt"


def matching_exit_deals(deals: tuple[DealFacts, ...] | None, trade: ManagedTrade) -> tuple[DealFacts, ...]:
    if deals is None:
        return ()
    return tuple(
        d
        for d in deals
        if d.position_id == trade.ticket
        and d.entry_role.upper() in {"OUT", "OUT_BY", "INOUT"}
        and d.volume > 0
    )


def complete_exit_proved(
    deals: tuple[DealFacts, ...] | None,
    trade: ManagedTrade,
    *,
    tolerance: float = 1e-8,
) -> bool:
    exits = matching_exit_deals(deals, trade)
    return bool(exits) and sum(d.volume for d in exits) + tolerance >= trade.volume


def close_origin(deals: tuple[DealFacts, ...] | None, trade: ManagedTrade, *, bot_magic: int) -> str:
    exits = matching_exit_deals(deals, trade)
    if not exits:
        return "UNKNOWN"
    flags = [d.magic == bot_magic for d in exits]
    return "BOT" if all(flags) else "EXTERNAL" if not any(flags) else "MIXED"


def archive_verified_close(
    store: StateStore,
    scope: str,
    trade: ManagedTrade,
    deals: tuple[DealFacts, ...],
    *,
    bot_magic: int,
    close_intent_id: str | None = None,
    reason: str,
) -> None:
    if not complete_exit_proved(deals, trade):
        raise ValueError("complete exit deal proof is required")
    existing = store.get(RECEIPT_NS, trade.trade_id)
    if existing is not None:
        prior = existing.payload.get("close_intent_id")
        if prior not in {None, close_intent_id} and close_intent_id is not None:
            raise StateIntegrityError("conflicting close intent for archived trade")
        clear(store, scope)
        return

    exits = matching_exit_deals(deals, trade)
    closed_at = max(d.time_utc for d in exits)
    origin = close_origin(deals, trade, bot_magic=bot_magic)
    net_money = sum(d.net_money for d in exits)
    serialized = [
        {
            "ticket": d.ticket,
            "position_id": d.position_id,
            "volume": d.volume,
            "net_money": d.net_money,
            "magic": d.magic,
            "entry_role": d.entry_role,
            "deal_type": d.deal_type,
            "time_utc": d.time_utc.isoformat(),
        }
        for d in exits
    ]
    payload = {
        "trade_id": trade.trade_id,
        "position_ticket": trade.ticket,
        "symbol": trade.symbol,
        "direction": trade.direction.value,
        "volume": trade.volume,
        "entry": trade.entry,
        "original_sl": trade.original_sl,
        "original_r_price": trade.original_r_price,
        "family": trade.family.value,
        "policy_version": trade.policy_version,
        "opened_at": None if trade.opened_at is None else trade.opened_at.isoformat(),
        "closed_at": closed_at.isoformat(),
        "close_origin": origin,
        "net_money": net_money,
        "close_intent_id": close_intent_id,
        "reason": reason,
        "deals": serialized,
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
    }
    enqueue(store, trade.trade_id, payload)
    store.put(
        RECEIPT_NS,
        trade.trade_id,
        {
            "trade_id": trade.trade_id,
            "position_ticket": trade.ticket,
            "closed_at": closed_at.isoformat(),
            "close_origin": origin,
            "close_intent_id": close_intent_id,
            "reason": reason,
            "net_money": net_money,
        },
        allow_replace=False,
    )
    clear(store, scope)
