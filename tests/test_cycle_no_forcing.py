from datetime import datetime,timedelta,timezone
from gold_scalp_trader.app.cycle import run_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import DataQuality,StrategyFamily,Timeframe
from gold_scalp_trader.domain.market import AccountFacts,Candle,MarketSnapshot,Quote,SymbolSpec
UTC=timezone.utc

def flat_market():
    now=datetime(2026,2,2,12,0,tzinfo=UTC); candles={}
    for tf,step,count in [(Timeframe.M1,1,80),(Timeframe.M5,5,80),(Timeframe.M15,15,80),(Timeframe.H1,60,80),(Timeframe.H4,240,60)]:
        start=now-timedelta(minutes=step*count); candles[tf]=tuple(Candle(tf,start+timedelta(minutes=step*i),100,100.1,99.9,100,10,0) for i in range(count))
    return MarketSnapshot(now,AccountFacts(1,"demo","USD",1000,1000,1000,True,True),SymbolSpec("XAUUSDm",3,.001,.001,1,.01,200,.01),Quote(100,100.1,now,now),candles,{tf:DataQuality.HEALTHY for tf in candles},(),DataQuality.HEALTHY)

def test_active_family_does_not_manufacture_trade_in_flat_market():
    result=run_cycle(flat_market(),Settings(active_strategy_family=StrategyFamily.BREAKOUT_RETEST_CONTINUATION))
    assert result.opportunity is None
    assert result.live_action=="WAIT"
