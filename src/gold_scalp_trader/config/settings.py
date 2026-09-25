"""Validated runtime settings and preserved policy constants.

Frozen policy is represented as code constants instead of permissive environment
variables. Environment values choose runtime scope/mode and approved optional
capabilities; they do not silently rewrite Risk bands.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Mapping

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args: object, **kwargs: object) -> bool:
        return False

from gold_scalp_trader.domain.enums import RuntimeMode, StrategyFamily


@dataclass(frozen=True, slots=True)
class RiskBand:
    normal_min_pct: float
    normal_max_pct: float
    elevated_max_pct: float
    hard_ceiling_pct: float
    daily_loss_lock_pct: float


PRESERVED_RISK_BANDS: Mapping[str, RiskBand] = {
    "SMALL": RiskBand(3.0, 4.5, 6.5, 7.0, 12.0),
    "MEDIUM": RiskBand(2.0, 3.0, 4.5, 5.0, 9.0),
    "NORMAL": RiskBand(1.0, 2.0, 3.5, 4.0, 7.0),
}


@dataclass(frozen=True, slots=True)
class Settings:
    mode: RuntimeMode = RuntimeMode.DRY_RUN
    preferred_symbol: str = "XAUUSDm"
    symbol_aliases: tuple[str, ...] = ("XAUUSDm", "XAUUSD")
    active_strategy_family: StrategyFamily | None = None
    max_open_positions: int = 1
    aggressive_small_account: bool = False
    manual_daily_loss_reset_enabled: bool = False
    max_consecutive_losses: int = 3
    consecutive_loss_cooldown_minutes: int = 30
    context_cache_ttl_seconds: int = 1800
    m1_history_bars: int = 300
    m5_history_bars: int = 1200
    m15_history_bars: int = 800
    h1_history_bars: int = 600
    h4_history_bars: int = 400
    demo_trading_confirm: str = "NO"
    real_trading_confirm: str = "NO"

    @property
    def demo_write_enabled(self) -> bool:
        return self.mode is RuntimeMode.DEMO and self.demo_trading_confirm == "YES_I_APPROVE_DEMO"

    @property
    def real_write_enabled(self) -> bool:
        return self.mode is RuntimeMode.REAL and self.real_trading_confirm == "YES_I_APPROVE_REAL"

    @property
    def broker_write_enabled(self) -> bool:
        return self.demo_write_enabled or self.real_write_enabled


def _bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    normalized = raw.strip().upper()
    if normalized in {"1", "TRUE", "YES", "ON"}:
        return True
    if normalized in {"0", "FALSE", "NO", "OFF"}:
        return False
    raise ValueError(f"{name} must be a boolean value")


def _family_env() -> StrategyFamily | None:
    raw = os.getenv("ACTIVE_STRATEGY_FAMILY", "").strip().upper()
    if not raw:
        return None
    try:
        return StrategyFamily(raw)
    except ValueError as exc:
        allowed = ", ".join(f.value for f in StrategyFamily)
        raise ValueError(f"ACTIVE_STRATEGY_FAMILY must be one of: {allowed}") from exc


def load_settings() -> Settings:
    load_dotenv()
    raw_mode = os.getenv("MODE", RuntimeMode.DRY_RUN.value).strip().upper()
    try:
        mode = RuntimeMode(raw_mode)
    except ValueError as exc:
        raise ValueError("MODE must be DRY_RUN, DEMO or REAL") from exc

    preferred = os.getenv("SYMBOL", "XAUUSDm").strip()
    aliases_raw = os.getenv("SYMBOL_ALIASES", "XAUUSDm,XAUUSD")
    aliases = tuple(dict.fromkeys(x.strip() for x in aliases_raw.split(",") if x.strip()))
    if preferred and preferred not in aliases:
        aliases = (preferred, *aliases)

    settings = Settings(
        mode=mode,
        preferred_symbol=preferred,
        symbol_aliases=aliases,
        active_strategy_family=_family_env(),
        max_open_positions=int(os.getenv("MAX_OPEN_POSITIONS", "1")),
        aggressive_small_account=_bool_env("AGGRESSIVE_SMALL_ACCOUNT", False),
        manual_daily_loss_reset_enabled=_bool_env("MANUAL_DAILY_LOSS_RESET_ENABLED", False),
        max_consecutive_losses=int(os.getenv("MAX_CONSECUTIVE_LOSSES", "3")),
        consecutive_loss_cooldown_minutes=int(os.getenv("LOSS_COOLDOWN_MINUTES", "30")),
        context_cache_ttl_seconds=int(os.getenv("CONTEXT_CACHE_TTL_SECONDS", "1800")),
        m1_history_bars=int(os.getenv("M1_HISTORY_BARS", "300")),
        m5_history_bars=int(os.getenv("M5_HISTORY_BARS", "1200")),
        m15_history_bars=int(os.getenv("M15_HISTORY_BARS", "800")),
        h1_history_bars=int(os.getenv("H1_HISTORY_BARS", "600")),
        h4_history_bars=int(os.getenv("H4_HISTORY_BARS", "400")),
        demo_trading_confirm=os.getenv("DEMO_TRADING_CONFIRM", "NO").strip().upper(),
        real_trading_confirm=os.getenv("REAL_TRADING_CONFIRM", "NO").strip().upper(),
    )
    validate_settings(settings)
    return settings


def validate_settings(settings: Settings) -> None:
    if not settings.preferred_symbol:
        raise ValueError("SYMBOL cannot be empty")
    if not settings.symbol_aliases:
        raise ValueError("at least one symbol alias is required")
    if settings.max_open_positions != 1:
        raise ValueError("MAX_OPEN_POSITIONS is preserved at 1 for the initial architecture")
    if settings.max_consecutive_losses != 3:
        raise ValueError("MAX_CONSECUTIVE_LOSSES baseline is preserved at 3")
    if settings.consecutive_loss_cooldown_minutes < 30:
        raise ValueError("loss cooldown cannot be below the preserved 30-minute baseline")
    if settings.context_cache_ttl_seconds <= 0:
        raise ValueError("context cache TTL must be positive")
    for name in ("m1_history_bars", "m5_history_bars", "m15_history_bars", "h1_history_bars", "h4_history_bars"):
        if getattr(settings, name) < 50:
            raise ValueError(f"{name} is too small for safe indicator/structure warm-up")
    if settings.mode in {RuntimeMode.DEMO, RuntimeMode.REAL} and settings.active_strategy_family is None:
        raise ValueError("ACTIVE_STRATEGY_FAMILY is required for write-capable modes")
    if settings.mode is RuntimeMode.DEMO and settings.demo_trading_confirm not in {"NO", "YES_I_APPROVE_DEMO"}:
        raise ValueError("invalid DEMO_TRADING_CONFIRM token")
    if settings.mode is RuntimeMode.REAL and settings.real_trading_confirm != "YES_I_APPROVE_REAL":
        raise ValueError("REAL mode is future-gated and requires explicit REAL_TRADING_CONFIRM")
