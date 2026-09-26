"""Immutable evidence identity for governed research packages."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json


@dataclass(frozen=True, slots=True)
class EvidenceIdentity:
    candidate_fingerprint: str
    dataset_sha256: str
    code_revision: str
    config_fingerprint: str
    policy_version: str
    execution_realism: str
    sha256: str


def _valid_sha256(value: str) -> bool:
    text = value.strip().lower()
    return len(text) == 64 and all(ch in "0123456789abcdef" for ch in text)


def _identity_values(
    *,
    candidate_fingerprint: str,
    dataset_sha256: str,
    code_revision: str,
    config_fingerprint: str,
    policy_version: str,
    execution_realism: str,
) -> dict[str, str]:
    values = {
        "candidate_fingerprint": candidate_fingerprint.strip().lower(),
        "dataset_sha256": dataset_sha256.strip().lower(),
        "code_revision": code_revision.strip(),
        "config_fingerprint": config_fingerprint.strip(),
        "policy_version": policy_version.strip(),
        "execution_realism": execution_realism.strip(),
    }
    if any(not value for value in values.values()):
        raise ValueError("all evidence identity fields are required")
    if not _valid_sha256(values["candidate_fingerprint"]):
        raise ValueError("candidate_fingerprint must be a SHA-256 hex digest")
    if not _valid_sha256(values["dataset_sha256"]):
        raise ValueError("dataset_sha256 must be a SHA-256 hex digest")
    return values


def _digest(values: dict[str, str]) -> str:
    canonical = json.dumps(values, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def build_evidence_identity(
    *,
    candidate_fingerprint: str,
    dataset_sha256: str,
    code_revision: str,
    config_fingerprint: str,
    policy_version: str,
    execution_realism: str,
) -> EvidenceIdentity:
    values = _identity_values(
        candidate_fingerprint=candidate_fingerprint,
        dataset_sha256=dataset_sha256,
        code_revision=code_revision,
        config_fingerprint=config_fingerprint,
        policy_version=policy_version,
        execution_realism=execution_realism,
    )
    return EvidenceIdentity(**values, sha256=_digest(values))


def verify_evidence_identity(identity: EvidenceIdentity) -> bool:
    try:
        values = _identity_values(
            candidate_fingerprint=identity.candidate_fingerprint,
            dataset_sha256=identity.dataset_sha256,
            code_revision=identity.code_revision,
            config_fingerprint=identity.config_fingerprint,
            policy_version=identity.policy_version,
            execution_realism=identity.execution_realism,
        )
    except ValueError:
        return False
    return _digest(values) == identity.sha256.lower()


def identity_payload(identity: EvidenceIdentity) -> dict[str, str]:
    if not verify_evidence_identity(identity):
        raise ValueError("evidence identity integrity check failed")
    return {str(key): str(value) for key, value in asdict(identity).items()}
