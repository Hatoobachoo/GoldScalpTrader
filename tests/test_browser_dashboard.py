from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from types import SimpleNamespace

from graphical_dashboard.server import HOST, STALE_AFTER_SECONDS, HTML, load_snapshot
from graphical_dashboard.snapshot import build_snapshot, publish_snapshot
from gold_scalp_trader.operator.presentation import DashboardData

NOW = datetime(2026, 9, 27, 4, 0, tzinfo=timezone.utc)


def _data() -> DashboardData:
    return DashboardData(
        symbol="XAUUSDm",
        bid=4300.1,
        ask=4300.4,
        spread=0.3,
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
        execution_text="IDLE",
        activity_text="Open Gold positions: 0",
        learning_text="Timing + management + actual/shadow evidence active",
    )


def _candle(tf: str, minutes: int, price: float) -> SimpleNamespace:
    return SimpleNamespace(
        open_time=NOW - timedelta(minutes=minutes),
        close_time=NOW - timedelta(minutes=max(0, minutes - 1)),
        open=price,
        high=price + 1.0,
        low=price - 0.8,
        close=price + 0.4,
        tick_volume=100 + minutes,
    )


def test_browser_visual_floor_is_localhost_read_only_and_matches_swing_style_hierarchy() -> None:
    assert HOST == "127.0.0.1"
    assert "GoldScalpTraderAI" in HTML
    assert "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ" in HTML
    assert "محفوظ عمل" in HTML
    assert "PRIMARY" not in HTML.split("SECONDARY localhost visual floor")[0] or "SECONDARY" in HTML
    for timeframe in ("M1", "M5", "M15", "H1", "H4"):
        assert f'"{timeframe}"' in HTML
    for marker in (
        "Indicators ON",
        "Drawings OFF",
        "Bars 60",
        "CURRENT SIGNAL / DECISION",
        "TIMING INTELLIGENCE",
        "TRADE PLAN",
        "CURRENT BLOCKER / GATE",
        "STRATEGY ISOLATION",
        "RISK & ACCOUNT",
        "OPEN / MANAGED TRADE",
        "LEARNING",
        "DISCOVERY",
        "SYSTEM",
        "no broker controls",
    ):
        assert marker in HTML
    assert "BUY NOW" not in HTML
    assert "SELL NOW" not in HTML
    assert "MODIFY NOW" not in HTML
    assert 'fetch("/api/snapshot"' in HTML


def test_browser_snapshot_carries_closed_market_and_completed_chart_facts(tmp_path: Path) -> None:
    candles = {
        "M1": (_candle("M1", 2, 4299.0),),
        "M5": (_candle("M5", 10, 4298.0), _candle("M5", 5, 4299.0)),
        "M15": (),
        "H1": (),
        "H4": (),
    }
    payload = build_snapshot(_data(), candles, generated_at_utc=NOW)
    assert payload["market"]["state"] == "CLOSED"
    assert payload["session"]["soft_session"] == "OFF HOURS"
    assert payload["decision"]["action"] == "WAIT"
    assert payload["charts"]["M5"][1]["close"] == 4299.4
    assert payload["shadows"] == ["LIQUIDITY_SWEEP_REVERSAL"]
    assert "strategy_board" in payload
    assert "timing" in payload
    assert "plan" in payload
    assert "risk" in payload

    target = tmp_path / "dashboard_snapshot.json"
    publish_snapshot(target, payload)
    disk = json.loads(target.read_text(encoding="utf-8"))
    assert disk["schema_version"] == 2
    assert not (tmp_path / ".dashboard_snapshot.json.tmp").exists()


def test_browser_snapshot_liveness_is_distinct_from_market_closed(tmp_path: Path) -> None:
    target = tmp_path / "dashboard_snapshot.json"
    publish_snapshot(target, build_snapshot(_data(), {}, generated_at_utc=NOW))

    live = load_snapshot(target, now_utc=NOW + timedelta(seconds=STALE_AFTER_SECONDS - 1))
    stale = load_snapshot(target, now_utc=NOW + timedelta(seconds=STALE_AFTER_SECONDS + 1))

    assert live["online"] is True
    assert live["snapshot"]["market"]["state"] == "CLOSED"
    assert live["message"] == "LIVE"
    assert stale["online"] is False
    assert stale["snapshot"]["market"]["state"] == "CLOSED"
    assert stale["message"] == "BOT OFFLINE / SNAPSHOT STALE"


def test_browser_snapshot_missing_file_still_returns_visible_wait_state(tmp_path: Path) -> None:
    state = load_snapshot(tmp_path / "missing.json", now_utc=NOW)
    assert state["ok"] is False
    assert state["online"] is False
    assert "Waiting" in state["message"]
