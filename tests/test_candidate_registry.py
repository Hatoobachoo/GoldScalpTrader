from hashlib import sha256

import pytest

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore
from gold_scalp_trader.research.candidate_registry import (
    advance_governed,
    load,
    record_stage_evidence,
    register_invention,
    runtime_activation_allowed,
)
from gold_scalp_trader.research.evidence import build_evidence_identity
from gold_scalp_trader.research.invention import Recipe
from gold_scalp_trader.research.promotion import PromotionStage
from gold_scalp_trader.research.timing_learning import NS as TIMING_NS


def _evidence(store: StateStore, key: str) -> None:
    store.append_event(TIMING_NS, key, {"kind": "test", "key": key})


def _identity(fingerprint: str, suffix: str):
    return build_evidence_identity(
        candidate_fingerprint=fingerprint,
        dataset_sha256=sha256(f"dataset-{suffix}".encode()).hexdigest(),
        code_revision=f"code-{suffix}",
        config_fingerprint=f"cfg-{suffix}",
        policy_version=f"policy-{suffix}",
        execution_realism=f"REALISM-{suffix}",
    )


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


def test_raw_runtime_evidence_cannot_masquerade_as_promotion_stage_proof():
    store = StateStore()
    recipe = Recipe(("M5_SETUP",), ("M1_ENTRY_TIMING",), "INDEPENDENT_CASES", "FAMILY_PROFILE")
    _evidence(store, "TIM-SOURCE")
    record = register_invention(store, recipe, ("TIM-SOURCE",))
    _evidence(store, "TIM-NOT-STAGE-PROOF")
    with pytest.raises(StateIntegrityError, match="typed candidate-stage evidence"):
        advance_governed(store, record.candidate.candidate_id, PromotionStage.RESEARCHING, evidence_id="TIM-NOT-STAGE-PROOF")


def test_stage_evidence_is_fingerprint_and_next_stage_bound():
    store = StateStore()
    recipe = Recipe(("M5_SETUP",), ("M1_ENTRY_TIMING",), "INDEPENDENT_CASES", "FAMILY_PROFILE")
    _evidence(store, "TIM-SOURCE")
    record = register_invention(store, recipe, ("TIM-SOURCE",))
    cid = record.candidate.candidate_id

    with pytest.raises(ValueError, match="next governed stage"):
        record_stage_evidence(
            store, cid, PromotionStage.VALIDATED,
            evidence_id="E-SKIP", identity=_identity(record.candidate.fingerprint, "skip"), artifact_sha256="b" * 64,
        )
    with pytest.raises(StateIntegrityError, match="fingerprint mismatch"):
        record_stage_evidence(
            store, cid, PromotionStage.RESEARCHING,
            evidence_id="E-WRONG-FP", identity=_identity("0" * 64, "wrong"), artifact_sha256="c" * 64,
        )


def test_governed_promotion_requires_typed_stage_evidence_and_cannot_self_activate():
    store = StateStore()
    recipe = Recipe(("M5_SETUP",), ("M1_ENTRY_TIMING",), "INDEPENDENT_CASES", "FAMILY_PROFILE")
    _evidence(store, "TIM-SOURCE")
    record = register_invention(store, recipe, ("TIM-SOURCE",))
    cid = record.candidate.candidate_id

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
        key = f"STAGE-{index}"
        record_stage_evidence(
            store, cid, stage,
            evidence_id=key,
            identity=_identity(record.candidate.fingerprint, str(index)),
            artifact_sha256=f"{index + 1:064x}",
            limitations=(f"stage-{stage.value}",),
        )
        record = advance_governed(store, cid, stage, evidence_id=key)
        assert record.candidate.stage is stage
        assert runtime_activation_allowed(record) is False

    record_stage_evidence(
        store, cid, PromotionStage.PRODUCTION,
        evidence_id="STAGE-PROD",
        identity=_identity(record.candidate.fingerprint, "prod"),
        artifact_sha256="f" * 64,
        limitations=("explicit-operator-approval-still-required",),
    )
    with pytest.raises(PermissionError, match="explicit operator approval"):
        advance_governed(store, cid, PromotionStage.PRODUCTION, evidence_id="STAGE-PROD", rollback_target="policy-v1")

    record = advance_governed(
        store, cid, PromotionStage.PRODUCTION,
        evidence_id="STAGE-PROD", rollback_target="policy-v1", operator_approved=True,
    )
    assert record.candidate.stage is PromotionStage.PRODUCTION
    assert record.candidate.rollback_target == "policy-v1"
    assert runtime_activation_allowed(record) is False
