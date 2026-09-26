from datetime import datetime,timedelta,timezone
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import DataQuality,Direction,RiskDecision,RiskProfile,Timeframe
from gold_scalp_trader.domain.market import AccountFacts,MarketSnapshot,Quote,SymbolSpec
from gold_scalp_trader.market_data.activity import DealFacts
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.risk.runtime import prepare
from gold_scalp_trader.risk.state import initial,load,record_closed_trade,save
UTC=timezone.utc
class StubReader:
    def __init__(self,deals=(),*,account_flat=True,position_deals=()):self.deals=deals;self.account_flat=account_flat;self.position_deals=position_deals
    def read_deals(self,*,from_time,to_time):return self.deals
    def account_positions_clear(self):return self.account_flat
    def read_position_deals(self,ticket,*,from_time,to_time):return self.position_deals
def market(as_of:datetime,*,equity:float=100.0)->MarketSnapshot:
    account=AccountFacts(12345,"Exness-Demo","USD",equity,equity,equity,True,True); spec=SymbolSpec("XAUUSDm",3,0.001,0.001,1.0,0.01,100.0,0.01); quote=Quote(4300.0,4300.2,as_of-timedelta(milliseconds=100),as_of); quality={tf:DataQuality.HEALTHY for tf in Timeframe}; candles={tf:() for tf in Timeframe}; return MarketSnapshot(as_of,account,spec,quote,candles,quality,(),DataQuality.HEALTHY)
def cash_deal(as_of:datetime,amount:float)->DealFacts:return DealFacts(1,None,"",None,0.0,amount,0.0,0.0,0.0,None,"UNKNOWN","BALANCE",as_of)
def external_close(as_of:datetime,amount:float)->DealFacts:return DealFacts(2,777,"XAUUSDm",Direction.BUY,0.01,amount,0.0,0.0,0.0,999,"OUT","BUY",as_of)
def test_fixed_profile_persists_even_if_current_equity_crosses_band():
    now=datetime(2026,9,26,5,0,tzinfo=UTC); store=StateStore(); save(store,"scope",initial(299.0,now)); result=prepare(store,"scope",StubReader(()),market(now,equity=310.0),Settings(),unresolved_lifecycle=False); assert result.decision is RiskDecision.PASS; assert result.state is not None; assert result.state.profile is RiskProfile.SMALL; assert result.state.day_start_equity==299.0
def test_midday_bootstrap_reconstructs_day_start_from_trades_and_cash_flow():
    now=datetime(2026,9,26,12,0,tzinfo=UTC); deals=(external_close(now-timedelta(hours=2),-10.0),cash_deal(now-timedelta(hours=1),5.0)); result=prepare(StateStore(),"scope",StubReader(deals),market(now,equity=95.0),Settings(),unresolved_lifecycle=False); assert result.decision is RiskDecision.PASS; assert result.state is not None; assert result.state.day_start_equity==100.0; assert result.state.account_safety_pl==-10.0; assert result.net_non_trading_cash_flow==5.0
def test_bootstrap_refuses_when_whole_account_not_flat():
    now=datetime(2026,9,26,12,0,tzinfo=UTC); result=prepare(StateStore(),"scope",StubReader((),account_flat=False),market(now),Settings(),unresolved_lifecycle=False); assert result.decision is RiskDecision.UNKNOWN; assert result.reason=="RISK_DAY_BOOTSTRAP_REQUIRES_FLAT_RECONCILED_ACCOUNT"
def test_daily_loss_lock_uses_persisted_day_start():
    now=datetime(2026,9,26,12,0,tzinfo=UTC); store=StateStore(); save(store,"scope",initial(100.0,now)); result=prepare(store,"scope",StubReader(()),market(now,equity=87.0),Settings(),unresolved_lifecycle=False); assert result.decision is RiskDecision.BLOCK; assert result.reason=="DAILY_LOSS_LOCKED"; assert result.state is not None and result.state.loss_locked
def test_three_verified_losses_create_cooldown_once():
    now=datetime(2026,9,26,12,0,tzinfo=UTC); store=StateStore(); save(store,"scope",initial(100.0,now))
    for idx in range(3):
        trade_id=f"TRD-{idx}"; store.put("managed_trade_closure_receipt",trade_id,{"trade_id":trade_id,"position_ticket":1000+idx,"closed_at":(now-timedelta(minutes=3-idx)).isoformat(),"net_money":-1.0})
    first=prepare(store,"scope",StubReader(()),market(now),Settings(),unresolved_lifecycle=False); assert first.decision is RiskDecision.BLOCK; assert first.reason=="CONSECUTIVE_LOSS_COOLDOWN"; assert first.state is not None and first.state.consecutive_losses==3
    second=prepare(store,"scope",StubReader(()),market(now),Settings(),unresolved_lifecycle=False); assert second.state is not None and second.state.consecutive_losses==3
def test_zero_result_does_not_count_as_loss():
    now=datetime(2026,9,26,12,0,tzinfo=UTC); state=record_closed_trade(initial(100.0,now),0.0,now); assert state.consecutive_losses==0; assert state.cooldown_until is None
def test_risk_state_round_trip_is_strict():
    now=datetime(2026,9,26,12,0,tzinfo=UTC); store=StateStore(); original=initial(250.0,now,aggressive_mode=True); save(store,"scope",original); assert load(store,"scope")==original
