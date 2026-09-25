"""Atomic read-only operator DTOs."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardData:
    symbol: str
    bid: float | None
    ask: float | None
    spread: float | None
    market_state: str
    soft_session: str
    bot_status: str
    detected_setup: str
    active_family: str
    live_action: str
    reason: str
    shadow_setups: tuple[str, ...]
    risk_text: str
    gate_text: str
    news_text: str
    system_text: str
    trade_plan_text: str = "NOT AVAILABLE"
    managed_trade_text: str = "NONE"
    execution_text: str = "IDLE"
    activity_text: str = ""
    learning_text: str = ""
