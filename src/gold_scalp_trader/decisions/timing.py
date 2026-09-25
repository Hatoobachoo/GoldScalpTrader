"""Subordinate M1 timing after a valid M5 Opportunity."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.enums import Direction,OpportunityState,Timeframe,TimingOutcome
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot
from .opportunity import Opportunity
@dataclass(frozen=True,slots=True)
class TimingDecision: outcome:TimingOutcome; reason:str; trigger_time:object|None; micro_extension_atr:float|None
def evaluate(opportunity:Opportunity|None,snapshot:IntelligenceSnapshot)->TimingDecision:
    if opportunity is None or opportunity.state not in {OpportunityState.ARMED,OpportunityState.WAITING,OpportunityState.READY}: return TimingDecision(TimingOutcome.INVALID,"no valid M5 Opportunity",None,None)
    m1=snapshot.by_timeframe.get(Timeframe.M1); candles=snapshot.market.series(Timeframe.M1)
    if m1 is None or len(candles)<2: return TimingDecision(TimingOutcome.WAIT,"M1 refinement unavailable",None,None)
    latest,prev=candles[-1],candles[-2]; ext=m1.quant.extension_atr
    if ext is not None and ext>1.50: return TimingDecision(TimingOutcome.MISSED,"M1 severely extended/chased",latest.close_time,ext)
    if opportunity.direction is Direction.BUY:
        ready=latest.close>latest.open and latest.close>prev.close and m1.quant.ema_flow in {"BUY","UNKNOWN"}; return TimingDecision(TimingOutcome.READY_BUY if ready else TimingOutcome.WAIT,"M1 bullish continuation/reclaim" if ready else "waiting for bullish M1 refinement",latest.close_time,ext)
    ready=latest.close<latest.open and latest.close<prev.close and m1.quant.ema_flow in {"SELL","UNKNOWN"}; return TimingDecision(TimingOutcome.READY_SELL if ready else TimingOutcome.WAIT,"M1 bearish continuation/reclaim" if ready else "waiting for bearish M1 refinement",latest.close_time,ext)
