"""Atomic read-only operator DTOs.

The presentation DTO is intentionally richer than the trading decision object so
both the primary terminal floor and the secondary localhost browser can render
the same authoritative facts without recomputing strategy, Risk, Gate or broker
authority.  Missing evidence stays ``None``/UNKNOWN rather than becoming fake 0.
"""
from __future__ import annotations

from dataclasses import dataclass

StrategyBoardRow = tuple[str, str, str, str, float | None, float | None]


@dataclass(frozen=True, slots=True)
class DashboardData:
    # Core facts kept positional for backward compatibility with existing callers.
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

    # Existing optional presentation facts.
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

    # GoldSwing-style operator facts.  Presentation only; no authority is created.
    account_mode: str = "DEMO"
    runtime_role: str = "PRIMARY"
    quote_time_utc: str | None = None
    analysis_time_utc: str | None = None
    hard_session_source: str | None = None
    hard_session_reason: str | None = None
    schedule_verified: bool | None = None
    news_health: str = "UNKNOWN"

    plan_state: str | None = None
    plan_direction: str | None = None
    plan_entry: float | None = None
    plan_stop: float | None = None
    plan_primary: float | None = None
    plan_expansion: float | None = None
    plan_primary_rr: float | None = None
    plan_expansion_rr: float | None = None
    plan_quality: float | None = None
    plan_invalidation_source: str | None = None

    position_count: int | None = None
    position_capacity: int = 1
    day_safety_pl: float | None = None
    bot_realized_pl_today: float | None = None
    bot_entries_today: int | None = None
    bot_total_trades: int | None = None
    daily_loss_limit_pct: float | None = None
    daily_remaining_pct: float | None = None
    loss_streak: int | None = None
    cooldown: str = "READY"

    controller_role: str = "LOCAL PRIMARY"
    broker_reconcile: str = "UNKNOWN"
    live_feed_state: str = "UNKNOWN"
    backup_state: str = "LOCAL"
    learning_state: str = "ACTIVE"
    discovery_state: str = "IDLE"
    candidate: str | None = None
    strategy_board_rows: tuple[StrategyBoardRow, ...] = ()


__all__ = ["DashboardData", "StrategyBoardRow"]
