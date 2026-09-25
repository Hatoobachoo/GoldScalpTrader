from types import SimpleNamespace

from gold_scalp_trader.app.graphical_demo_runner import RuntimeDashboardProvider, run_graphical_demo
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, StrategyFamily, Timeframe
from gold_scalp_trader.persistence.store import StateStore
import gold_scalp_trader.app.graphical_demo_runner as graphical_runner


class FakeMarket:
    def series(self, timeframe):
        return (timeframe.value,)


class FakeDashboard:
    def __init__(self, provider, *, refresh_ms, on_close):
        self.provider = provider
        self.refresh_ms = refresh_ms
        self.on_close = on_close
        self.payload = None

    def run(self):
        self.payload = self.provider()
        self.on_close()


def _settings(path=":memory:"):
    return Settings(
        mode=RuntimeMode.DEMO,
        active_strategy_family=StrategyFamily.TREND_PULLBACK_CONTINUATION,
        target_risk_percent=1.0,
        demo_trading_confirm="YES_I_APPROVE_DEMO",
        state_db_path=str(path),
        dashboard_mode="GUI",
    )


def test_graphical_provider_advances_exactly_one_runtime_cycle_per_poll(monkeypatch):
    result = SimpleNamespace(
        cycle=SimpleNamespace(intelligence=SimpleNamespace(market=FakeMarket()))
    )
    calls = []

    def step(settings, api, store):
        calls.append(1)
        return result

    monkeypatch.setattr(graphical_runner, "from_runtime", lambda value, market_state: "DTO")
    store = StateStore()
    provider = RuntimeDashboardProvider(_settings(), object(), store, step=step)
    data, candles = provider()
    assert data == "DTO"
    assert calls == [1]
    assert provider.calls == 1
    assert candles["M1"] == ("M1",)
    assert candles["H4"] == ("H4",)
    store.close()


def test_graphical_runner_uses_timer_provider_and_writes_checkpoint(tmp_path, monkeypatch):
    state_path = tmp_path / "demo.sqlite3"
    result = SimpleNamespace(
        cycle=SimpleNamespace(intelligence=SimpleNamespace(market=FakeMarket()))
    )

    def step(settings, api, store):
        return result

    monkeypatch.setattr(graphical_runner, "from_runtime", lambda value, market_state: "DTO")
    assert run_graphical_demo(
        _settings(state_path),
        object(),
        dashboard_cls=FakeDashboard,
        step=step,
    ) == 0
    assert state_path.with_suffix(".checkpoint.json").exists()
