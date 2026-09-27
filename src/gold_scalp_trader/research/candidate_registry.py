"""Durable governed registry for autonomous research candidates.

Registration and promotion are research/governance operations only. Reaching a
stage never edits runtime Settings, Risk, Gate, active strategy selection or
broker authority. Stage evidence can only be issued by the verified immutable
stage-package protocol; arbitrary caller hashes cannot manufacture PASS proof.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore

from .evidence import EvidenceIdentity, identity_payload, verify_evidence_identity
from .invention import Recipe, invent
from .outcomes import SHADOW_OUTCOME_NS
from .promotion import Candidate, PromotionStage, advance
from .runtime_evidence import MANAGEMENT_NS, SHADOW_NS
from .timing_learning import NS as TIMING_NS

NS = "governed_strategy_candidates"
STAGE_EVIDENCE_NS = "candidate_stage_evidence"
VERIFIED_STAGE_ISSUER = "VERIFIED_STAGE_PACKAGE_V1"
KNOWN_SOURCE_NAMESPACES = (
    TIMING_NS,
    MANAGEMENT_NS,
    SHADOW_NS,
    SHADOW_OUTCOME_NS,
    "strategy_learning_memory",
)


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
    issuer: str = VERIFIED_STAGE_ISSUER
    package_manifest_sha256: str | None = None


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


def _record_verified_stage_evidence(
    store: StateStore,
    candidate_id: str,
    target_stage: PromotionStage,
    *,
    evidence_id: str,
    identity: EvidenceIdentity,
    artifact_sha256: str,
    package_manifest_sha256: str,
    limitations: Iterable[str] = (),
    issuer: str,
) -> StageEvidence:
    """Low-level sink reserved for the verified stage-package issuer."""
    if issuer != VERIFIED_STAGE_ISSUER:
        raise PermissionError("candidate stage evidence requires verified package issuer")
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
    if not verify_evidence_identity(identity):
        raise StateIntegrityError("stage evidence identity integrity check failed")
    if not _valid_sha256(artifact_sha256) or not _valid_sha256(package_manifest_sha256):
        raise ValueError("stage evidence package/artifact hashes must be valid SHA-256")

    payload = {
        "evidence_id": evidence_id,
        "candidate_id": candidate_id,
        "candidate_fingerprint": candidate.fingerprint,
        "target_stage": target_stage.value,
        "evidence_identity": identity_payload(identity),
        "evidence_identity_sha256": identity.sha256,
        "artifact_sha256": artifact_sha256.lower(),
        "package_manifest_sha256": package_manifest_sha256.lower(),
        "limitations": [str(item) for item in limitations],
        "result": "PASS",
        "issuer": issuer,
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
        issuer,
        package_manifest_sha256.lower(),
    )


def load_stage_evidence(store: StateStore, evidence_id: str) -> StageEvidence | None:
    row = store.get(STAGE_EVIDENCE_NS, evidence_id)
    if row is None:
        return None
    payload = row.payload
    if payload.get("runtime_authority") != "NONE" or payload.get("broker_authority") != "NONE":
        raise StateIntegrityError("stage evidence authority corruption")
    if payload.get("issuer") != VERIFIED_STAGE_ISSUER:
        raise StateIntegrityError("stage evidence issuer is not verified")
    package_hash = str(payload.get("package_manifest_sha256", ""))
    if not _valid_sha256(package_hash):
        raise StateIntegrityError("stage evidence package manifest hash invalid")
    identity_payload_raw = payload.get("evidence_identity")
    if not isinstance(identity_payload_raw, dict):
        raise StateIntegrityError("stage evidence identity missing")
    try:
        identity = EvidenceIdentity(
            candidate_fingerprint=str(identity_payload_raw["candidate_fingerprint"]),
            dataset_sha256=str(identity_payload_raw["dataset_sha256"]),
            code_revision=str(identity_payload_raw["code_revision"]),
            config_fingerprint=str(identity_payload_raw["config_fingerprint"]),
            policy_version=str(identity_payload_raw["policy_version"]),
            execution_realism=str(identity_payload_raw["execution_realism"]),
            sha256=str(identity_payload_raw["sha256"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise StateIntegrityError("stage evidence identity malformed") from exc
    if not verify_evidence_identity(identity):
        raise StateIntegrityError("stage evidence identity integrity mismatch")
    if identity.sha256 != payload.get("evidence_identity_sha256"):
        raise StateIntegrityError("stage evidence identity hash mismatch")
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
        identity.sha256,
        artifact_sha256,
        tuple(str(item) for item in payload.get("limitations", ())),
        VERIFIED_STAGE_ISSUER,
        package_hash,
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
        raise StateIntegrityError("promotion requires verified typed candidate-stage evidence")
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
    return False


__all__ = [
    "KNOWN_SOURCE_NAMESPACES",
    "NS",
    "STAGE_EVIDENCE_NS",
    "CandidateRecord",
    "StageEvidence",
    "advance_governed",
    "load",
    "load_stage_evidence",
    "register_invention",
    "runtime_activation_allowed",
]
