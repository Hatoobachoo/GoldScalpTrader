from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    mode: str = "DRY_RUN"
    symbol: str = "XAUUSDm"
    timeframe: str = "M5"
    risk_percent: float = 0.50
    daily_loss_limit_percent: float = 2.00
    max_open_positions: int = 1
    max_consecutive_losses: int = 3
    max_spread_points: int = 500
    live_trading_confirm: str = "NO"

    @property
    def live_trading_enabled(self) -> bool:
        return (
            self.mode.upper() == "LIVE"
            and self.live_trading_confirm.upper() == "YES_I_UNDERSTAND"
        )


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        mode=os.getenv("MODE", "DRY_RUN").strip().upper(),
        symbol=os.getenv("SYMBOL", "XAUUSDm").strip(),
        timeframe=os.getenv("TIMEFRAME", "M5").strip().upper(),
        risk_percent=float(os.getenv("RISK_PERCENT", "0.50")),
        daily_loss_limit_percent=float(os.getenv("DAILY_LOSS_LIMIT_PERCENT", "2.00")),
        max_open_positions=int(os.getenv("MAX_OPEN_POSITIONS", "1")),
        max_consecutive_losses=int(os.getenv("MAX_CONSECUTIVE_LOSSES", "3")),
        max_spread_points=int(os.getenv("MAX_SPREAD_POINTS", "500")),
        live_trading_confirm=os.getenv("LIVE_TRADING_CONFIRM", "NO").strip().upper(),
    )


def validate_settings(settings: Settings) -> None:
    if settings.mode not in {"DRY_RUN", "LIVE"}:
        raise ValueError("MODE must be DRY_RUN or LIVE")
    if settings.timeframe != "M5":
        raise ValueError("Initial release is intentionally locked to M5")
    if not 0 < settings.risk_percent <= 2.0:
        raise ValueError("RISK_PERCENT must be > 0 and <= 2.0")
    if not 0 < settings.daily_loss_limit_percent <= 5.0:
        raise ValueError("DAILY_LOSS_LIMIT_PERCENT must be > 0 and <= 5.0")
    if settings.max_open_positions != 1:
        raise ValueError("MAX_OPEN_POSITIONS is safety-locked to 1")
    if settings.max_consecutive_losses < 1:
        raise ValueError("MAX_CONSECUTIVE_LOSSES must be at least 1")
    if settings.max_spread_points <= 0:
        raise ValueError("MAX_SPREAD_POINTS must be positive")
