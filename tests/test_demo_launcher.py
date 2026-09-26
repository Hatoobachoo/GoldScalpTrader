from contextlib import contextmanager

from gold_scalp_trader.app import main as app_main
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, StrategyFamily


def _settings(*, dashboard_mode: str) -> Settings:
    return Settings(
        mode=RuntimeMode.DEMO,
        active_strategy_family=StrategyFamily.TREND_PULLBACK_CONTINUATION,
        target_risk_percent=1.0,
        demo_trading_confirm="YES_I_APPROVE_DEMO",
        dashboard_mode=dashboard_mode,
    )


def test_main_routes_terminal_demo_mode_through_mt5_session(monkeypatch):
    settings = _settings(dashboard_mode="TERMINAL")
    marker = object()
    called = {}

    @contextmanager
    def fake_session():
        yield marker

    def fake_demo_runner(received_settings, api):
        called["settings"] = received_settings
        called["api"] = api
        return 0

    monkeypatch.setattr(app_main, "load_settings", lambda: settings)
    monkeypatch.setattr(app_main, "mt5_session", fake_session)
    monkeypatch.setattr(app_main, "run_live_demo", fake_demo_runner)

    assert app_main.run() == 0
    assert called["settings"] is settings
    assert called["api"] is marker


def test_main_starts_gui_before_mt5_session(monkeypatch):
    settings = _settings(dashboard_mode="GUI")
    called = {}

    def forbidden_session():
        raise AssertionError("GUI startup must not require mt5_session before dashboard creation")

    def fake_graphical(received_settings):
        called["settings"] = received_settings
        return 0

    monkeypatch.setattr(app_main, "load_settings", lambda: settings)
    monkeypatch.setattr(app_main, "mt5_session", forbidden_session)
    monkeypatch.setattr(app_main, "run_graphical_demo_standalone", fake_graphical)

    assert app_main.run() == 0
    assert called["settings"] is settings


def test_configuration_failure_routes_to_fail_visible_error_dashboard(monkeypatch):
    called = {}

    def broken_settings():
        raise ValueError("bad configuration")

    def fake_error_dashboard(title, exc):
        called["title"] = title
        called["error"] = str(exc)
        return 2

    monkeypatch.setattr(app_main, "load_settings", broken_settings)
    monkeypatch.setattr(app_main, "run_error_dashboard", fake_error_dashboard)

    assert app_main.run() == 2
    assert called["title"] == "CONFIGURATION ERROR"
    assert "bad configuration" in called["error"]
