"""Live graphical DEMO runtime adapter.

The dashboard is presentation-only. This adapter owns the fixed timer provider
that advances the governed DEMO runtime and returns one atomic immutable view
for the UI to render. Chart buttons never call this provider directly.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Type

from gold_scalp_trader.app.runtime import RuntimeResult, run_guarded_demo_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, Timeframe
from gold_scalp_trader.operator.graphical_snapshot import from_runtime
from gold_scalp_trader.persistence.checkpoint import export_checkpoint
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.timing_learning import record_runtime_timing


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
        self.calls = 0

    def __call__(self):
        """Advance exactly one governed broker cycle and return one UI snapshot."""
        result = self.step(self.settings, self.api, self.store)
        record_runtime_timing(self.store, result)
        self.last_result = result
        self.calls += 1
        market = result.cycle.intelligence.market
        candles_by_tf = {
            timeframe.value: market.series(timeframe)
            for timeframe in Timeframe
        }
        return from_runtime(result, market_state="DEMO"), candles_by_tf


class _DashboardResources:
    def __init__(self, store: StateStore, state_path: Path) -> None:
        self.store = store
        self.state_path = state_path
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
            self.store.close()


def run_graphical_demo(
    settings: Settings,
    api,
    *,
    dashboard_cls: Type | None = None,
    step: Callable[..., RuntimeResult] = run_guarded_demo_cycle,
) -> int:
    if settings.mode is not RuntimeMode.DEMO or not settings.demo_write_enabled:
        raise PermissionError("DEMO mode with explicit DEMO confirmation is required")

    state_path = Path(settings.state_db_path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    store = StateStore(state_path)
    resources = _DashboardResources(store, state_path)
    provider = RuntimeDashboardProvider(settings, api, store, step=step)

    if dashboard_cls is None:
        # Lazy import keeps headless/offline tests independent from Tk.
        from graphical_dashboard.ui import DashboardApp

        dashboard_cls = DashboardApp

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
