from contextlib import contextmanager

from gold_scalp_trader.app import main as app_main
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, StrategyFamily


def test_main_routes_demo_mode_to_continuous_demo_runner(monkeypatch):
    settings = Settings(
        mode=RuntimeMode.DEMO,
        active_strategy_family=StrategyFamily.TREND_PULLBACK_CONTINUATION,
        target_risk_percent=1.0,
        demo_trading_confirm="YES_I_APPROVE_DEMO",
    )
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
