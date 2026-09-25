from datetime import datetime,timedelta,timezone
from gold_scalp_trader.domain.enums import DataQuality,StrategyFamily,Timeframe
from gold_scalp_trader.domain.market import AccountFacts,Candle,MarketSnapshot,Quote,SymbolSpec
from gold_scalp_trader.intelligence.snapshot import build as build_intelligence
from gold_scalp_trader.strategies.setup_detector import detect
from gold_scalp_trader.strategies.isolation import apply
UTC=timezone.utc
def _snapshot():
    now=datetime(2026,1,2,12,0,tzinfo=UTC); candles={}
    for tf,step,count in [(Timeframe.M1,1,80),(Timeframe.M5,5,100),(Timeframe.M15,15,100),(Timeframe.H1,60,100),(Timeframe.H4,240,60)]:
        start=now-timedelta(minutes=step*count); series=[]; price=100.0
        for i in range(count): price+=.05; series.append(Candle(tf,start+timedelta(minutes=step*i),price-.05,price+.2,price-.2,price,10,0))
        candles[tf]=tuple(series)
    return MarketSnapshot(now,AccountFacts(1,"demo","USD",1000,1000,1000,True,True),SymbolSpec("XAUUSDm",3,.001,.001,1,.01,200,.01),Quote(105,105.1,now,now),candles,{tf:DataQuality.HEALTHY for tf in candles},(),DataQuality.HEALTHY)
def test_active_family_does_not_force_setup():
    result=apply(detect(build_intelligence(_snapshot())),StrategyFamily.LIQUIDITY_SWEEP_REVERSAL)
    if result.live_candidate is not None: assert result.live_candidate.family is StrategyFamily.LIQUIDITY_SWEEP_REVERSAL
def test_exactly_one_family_is_marked_active_when_configured():
    result=apply(detect(build_intelligence(_snapshot())),StrategyFamily.BREAKOUT_RETEST_CONTINUATION); assert len([x for x in result.candidates if x.mode.value=="ACTIVE_EXECUTION"])==1
