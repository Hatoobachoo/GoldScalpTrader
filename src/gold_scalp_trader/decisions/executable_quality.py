"""Fresh current-price economics separate from structural TradePlan."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.enums import Direction
from gold_scalp_trader.domain.market import Quote
from .trade_plan import TradePlan
@dataclass(frozen=True,slots=True)
class QualityPolicy:
    version:str="BASELINE_UNCALIBRATED_V1"; emergency_spread_price:float|None=None; max_spread_sl_ratio:float|None=None; max_spread_target_ratio:float|None=None; max_cost_reward_ratio:float|None=None; slippage_allowance_price:float=0.0
@dataclass(frozen=True,slots=True)
class ExecutableQuality:
    passed:bool; spread:float; spread_sl_ratio:float; spread_target_ratio:float; cost_reward_ratio:float; drift:float; reasons:tuple[str,...]
def evaluate(plan:TradePlan,quote:Quote,policy:QualityPolicy)->ExecutableQuality:
    executable=quote.ask if plan.direction is Direction.BUY else quote.bid; spread=quote.spread; sl_distance=abs(executable-plan.initial_sl); target_distance=abs(plan.primary_target-executable)
    if sl_distance<=0 or target_distance<=0:return ExecutableQuality(False,spread,float("inf"),float("inf"),float("inf"),executable-plan.entry_reference,("geometry no longer executable",))
    ssl=spread/sl_distance; st=spread/target_distance; cr=(spread+max(0.0,policy.slippage_allowance_price))/target_distance; reasons=[]
    if policy.emergency_spread_price is not None and spread>policy.emergency_spread_price: reasons.append("EMERGENCY_SPREAD")
    if policy.max_spread_sl_ratio is not None and ssl>policy.max_spread_sl_ratio: reasons.append("SPREAD_SL_RATIO")
    if policy.max_spread_target_ratio is not None and st>policy.max_spread_target_ratio: reasons.append("SPREAD_TARGET_RATIO")
    if policy.max_cost_reward_ratio is not None and cr>policy.max_cost_reward_ratio: reasons.append("COST_REWARD_RATIO")
    return ExecutableQuality(not reasons,spread,ssl,st,cr,executable-plan.entry_reference,tuple(reasons) or ("PASS",))
