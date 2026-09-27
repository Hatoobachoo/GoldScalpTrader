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
    account_balance: float | None = None
    account_equity: float | None = None
    free_margin: float | None = None
    buy_score: float | None = None
    sell_score: float | None = None
    leading_score: float | None = None
    evidence_coverage: float | None = None
    m5_seconds_remaining: int | None = None
    ema20: float | None = None
    ema50: float | None = None
    rsi14: float | None = None
    atr14: float | None = None
    h4_structure: str = "UNKNOWN"
    h1_structure: str = "UNKNOWN"
    m15_structure: str = "UNKNOWN"
    m5_structure: str = "UNKNOWN"
    risk_profile: str = "NOT EVALUATED"
    risk_pct: float | None = None
    risk_volume: float | None = None
