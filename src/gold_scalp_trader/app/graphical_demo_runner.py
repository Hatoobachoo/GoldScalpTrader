"""Live graphical DEMO runtime adapter.

The normal GUI path publishes a read-only atomic snapshot and serves the
GoldSwingTrader-style localhost browser floor.  Browser presentation has no MT5,
Risk, Gate or broker-write authority.  Runtime faults remain visible while
trading fails closed.
"""
from __future__ import annotations

from dataclasses import replace
import importlib
from pathlib import Path
import time
from typing import Callable, Type

from gold_scalp_trader.app.runtime import RuntimeResult, run_guarded_demo_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, Timeframe
from gold_scalp_trader.operator.graphical_snapshot import from_runtime
from gold_scalp_trader.operator.presentation import DashboardData
from gold_scalp_trader.persistence.checkpoint import export_checkpoint
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.runtime_evidence import record_runtime_research
from gold_scalp_trader.research.timing_learning import record_runtime_timing


class LazyMt5Api:
    """Lazily initialize MT5 so dashboard creation never depends on MT5 health."""

    def __init__(self) -> None:
        self._module = None
        self._initialized = False

    def _ensure(self):
        if self._module is None:
            self._module = importlib.import_module("MetaTrader5")
        if not self._initialized:
            if not self._module.initialize():
                error = self._module.last_error() if hasattr(self._module, "last_error") else "UNKNOWN"
                raise RuntimeError(f"MT5 initialize failed: {error}")
            self._initialized = True
        return self._module

    def __getattr__(self, name):
        return getattr(self._ensure(), name)

    def close(self) -> None:
        if self._module is not None and self._initialized:
            try:
                self._module.shutdown()
            finally:
                self._initialized = False


def _active_family_text(settings: Settings) -> str:
    family = settings.active_strategy_family
    return "UNSET" if family is None else family.value


def _initial_degraded_data(settings: Settings, exc: Exception) -> DashboardData:
    symbol = settings.symbol_aliases[0] if settings.symbol_aliases else "XAUUSD"
    message = f"{type(exc).__name__}: {exc}"
    return DashboardData(
        symbol=symbol,
        bid=None,
        ask=None,
        spread=None,
        market_state="UNKNOWN",
        soft_session="UNKNOWN",
        bot_status="DEGRADED",
        detected_setup="UNAVAILABLE",
        active_family=_active_family_text(settings),
        live_action="WAIT",
        reason=message,
        shadow_setups=(),
        risk_text="NOT EVALUATED • runtime health unavailable",
        gate_text="BLOCKED • runtime health unavailable",
        news_text="UNKNOWN • SOFT ONLY",
        system_text=f"DASHBOARD ALIVE • TRADING FAIL-CLOSED • {message}",
        trade_plan_text="NOT AVAILABLE",
        managed_trade_text="UNKNOWN",
        execution_text="NO BROKER ACTION FROM FAILED CYCLE",
        activity_text=f"Runtime issue: {message}",
        learning_text="Evidence collection paused until runtime health recovers",
    )


class RuntimeDashboardProvider:
    def __init__(
        self,
        settings: Settings,
        api,
        store: StateStore,
        *,
        step: Callable[..., RuntimeResult] = run_guarded_demo_cycle,
    ) -> None:
        self.settings = settings
        self.api = api
        self.store = store
        self.step = step
        self.last_result: RuntimeResult | None = None
        self.last_snapshot: DashboardData | None = None
        self.last_candles_by_tf: dict[str, tuple] = {}
        self.last_error: str | None = None
        self.calls = 0

    def _degraded(self, exc: Exception):
        message = f"{type(exc).__name__}: {exc}"
        self.last_error = message
        if self.last_snapshot is None:
            data = _initial_degraded_data(self.settings, exc)
        else:
            data = replace(
                self.last_snapshot,
                bot_status="DEGRADED",
                live_action="WAIT",
                reason=message,
                gate_text="BLOCKED • runtime health unavailable",
                system_text=f"DASHBOARD ALIVE • TRADING FAIL-CLOSED • {message}",
                execution_text="NO BROKER ACTION FROM FAILED CYCLE",
            )
        return data, dict(self.last_candles_by_tf)

    def __call__(self):
        """Advance one governed cycle; convert runtime faults into visible UI state."""
        self.calls += 1
        try:
            result = self.step(self.settings, self.api, self.store)
            record_runtime_timing(self.store, result)
            record_runtime_research(self.store, result)
            market = result.cycle.intelligence.market
            candles_by_tf = {timeframe.value: market.series(timeframe) for timeframe in Timeframe}
            snapshot = from_runtime(result, market_state="DEMO")
            self.last_result = result
            self.last_snapshot = snapshot
            self.last_candles_by_tf = candles_by_tf
            self.last_error = None
            return snapshot, candles_by_tf
        except Exception as exc:
            return self._degraded(exc)


class _DashboardResources:
    def __init__(self, store: StateStore, state_path: Path, api=None) -> None:
        self.store = store
        self.state_path = state_path
        self.api = api
        self.closed = False

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            checkpoint = self.state_path.with_suffix(".checkpoint.json")
            export_checkpoint(self.store, checkpoint)
            print(f"Local runtime checkpoint: {checkpoint}")
        finally:
            try:
                close = getattr(self.api, "close", None)
                if callable(close):
                    close()
            finally:
                self.store.close()


def _run_browser_floor(
    settings: Settings,
    provider: RuntimeDashboardProvider,
    resources: _DashboardResources,
) -> int:
    """Run authoritative runtime polling in this thread and UI HTTP in a daemon thread."""
    from graphical_dashboard.server import start_background, stop_background
    from graphical_dashboard.snapshot import build_snapshot, publish_snapshot

    snapshot_path = resources.state_path.parent / "dashboard_snapshot.json"
    starting = _initial_degraded_data(settings, RuntimeError("Runtime starting"))
    publish_snapshot(snapshot_path, build_snapshot(starting, {}))
    server, server_thread = start_background(snapshot_path, open_browser=True)
    try:
        while True:
            data, candles = provider()
            try:
                payload = build_snapshot(
                    data,
                    candles,
                    runtime_result=provider.last_result,
                )
            except Exception as exc:
                # Presentation serialization must never terminate the trading loop.
                degraded = _initial_degraded_data(
                    settings,
                    RuntimeError(f"dashboard snapshot unavailable: {type(exc).__name__}"),
                )
                payload = build_snapshot(degraded, {})
            try:
                publish_snapshot(snapshot_path, payload)
            except Exception as exc:
                # Keep the server and trading process alive. The browser will truthfully
                # mark the previous frame stale if publication cannot recover.
                print(f"DASHBOARD SNAPSHOT ERROR: {type(exc).__name__}: {exc}")
            time.sleep(max(0.25, float(settings.loop_interval_seconds)))
    except KeyboardInterrupt:
        return 0
    finally:
        stop_background(server, server_thread)
        resources.close()


def run_graphical_demo(
    settings: Settings,
    api,
    *,
    dashboard_cls: Type | None = None,
    step: Callable[..., RuntimeResult] = run_guarded_demo_cycle,
) -> int:
    """Run browser visual floor normally; retain injected legacy UI seam for tests."""
    state_path = Path(settings.state_db_path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    store = StateStore(state_path)
    resources = _DashboardResources(store, state_path, api)
    provider = RuntimeDashboardProvider(settings, api, store, step=step)

    if dashboard_cls is None:
        return _run_browser_floor(settings, provider, resources)

    # Compatibility/test seam. Production GUI uses the browser floor above.
    app = dashboard_cls(
        provider,
        refresh_ms=max(250, int(settings.loop_interval_seconds * 1000)),
        on_close=resources.close,
    )
    try:
        app.run()
        return 0
    finally:
        resources.close()


def run_graphical_demo_standalone(settings: Settings, *, dashboard_cls: Type | None = None) -> int:
    """Create the visual floor before the first MT5 initialize attempt."""
    if settings.mode is not RuntimeMode.DEMO:
        raise PermissionError("graphical live runtime is available only in DEMO mode")
    return run_graphical_demo(settings, LazyMt5Api(), dashboard_cls=dashboard_cls)


def run_error_dashboard(title: str, exc: Exception, *, dashboard_cls: Type | None = None) -> int:
    """Show startup/configuration failure in the same browser visual floor."""
    message = f"{type(exc).__name__}: {exc}"
    data = DashboardData(
        symbol="XAUUSD",
        bid=None,
        ask=None,
        spread=None,
        market_state="UNKNOWN",
        soft_session="UNKNOWN",
        bot_status="SAFETY BLOCK",
        detected_setup="UNAVAILABLE",
        active_family="UNAVAILABLE",
        live_action="WAIT",
        reason=message,
        shadow_setups=(),
        risk_text="BLOCKED",
        gate_text="BLOCKED",
        news_text="UNKNOWN • SOFT ONLY",
        system_text=f"{title} • DASHBOARD ALIVE • NO BROKER WRITE",
        activity_text=message,
        learning_text="Unavailable until startup/configuration is corrected",
    )

    if dashboard_cls is not None:
        def provider():
            return data, {}
        app = dashboard_cls(provider, refresh_ms=2000, on_close=None)
        app.run()
        return 2

    from graphical_dashboard.server import start_background, stop_background
    from graphical_dashboard.snapshot import build_snapshot, publish_snapshot

    state_dir = Path(".state")
    snapshot_path = state_dir / "dashboard_snapshot.json"
    publish_snapshot(snapshot_path, build_snapshot(data, {}))
    server, thread = start_background(snapshot_path, open_browser=True)
    try:
        while True:
            time.sleep(1.0)
            # Refresh timestamp so a deliberate safety-block dashboard stays visibly alive.
            publish_snapshot(snapshot_path, build_snapshot(data, {}))
    except KeyboardInterrupt:
        return 2
    finally:
        stop_background(server, thread)
