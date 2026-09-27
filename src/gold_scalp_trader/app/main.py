from gold_scalp_trader.app.demo_runner import render_startup_error, run_live_demo
from gold_scalp_trader.app.graphical_demo_runner import LazyMt5Api
from gold_scalp_trader.app.startup import mt5_session
from gold_scalp_trader.app.runtime import run_read_cycle
from gold_scalp_trader.config import load_settings
from gold_scalp_trader.domain.enums import RuntimeMode
from gold_scalp_trader.operator.graphical_snapshot import from_cycle
from gold_scalp_trader.operator.terminal_dashboard import render


def _show_startup_error(title: str, exc: Exception) -> int:
    """Fail visibly in the primary terminal dashboard before runtime exists."""
    print(render_startup_error(title, exc))
    print("No broker write was attempted.")
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

    # DEMO presentation is terminal-first and fail-visible.  MT5 is acquired
    # lazily so initialize/login/feed failures happen inside run_live_demo, where
    # they become DEGRADED dashboard frames instead of terminating before the
    # operator surface appears. GUI mode only adds the secondary browser view.
    if settings.mode is RuntimeMode.DEMO:
        api = LazyMt5Api()
        try:
            return run_live_demo(settings, api)
        finally:
            api.close()

    try:
        with mt5_session() as mt5:
            result = run_read_cycle(settings, mt5)
    except Exception as exc:
        return _show_startup_error("STARTUP/RUNTIME ERROR", exc)

    dto = from_cycle(result.cycle)
    print(render(dto))
    print(f"Broker write: {'YES' if result.wrote_broker else 'NO'}")
    return 0


def main() -> None:
    raise SystemExit(run())
