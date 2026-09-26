from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from gold_scalp_trader.domain.enums import Direction, StrategyFamily


@dataclass(frozen=True, slots=True)
class ManagedTrade:
    trade_id: str
    ticket: int
    symbol: str
    direction: Direction
    volume: float
    entry: float
    original_sl: float
    current_sl: float
    primary_target: float
    expansion_target: float | None
    family: StrategyFamily
    policy_version: str
    original_r_price: float
    opened_at: datetime | None = None
    opportunity_id: str | None = None
    episode_id: str | None = None
    trade_plan_id: str | None = None
    entry_reference: float | None = None
    m5_source_event_ids: tuple[str, ...] = ()
    m5_event_time: datetime | None = None
    timing_profile: str | None = None
    timing_policy_version: str | None = None
    timing_trigger_time: datetime | None = None
    m5_event_age_seconds: float | None = None
    m5_event_age_bars: int | None = None
    trigger_age_seconds: float | None = None
    chase_atr: float | None = None
    micro_extension_atr: float | None = None
