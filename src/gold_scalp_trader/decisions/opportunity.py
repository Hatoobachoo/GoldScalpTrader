"""Persistent analytical Opportunity identity and lifecycle primitives."""
from __future__ import annotations
from dataclasses import dataclass,replace
from datetime import datetime
from gold_scalp_trader.domain.enums import Direction,OpportunityState,StrategyFamily
from gold_scalp_trader.domain.ids import new_id
from .fusion import DecisionBoard
@dataclass(frozen=True,slots=True)
class Opportunity:
    opportunity_id:str; episode_id:str; family:StrategyFamily; direction:Direction; created_at:datetime; updated_at:datetime; state:OpportunityState; source_event_ids:tuple[str,...]; score:float; reasons:tuple[str,...]
def create(board:DecisionBoard,as_of:datetime)->Opportunity|None:
    c=board.candidate
    if c is None or board.recommendation!="ARM" or board.leading_direction is Direction.NONE: return None
    return Opportunity(str(new_id("OPP")),str(new_id("EP")),c.family,board.leading_direction,as_of,as_of,OpportunityState.ARMED,c.source_event_ids,c.score,c.reasons)
def transition(opp:Opportunity,state:OpportunityState,as_of:datetime,reason:str)->Opportunity:
    legal={OpportunityState.ARMED:{OpportunityState.WAITING,OpportunityState.READY,OpportunityState.MISSED,OpportunityState.INVALIDATED},OpportunityState.WAITING:{OpportunityState.READY,OpportunityState.MISSED,OpportunityState.INVALIDATED},OpportunityState.READY:{OpportunityState.WAITING,OpportunityState.TRIGGERED,OpportunityState.MISSED,OpportunityState.INVALIDATED}}
    if opp.state in {OpportunityState.MISSED,OpportunityState.INVALIDATED,OpportunityState.TRIGGERED}: raise ValueError("terminal Opportunity identity cannot transition")
    if state not in legal.get(opp.state,set()): raise ValueError(f"illegal opportunity transition {opp.state}->{state}")
    return replace(opp,state=state,updated_at=as_of,reasons=(*opp.reasons,reason))
