"""Create a secret-clean local recovery package around a verified checkpoint."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib, json, zipfile
from pathlib import Path
from gold_scalp_trader.security.financial_secrets import contains_probable_secret

@dataclass(frozen=True, slots=True)
class RecoveryPackage:
    checkpoint_path: str
    source_revision: str | None
    secret_scan_passed: bool
    package_path: str | None = None
    sha256: str | None = None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_recovery_package(*, checkpoint_path: str | Path, output_zip: str | Path, source_revision: str | None = None) -> RecoveryPackage:
    checkpoint = Path(checkpoint_path)
    if not checkpoint.is_file():
        raise FileNotFoundError(checkpoint)
    checkpoint_text = checkpoint.read_text(encoding="utf-8")
    if contains_probable_secret(checkpoint_text):
        raise ValueError("checkpoint contains probable authority-bearing secret; package not created")
    manifest = {
        "schema": 1,
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "checkpoint_file": checkpoint.name,
        "checkpoint_sha256": _sha256(checkpoint),
        "source_revision": source_revision,
        "credentials_included": False,
        "restore_requires_fresh_broker_reconciliation": True,
    }
    out = Path(output_zip)
    out.parent.mkdir(parents=True, exist_ok=True)
    temp = out.with_suffix(out.suffix + ".tmp")
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(checkpoint, arcname=checkpoint.name)
        archive.writestr("recovery_manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
    temp.replace(out)
    return RecoveryPackage(str(checkpoint), source_revision, True, str(out), _sha256(out))
