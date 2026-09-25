from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.config import Settings
from gold_scalp_trader.decisions.executable_quality import ExecutableQuality,QualityPolicy,evaluate as quality_eval
from gold_scalp_trader.decisions.fusion import DecisionBoard,evaluate as fuse
from gold_scalp_trader.decisions.opportunity import Opportunity,create as create_opportunity
from gold_scalp_trader.decisions.timing import TimingDecision,evaluate as timing_eval
from gold_scalp_trader.decisions.trade_plan import TradePlan,build as build_plan
from gold_scalp_trader.domain.enums import RiskDecision,TimingOutcome
from gold_scalp_trader.domain.market import MarketSnapshot
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot,build as build_intelligence
from gold_scalp_trader.risk.engine import RiskEvaluation,evaluate as risk_eval
from gold_scalp_trader.strategies.isolation import IsolationResult,apply as isolate
from gold_scalp_trader.strategies.setup_detector import SetupRegistry,detect
@dataclass(frozen=True,slots=True)
class CycleResult:
    intelligence:IntelligenceSnapshot; registry:SetupRegistry; isolation:IsolationResult; board:DecisionBoard; opportunity:Opportunity|None; timing:TimingDecision|None; trade_plan:TradePlan|None; quality:ExecutableQuality|None; risk:RiskEvaluation|None; live_action:str; status:str; reason:str; gate_text:str="NOT EVALUATED"; system_text:str="ANALYTICS READY"
def run_cycle(market:MarketSnapshot,settings:Settings,*,quality_policy:QualityPolicy|None=None,target_risk_pct:float|None=None)->CycleResult:
    intel=build_intelligence(market); registry=detect(intel); isolation=isolate(registry,settings.active_strategy_family); board=fuse(isolation.live_candidate); opp=create_opportunity(board,market.captured_at)
    if opp is None:return CycleResult(intel,registry,isolation,board,None,None,None,None,None,"WAIT","SCANNING",isolation.reason)
    timing=timing_eval(opp,intel)
    if timing.outcome in {TimingOutcome.WAIT,TimingOutcome.MISSED,TimingOutcome.INVALID}:return CycleResult(intel,registry,isolation,board,opp,timing,None,None,None,"WAIT","TIMING",timing.reason)
    plan=build_plan(opp,timing,intel)
    if plan is None:return CycleResult(intel,registry,isolation,board,opp,timing,None,None,None,"WAIT","PLAN","TRADE_PLAN_UNAVAILABLE")
    quality=quality_eval(plan,market.quote,quality_policy or QualityPolicy())
    if not quality.passed:return CycleResult(intel,registry,isolation,board,opp,timing,plan,quality,None,"WAIT","QUALITY",",".join(quality.reasons))
    if target_risk_pct is None:return CycleResult(intel,registry,isolation,board,opp,timing,plan,quality,None,"READY_ANALYTICAL","RISK_PENDING","TARGET_RISK_PERCENT_NOT_SET")
    risk=risk_eval(plan,market.account,market.symbol_spec,day_start_equity=market.account.equity,target_risk_pct=target_risk_pct,aggressive_mode=settings.aggressive_small_account)
    action="READY_FOR_HARD_AUTHORITIES" if risk.decision is RiskDecision.PASS else "WAIT"
    return CycleResult(intel,registry,isolation,board,opp,timing,plan,quality,risk,action,"RISK",risk.reason)
