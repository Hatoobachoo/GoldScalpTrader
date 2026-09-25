from gold_scalp_trader.app.demo_runner import run_live_demo
from gold_scalp_trader.app.startup import mt5_session
from gold_scalp_trader.app.runtime import run_read_cycle
from gold_scalp_trader.config import load_settings
from gold_scalp_trader.domain.enums import RuntimeMode
from gold_scalp_trader.operator.graphical_snapshot import from_cycle
from gold_scalp_trader.operator.terminal_dashboard import render


def run() -> int:
    settings = load_settings()
    if settings.real_write_enabled:
        raise RuntimeError("REAL broker writes are not enabled in the current release")

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
