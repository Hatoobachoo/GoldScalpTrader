"""Broker activity helpers.

Missing activity/history is UNKNOWN, not an empty list. Deal/cash-flow expansion
is added in the broker-accounting phase.
"""
from __future__ import annotations

from dataclasses import dataclass
from gold_scalp_trader.domain.enums import DataQuality


@dataclass(frozen=True, slots=True)
class ActivitySummary:
    quality: DataQuality
    bot_entries: int | None = None
    external_open_positions: int | None = None
    net_non_trading_cash_flow: float | None = None
