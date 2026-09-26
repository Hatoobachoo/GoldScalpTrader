"""Durable governed registry for autonomous research candidates.

Registration and promotion are research/governance operations only. Reaching a
stage never edits runtime Settings, Risk, Gate, active strategy selection or
broker authority. Production-stage evidence still requires explicit operator
approval plus rollback lineage and a separate governed deployment action.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore

from .evidence import EvidenceIdentity, identity_payload
from .invention import Recipe, invent
from .promotion import Candidate, PromotionStage, advance
from .runtime_evidence import MANAGEMENT_NS, SHADOW_NS
from .timing_learning import NS as TIMING_NS

NS = "governed_strategy_candidates"
STAGE_EVIDENCE_NS = "candidate_stage_evidence"
KNOWN_SOURCE_NAMESPACES = (TIMING_NS, MANAGEMENT_NS, SHADOW_NS, "strategy_learning_memory")


@dataclass(frozen=True, slots=True)
class CandidateRecord:
    candidate: Candidate
    evidence_chain: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StageEvidence:
    evidence_id: str
    candidate_id: str
    candidate_fingerprint: str
    target_stage: PromotionStage
    evidence_identity_sha256: str
    artifact_sha256: str
    limitations: tuple[str, ...] = ()


def _payload(record: CandidateRecord) -> dict:
    candidate = record.candidate
    return {
        "candidate_id": candidate.candidate_id,
        "kind": candidate.kind,
        "semantics": candidate.semantics,
        "stage": candidate.stage.value,
        "holdout_consumed": candidate.holdout_consumed,
        "rollback_target": candidate.rollback_target,
        "fingerprint": candidate.fingerprint,
        "evidence_chain": list(record.evidence_chain),
        "runtime_authority": "NONE",
        "broker_authority": "NONE",
    }


def _restore_semantics(value):
    """Restore invention tuple semantics lost by JSON serialization."""
    if not isinstance(value, dict):
        raise StateIntegrityError("candidate semantics must be an object")
    restored = dict(value)
    for key in ("required", "supportive", "sources"):
        item = restored.get(key)
        if isinstance(item, list):
            restored[key] = tuple(item)
    return restored


def _candidate(payload: dict) -> Candidate:
    return Candidate(
        candidate_id=str(payload["candidate_id"]),
        kind=str(payload["kind"]),
        semantics=_restore_semantics(payload["semantics"]),
        stage=PromotionStage(str(payload["stage"])),
        holdout_consumed=bool(payload.get("holdout_consumed", False)),
        rollback_target=None if payload.get("rollback_target") is None else str(payload["rollback_target"]),
    )


def load(store: StateStore, candidate_id: str) -> CandidateRecord | None:
    row = store.get(NS, candidate_id)
    if row is None:
        return None
    candidate = _candidate(row.payload)
    if row.payload.get("fingerprint") != candidate.fingerprint:
        raise StateIntegrityError(f"candidate fingerprint mismatch {candidate_id}")
    if row.payload.get("runtime_authority") != "NONE" or row.payload.get("broker_authority") != "NONE":
        raise StateIntegrityError(f"candidate authority corruption {candidate_id}")
    return CandidateRecord(candidate, tuple(str(x) for x in row.payload.get("evidence_chain", ())))


def _source_evidence_exists(store: StateStore, evidence_id: str) -> bool:
    if not evidence_id:
        return False
    for namespace in KNOWN_SOURCE_NAMESPACES:
        if any(event.event_key == evidence_id for event in store.list_events(namespace)):
            return True
        if store.get(namespace, evidence_id) is not None:
            return True
    return False


def _valid_sha256(value: str) -> bool:
    text = str(value).lower()
    return len(text) == 64 and all(ch in "0123456789abcdef" for ch in text)


def _expected_next_stage(candidate: Candidate) -> PromotionStage:
    automated = (
        PromotionStage.PROPOSED,
        PromotionStage.RESEARCHING,
        PromotionStage.VALIDATED,
        PromotionStage.LOCKED,
        PromotionStage.HOLDOUT_PASSED,
        PromotionStage.STRESS_PASSED,
        PromotionStage.SHADOW,
        PromotionStage.DEMO_CANDIDATE,
        PromotionStage.APPROVAL_REQUIRED,
    )
    if candidate.stage is PromotionStage.APPROVAL_REQUIRED:
        return PromotionStage.PRODUCTION
    if candidate.stage not in automated:
        raise ValueError("candidate has no promotable next stage")
    index = automated.index(candidate.stage)
    if index + 1 >= len(automated):
        return PromotionStage.PRODUCTION
    return automated[index + 1]


def record_stage_evidence(
    store: StateStore,
    candidate_id: str,
    target_stage: PromotionStage,
    *,
    evidence_id: str,
    identity: EvidenceIdentity,
    artifact_sha256: str,
    limitations: Iterable[str] = (),
) -> StageEvidence:
    """Bind immutable research evidence to exactly one candidate and next stage."""
    current = load(store, candidate_id)
    if current is None:
        raise StateIntegrityError(f"unknown candidate {candidate_id}")
    candidate = current.candidate
    expected = _expected_next_stage(candidate)
    if target_stage is not expected:
        raise ValueError(f"stage evidence must target the next governed stage: {expected.value}")
    if not evidence_id.strip():
        raise ValueError("stage evidence_id is required")
    if identity.candidate_fingerprint != candidate.fingerprint:
        raise StateIntegrityError("stage evidence candidate fingerprint mismatch")
    if not _valid_sha256(identity.sha256):
        raise StateIntegrityError("stage evidence identity hash invalid")
    if not _valid_sha256(artifact_sha256):
        raise ValueError("stage evidence artifact_sha256 must be a valid SHA-256")

    payload = {
        "evidence_id": evidence_id,
        "candidate_id": candidate_id,
        "candidate_fingerprint": candidate.fingerprint,
        "target_stage": target_stage.value,
        "evidence_identity": identity_payload(identity),
        "evidence_identity_sha256": identity.sha256,
        "artifact_sha256": artifact_sha256.lower(),
        "limitations": [str(item) for item in limitations],
        "result": "PASS",
        "runtime_authority": "NONE",
        "broker_authority": "NONE",
    }
    store.put(STAGE_EVIDENCE_NS, evidence_id, payload, allow_replace=False)
    return StageEvidence(
        evidence_id,
        candidate_id,
        candidate.fingerprint,
        target_stage,
        identity.sha256,
        artifact_sha256.lower(),
        tuple(str(item) for item in limitations),
    )


def load_stage_evidence(store: StateStore, evidence_id: str) -> StageEvidence | None:
    row = store.get(STAGE_EVIDENCE_NS, evidence_id)
    if row is None:
        return None
    payload = row.payload
    if payload.get("runtime_authority") != "NONE" or payload.get("broker_authority") != "NONE":
        raise StateIntegrityError("stage evidence authority corruption")
    identity = payload.get("evidence_identity")
    if not isinstance(identity, dict) or identity.get("sha256") != payload.get("evidence_identity_sha256"):
        raise StateIntegrityError("stage evidence identity mismatch")
    if payload.get("result") != "PASS":
        raise StateIntegrityError("stage evidence is not PASS")
    artifact_sha256 = str(payload.get("artifact_sha256", ""))
    if not _valid_sha256(artifact_sha256):
        raise StateIntegrityError("stage evidence artifact hash invalid")
    return StageEvidence(
        str(payload["evidence_id"]),
        str(payload["candidate_id"]),
        str(payload["candidate_fingerprint"]),
        PromotionStage(str(payload["target_stage"])),
        str(payload["evidence_identity_sha256"]),
        artifact_sha256,
        tuple(str(item) for item in payload.get("limitations", ())),
    )


def register_invention(store: StateStore, recipe: Recipe, source_evidence_ids: Iterable[str]) -> CandidateRecord:
    evidence_ids = tuple(dict.fromkeys(str(x) for x in source_evidence_ids if str(x)))
    if not evidence_ids:
        raise ValueError("autonomous invention requires durable source evidence")
    missing = tuple(eid for eid in evidence_ids if not _source_evidence_exists(store, eid))
    if missing:
        raise StateIntegrityError(f"candidate source evidence missing: {missing}")
    candidate = invent(recipe, evidence_ids)
    record = CandidateRecord(candidate, evidence_ids)
    store.put(NS, candidate.candidate_id, _payload(record), allow_replace=False)
    return record


def advance_governed(
    store: StateStore,
    candidate_id: str,
    target: PromotionStage,
    *,
    evidence_id: str,
    operator_approved: bool = False,
    rollback_target: str | None = None,
) -> CandidateRecord:
    current = load(store, candidate_id)
    if current is None:
        raise StateIntegrityError(f"unknown candidate {candidate_id}")
    evidence = load_stage_evidence(store, evidence_id)
    if evidence is None:
        raise StateIntegrityError("promotion requires typed candidate-stage evidence")
    if evidence.candidate_id != candidate_id:
        raise StateIntegrityError("promotion evidence belongs to a different candidate")
    if evidence.candidate_fingerprint != current.candidate.fingerprint:
        raise StateIntegrityError("promotion evidence fingerprint mismatch")
    if evidence.target_stage is not target:
        raise StateIntegrityError("promotion evidence target-stage mismatch")

    candidate = current.candidate
    if rollback_target is not None:
        candidate = replace(candidate, rollback_target=rollback_target)
    promoted = advance(
        candidate,
        target,
        evidence_id=evidence_id,
        operator_approved=operator_approved,
    )
    chain = (*current.evidence_chain, evidence_id)
    record = CandidateRecord(promoted, chain)
    store.put(NS, candidate_id, _payload(record), allow_replace=True)
    return record


def runtime_activation_allowed(record: CandidateRecord) -> bool:
    """Registry stage alone can never activate a strategy in live runtime."""
    return False
