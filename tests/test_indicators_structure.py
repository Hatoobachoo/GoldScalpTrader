from datetime import datetime,timedelta,timezone
from gold_scalp_trader.domain.enums import Direction,Timeframe
from gold_scalp_trader.domain.market import Candle
from gold_scalp_trader.intelligence.candle_structure import confirmed_swings
from gold_scalp_trader.intelligence.indicators import calculate
UTC=timezone.utc

def make_series(n=80):
    start=datetime(2026,1,1,tzinfo=UTC); out=[]; price=100.0
    for i in range(n):
        price += .2 if i%7 else -.4; out.append(Candle(Timeframe.M5,start+timedelta(minutes=5*i),price-.1,price+.4,price-.5,price,10,0))
    return tuple(out)

def test_indicator_warmup_and_latest_values_are_causal():
    series,report=calculate(make_series()); assert series.ema20[10] is None; assert series.ema20[-1] is not None; assert series.ema50[-1] is not None; assert report.atr14 is not None

def test_swing_confirmation_time_is_after_pivot_time():
    start=datetime(2026,1,1,tzinfo=UTC); highs=[1,2,5,2,1,2,1]; candles=tuple(Candle(Timeframe.M5,start+timedelta(minutes=5*i),h-.5,h,h-1,h-.2,1,0) for i,h in enumerate(highs)); swings=confirmed_swings(candles,left=2,right=2); top=next(s for s in swings if s.direction is Direction.SELL and s.price==5); assert top.confirmed_at>top.pivot_time; assert top.confirmed_at==candles[4].close_time
