from datetime import datetime,timedelta,timezone
from gold_scalp_trader.domain.enums import Timeframe
from gold_scalp_trader.domain.market import Candle
from gold_scalp_trader.intelligence.candle_structure import analyze as structure
from gold_scalp_trader.intelligence.confluence import analyze
UTC=timezone.utc
def test_confluence_is_causal_optional_context():
    start=datetime(2026,1,1,tzinfo=UTC);candles=[]
    for i in range(70):base=100+i*.05;candles.append(Candle(Timeframe.M5,start+timedelta(minutes=5*i),base,base+.4,base-.3,base+.1,10+i,0))
    series=tuple(candles);report=analyze(series,structure(series));assert report.poc is not None;assert report.poc_source=="TICK_VOLUME";assert 0<=report.coverage<=1
