from contextlib import contextmanager

from gold_scalp_trader.app import main as app_main
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, StrategyFamily
from gold_scalp_trader.operator.presentation import DashboardData
from gold_scalp_trader.operator.terminal_dashboard import render, render_error


def _settings(*, dashboard_mode: str) -> Settings:
    return Settings(
        mode=RuntimeMode.DEMO,
        active_strategy_family=StrategyFamily.TREND_PULLBACK_CONTINUATION,
        target_risk_percent=1.0,
        demo_trading_confirm="YES_I_APPROVE_DEMO",
        dashboard_mode=dashboard_mode,
    )


class FakeLazyApi:
    def __init__(self): self.closed = False
    def close(self): self.closed = True


def _assert_demo_mode_uses_terminal_first_lazy_runtime(monkeypatch, dashboard_mode: str):
    settings = _settings(dashboard_mode=dashboard_mode); api = FakeLazyApi(); called = {}
    def forbidden_session(): raise AssertionError("DEMO dashboard must not require eager mt5_session startup")
    def fake_demo_runner(received_settings, received_api): called["settings"] = received_settings; called["api"] = received_api; return 0
    monkeypatch.setattr(app_main, "load_settings", lambda: settings); monkeypatch.setattr(app_main, "mt5_session", forbidden_session); monkeypatch.setattr(app_main, "LazyMt5Api", lambda: api); monkeypatch.setattr(app_main, "run_live_demo", fake_demo_runner)
    assert app_main.run() == 0; assert called["settings"] is settings; assert called["api"] is api; assert api.closed is True


def test_terminal_mode_uses_primary_terminal_runtime(monkeypatch): _assert_demo_mode_uses_terminal_first_lazy_runtime(monkeypatch, "TERMINAL")
def test_gui_mode_uses_same_primary_runtime_and_only_adds_secondary_view(monkeypatch): _assert_demo_mode_uses_terminal_first_lazy_runtime(monkeypatch, "GUI")


def test_non_demo_read_mode_still_uses_mt5_session(monkeypatch):
    settings=Settings(mode=RuntimeMode.DRY_RUN,dashboard_mode="TERMINAL"); marker=object(); called={}
    @contextmanager
    def fake_session(): called["session"]=True; yield marker
    class Result: wrote_broker=False; cycle=object()
    monkeypatch.setattr(app_main,"load_settings",lambda:settings); monkeypatch.setattr(app_main,"mt5_session",fake_session); monkeypatch.setattr(app_main,"run_read_cycle",lambda received_settings,api:Result()); monkeypatch.setattr(app_main,"from_cycle",lambda cycle:"DTO"); monkeypatch.setattr(app_main,"render",lambda dto:"FRAME")
    assert app_main.run()==0; assert called["session"] is True


def test_configuration_failure_renders_primary_terminal_error(monkeypatch,capsys):
    def broken_settings(): raise ValueError("bad configuration")
    monkeypatch.setattr(app_main,"load_settings",broken_settings); assert app_main.run()==2; output=capsys.readouterr().out; assert "GoldScalpTraderAI" in output; assert "CONFIGURATION ERROR" in output; assert "bad configuration" in output; assert "No broker write was attempted" in output


def _dashboard_data():
    rows=(("TREND_PULLBACK_CONTINUATION","ACTIVE_EXECUTION","QUALIFIED","BUY",0.62,0.78),("BREAKOUT_RETEST","SHADOW_ONLY","QUALIFIED","BUY",0.55,0.72),("LIQUIDITY_SWEEP_REVERSAL","SHADOW_ONLY","NOT_QUALIFIED","NONE",0.31,0.61),("RANGE_REJECTION","SHADOW_ONLY","NOT_QUALIFIED","NONE",0.22,0.55),("MOMENTUM_CONTINUATION","SHADOW_ONLY","NOT_QUALIFIED","NONE",0.28,0.58),("FAILED_BREAK_REVERSAL","SHADOW_ONLY","NOT_QUALIFIED","NONE",0.19,0.49))
    return DashboardData(symbol="XAUUSDm",bid=4300.123,ask=4300.321,spread=0.198,market_state="CLOSED",soft_session="OFF_HOURS",bot_status="SCANNING",detected_setup="TREND_PULLBACK_CONTINUATION",active_family="TREND_PULLBACK_CONTINUATION",live_action="WAIT",reason="market is closed; dashboard remains available",shadow_setups=("BREAKOUT_RETEST",),risk_text="NOT EVALUATED",gate_text="NOT EVALUATED",news_text="UNKNOWN • SOFT ONLY",system_text="HEALTHY",trade_plan_text="NOT AVAILABLE",managed_trade_text="NONE",execution_text="IDLE",activity_text="Timing: WAIT\nHard Session: CLOSED",learning_text="governed learning active",account_balance=100.0,account_equity=99.5,free_margin=99.5,buy_score=0.41,sell_score=0.58,leading_score=0.58,evidence_coverage=0.75,m5_seconds_remaining=239,ema20=4298.123,ema50=4296.456,rsi14=61.2,atr14=3.912,h4_structure="TRANSITION",h1_structure="BEARISH",m15_structure="BULLISH",m5_structure="TRANSITION",risk_profile="SMALL",strategy_board_rows=rows,live_feed_state="LIVE",controller_role="LOCAL PRIMARY",broker_reconcile="CLEAR",learning_state="ACTIVE",discovery_state="ACTIVE")


def test_primary_terminal_dashboard_is_roman_urdu_emoji_full_frame_and_closed_market_visible():
    frame=render(_dashboard_data(),width=90,color=False)
    for marker in ("GoldScalpTraderAI","🪙","CURRENT DECISION","Maujooda Faisla","Mansuba","Intazar","Market CLOSED","Browser SECONDARY","EMA20","RSI","STRATEGY / SETUP BOARD"):
        assert marker in frame
    assert "ACTIVE EXECUTION" in frame; assert len(frame.splitlines())>=24
    assert "انتظار" not in frame


def test_wide_primary_terminal_dashboard_matches_swing_style_operator_hierarchy():
    frame=render(_dashboard_data(),width=132,color=False)
    for marker in ("GoldScalpTraderAI","PRIMARY LIVE SCALPING FLOOR","MARKET PICTURE","TRADE SETUP","CURRENT DECISION","TRADE PLAN","STRATEGY / SETUP BOARD","RISK & ACCOUNT","TODAY / ACTIVITY","SYSTEM / EXECUTION","LEARNING / DISCOVERY","Mehfooz risk"):
        assert marker in frame


def test_primary_terminal_error_frame_is_fail_visible():
    frame=render_error("MT5 ERROR",RuntimeError("terminal unavailable"),width=90)
    for marker in ("SAFETY BLOCK / DEGRADED","MT5 ERROR","terminal unavailable","TRADING FAIL-CLOSED","NO BROKER WRITE"):
        assert marker in frame
