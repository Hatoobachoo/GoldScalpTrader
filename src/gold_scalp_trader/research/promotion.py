"""Evidence-bound candidate promotion; production requires explicit operator approval."""
from __future__ import annotations
from dataclasses import dataclass,replace
from enum import Enum
from hashlib import sha256
import json
class PromotionStage(str,Enum):
    PROPOSED="PROPOSED"; RESEARCHING="RESEARCHING"; VALIDATED="VALIDATED"; LOCKED="LOCKED"; HOLDOUT_PASSED="HOLDOUT_PASSED"; STRESS_PASSED="STRESS_PASSED"; SHADOW="SHADOW"; DEMO_CANDIDATE="DEMO_CANDIDATE"; APPROVAL_REQUIRED="APPROVAL_REQUIRED"; PRODUCTION="PRODUCTION"; REJECTED="REJECTED"
_ORDER=[PromotionStage.PROPOSED,PromotionStage.RESEARCHING,PromotionStage.VALIDATED,PromotionStage.LOCKED,PromotionStage.HOLDOUT_PASSED,PromotionStage.STRESS_PASSED,PromotionStage.SHADOW,PromotionStage.DEMO_CANDIDATE,PromotionStage.APPROVAL_REQUIRED]
@dataclass(frozen=True,slots=True)
class Candidate:
    candidate_id:str; kind:str; semantics:dict; stage:PromotionStage=PromotionStage.PROPOSED; holdout_consumed:bool=False; rollback_target:str|None=None
    @property
    def fingerprint(self)->str:return sha256(json.dumps(self.semantics,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
def advance(c:Candidate,target:PromotionStage,*,evidence_id:str,operator_approved:bool=False)->Candidate:
    if not evidence_id:raise ValueError("evidence_id required")
    if target is PromotionStage.PRODUCTION:
        if c.stage is not PromotionStage.APPROVAL_REQUIRED or not operator_approved:raise PermissionError("production promotion requires explicit operator approval")
        if not c.rollback_target:raise ValueError("rollback target required")
        return replace(c,stage=target)
    if c.stage not in _ORDER or target not in _ORDER:raise ValueError("invalid automated stage")
    if _ORDER.index(target)!=_ORDER.index(c.stage)+1:raise ValueError("stage skipping is forbidden")
    holdout=c.holdout_consumed or target is PromotionStage.HOLDOUT_PASSED
    if c.holdout_consumed and target is PromotionStage.HOLDOUT_PASSED:raise ValueError("holdout already consumed")
    return replace(c,stage=target,holdout_consumed=holdout)
