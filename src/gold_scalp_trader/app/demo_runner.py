"""Continuous guarded DEMO runtime.

This module is the only normal launcher path that can reach DEMO broker writes.
REAL trading remains disabled by configuration policy.
"""
from __future__ import annotations

from pathlib import Path
import os
import sys
import time
from typing import Callable

from gold_scalp_trader.app.runtime import RuntimeResult, run_guarded_demo_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode
from gold_scalp_trader.market_data.mt5_reader import Mt5ReadError
from gold_scalp_trader.operator.graphical_snapshot import from_cycle
from gold_scalp_trader.operator.terminal_dashboard import render
from gold_scalp_trader.persistence.checkpoint import export_checkpoint
from gold_scalp_trader.persistence.store import StateStore


def _clear_screen() -> None:
    if not sys.stdout.isatty():
        return
    os.system("cls" if os.name == "nt" else "clear")


def _state_path(settings: Settings) -> Path:
    path = Path(settings.state_db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _print_result(result: RuntimeResult, state_path: Path) -> None:
    _clear_screen()
    print("=" * 78)
    print(" GOLD SCALP TRADER — LIVE DEMO")
    print("=" * 78)
    print(render(from_cycle(result.cycle, market_state="DEMO")))
    print("-" * 78)
    print("Mode         : DEMO")
    print(f"State DB     : {state_path}")
    print(f"Broker write : {'YES' if result.wrote_broker else 'NO'}")
    if result.intent is not None:
        print(f"Intent       : {result.intent.intent_id} • {result.intent.state.value}")
        print(f"Send count   : {result.intent.send_count}")
        if result.intent.broker_ticket is not None:
            print(f"Broker ticket: {result.intent.broker_ticket}")
    print("-" * 78)
    print("Ctrl+C = safe local stop + checkpoint. REAL trading remains disabled.")


def run_live_demo(
    settings: Settings,
    api,
    *,
    max_cycles: int | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> int:
    if settings.mode is not RuntimeMode.DEMO or not settings.demo_write_enabled:
        raise PermissionError("DEMO mode with explicit DEMO confirmation is required")

    state_path = _state_path(settings)
    store = StateStore(state_path)
    completed = 0
    try:
        while max_cycles is None or completed < max_cycles:
            try:
                result = run_guarded_demo_cycle(settings, api, store)
            except PermissionError:
                raise
            except Mt5ReadError as exc:
                _clear_screen()
                print(f"MT5 READ DEGRADED: {exc}")
                print("No broker write attempted this cycle.")
                completed += 1
                if max_cycles is None or completed < max_cycles:
                    sleep_fn(settings.loop_interval_seconds)
                continue

            _print_result(result, state_path)
            completed += 1
            if max_cycles is None or completed < max_cycles:
                sleep_fn(settings.loop_interval_seconds)
        return 0
    except KeyboardInterrupt:
        print("\nDEMO runtime stop requested.")
        return 0
    finally:
        try:
            checkpoint = state_path.with_suffix(".checkpoint.json")
            export_checkpoint(store, checkpoint)
            print(f"Local runtime checkpoint: {checkpoint}")
        finally:
            store.close()
