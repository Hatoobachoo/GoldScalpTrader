from hashlib import sha256

import pytest

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore
from gold_scalp_trader.research.candidate_registry import (
    STAGE_EVIDENCE_NS,
    advance_governed,
    load,
    load_stage_evidence,
    register_invention,
    runtime_activation_allowed,
)
from gold_scalp_trader.research.evidence import build_evidence_identity
from gold_scalp_trader.research.invention import Recipe
from gold_scalp_trader.research.promotion import PromotionStage
from gold_scalp_trader.research.stage_orchestrator import (
    issue_stage_evidence,
    required_checks,
    write_stage_proof_package,
)
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


def _candidate(store: StateStore):
    recipe = Recipe(("M5_SETUP",), ("M1_ENTRY_TIMING",), "INDEPENDENT_CASES", "FAMILY_PROFILE")
    _evidence(store, "TIM-SOURCE")
    return register_invention(store, recipe, ("TIM-SOURCE",))


def _issue(tmp_path, store, record, stage, key):
    checks = {name: True for name in required_checks(stage)}
    package = write_stage_proof_package(
        tmp_path,
        package_id=f"pkg-{key}",
        stage=stage,
        evidence=_identity(record.candidate.fingerprint, key),
        checks=checks,
        observations={"stage": stage.value},
        limitations=(f"stage-{stage.value}",),
    )
    return issue_stage_evidence(
        store,
        record.candidate.candidate_id,
        stage,
        evidence_id=key,
        package_path=package,
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
    record = _candidate(store)
    _evidence(store, "TIM-NOT-STAGE-PROOF")
    with pytest.raises(StateIntegrityError, match="verified typed candidate-stage evidence"):
        advance_governed(
            store,
            record.candidate.candidate_id,
            PromotionStage.RESEARCHING,
            evidence_id="TIM-NOT-STAGE-PROOF",
        )


def test_stage_package_requires_stage_specific_checks(tmp_path):
    record_store = StateStore()
    record = _candidate(record_store)
    with pytest.raises(ValueError, match="missing/failed required checks"):
        write_stage_proof_package(
            tmp_path,
            package_id="bad",
            stage=PromotionStage.VALIDATED,
            evidence=_identity(record.candidate.fingerprint, "bad"),
            checks={"chronological_replay_complete": True},
        )


def test_stage_evidence_is_fingerprint_and_next_stage_bound(tmp_path):
    store = StateStore()
    record = _candidate(store)
    cid = record.candidate.candidate_id

    skip = write_stage_proof_package(
        tmp_path,
        package_id="skip",
        stage=PromotionStage.VALIDATED,
        evidence=_identity(record.candidate.fingerprint, "skip"),
        checks={name: True for name in required_checks(PromotionStage.VALIDATED)},
    )
    with pytest.raises(ValueError, match="next governed stage"):
        issue_stage_evidence(store, cid, PromotionStage.VALIDATED, evidence_id="E-SKIP", package_path=skip)

    wrong = write_stage_proof_package(
        tmp_path,
        package_id="wrong",
        stage=PromotionStage.RESEARCHING,
        evidence=_identity("0" * 64, "wrong"),
        checks={name: True for name in required_checks(PromotionStage.RESEARCHING)},
    )
    with pytest.raises(StateIntegrityError, match="fingerprint mismatch"):
        issue_stage_evidence(store, cid, PromotionStage.RESEARCHING, evidence_id="E-WRONG", package_path=wrong)


def test_stage_evidence_identity_is_reverified_when_loaded(tmp_path):
    store = StateStore()
    record = _candidate(store)
    _issue(tmp_path, store, record, PromotionStage.RESEARCHING, "E-TAMPER")
    row = store.get(STAGE_EVIDENCE_NS, "E-TAMPER")
    assert row is not None
    payload = dict(row.payload)
    identity = dict(payload["evidence_identity"])
    identity["code_revision"] = "tampered"
    payload["evidence_identity"] = identity
    store.put(STAGE_EVIDENCE_NS, "E-TAMPER", payload, allow_replace=True)
    with pytest.raises(StateIntegrityError, match="identity integrity mismatch"):
        load_stage_evidence(store, "E-TAMPER")


def test_governed_promotion_requires_verified_stage_packages_and_cannot_self_activate(tmp_path):
    store = StateStore()
    record = _candidate(store)
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
        proof = _issue(tmp_path, store, record, stage, key)
        assert proof.issuer == "VERIFIED_STAGE_PACKAGE_V1"
        assert proof.package_manifest_sha256 is not None
        record = advance_governed(store, cid, stage, evidence_id=key)
        assert record.candidate.stage is stage
        assert runtime_activation_allowed(record) is False

    _issue(tmp_path, store, record, PromotionStage.PRODUCTION, "STAGE-PROD")
    with pytest.raises(PermissionError, match="explicit operator approval"):
        advance_governed(
            store,
            cid,
            PromotionStage.PRODUCTION,
            evidence_id="STAGE-PROD",
            rollback_target="policy-v1",
        )

    record = advance_governed(
        store,
        cid,
        PromotionStage.PRODUCTION,
        evidence_id="STAGE-PROD",
        rollback_target="policy-v1",
        operator_approved=True,
    )
    assert record.candidate.stage is PromotionStage.PRODUCTION
    assert record.candidate.rollback_target == "policy-v1"
    assert runtime_activation_allowed(record) is False
