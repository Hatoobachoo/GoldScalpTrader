"""Structural TradePlan geometry; no monetary sizing authority."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.enums import Direction,Timeframe,TimingOutcome
from gold_scalp_trader.domain.ids import new_id
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot
from .opportunity import Opportunity
from .timing import TimingDecision
@dataclass(frozen=True,slots=True)
class TradePlan:
    trade_plan_id:str; opportunity_id:str; direction:Direction; entry_reference:float; initial_sl:float; primary_target:float; expansion_target:float|None; invalidation_source:str; gross_r:float; state:str; reasons:tuple[str,...]
def build(opportunity:Opportunity,timing:TimingDecision,snapshot:IntelligenceSnapshot)->TradePlan|None:
    if timing.outcome not in {TimingOutcome.READY_BUY,TimingOutcome.READY_SELL}: return None
    m5=snapshot.by_timeframe.get(Timeframe.M5); m15=snapshot.by_timeframe.get(Timeframe.M15)
    if m5 is None:return None
    entry=snapshot.market.quote.ask if opportunity.direction is Direction.BUY else snapshot.market.quote.bid; atr=m5.quant.atr14
    if atr is None or atr<=0:return None
    buffer=max(atr*.10,snapshot.market.symbol_spec.tick_size)
    if opportunity.direction is Direction.BUY:
        base=m5.structure.last_swing_low.price if m5.structure.last_swing_low else entry-atr; sl=base-buffer; target=m15.technical.resistance.lower if m15 and m15.technical.resistance else entry+atr
        if target<=entry: target=entry+atr
        expansion=entry+(target-entry)*1.75; risk=entry-sl; reward=target-entry; source="M5_STRUCTURAL_LOW"
    else:
        base=m5.structure.last_swing_high.price if m5.structure.last_swing_high else entry+atr; sl=base+buffer; target=m15.technical.support.upper if m15 and m15.technical.support else entry-atr
        if target>=entry: target=entry-atr
        expansion=entry-(entry-target)*1.75; risk=sl-entry; reward=entry-target; source="M5_STRUCTURAL_HIGH"
    if risk<=0 or reward<=0:return None
    return TradePlan(str(new_id("PLAN")),opportunity.opportunity_id,opportunity.direction,entry,sl,target,expansion,source,reward/risk,"READY",("structural geometry built",))
