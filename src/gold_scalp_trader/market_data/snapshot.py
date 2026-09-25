"""Helpers for constructing immutable MarketSnapshot objects."""
from __future__ import annotations

from datetime import datetime
from typing import Mapping

from gold_scalp_trader.domain.enums import DataQuality, Timeframe
from gold_scalp_trader.domain.market import AccountFacts, Candle, MarketSnapshot, PositionFacts, Quote, SymbolSpec


def build_snapshot(*, captured_at: datetime, account: AccountFacts, symbol_spec: SymbolSpec, quote: Quote,
                   candles: Mapping[Timeframe, tuple[Candle, ...]], quality: Mapping[Timeframe, DataQuality],
                   positions: tuple[PositionFacts, ...] | None, positions_quality: DataQuality) -> MarketSnapshot:
    return MarketSnapshot(captured_at, account, symbol_spec, quote, candles, quality, positions, positions_quality)
