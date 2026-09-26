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
from .invention import Recipe, invent
from .promotion import Candidate, PromotionStage, advance
from .runtime_evidence import MANAGEMENT_NS, SHADOW_NS
from .timing_learning import NS as TIMING_NS

NS = "governed_strategy_candidates"
KNOWN_EVIDENCE_NAMESPACES = (TIMING_NS, MANAGEMENT_NS, SHADOW_NS, "strategy_learning_memory")


@dataclass(frozen=True, slots=True)
class CandidateRecord:
    candidate: Candidate
    evidence_chain: tuple[str, ...]


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
    """Restore invention tuple semantics lost by JSON serialization.

    Candidate fingerprints are JSON-canonical and therefore unaffected by
    tuple/list representation, but dataclass round-trip equality should retain
    the immutable tuple shape produced by ``invent``.
    """
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


def _evidence_exists(store: StateStore, evidence_id: str) -> bool:
    if not evidence_id:
        return False
    for namespace in KNOWN_EVIDENCE_NAMESPACES:
        if any(event.event_key == evidence_id for event in store.list_events(namespace)):
            return True
        if store.get(namespace, evidence_id) is not None:
            return True
    return False


def register_invention(store: StateStore, recipe: Recipe, source_evidence_ids: Iterable[str]) -> CandidateRecord:
    evidence_ids = tuple(dict.fromkeys(str(x) for x in source_evidence_ids if str(x)))
    if not evidence_ids:
        raise ValueError("autonomous invention requires durable source evidence")
    missing = tuple(eid for eid in evidence_ids if not _evidence_exists(store, eid))
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
    if not _evidence_exists(store, evidence_id):
        raise StateIntegrityError(f"promotion evidence missing: {evidence_id}")
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
