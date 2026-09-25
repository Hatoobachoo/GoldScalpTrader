"""Preserved monetary Risk profiles and broker-aware sizing."""
from __future__ import annotations
from dataclasses import dataclass
from math import floor
from gold_scalp_trader.config import PRESERVED_RISK_BANDS
from gold_scalp_trader.domain.enums import RiskDecision,RiskProfile
from gold_scalp_trader.domain.market import AccountFacts,SymbolSpec
from gold_scalp_trader.decisions.trade_plan import TradePlan
@dataclass(frozen=True,slots=True)
class RiskEvaluation:profile:RiskProfile; decision:RiskDecision; target_risk_pct:float; volume:float|None; actual_risk_money:float|None; actual_risk_pct:float|None; reason:str
def resolve_profile(day_start_equity:float)->RiskProfile:
    if day_start_equity<=0:raise ValueError("DayStartEquity must be positive")
    if day_start_equity<300:return RiskProfile.SMALL
    if day_start_equity<1000:return RiskProfile.MEDIUM
    return RiskProfile.NORMAL
def _normalize_volume(raw:float,spec:SymbolSpec)->float:
    if raw<=spec.volume_min:return spec.volume_min
    steps=floor((raw-spec.volume_min)/spec.volume_step); volume=spec.volume_min+steps*spec.volume_step; return round(min(spec.volume_max,max(spec.volume_min,volume)),8)
def evaluate(plan:TradePlan,account:AccountFacts,spec:SymbolSpec,*,day_start_equity:float,target_risk_pct:float,aggressive_mode:bool=False,aggregate_open_risk_pct:float=0.0)->RiskEvaluation:
    profile=resolve_profile(day_start_equity); band=PRESERVED_RISK_BANDS[profile.value]; hard=8.0 if aggressive_mode else band.hard_ceiling_pct
    if target_risk_pct<=0 or target_risk_pct>hard:return RiskEvaluation(profile,RiskDecision.BLOCK,target_risk_pct,None,None,None,"TARGET_RISK_OUTSIDE_HARD_POLICY")
    if aggregate_open_risk_pct<0:return RiskEvaluation(profile,RiskDecision.UNKNOWN,target_risk_pct,None,None,None,"AGGREGATE_RISK_UNKNOWN")
    if spec.tick_value is None or spec.tick_value<=0:return RiskEvaluation(profile,RiskDecision.UNKNOWN,target_risk_pct,None,None,None,"TICK_VALUE_UNKNOWN")
    stop_distance=abs(plan.entry_reference-plan.initial_sl)
    if stop_distance<=0:return RiskEvaluation(profile,RiskDecision.BLOCK,target_risk_pct,None,None,None,"INVALID_STOP_DISTANCE")
    risk_per_lot=(stop_distance/spec.tick_size)*spec.tick_value
    if risk_per_lot<=0:return RiskEvaluation(profile,RiskDecision.UNKNOWN,target_risk_pct,None,None,None,"RISK_PER_LOT_UNKNOWN")
    budget=account.equity*(target_risk_pct/100.0); volume=_normalize_volume(budget/risk_per_lot,spec); actual=risk_per_lot*volume; actual_pct=(actual/account.equity)*100 if account.equity>0 else float("inf")
    if actual_pct>hard:return RiskEvaluation(profile,RiskDecision.BLOCK,target_risk_pct,volume,actual,actual_pct,"MIN_OR_NORMALIZED_VOLUME_EXCEEDS_HARD_CEILING")
    if aggressive_mode and aggregate_open_risk_pct+actual_pct>16.0:return RiskEvaluation(profile,RiskDecision.BLOCK,target_risk_pct,volume,actual,actual_pct,"AGGRESSIVE_AGGREGATE_RISK_EXCEEDS_16_PERCENT")
    classification="NORMAL" if band.normal_min_pct<=actual_pct<=band.normal_max_pct else "ELEVATED" if actual_pct<=band.elevated_max_pct else "CONSERVATIVE" if actual_pct<band.normal_min_pct else "WITHIN_HARD_CEILING"
    return RiskEvaluation(profile,RiskDecision.PASS,target_risk_pct,volume,actual,actual_pct,classification)
