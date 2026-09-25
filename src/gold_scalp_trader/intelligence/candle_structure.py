"""Causal candle anatomy, confirmed swings and simple break-state reporting."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from gold_scalp_trader.domain.enums import BreakEvent, Direction, StructureState
from gold_scalp_trader.domain.market import Candle

@dataclass(frozen=True, slots=True)
class CandleAnatomy:
    body: float; range: float; upper_wick: float; lower_wick: float; body_ratio: float | None; close_position: float | None

@dataclass(frozen=True, slots=True)
class Swing:
    direction: Direction; price: float; pivot_time: datetime; confirmed_at: datetime; source_index: int

@dataclass(frozen=True, slots=True)
class StructureReport:
    state: StructureState; last_swing_high: Swing | None; last_swing_low: Swing | None; break_event: BreakEvent; break_direction: Direction; event_time: datetime | None; coverage: float

def anatomy(candle: Candle) -> CandleAnatomy:
    rng = candle.high - candle.low; body = abs(candle.close - candle.open)
    return CandleAnatomy(body, rng, candle.high-max(candle.open,candle.close), min(candle.open,candle.close)-candle.low,
                         None if rng <= 0 else body/rng, None if rng <= 0 else (candle.close-candle.low)/rng)

def confirmed_swings(candles: tuple[Candle, ...], left: int = 2, right: int = 2) -> tuple[Swing, ...]:
    if left < 1 or right < 1: raise ValueError("left/right must be positive")
    swings: list[Swing] = []
    for pivot in range(left, len(candles)-right):
        window = candles[pivot-left:pivot+right+1]; current = candles[pivot]
        highs=[c.high for c in window]; lows=[c.low for c in window]; confirmed_at=candles[pivot+right].close_time
        if current.high == max(highs) and highs.count(current.high)==1:
            swings.append(Swing(Direction.SELL,current.high,current.open_time,confirmed_at,pivot))
        if current.low == min(lows) and lows.count(current.low)==1:
            swings.append(Swing(Direction.BUY,current.low,current.open_time,confirmed_at,pivot))
    return tuple(sorted(swings,key=lambda s:(s.confirmed_at,s.source_index,s.direction.value)))

def analyze(candles: tuple[Candle, ...]) -> StructureReport:
    if len(candles)<7: return StructureReport(StructureState.UNDETERMINED,None,None,BreakEvent.NONE,Direction.NONE,None,0.0)
    swings=confirmed_swings(candles); highs=[s for s in swings if s.direction is Direction.SELL]; lows=[s for s in swings if s.direction is Direction.BUY]
    last_high=highs[-1] if highs else None; last_low=lows[-1] if lows else None; state=StructureState.UNDETERMINED
    if len(highs)>=2 and len(lows)>=2:
        hh=highs[-1].price>highs[-2].price; hl=lows[-1].price>lows[-2].price; lh=highs[-1].price<highs[-2].price; ll=lows[-1].price<lows[-2].price
        state=StructureState.BULLISH if hh and hl else StructureState.BEARISH if lh and ll else StructureState.TRANSITION if (hh and ll) or (lh and hl) else StructureState.RANGE
    latest=candles[-1]; event=BreakEvent.NONE; direction=Direction.NONE
    if last_high is not None and latest.close>last_high.price and latest.close_time>last_high.confirmed_at:
        direction=Direction.BUY; event=BreakEvent.BOS if state is StructureState.BULLISH else BreakEvent.MSS_CANDIDATE
    elif last_low is not None and latest.close<last_low.price and latest.close_time>last_low.confirmed_at:
        direction=Direction.SELL; event=BreakEvent.BOS if state is StructureState.BEARISH else BreakEvent.MSS_CANDIDATE
    return StructureReport(state,last_high,last_low,event,direction,latest.close_time if event is not BreakEvent.NONE else None,min(1.0,len(candles)/50.0))
