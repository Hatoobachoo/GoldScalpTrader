from __future__ import annotations

from gold_scalp_trader.operator.presentation import DashboardData
from gold_scalp_trader.operator.terminal_dashboard import render


def _data() -> DashboardData:
    return DashboardData(
        symbol="XAUUSDm",
        bid=4300.100,
        ask=4300.400,
        spread=0.300,
        market_state="CLOSED",
        soft_session="OFF HOURS",
        bot_status="WAITING",
        detected_setup="NO VALID SETUP",
        active_family="TREND_PULLBACK_CONTINUATION",
        live_action="WAIT",
        reason="SESSION_CLOSED",
        shadow_setups=("LIQUIDITY_SWEEP_REVERSAL",),
        risk_text="NOT EVALUATED",
        gate_text="BLOCKED • SESSION_CLOSED",
        news_text="UNKNOWN • SOFT ONLY",
        system_text="DASHBOARD ALIVE • TRADING FAIL-CLOSED",
        trade_plan_text="NOT AVAILABLE",
        managed_trade_text="NONE",
        execution_text="NO BROKER ACTION",
        activity_text="Open Gold positions: 0",
        learning_text="Verified evidence ka intazar",
        live_feed_state="STALE",
        account_mode="DEMO",
        runtime_role="PRIMARY",
        m5_seconds_remaining=125,
        h4_structure="UNKNOWN",
        h1_structure="UNKNOWN",
        m15_structure="UNKNOWN",
        m5_structure="UNKNOWN",
        strategy_board_rows=(
            ("TREND_PULLBACK_CONTINUATION", "ACTIVE_EXECUTION", "QUALIFIED", "BUY", 0.72, 0.80),
            ("LIQUIDITY_SWEEP_REVERSAL", "SHADOW_ONLY", "RESEARCH", "NONE", 0.31, 0.55),
        ),
    )


def test_wide_primary_terminal_follows_swing_floor_hierarchy_and_stays_visible_closed():
    output = render(_data(), width=140, emoji=False, color=False)
    for marker in (
        "GoldScalpTraderAI",
        "PRIMARY LIVE SCALPING FLOOR",
        "Market CLOSED",
        "XAUUSDm",
        "CURRENT DECISION",
        "WAIT",
        "Intazar",
        "MARKET PICTURE · Market Jaiza",
        "TRADE SETUP · Setup aur Route",
        "TRADE PLAN",
        "STRATEGY / SETUP BOARD  |  1 ROUTED + 5 SHADOW",
        "RISK & ACCOUNT",
        "Mehfooz risk",
        "TODAY / ACTIVITY · Aaj ki Soorat",
        "SYSTEM / EXECUTION · Nizam aur Ijazat",
        "LEARNING / DISCOVERY · Seekhna aur Daryaft",
        "Scores = research/diagnostic facts only",
        "Browser = SECONDARY read-only projection",
    ):
        assert marker in output
    assert "SESSION_CLOSED" in output
    assert "BUY NOW" not in output
    assert "SELL NOW" not in output
    assert "MODIFY NOW" not in output
    assert "CLOSE NOW" not in output


def test_primary_operational_wording_has_no_urdu_script():
    output = render(_data(), width=140, emoji=False, color=False)
    for forbidden in ("انتظار", "فروخت", "خرید", "موجودہ", "فیصلہ"):
        assert forbidden not in output
