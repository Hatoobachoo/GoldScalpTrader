from hashlib import sha256

from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.candidate_registry import (
    advance_governed,
    register_invention,
    transition_history,
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


def test_candidate_transition_history_is_contiguous_actor_attributed_and_durable(tmp_path):
    store = StateStore()
    store.append_event(TIMING_NS, "SRC", {"kind": "timing"})
    record = register_invention(
        store,
        Recipe(("M5_SETUP",), ("M1_ENTRY_TIMING",), "INDEPENDENT_CASES", "FAMILY_PROFILE"),
        ("SRC",),
    )
    identity = build_evidence_identity(
        candidate_fingerprint=record.candidate.fingerprint,
        dataset_sha256=sha256(b"dataset").hexdigest(),
        code_revision="code",
        config_fingerprint="cfg",
        policy_version="policy",
        execution_realism="REPLAY",
    )
    stage = PromotionStage.RESEARCHING
    package = write_stage_proof_package(
        tmp_path,
        package_id="researching",
        stage=stage,
        evidence=identity,
        checks={name: True for name in required_checks(stage)},
    )
    issue_stage_evidence(
        store,
        record.candidate.candidate_id,
        stage,
        evidence_id="E1",
        package_path=package,
    )
    advance_governed(store, record.candidate.candidate_id, stage, evidence_id="E1")

    history = transition_history(store, record.candidate.candidate_id)
    assert len(history) == 1
    assert history[0]["from_stage"] == "PROPOSED"
    assert history[0]["to_stage"] == "RESEARCHING"
    assert history[0]["actor"] == "AUTO_RESEARCH"
    assert history[0]["evidence_id"] == "E1"
    assert history[0]["runtime_authority"] == "NONE"
    assert history[0]["broker_authority"] == "NONE"
    assert history[0]["recorded_at_utc"]
