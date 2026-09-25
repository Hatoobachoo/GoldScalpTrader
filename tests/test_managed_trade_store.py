from gold_scalp_trader.domain.enums import Direction,StrategyFamily
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.management.store import load,save
from gold_scalp_trader.persistence.store import StateStore
def test_managed_trade_roundtrip_preserves_original_family_and_r():
    s=StateStore();t=ManagedTrade("T",7,"XAUUSDm",Direction.BUY,.01,100,99,99,102,104,StrategyFamily.BREAKOUT_RETEST_CONTINUATION,"v3",1.0);save(s,"scope",t);assert load(s,"scope")==t
