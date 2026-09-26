from gold_scalp_trader.app.demo_runner import run_live_demo
from gold_scalp_trader.app.graphical_demo_runner import run_error_dashboard, run_graphical_demo_standalone
from gold_scalp_trader.app.startup import mt5_session
from gold_scalp_trader.app.runtime import run_read_cycle
from gold_scalp_trader.config import load_settings
from gold_scalp_trader.domain.enums import RuntimeMode
from gold_scalp_trader.operator.graphical_snapshot import from_cycle
from gold_scalp_trader.operator.terminal_dashboard import render


def _show_startup_error(title: str, exc: Exception) -> int:
    """Best-effort fail-visible GUI for errors that happen before MT5 runtime exists."""
    print(f"{title}: {type(exc).__name__}: {exc}")
    print("No broker write was attempted.")
    try:
        return run_error_dashboard(title, exc)
    except Exception as dashboard_exc:
        print(f"DASHBOARD ERROR: {type(dashboard_exc).__name__}: {dashboard_exc}")
        return 2


def run() -> int:
    try:
        settings = load_settings()
    except Exception as exc:
        return _show_startup_error("CONFIGURATION ERROR", exc)

    if settings.real_write_enabled:
        return _show_startup_error(
            "REAL SAFETY LOCK",
            RuntimeError("REAL broker writes are not enabled in the current release"),
        )

    # GUI DEMO is intentionally started before MT5 initialization.  Its provider
    # lazily acquires MT5 so connection/login/market-data failures remain visible
    # inside the dashboard instead of terminating the process before UI creation.
    if settings.mode is RuntimeMode.DEMO and settings.dashboard_mode == "GUI":
        try:
            return run_graphical_demo_standalone(settings)
        except Exception as exc:
            return _show_startup_error("GRAPHICAL DASHBOARD STARTUP ERROR", exc)

    try:
        with mt5_session() as mt5:
            if settings.mode is RuntimeMode.DEMO:
                return run_live_demo(settings, mt5)

            result = run_read_cycle(settings, mt5)
    except Exception as exc:
        print(f"STARTUP/RUNTIME ERROR: {type(exc).__name__}: {exc}")
        print("No unverified REAL broker write was attempted.")
        return 2

    dto = from_cycle(result.cycle)
    print(render(dto))
    print(f"Broker write: {'YES' if result.wrote_broker else 'NO'}")
    return 0


def main() -> None:
    raise SystemExit(run())
