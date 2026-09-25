from datetime import datetime,timezone
from types import SimpleNamespace
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import DataQuality,Timeframe
from gold_scalp_trader.market_data.mt5_reader import Mt5Reader
UTC=timezone.utc
class FakeMt5:
    TIMEFRAME_M1=1; TIMEFRAME_M5=5; TIMEFRAME_M15=15; TIMEFRAME_H1=60; TIMEFRAME_H4=240
    def account_info(self): return SimpleNamespace(login=7,server="demo",currency="USD",balance=100,equity=100,margin_free=100,trade_allowed=True,trade_expert=True)
    def symbol_info(self,symbol):
        if symbol!="XAUUSDm": return None
        return SimpleNamespace(digits=3,point=.001,trade_tick_size=.001,trade_tick_value=1.0,volume_min=.01,volume_max=200,volume_step=.01,trade_stops_level=0,trade_freeze_level=0,trade_mode=4,filling_mode=1)
    def symbol_info_tick(self,symbol): return SimpleNamespace(bid=100.0,ask=100.2,time=1767225590)
    def copy_rates_from_pos(self,symbol,timeframe,start_pos,count):
        assert start_pos==1; step={1:60,5:300,15:900,60:3600,240:14400}[timeframe]; end=1767225300; n=min(count,60); rows=[]
        for i in range(n):
            t=end-(n-1-i)*step; rows.append({"time":t,"open":100+i*.01,"high":101+i*.01,"low":99+i*.01,"close":100.5+i*.01,"tick_volume":10,"real_volume":0})
        return rows
    def positions_get(self,symbol=None): return []

def test_reader_builds_one_completed_snapshot_and_distinguishes_verified_zero_positions():
    result=Mt5Reader(Settings(),FakeMt5()).read(captured_at=datetime(2026,1,1,0,0,tzinfo=UTC)); assert result.resolved_symbol=="XAUUSDm"; assert result.snapshot.positions==(); assert result.snapshot.positions_quality is DataQuality.HEALTHY; assert len(result.snapshot.series(Timeframe.M5))>=50
