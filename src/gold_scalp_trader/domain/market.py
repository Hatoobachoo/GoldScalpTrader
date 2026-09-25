"""Immutable normalized market facts.

Raw MT5 values are normalized once at the market-data boundary. Analytical
modules consume these DTOs and never call MetaTrader5 directly.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from .enums import DataQuality, Direction, Timeframe

UTC = timezone.utc


def _require_utc(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


def _finite(value: float, name: str) -> None:
    if not isfinite(float(value)):
        raise ValueError(f"{name} must be finite")


_TIMEFRAME_DURATION = {
    Timeframe.M1: timedelta(minutes=1),
    Timeframe.M5: timedelta(minutes=5),
    Timeframe.M15: timedelta(minutes=15),
    Timeframe.H1: timedelta(hours=1),
    Timeframe.H4: timedelta(hours=4),
}


@dataclass(frozen=True, slots=True)
class Candle:
    timeframe: Timeframe
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    tick_volume: int = 0
    real_volume: int = 0

    def __post_init__(self) -> None:
        _require_utc(self.open_time, "open_time")
        for name in ("open", "high", "low", "close"):
            _finite(getattr(self, name), name)
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("candle high is inconsistent")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("candle low is inconsistent")
        if self.tick_volume < 0 or self.real_volume < 0:
            raise ValueError("volume cannot be negative")

    @property
    def close_time(self) -> datetime:
        return self.open_time + _TIMEFRAME_DURATION[self.timeframe]

    @property
    def range(self) -> float:
        return self.high - self.low


@dataclass(frozen=True, slots=True)
class Quote:
    bid: float
    ask: float
    source_time: datetime
    captured_at: datetime

    def __post_init__(self) -> None:
        _finite(self.bid, "bid")
        _finite(self.ask, "ask")
        _require_utc(self.source_time, "source_time")
        _require_utc(self.captured_at, "captured_at")
        if self.bid <= 0 or self.ask <= 0 or self.ask < self.bid:
            raise ValueError("invalid Bid/Ask")

    @property
    def spread(self) -> float:
        return self.ask - self.bid

    @property
    def age_seconds(self) -> float:
        return (self.captured_at - self.source_time).total_seconds()


@dataclass(frozen=True, slots=True)
class SymbolSpec:
    symbol: str
    digits: int
    point: float
    tick_size: float
    tick_value: float | None
    volume_min: float
    volume_max: float
    volume_step: float
    stops_level_points: int = 0
    freeze_level_points: int = 0
    trade_mode: int | str | None = None
    filling_mode: int | str | None = None

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("symbol cannot be empty")
        if self.digits < 0:
            raise ValueError("digits cannot be negative")
        for name in ("point", "tick_size", "volume_min", "volume_max", "volume_step"):
            value = float(getattr(self, name))
            _finite(value, name)
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.tick_value is not None:
            _finite(self.tick_value, "tick_value")
            if self.tick_value <= 0:
                raise ValueError("tick_value must be positive when present")
        if self.volume_max < self.volume_min:
            raise ValueError("volume_max cannot be below volume_min")


@dataclass(frozen=True, slots=True)
class AccountFacts:
    login: int
    server: str
    currency: str
    balance: float
    equity: float
    margin_free: float
    trade_allowed: bool | None
    trade_expert: bool | None

    def __post_init__(self) -> None:
        if self.login <= 0:
            raise ValueError("login must be positive")
        if not self.server or not self.currency:
            raise ValueError("server/currency required")
        for name in ("balance", "equity", "margin_free"):
            _finite(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class PositionFacts:
    ticket: int
    symbol: str
    direction: Direction
    volume: float
    price_open: float
    sl: float | None
    tp: float | None
    magic: int | None
    comment: str = ""

    def __post_init__(self) -> None:
        if self.ticket <= 0 or self.volume <= 0 or self.price_open <= 0:
            raise ValueError("invalid position facts")
        if self.direction not in {Direction.BUY, Direction.SELL}:
            raise ValueError("position direction must be BUY or SELL")


@dataclass(frozen=True, slots=True)
class MarketSnapshot:
    captured_at: datetime
    account: AccountFacts
    symbol_spec: SymbolSpec
    quote: Quote
    candles: Mapping[Timeframe, tuple[Candle, ...]]
    quality: Mapping[Timeframe, DataQuality]
    positions: tuple[PositionFacts, ...] | None
    positions_quality: DataQuality

    def __post_init__(self) -> None:
        _require_utc(self.captured_at, "captured_at")
        normalized: dict[Timeframe, tuple[Candle, ...]] = {}
        for tf, series in self.candles.items():
            tup = tuple(series)
            previous: datetime | None = None
            for candle in tup:
                if candle.timeframe is not tf:
                    raise ValueError("candle timeframe key mismatch")
                if candle.close_time > self.captured_at:
                    raise ValueError("forming/future candle cannot enter completed history")
                if previous is not None and candle.open_time <= previous:
                    raise ValueError("candles must be strictly chronological")
                previous = candle.open_time
            normalized[tf] = tup
        object.__setattr__(self, "candles", MappingProxyType(normalized))
        object.__setattr__(self, "quality", MappingProxyType(dict(self.quality)))
        if self.positions is not None:
            object.__setattr__(self, "positions", tuple(self.positions))

    def series(self, timeframe: Timeframe) -> tuple[Candle, ...]:
        return self.candles.get(timeframe, ())
