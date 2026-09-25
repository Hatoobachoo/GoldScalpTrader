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


def build_evidence_identity(
    *,
    candidate_fingerprint: str,
    dataset_sha256: str,
    code_revision: str,
    config_fingerprint: str,
    policy_version: str,
    execution_realism: str,
) -> EvidenceIdentity:
    values = {
        "candidate_fingerprint": candidate_fingerprint.strip(),
        "dataset_sha256": dataset_sha256.strip(),
        "code_revision": code_revision.strip(),
        "config_fingerprint": config_fingerprint.strip(),
        "policy_version": policy_version.strip(),
        "execution_realism": execution_realism.strip(),
    }
    if any(not value for value in values.values()):
        raise ValueError("all evidence identity fields are required")
    canonical = json.dumps(values, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    return EvidenceIdentity(**values, sha256=digest)


def identity_payload(identity: EvidenceIdentity) -> dict[str, str]:
    return {str(key): str(value) for key, value in asdict(identity).items()}
