from datetime import datetime,timezone
from types import SimpleNamespace
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import RuntimeMode,StrategyFamily
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.app.runtime import run_guarded_demo_cycle
UTC=timezone.utc
class Api:
    TIMEFRAME_M1=1;TIMEFRAME_M5=5;TIMEFRAME_M15=15;TIMEFRAME_H1=60;TIMEFRAME_H4=240;TRADE_ACTION_DEAL=1;ORDER_TYPE_BUY=0;ORDER_TYPE_SELL=1;TRADE_RETCODE_DONE=10009
    def __init__(self):self.sent=0;self.opened=False
    def account_info(self):return SimpleNamespace(login=7,server="demo",currency="USD",balance=1000,equity=1000,margin_free=1000,trade_allowed=True,trade_expert=True)
    def symbol_info(self,s):return SimpleNamespace(digits=3,point=.001,trade_tick_size=.001,trade_tick_value=1,volume_min=.01,volume_max=200,volume_step=.01,trade_stops_level=0,trade_freeze_level=0,trade_mode=4,filling_mode=1) if s=="XAUUSDm" else None
    def symbol_info_tick(self,s):return SimpleNamespace(bid=100,ask=100.02,time=int(datetime.now(tz=UTC).timestamp()))
    def copy_rates_from_pos(self,s,tf,start,count):
        now=int(datetime.now(tz=UTC).timestamp());step={1:60,5:300,15:900,60:3600,240:14400}[tf];rows=[];n=min(count,80)
        for i in range(n):
            t=now-(n-i)*step; price=100+(i*.02); rows.append({"time":t,"open":price-.01,"high":price+.08,"low":price-.08,"close":price+.01,"tick_volume":10,"real_volume":0})
        return rows
    def positions_get(self,symbol=None):
        if not self.opened:return []
        return [SimpleNamespace(ticket=88,symbol="XAUUSDm",type=0,volume=.01,price_open=100.02,sl=99,tp=101,magic=0,comment="")]
    def order_check(self,request):return SimpleNamespace(retcode=0)
    def order_send(self,request):self.sent+=1;self.opened=True;return SimpleNamespace(retcode=10009,order=88,deal=99,comment="done")
def test_demo_path_never_writes_without_a_complete_trade_setup():
    api=Api(); settings=Settings(mode=RuntimeMode.DEMO,active_strategy_family=StrategyFamily.BREAKOUT_RETEST_CONTINUATION,target_risk_percent=1.0,demo_trading_confirm="YES_I_APPROVE_DEMO")
    result=run_guarded_demo_cycle(settings,api,StateStore(),market_open=True)
    assert api.sent in {0,1}
    if api.sent==1:assert result.intent.state.value=="ACCEPTED_VERIFIED"
