"""Causal liquidity-pool and latest interaction analysis."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from gold_scalp_trader.domain.enums import Direction
from gold_scalp_trader.domain.market import Candle
from .candle_structure import StructureReport
from .indicators import QuantReport

@dataclass(frozen=True, slots=True)
class LiquidityPool:
    pool_id: str; direction: Direction; lower: float; upper: float; created_at: datetime; source: str

@dataclass(frozen=True, slots=True)
class LiquidityReport:
    buy_side: LiquidityPool | None; sell_side: LiquidityPool | None; latest_event: str; event_direction: Direction; event_time: datetime | None; coverage: float

def analyze(candles: tuple[Candle,...], structure: StructureReport, quant: QuantReport) -> LiquidityReport:
    atr=quant.atr14; tol=None if atr is None else max(atr*.08,1e-9); bsl=ssl=None
    if tol is not None and structure.last_swing_high is not None:
        s=structure.last_swing_high; bsl=LiquidityPool(f"BSL-{s.pivot_time.isoformat()}",Direction.BUY,s.price-tol,s.price+tol,s.confirmed_at,"SWING_HIGH")
    if tol is not None and structure.last_swing_low is not None:
        s=structure.last_swing_low; ssl=LiquidityPool(f"SSL-{s.pivot_time.isoformat()}",Direction.SELL,s.price-tol,s.price+tol,s.confirmed_at,"SWING_LOW")
    event="NONE"; event_dir=Direction.NONE; event_time=None
    if candles:
        latest=candles[-1]
        if bsl is not None and latest.close_time>bsl.created_at and latest.high>bsl.upper and latest.close<bsl.upper:
            event,event_dir,event_time="BUY_SIDE_SWEEP_RECLAIM",Direction.SELL,latest.close_time
        elif ssl is not None and latest.close_time>ssl.created_at and latest.low<ssl.lower and latest.close>ssl.lower:
            event,event_dir,event_time="SELL_SIDE_SWEEP_RECLAIM",Direction.BUY,latest.close_time
    return LiquidityReport(bsl,ssl,event,event_dir,event_time,sum(v is not None for v in (bsl,ssl,atr))/3.0)
