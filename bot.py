from __future__ import annotations

from gold_scalp_trader.config import load_settings, validate_settings


def main() -> None:
    settings = load_settings()
    validate_settings(settings)

    print("=" * 58)
    print(" GOLD SCALP TRADER — SAFETY BOOT")
    print("=" * 58)
    print(f"Mode       : {settings.mode}")
    print(f"Symbol     : {settings.symbol}")
    print(f"Timeframe  : {settings.timeframe}")
    print(f"Risk       : {settings.risk_percent:.2f}%")
    print(f"Max trades : {settings.max_open_positions}")
    print("-" * 58)

    if settings.live_trading_enabled:
        raise RuntimeError(
            "LIVE execution engine is intentionally not implemented in the "
            "foundation milestone. No order was sent."
        )

    print("DRY RUN safety lock is active. No order can be sent.")
    print("Foundation check passed.")


if __name__ == "__main__":
    main()
