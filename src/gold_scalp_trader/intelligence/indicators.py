"""Causal EMA/RSI/ATR calculations and quantitative context."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import median

from gold_scalp_trader.domain.market import Candle


@dataclass(frozen=True, slots=True)
class IndicatorSeries:
    ema20: tuple[float | None, ...]
    ema50: tuple[float | None, ...]
    rsi14: tuple[float | None, ...]
    atr14: tuple[float | None, ...]


@dataclass(frozen=True, slots=True)
class QuantReport:
    ema20: float | None
    ema50: float | None
    rsi14: float | None
    atr14: float | None
    ema_flow: str
    volatility_ratio: float | None
    volatility_state: str
    extension_atr: float | None
    extension_state: str
    coverage: float


def ema(values: list[float], period: int) -> tuple[float | None, ...]:
    if period <= 0:
        raise ValueError("period must be positive")
    out: list[float | None] = [None] * len(values)
    if len(values) < period:
        return tuple(out)
    seed = sum(values[:period]) / period
    out[period - 1] = seed
    alpha = 2.0 / (period + 1.0)
    prev = seed
    for i in range(period, len(values)):
        prev = values[i] * alpha + prev * (1.0 - alpha)
        out[i] = prev
    return tuple(out)


def rsi_wilder(values: list[float], period: int = 14) -> tuple[float | None, ...]:
    out: list[float | None] = [None] * len(values)
    if len(values) <= period:
        return tuple(out)
    gains, losses = [], []
    for i in range(1, period + 1):
        diff = values[i] - values[i - 1]
        gains.append(max(diff, 0.0)); losses.append(max(-diff, 0.0))
    avg_gain, avg_loss = sum(gains) / period, sum(losses) / period
    out[period] = _rsi_from_averages(avg_gain, avg_loss)
    for i in range(period + 1, len(values)):
        diff = values[i] - values[i - 1]
        gain, loss = max(diff, 0.0), max(-diff, 0.0)
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        out[i] = _rsi_from_averages(avg_gain, avg_loss)
    return tuple(out)


def _rsi_from_averages(avg_gain: float, avg_loss: float) -> float:
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    return 100.0 - (100.0 / (1.0 + avg_gain / avg_loss))


def atr_wilder(candles: tuple[Candle, ...], period: int = 14) -> tuple[float | None, ...]:
    out: list[float | None] = [None] * len(candles)
    if len(candles) < period:
        return tuple(out)
    trs: list[float] = []
    for i, candle in enumerate(candles):
        if i == 0:
            tr = candle.high - candle.low
        else:
            prev_close = candles[i - 1].close
            tr = max(candle.high - candle.low, abs(candle.high - prev_close), abs(candle.low - prev_close))
        trs.append(tr)
    seed = sum(trs[:period]) / period
    out[period - 1] = seed
    prev = seed
    for i in range(period, len(trs)):
        prev = ((prev * (period - 1)) + trs[i]) / period
        out[i] = prev
    return tuple(out)


def calculate(candles: tuple[Candle, ...]) -> tuple[IndicatorSeries, QuantReport]:
    closes = [c.close for c in candles]
    if any(not isfinite(value) for value in closes):
        raise ValueError("non-finite close")
    e20, e50, r14, a14 = ema(closes, 20), ema(closes, 50), rsi_wilder(closes, 14), atr_wilder(candles, 14)
    series = IndicatorSeries(e20, e50, r14, a14)
    latest20 = e20[-1] if e20 else None; latest50 = e50[-1] if e50 else None
    latest_rsi = r14[-1] if r14 else None; latest_atr = a14[-1] if a14 else None
    flow = "UNKNOWN" if latest20 is None or latest50 is None else "BUY" if latest20 > latest50 else "SELL" if latest20 < latest50 else "NONE"
    valid_atr = [x for x in a14[-50:] if x is not None and x > 0]
    vol_ratio, vol_state = None, "UNKNOWN"
    if latest_atr is not None and valid_atr:
        baseline = median(valid_atr)
        if baseline > 0:
            vol_ratio = latest_atr / baseline
            vol_state = "QUIET" if vol_ratio < .70 else "NORMAL" if vol_ratio < 1.15 else "BUILDING" if vol_ratio < 1.50 else "EXPANDING" if vol_ratio < 2.0 else "EXTREME"
    extension, extension_state = None, "UNKNOWN"
    if candles and latest20 is not None and latest_atr is not None and latest_atr > 0:
        extension = abs(candles[-1].close - latest20) / latest_atr
        extension_state = "FRESH" if extension < .35 else "NORMAL" if extension < .90 else "EXTENDED" if extension < 1.50 else "SEVERELY_EXTENDED"
    fields = (latest20, latest50, latest_rsi, latest_atr)
    return series, QuantReport(latest20, latest50, latest_rsi, latest_atr, flow, vol_ratio, vol_state,
                               extension, extension_state, sum(v is not None for v in fields) / len(fields))
