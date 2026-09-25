from datetime import datetime,timezone
from gold_scalp_trader.domain.enums import DataQuality,Direction
from gold_scalp_trader.market_data.activity import DealFacts,account_safety_pl,classify_deals
UTC=timezone.utc
def deal(ticket,position,magic,role,dtype,profit=0.0):return DealFacts(ticket,position,"XAUUSDm",Direction.BUY if dtype=="BUY" else None,.01,profit,0,0,0,magic,role,dtype,datetime.now(tz=UTC))
def test_bot_and_external_activity_are_separate():
    rows=(deal(1,10,77,"IN","BUY"),deal(2,10,77,"OUT","BUY",5),deal(3,20,0,"OUT","BUY",-2),deal(4,None,0,"NONE","BALANCE",100));s=classify_deals(rows,bot_magic=77,external_open_positions=0);assert s.quality is DataQuality.HEALTHY;assert s.bot_entries==1 and s.bot_realized==5 and s.external_realized==-2 and s.net_non_trading_cash_flow==100;assert account_safety_pl(current_equity=205,day_start_equity=100,net_non_trading_cash_flow=100)==5
def test_missing_activity_is_unknown_not_zero():assert classify_deals(None,bot_magic=77).quality is DataQuality.UNKNOWN
