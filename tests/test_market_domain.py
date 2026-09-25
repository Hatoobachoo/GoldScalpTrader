from datetime import datetime,timedelta,timezone
import pytest
from gold_scalp_trader.domain.enums import DataQuality,Timeframe
from gold_scalp_trader.domain.market import AccountFacts,Candle,MarketSnapshot,Quote,SymbolSpec
UTC=timezone.utc

def candle(open_time,tf=Timeframe.M5): return Candle(tf,open_time,100.0,102.0,99.0,101.0,10,0)

def test_quote_future_age_is_signed_not_absolute():
    now=datetime(2026,1,1,tzinfo=UTC); quote=Quote(100.0,100.2,now+timedelta(seconds=1),now); assert quote.age_seconds==-1.0

def test_snapshot_rejects_forming_candle():
    now=datetime(2026,1,1,12,3,tzinfo=UTC)
    with pytest.raises(ValueError,match="forming/future"):
        MarketSnapshot(now,AccountFacts(1,"srv","USD",100,100,100,True,True),SymbolSpec("XAUUSDm",3,.001,.001,1.0,.01,10.0,.01),Quote(100,100.1,now,now),{Timeframe.M5:(candle(datetime(2026,1,1,12,0,tzinfo=UTC)),)},{Timeframe.M5:DataQuality.HEALTHY},(),DataQuality.HEALTHY)
