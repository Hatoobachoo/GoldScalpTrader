"""Primary terminal dashboard dispatcher.

GoldSwingTrader-style operator hierarchy: Rich wide terminal, width-safe narrow
terminal, crash-safe compact fallback. Presentation only; no trading authority.
"""
from __future__ import annotations

from shutil import get_terminal_size

from .compact_dashboard import render_dashboard as _render_compact
from .narrow_dashboard import render_dashboard as _render_narrow
from .presentation import DashboardData
from .rich_dashboard import render_dashboard as _render_rich

NARROW_TERMINAL_MAX_WIDTH = 95
MIN_WIDTH = 64
MAX_WIDTH = 180


def render(
    data: DashboardData,
    *,
    width: int | None = None,
    emoji: bool = True,
    color: bool | None = None,
) -> str:
    """Render one always-visible primary operator frame."""
    actual = width or get_terminal_size((120, 30)).columns
    actual = max(MIN_WIDTH, min(MAX_WIDTH, int(actual)))
    try:
        if actual <= NARROW_TERMINAL_MAX_WIDTH:
            return _render_narrow(data, emoji=emoji, width=actual, color=color)
        return _render_rich(data, emoji=emoji, width=actual, color=color)
    except Exception:
        return _render_compact(data, emoji=emoji, width=actual, color=color)


def render_error(title: str, exc: Exception, *, width: int | None = None) -> str:
    """Render a fail-visible primary frame before normal runtime facts exist."""
    data = DashboardData(
        symbol="XAUUSDm",
        bid=None,
        ask=None,
        spread=None,
        market_state="UNKNOWN",
        soft_session="UNKNOWN",
        bot_status="SAFETY BLOCK / DEGRADED",
        detected_setup="UNAVAILABLE",
        active_family="UNAVAILABLE",
        live_action="WAIT",
        reason=f"{title}: {type(exc).__name__}: {exc}",
        shadow_setups=(),
        risk_text="NOT EVALUATED",
        gate_text="NOT EVALUATED",
        news_text="UNKNOWN • SOFT ONLY",
        system_text="DASHBOARD ALIVE • TRADING FAIL-CLOSED • NO BROKER WRITE FROM FAILED CYCLE",
        trade_plan_text="NOT AVAILABLE",
        managed_trade_text="UNKNOWN",
        execution_text="NO BROKER ACTION FROM FAILED CYCLE",
        activity_text="Runtime/startup facts unavailable",
        learning_text="PAUSED until runtime health recovers",
    )
    return render(data, width=width)


__all__ = ["NARROW_TERMINAL_MAX_WIDTH", "render", "render_error"]
