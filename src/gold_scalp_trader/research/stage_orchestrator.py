"""Stage-specific research proof issuance for governed candidate promotion.

A candidate cannot advance from an arbitrary caller-supplied artifact hash.  A
stage proof must be an immutable verified evidence package whose candidate
fingerprint, target stage and required structural checks all match.  This module
still grants zero runtime/broker authority and does not invent profitability
thresholds that are not present in frozen policy.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore

from .candidate_registry import _record_verified_stage_evidence, load
from .evidence import EvidenceIdentity, verify_evidence_identity
from .packages import verify_evidence_package, write_evidence_package
from .promotion import PromotionStage

ISSUER = "VERIFIED_STAGE_PACKAGE_V1"

_REQUIRED_CHECKS: dict[PromotionStage, tuple[str, ...]] = {
    PromotionStage.RESEARCHING: ("source_evidence_bound",),
    PromotionStage.VALIDATED: ("chronological_replay_complete", "no_lookahead_verified"),
    PromotionStage.LOCKED: ("candidate_fingerprint_locked", "policy_version_locked"),
    PromotionStage.HOLDOUT_PASSED: ("one_shot_holdout_consumed", "holdout_identity_match"),
    PromotionStage.STRESS_PASSED: ("stress_scenarios_complete", "execution_costs_explicit"),
    PromotionStage.SHADOW: ("shadow_only_no_broker_authority", "causal_shadow_outcomes_present"),
    PromotionStage.DEMO_CANDIDATE: ("demo_only_evidence", "verified_close_evidence"),
    PromotionStage.APPROVAL_REQUIRED: ("limitations_recorded", "rollback_target_identified"),
    PromotionStage.PRODUCTION: ("operator_approval_recorded", "rollback_target_verified"),
}


def required_checks(stage: PromotionStage) -> tuple[str, ...]:
    try:
        return _REQUIRED_CHECKS[stage]
    except KeyError as exc:
        raise ValueError(f"no stage-proof protocol for {stage.value}") from exc


def write_stage_proof_package(
    root: str | Path,
    *,
    package_id: str,
    stage: PromotionStage,
    evidence: EvidenceIdentity,
    checks: Mapping[str, bool],
    observations: Mapping[str, object] | None = None,
    limitations: tuple[str, ...] = (),
) -> Path:
    """Write one immutable stage proof only when required checks are satisfied."""
    if not verify_evidence_identity(evidence):
        raise ValueError("evidence identity integrity check failed")
    required = required_checks(stage)
    missing = tuple(name for name in required if checks.get(name) is not True)
    if missing:
        raise ValueError(f"stage proof missing/failed required checks: {missing}")
    metrics = {
        "proof_protocol": ISSUER,
        "target_stage": stage.value,
        "candidate_fingerprint": evidence.candidate_fingerprint,
        "checks": {str(k): bool(v) for k, v in sorted(checks.items())},
        "observations": dict(observations or {}),
        "passed": True,
    }
    return write_evidence_package(
        root,
        package_id=package_id,
        evidence=evidence,
        metrics=metrics,
        limitations=limitations,
    )


def _load_verified_package(path: Path) -> tuple[dict, dict, bytes]:
    if not verify_evidence_package(path):
        raise StateIntegrityError("stage evidence package integrity verification failed")
    try:
        evidence = json.loads((path / "evidence_manifest.json").read_text(encoding="utf-8"))
        metrics = json.loads((path / "metrics.json").read_text(encoding="utf-8"))
        manifest_bytes = (path / "package_manifest.json").read_bytes()
    except (OSError, json.JSONDecodeError) as exc:
        raise StateIntegrityError("stage evidence package cannot be read") from exc
    if not isinstance(evidence, dict) or not isinstance(metrics, dict):
        raise StateIntegrityError("stage evidence package payload malformed")
    return evidence, metrics, manifest_bytes


def issue_stage_evidence(
    store: StateStore,
    candidate_id: str,
    target_stage: PromotionStage,
    *,
    evidence_id: str,
    package_path: str | Path,
) :
    """Verify an immutable package and issue typed candidate-stage evidence."""
    current = load(store, candidate_id)
    if current is None:
        raise StateIntegrityError(f"unknown candidate {candidate_id}")
    evidence_raw, metrics, manifest_bytes = _load_verified_package(Path(package_path))
    if metrics.get("proof_protocol") != ISSUER:
        raise StateIntegrityError("stage package was not produced by verified stage protocol")
    if metrics.get("target_stage") != target_stage.value:
        raise StateIntegrityError("stage package target mismatch")
    if metrics.get("candidate_fingerprint") != current.candidate.fingerprint:
        raise StateIntegrityError("stage package candidate fingerprint mismatch")
    if metrics.get("passed") is not True:
        raise StateIntegrityError("stage package is not PASS")
    checks = metrics.get("checks")
    if not isinstance(checks, dict):
        raise StateIntegrityError("stage package checks missing")
    missing = tuple(name for name in required_checks(target_stage) if checks.get(name) is not True)
    if missing:
        raise StateIntegrityError(f"stage package required checks failed: {missing}")

    try:
        identity = EvidenceIdentity(
            candidate_fingerprint=str(evidence_raw["candidate_fingerprint"]),
            dataset_sha256=str(evidence_raw["dataset_sha256"]),
            code_revision=str(evidence_raw["code_revision"]),
            config_fingerprint=str(evidence_raw["config_fingerprint"]),
            policy_version=str(evidence_raw["policy_version"]),
            execution_realism=str(evidence_raw["execution_realism"]),
            sha256=str(evidence_raw["sha256"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise StateIntegrityError("stage package evidence identity malformed") from exc
    if not verify_evidence_identity(identity):
        raise StateIntegrityError("stage package evidence identity mismatch")
    if identity.candidate_fingerprint != current.candidate.fingerprint:
        raise StateIntegrityError("stage package evidence belongs to different candidate")

    return _record_verified_stage_evidence(
        store,
        candidate_id,
        target_stage,
        evidence_id=evidence_id,
        identity=identity,
        artifact_sha256=sha256(manifest_bytes).hexdigest(),
        package_manifest_sha256=sha256(manifest_bytes).hexdigest(),
        limitations=tuple(str(x) for x in json.loads((Path(package_path) / "package_manifest.json").read_text(encoding="utf-8")).get("limitations", ())),
        issuer=ISSUER,
    )


__all__ = ["ISSUER", "issue_stage_evidence", "required_checks", "write_stage_proof_package"]
