"""Write-new immutable research evidence packages.

Packages contain research evidence only and carry zero broker authority. Existing
package directories are never overwritten so a later run cannot silently mutate
an earlier holdout/stress/shadow result.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .evidence import EvidenceIdentity, build_evidence_identity, identity_payload, verify_evidence_identity


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2, allow_nan=False, ensure_ascii=True) + "\n").encode("utf-8")


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _plain(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return value


def write_evidence_package(
    root: str | Path,
    *,
    package_id: str,
    evidence: EvidenceIdentity,
    metrics: Mapping[str, Any] | Any,
    limitations: tuple[str, ...] = (),
) -> Path:
    if not package_id.strip() or any(ch in package_id for ch in ("/", "\\", "..")):
        raise ValueError("package_id must be a simple non-empty name")
    if not verify_evidence_identity(evidence):
        raise ValueError("evidence identity integrity check failed")
    target = Path(root) / package_id
    target.mkdir(parents=True, exist_ok=False)

    evidence_payload = identity_payload(evidence)
    metrics_payload = _plain(metrics)
    if not isinstance(metrics_payload, dict):
        raise TypeError("metrics must be a mapping or dataclass")

    evidence_bytes = _json_bytes(evidence_payload)
    metrics_bytes = _json_bytes(metrics_payload)
    (target / "evidence_manifest.json").write_bytes(evidence_bytes)
    (target / "metrics.json").write_bytes(metrics_bytes)

    manifest = {
        "package_id": package_id,
        "evidence_sha256": evidence.sha256,
        "files": {
            "evidence_manifest.json": _hash(evidence_bytes),
            "metrics.json": _hash(metrics_bytes),
        },
        "limitations": list(limitations),
        "broker_authority": "NONE",
    }
    (target / "package_manifest.json").write_bytes(_json_bytes(manifest))
    return target


def verify_evidence_package(path: str | Path) -> bool:
    target = Path(path)
    try:
        manifest = json.loads((target / "package_manifest.json").read_text(encoding="utf-8"))
        if manifest.get("broker_authority") != "NONE":
            return False
        expected = manifest["files"]
        for name, digest in expected.items():
            data = (target / name).read_bytes()
            if _hash(data) != digest:
                return False
        evidence = json.loads((target / "evidence_manifest.json").read_text(encoding="utf-8"))
        rebuilt = build_evidence_identity(
            candidate_fingerprint=str(evidence["candidate_fingerprint"]),
            dataset_sha256=str(evidence["dataset_sha256"]),
            code_revision=str(evidence["code_revision"]),
            config_fingerprint=str(evidence["config_fingerprint"]),
            policy_version=str(evidence["policy_version"]),
            execution_realism=str(evidence["execution_realism"]),
        )
        return (
            str(evidence.get("sha256", "")).lower() == rebuilt.sha256
            and str(manifest.get("evidence_sha256", "")).lower() == rebuilt.sha256
        )
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False
