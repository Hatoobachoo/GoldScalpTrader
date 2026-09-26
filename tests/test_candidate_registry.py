import pytest

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore
from gold_scalp_trader.research.candidate_registry import (
    advance_governed,
    load,
    register_invention,
    runtime_activation_allowed,
)
from gold_scalp_trader.research.invention import Recipe
from gold_scalp_trader.research.promotion import PromotionStage
from gold_scalp_trader.research.timing_learning import NS as TIMING_NS


def _evidence(store: StateStore, key: str) -> None:
    store.append_event(TIMING_NS, key, {"kind": "test", "key": key})


def test_autonomous_candidate_requires_real_durable_source_evidence():
    store = StateStore()
    recipe = Recipe(("M5_SETUP",), ("M1_ENTRY_TIMING",), "INDEPENDENT_CASES", "FAMILY_PROFILE")
    with pytest.raises(StateIntegrityError, match="source evidence missing"):
        register_invention(store, recipe, ("TIM-MISSING",))

    _evidence(store, "TIM-1")
    record = register_invention(store, recipe, ("TIM-1",))
    assert record.candidate.stage is PromotionStage.PROPOSED
    assert record.evidence_chain == ("TIM-1",)
    assert runtime_activation_allowed(record) is False
    assert load(store, record.candidate.candidate_id) == record


def test_governed_promotion_cannot_skip_or_self_activate_production():
    store = StateStore()
    recipe = Recipe(("M5_SETUP",), ("M1_ENTRY_TIMING",), "INDEPENDENT_CASES", "FAMILY_PROFILE")
    _evidence(store, "TIM-SOURCE")
    record = register_invention(store, recipe, ("TIM-SOURCE",))
    cid = record.candidate.candidate_id

    _evidence(store, "E-RESEARCH")
    with pytest.raises(ValueError, match="stage skipping"):
        advance_governed(store, cid, PromotionStage.VALIDATED, evidence_id="E-RESEARCH")

    stages = (
        PromotionStage.RESEARCHING,
        PromotionStage.VALIDATED,
        PromotionStage.LOCKED,
        PromotionStage.HOLDOUT_PASSED,
        PromotionStage.STRESS_PASSED,
        PromotionStage.SHADOW,
        PromotionStage.DEMO_CANDIDATE,
        PromotionStage.APPROVAL_REQUIRED,
    )
    for index, stage in enumerate(stages):
        key = f"E-{index}"
        _evidence(store, key)
        record = advance_governed(store, cid, stage, evidence_id=key)
        assert record.candidate.stage is stage
        assert runtime_activation_allowed(record) is False

    _evidence(store, "E-PROD")
    with pytest.raises(PermissionError, match="explicit operator approval"):
        advance_governed(
            store,
            cid,
            PromotionStage.PRODUCTION,
            evidence_id="E-PROD",
            rollback_target="policy-v1",
        )

    record = advance_governed(
        store,
        cid,
        PromotionStage.PRODUCTION,
        evidence_id="E-PROD",
        rollback_target="policy-v1",
        operator_approved=True,
    )
    assert record.candidate.stage is PromotionStage.PRODUCTION
    assert record.candidate.rollback_target == "policy-v1"
    assert runtime_activation_allowed(record) is False
