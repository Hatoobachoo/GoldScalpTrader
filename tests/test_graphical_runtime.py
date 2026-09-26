from types import SimpleNamespace

from gold_scalp_trader.app.graphical_demo_runner import RuntimeDashboardProvider, run_graphical_demo
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, StrategyFamily
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
        if self.on_close is not None:
            self.on_close()


def _settings(path=":memory:", *, confirmed=True):
    return Settings(
        mode=RuntimeMode.DEMO,
        active_strategy_family=StrategyFamily.TREND_PULLBACK_CONTINUATION,
        target_risk_percent=1.0,
        demo_trading_confirm="YES_I_APPROVE_DEMO" if confirmed else "NO",
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

    monkeypatch.setattr(graphical_runner, "record_runtime_timing", lambda store, value: None)
    monkeypatch.setattr(graphical_runner, "record_runtime_research", lambda store, value: None)
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


def test_graphical_provider_turns_runtime_failure_into_visible_degraded_snapshot():
    store = StateStore()

    def broken_step(settings, api, state_store):
        raise RuntimeError("MT5 initialize failed: terminal unavailable")

    provider = RuntimeDashboardProvider(_settings(), object(), store, step=broken_step)
    data, candles = provider()
    assert data.bot_status == "DEGRADED"
    assert data.live_action == "WAIT"
    assert "MT5 initialize failed" in data.reason
    assert "TRADING FAIL-CLOSED" in data.system_text
    assert data.gate_text.startswith("BLOCKED")
    assert candles == {}
    assert provider.calls == 1
    store.close()


def test_graphical_provider_retains_last_healthy_snapshot_and_candles_on_later_fault(monkeypatch):
    result = SimpleNamespace(
        cycle=SimpleNamespace(intelligence=SimpleNamespace(market=FakeMarket()))
    )
    state = {"calls": 0}

    def step(settings, api, store):
        state["calls"] += 1
        if state["calls"] == 1:
            return result
        raise RuntimeError("quote feed unavailable")

    from gold_scalp_trader.operator.presentation import DashboardData

    healthy = DashboardData(
        "XAUUSDm", 100.0, 100.2, 0.2, "CLOSED", "WEEKEND", "SCANNING",
        "NO VALID SETUP", "TREND_PULLBACK_CONTINUATION", "WAIT", "market closed", (),
        "NOT EVALUATED", "BLOCKED", "SOFT CONTEXT", "SYSTEM HEALTHY",
    )
    monkeypatch.setattr(graphical_runner, "record_runtime_timing", lambda store, value: None)
    monkeypatch.setattr(graphical_runner, "record_runtime_research", lambda store, value: None)
    monkeypatch.setattr(graphical_runner, "from_runtime", lambda value, market_state: healthy)
    store = StateStore()
    provider = RuntimeDashboardProvider(_settings(), object(), store, step=step)
    first_data, first_candles = provider()
    second_data, second_candles = provider()
    assert first_data.market_state == "CLOSED"
    assert second_data.market_state == "CLOSED"
    assert second_data.bot_status == "DEGRADED"
    assert "quote feed unavailable" in second_data.reason
    assert second_candles == first_candles
    store.close()


def test_graphical_runner_uses_timer_provider_and_writes_checkpoint(tmp_path, monkeypatch):
    state_path = tmp_path / "demo.sqlite3"
    result = SimpleNamespace(
        cycle=SimpleNamespace(intelligence=SimpleNamespace(market=FakeMarket()))
    )

    def step(settings, api, store):
        return result

    monkeypatch.setattr(graphical_runner, "record_runtime_timing", lambda store, value: None)
    monkeypatch.setattr(graphical_runner, "record_runtime_research", lambda store, value: None)
    monkeypatch.setattr(graphical_runner, "from_runtime", lambda value, market_state: "DTO")
    assert run_graphical_demo(
        _settings(state_path),
        object(),
        dashboard_cls=FakeDashboard,
        step=step,
    ) == 0
    assert state_path.with_suffix(".checkpoint.json").exists()


def test_graphical_runner_still_opens_when_demo_permission_is_blocked(tmp_path):
    state_path = tmp_path / "blocked.sqlite3"

    def blocked_step(settings, api, store):
        raise PermissionError("DEMO confirmation missing")

    dashboard = FakeDashboard
    assert run_graphical_demo(
        _settings(state_path, confirmed=False),
        object(),
        dashboard_cls=dashboard,
        step=blocked_step,
    ) == 0
    assert state_path.with_suffix(".checkpoint.json").exists()
