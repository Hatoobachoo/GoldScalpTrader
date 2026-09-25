"""Verified local runtime-backup helpers.

The canonical runtime artifact is a StateStore checkpoint, not a live SQLite
file copy and never a Git operation.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
from .checkpoint import export_checkpoint
from .store import StateStore

@dataclass(frozen=True, slots=True)
class BackupStatus:
    created_at: datetime
    path: str
    verified: bool
    sha256: str | None = None


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_verified_checkpoint_backup(store: StateStore, path: str | Path) -> BackupStatus:
    out = export_checkpoint(store, path)
    # Parse/verify by restoring to an isolated in-memory store before reporting success.
    from .checkpoint import restore_checkpoint
    probe = StateStore(":memory:")
    try:
        restore_checkpoint(out, probe)
        if not probe.integrity_check():
            raise RuntimeError("restored checkpoint failed SQLite integrity check")
    finally:
        probe.close()
    return BackupStatus(datetime.now(tz=timezone.utc), str(out), True, sha256_file(out))
