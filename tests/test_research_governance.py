import pytest
from gold_scalp_trader.persistence.store import StateStore,StateIntegrityError
from gold_scalp_trader.research.learning import LearningObservation,save
from gold_scalp_trader.research.promotion import Candidate,PromotionStage,advance

def test_learning_is_idempotent_but_conflicting_source_is_integrity_error():
    s=StateStore(); a=LearningObservation("trade:1","BREAKOUT_RETEST","v1",1.2,.9,.7); save(s,a); save(s,a)
    with pytest.raises(StateIntegrityError): save(s,LearningObservation("trade:1","BREAKOUT_RETEST","v1",2.0,.9,.7))

def test_candidate_cannot_self_promote_to_production():
    c=Candidate("C1","ENTRY_POLICY",{"x":1},PromotionStage.APPROVAL_REQUIRED,rollback_target="champion-v1")
    with pytest.raises(PermissionError): advance(c,PromotionStage.PRODUCTION,evidence_id="ev",operator_approved=False)
    assert advance(c,PromotionStage.PRODUCTION,evidence_id="ev",operator_approved=True).stage is PromotionStage.PRODUCTION
