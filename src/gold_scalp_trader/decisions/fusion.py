"""Active-family BUY/SELL synthesis and Red-Team challenge."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.enums import Direction
from gold_scalp_trader.domain.models import SetupCandidate
@dataclass(frozen=True,slots=True)
class Thesis: direction:Direction; score:float; reasons:tuple[str,...]
@dataclass(frozen=True,slots=True)
class DecisionBoard: candidate:SetupCandidate|None; buy:Thesis; sell:Thesis; leading_direction:Direction; red_team_objections:tuple[str,...]; recommendation:str
def evaluate(candidate:SetupCandidate|None)->DecisionBoard:
    if candidate is None or not candidate.qualified:
        e=Thesis(Direction.NONE,0.0,("no qualified active-family setup",)); return DecisionBoard(candidate,e,e,Direction.NONE,("NO_ACTIVE_SETUP",),"WAIT")
    bs=candidate.score if candidate.direction is Direction.BUY else max(0.0,1.0-candidate.score); ss=candidate.score if candidate.direction is Direction.SELL else max(0.0,1.0-candidate.score)
    buy=Thesis(Direction.BUY,bs,candidate.reasons if candidate.direction is Direction.BUY else ("opposing case weaker",)); sell=Thesis(Direction.SELL,ss,candidate.reasons if candidate.direction is Direction.SELL else ("opposing case weaker",))
    objections=[]
    if candidate.coverage<.60: objections.append("LOW_EVIDENCE_COVERAGE")
    if abs(bs-ss)<.15: objections.append("DIRECTIONAL_CONFLICT")
    lead=Direction.BUY if bs>ss else Direction.SELL if ss>bs else Direction.NONE
    return DecisionBoard(candidate,buy,sell,lead,tuple(objections),"ARM" if lead is not Direction.NONE and not objections else "WAIT")
