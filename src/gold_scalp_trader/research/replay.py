"""Chronological multi-timeframe replay helpers with explicit no-lookahead cutoffs.

Research consumes completed candles only.  The decision clock defaults to M5;
M1 is therefore visible only when its candle close is already knowable at the
M5 decision timestamp.  Nothing in this module has production/broker authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Iterator, Mapping

from gold_scalp_trader.domain.enums import Timeframe
from gold_scalp_trader.domain.market import Candle


@dataclass(frozen=True, slots=True)
class ReplayPoint:
    as_of: datetime
    decision_timeframe: Timeframe
    candles: Mapping[Timeframe, tuple[Candle, ...]]

    def __post_init__(self) -> None:
        if self.as_of.tzinfo is None or self.as_of.utcoffset() is None:
            raise ValueError("replay as_of must be timezone-aware")
        normalized = {tf: tuple(series) for tf, series in self.candles.items()}
        for tf, series in normalized.items():
            if any(c.timeframe is not tf for c in series):
                raise ValueError(f"replay series contains wrong timeframe for {tf}")
            if any(c.close_time > self.as_of for c in series):
                raise ValueError(f"future candle leaked into replay point for {tf}")
        object.__setattr__(self, "candles", MappingProxyType(normalized))


def _validated_series(series_by_tf: Mapping[Timeframe, tuple[Candle, ...]]) -> dict[Timeframe, tuple[Candle, ...]]:
    out: dict[Timeframe, tuple[Candle, ...]] = {}
    for tf, raw in series_by_tf.items():
        series = tuple(raw)
        previous: datetime | None = None
        for candle in series:
            if candle.timeframe is not tf:
                raise ValueError(f"candle timeframe mismatch in {tf}")
            if previous is not None and candle.open_time <= previous:
                raise ValueError(f"{tf} replay candles must be strictly chronological")
            previous = candle.open_time
        out[tf] = series
    return out


def prefixes(candles: tuple[Candle, ...], warmup: int = 50) -> Iterator[tuple[Candle, ...]]:
    """Backward-compatible single-series causal prefix iterator."""
    if warmup < 1:
        raise ValueError("warmup must be positive")
    validated = _validated_series({candles[0].timeframe: candles}) if candles else {}
    series = next(iter(validated.values()), ())
    for end in range(warmup, len(series) + 1):
        yield series[:end]


def chronological_points(
    series_by_tf: Mapping[Timeframe, tuple[Candle, ...]],
    *,
    decision_timeframe: Timeframe = Timeframe.M5,
    warmup: int = 50,
    minimum_bars: Mapping[Timeframe, int] | None = None,
) -> Iterator[ReplayPoint]:
    """Yield causal multi-timeframe prefixes at each completed decision candle.

    The yielded snapshot contains only candles whose *close time* is less than
    or equal to the current decision timestamp.  Higher/lower timeframe bars
    still forming at that timestamp are excluded, preventing retrospective
    structure or M1 timing leakage.
    """
    if warmup < 1:
        raise ValueError("warmup must be positive")
    validated = _validated_series(series_by_tf)
    decision_series = validated.get(decision_timeframe, ())
    if not decision_series:
        return

    mins = dict(minimum_bars or {})
    mins.setdefault(decision_timeframe, warmup)
    start = max(1, mins[decision_timeframe])

    for index in range(start - 1, len(decision_series)):
        as_of = decision_series[index].close_time
        visible: dict[Timeframe, tuple[Candle, ...]] = {}
        eligible = True
        for tf, series in validated.items():
            causal = tuple(c for c in series if c.close_time <= as_of)
            visible[tf] = causal
            if len(causal) < mins.get(tf, 0):
                eligible = False
        if eligible:
            yield ReplayPoint(as_of, decision_timeframe, visible)
