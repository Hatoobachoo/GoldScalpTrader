"""Chronological prefix iterator for no-lookahead replay."""
from __future__ import annotations
from collections.abc import Iterator
from gold_scalp_trader.domain.market import Candle
def prefixes(candles:tuple[Candle,...],warmup:int=50)->Iterator[tuple[Candle,...]]:
    for end in range(warmup,len(candles)+1):yield candles[:end]
