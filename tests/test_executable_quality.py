from datetime import datetime,timezone
from gold_scalp_trader.domain.enums import Direction
from gold_scalp_trader.domain.market import Quote
from gold_scalp_trader.decisions.trade_plan import TradePlan
from gold_scalp_trader.decisions.executable_quality import QualityPolicy,evaluate
UTC=timezone.utc
def plan():return TradePlan("p","o",Direction.BUY,100,99,102,103,"M5",2.0,"READY",())
def test_quality_reports_spread_sl_and_target_ratios():
    q=Quote(100,100.2,datetime.now(tz=UTC),datetime.now(tz=UTC)); r=evaluate(plan(),q,QualityPolicy(max_spread_sl_ratio=.25,max_spread_target_ratio=.2,max_cost_reward_ratio=.2)); assert r.spread_sl_ratio>0 and r.spread_target_ratio>0
