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
