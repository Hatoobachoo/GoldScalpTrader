from datetime import datetime, timezone

from graphical_dashboard.controls import ChartControlState
from graphical_dashboard.server import SUPPORTED_SCHEMAS, load_snapshot
from graphical_dashboard.snapshot import build_snapshot
from graphical_dashboard.ui import HTML
from gold_scalp_trader.operator.presentation import DashboardData

UTC = timezone.utc


def _data() -> DashboardData:
    return DashboardData(
        symbol="XAUUSDm",
        bid=4285.897,
        ask=4286.157,
        spread=0.260,
        market_state="CLOSED",
        soft_session="OFF_HOURS",
        bot_status="SCANNING",
        detected_setup="BREAKOUT_EXPANSION",
        active_family="TREND_PULLBACK_CONTINUATION",
        live_action="WAIT",
        reason="ACTIVE_FAMILY_SETUP_NOT_PRESENT",
        shadow_setups=("BREAKOUT_EXPANSION",),
        risk_text="NOT EVALUATED",
        gate_text="NOT EVALUATED",
        news_text="UNAVAILABLE • SOFT ONLY",
        system_text="DASHBOARD ALIVE",
    )


def test_chart_controls_are_functional_presentation_state_only():
    state = ChartControlState()
    state.set_timeframe("M1")
    assert state.timeframe == "M1"
    old = state.indicators_visible
    state.toggle_indicators()
    assert state.indicators_visible is not old
    state.toggle_drawings()
    assert state.drawings_enabled
    state.add_horizontal_drawing(4312.5)
    assert state.horizontal_drawings == [4312.5]
    state.clear_drawings()
    assert state.horizontal_drawings == []
    state.toggle_settings()
    assert state.settings_open
    state.toggle_overlay("EMA20")
    assert "EMA20" not in state.overlays
    state.set_candle_limit(120)
    assert state.candle_limit == 120


def test_visual_floor_keeps_swing_style_information_hierarchy_without_trade_controls():
    for label in (
        "CANDLE CLOSE (M5)",
        "CURRENT SIGNAL / DECISION",
        "TRADE PLAN",
        "CURRENT BLOCKER / GATE",
        "STRATEGY / SETUP BOARD",
        "OPEN / MANAGED TRADE",
        "EXECUTION & CONTROLLER",
        "LEARNING & DISCOVERY",
        "SYSTEM & DATA",
        "RECENT VERIFIED CLOSES",
        "Terminal = PRIMARY",
        "Browser = SECONDARY",
    ):
        assert label in HTML
    assert 'class="tabs"' in HTML
    for timeframe in ("M1", "M5", "M15", "H1", "H4"):
        assert f'data-tf="{timeframe}"' in HTML
    assert 'id="indBtn"' in HTML
    assert 'id="drawBtn"' in HTML
    assert 'id="settingsBtn"' in HTML
    assert 'type="submit"' not in HTML
    assert "order_send" not in HTML


def test_snapshot_v2_exposes_all_six_families_and_active_isolation_without_authority():
    payload = build_snapshot(
        _data(),
        {},
        generated_at_utc=datetime(2026, 9, 27, 12, 0, tzinfo=UTC),
    )
    assert payload["schema_version"] == 2
    assert len(payload["strategy_board"]) == 6
    active = [row for row in payload["strategy_board"] if row["mode"] == "ACTIVE_EXECUTION"]
    assert len(active) == 1
    assert active[0]["family"] == "TREND_PULLBACK_CONTINUATION"
    assert payload["shadows"] == ["BREAKOUT_EXPANSION"]


def test_server_accepts_v2_snapshot_and_preserves_stale_visibility(tmp_path):
    path = tmp_path / "dashboard_snapshot.json"
    payload = build_snapshot(
        _data(),
        {},
        generated_at_utc=datetime(2026, 9, 27, 12, 0, tzinfo=UTC),
    )
    import json

    path.write_text(json.dumps(payload), encoding="utf-8")
    result = load_snapshot(path, now_utc=datetime(2026, 9, 27, 12, 0, 10, tzinfo=UTC))
    assert 2 in SUPPORTED_SCHEMAS
    assert result["ok"] is True
    assert result["online"] is False
    assert result["message"] == "BOT OFFLINE / SNAPSHOT STALE"
