from gold_scalp_trader.domain.enums import Direction,RiskDecision,RiskProfile
from gold_scalp_trader.domain.market import AccountFacts,SymbolSpec
from gold_scalp_trader.decisions.trade_plan import TradePlan
from gold_scalp_trader.risk.engine import evaluate,resolve_profile
def test_profile_boundaries_are_preserved():
    assert resolve_profile(100) is RiskProfile.SMALL; assert resolve_profile(300) is RiskProfile.MEDIUM; assert resolve_profile(999.99) is RiskProfile.MEDIUM; assert resolve_profile(1000) is RiskProfile.NORMAL
def test_min_lot_is_evaluated_not_automatically_rejected():
    p=TradePlan("p","o",Direction.BUY,100,99.9,101,None,"M5",10,"READY",()); a=AccountFacts(1,"demo","USD",100,100,100,True,True); s=SymbolSpec("XAUUSDm",3,.001,.001,1,.01,200,.01); r=evaluate(p,a,s,day_start_equity=100,target_risk_pct=3.0); assert r.volume is not None and r.decision in {RiskDecision.PASS,RiskDecision.BLOCK}
def test_target_above_hard_ceiling_blocks():
    p=TradePlan("p","o",Direction.BUY,100,99,101,None,"M5",1,"READY",()); a=AccountFacts(1,"demo","USD",100,100,100,True,True); s=SymbolSpec("XAUUSDm",3,.001,.001,1,.01,200,.01); assert evaluate(p,a,s,day_start_equity=100,target_risk_pct=7.1).decision is RiskDecision.BLOCK
