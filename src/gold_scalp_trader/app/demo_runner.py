"""Continuous guarded DEMO runtime with terminal-first presentation.

The VS Code/terminal dashboard is the primary operator surface. When
``DASHBOARD_MODE=GUI`` the localhost browser floor is a secondary read-only
projection. Research evidence is best-effort relative to broker authority: a
research failure is surfaced as degraded research evidence but cannot erase or
reclassify a completed broker cycle.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import os
import sys
import time
from typing import Callable

from gold_scalp_trader.app.runtime import RuntimeResult, run_guarded_demo_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode, Timeframe
from gold_scalp_trader.operator.graphical_snapshot import from_runtime
from gold_scalp_trader.operator.presentation import DashboardData
from gold_scalp_trader.operator.terminal_dashboard import render, render_error
from gold_scalp_trader.persistence.checkpoint import export_checkpoint
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.runtime_evidence import record_runtime_research
from gold_scalp_trader.research.shadow_runtime import record_shadow_runtime
from gold_scalp_trader.research.timing_learning import record_runtime_timing


def _clear_screen() -> None:
    if not sys.stdout.isatty():
        return
    os.system("cls" if os.name == "nt" else "clear")


def _state_path(settings: Settings) -> Path:
    path = Path(settings.state_db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _active_family(settings: Settings) -> str:
    return "UNSET" if settings.active_strategy_family is None else settings.active_strategy_family.value


def _degraded_data(settings: Settings, title: str, exc: Exception) -> DashboardData:
    symbol = settings.symbol_aliases[0] if settings.symbol_aliases else "XAUUSD"
    message = f"{title}: {type(exc).__name__}: {exc}"
    return DashboardData(
        symbol=symbol,
        bid=None,
        ask=None,
        spread=None,
        market_state="UNKNOWN",
        soft_session="UNKNOWN",
        bot_status="DEGRADED",
        detected_setup="UNAVAILABLE",
        active_family=_active_family(settings),
        live_action="WAIT",
        reason=message,
        shadow_setups=(),
        risk_text="NOT EVALUATED",
        gate_text="NOT EVALUATED",
        news_text="UNKNOWN • SOFT ONLY",
        system_text="DASHBOARD ALIVE • TRADING FAIL-CLOSED • NO BROKER WRITE FROM FAILED CYCLE",
        trade_plan_text="NOT AVAILABLE",
        managed_trade_text="UNKNOWN",
        execution_text="NO BROKER ACTION FROM FAILED CYCLE",
        activity_text="Runtime facts unavailable; polling will continue",
        learning_text="PAUSED until runtime health recovers",
    )


def _record_research_best_effort(store: StateStore, result: RuntimeResult) -> tuple[str, ...]:
    """Record research evidence without granting it runtime/broker authority."""
    failures: list[str] = []
    for label, recorder in (
        ("TIMING", record_runtime_timing),
        ("MANAGEMENT_SHADOW", record_runtime_research),
        ("SHADOW_OUTCOME", record_shadow_runtime),
    ):
        try:
            recorder(store, result)
        except Exception as exc:
            failures.append(f"{label}:{type(exc).__name__}")
    return tuple(failures)


def _print_data(data: DashboardData, state_path: Path, *, wrote_broker: bool | None = None) -> None:
    _clear_screen()
    print(render(data))
    print(f"State DB: {state_path}")
    if wrote_broker is not None:
        print(f"Broker write this cycle: {'YES' if wrote_broker else 'NO'}")


class _SecondaryBrowser:
    """Best-effort browser projection; failure never affects the primary dashboard."""

    def __init__(self, enabled: bool, snapshot_path: Path) -> None:
        self.enabled = enabled
        self.snapshot_path = snapshot_path
        self.server = None
        self.thread = None
        self.error: str | None = None

    def publish(self, data: DashboardData, result: RuntimeResult | None = None) -> DashboardData:
        if not self.enabled:
            return data
        try:
            from graphical_dashboard.server import start_background
            from graphical_dashboard.snapshot import build_snapshot, publish_snapshot

            candles = {}
            if result is not None:
                market = result.cycle.intelligence.market
                candles = {timeframe.value: market.series(timeframe) for timeframe in Timeframe}
            publish_snapshot(
                self.snapshot_path,
                build_snapshot(data, candles, runtime_result=result),
            )
            if self.server is None:
                self.server, self.thread = start_background(self.snapshot_path, open_browser=True)
            self.error = None
            return data
        except Exception as exc:
            self.error = f"SECONDARY GRAPHICAL UNAVAILABLE: {type(exc).__name__}: {exc}"
            return replace(data, system_text=f"{data.system_text} • {self.error}")

    def close(self) -> None:
        if self.server is None:
            return
        try:
            from graphical_dashboard.server import stop_background
            stop_background(self.server, self.thread)
        finally:
            self.server = None
            self.thread = None


def run_live_demo(
    settings: Settings,
    api,
    *,
    max_cycles: int | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> int:
    """Run DEMO with fail-visible presentation and isolated research evidence."""
    if settings.mode is not RuntimeMode.DEMO:
        raise PermissionError("DEMO runtime requires DEMO mode")

    state_path = _state_path(settings)
    store = StateStore(state_path)
    secondary = _SecondaryBrowser(
        enabled=settings.dashboard_mode == "GUI" and max_cycles is None,
        snapshot_path=state_path.parent / "dashboard_snapshot.json",
    )
    completed = 0
    try:
        while max_cycles is None or completed < max_cycles:
            try:
                result = run_guarded_demo_cycle(settings, api, store)
                research_failures = _record_research_best_effort(store, result)
                data = from_runtime(result, market_state="DEMO")
                if research_failures:
                    warning = "RESEARCH DEGRADED • " + " • ".join(research_failures)
                    data = replace(
                        data,
                        learning_text=f"{data.learning_text} • {warning}",
                        system_text=f"{data.system_text} • {warning}",
                    )
                data = secondary.publish(data, result)
                _print_data(data, state_path, wrote_broker=result.wrote_broker)
            except Exception as exc:
                data = _degraded_data(settings, "RUNTIME ISSUE", exc)
                data = secondary.publish(data, None)
                _print_data(data, state_path, wrote_broker=False)

            completed += 1
            if max_cycles is None or completed < max_cycles:
                sleep_fn(settings.loop_interval_seconds)
        return 0
    except KeyboardInterrupt:
        print("\nDEMO runtime stop requested.")
        return 0
    finally:
        secondary.close()
        try:
            checkpoint = state_path.with_suffix(".checkpoint.json")
            export_checkpoint(store, checkpoint)
            print(f"Local runtime checkpoint: {checkpoint}")
        finally:
            store.close()


def render_startup_error(title: str, exc: Exception) -> str:
    return render_error(title, exc)
