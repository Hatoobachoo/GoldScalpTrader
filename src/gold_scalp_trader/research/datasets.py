"""Portable research dataset identity and integrity helpers.

Research datasets are immutable evidence inputs.  This module deliberately has
no broker or production-policy authority.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True, slots=True)
class DatasetIdentity:
    source: str
    symbol: str
    version: str
    sha256: str
    files: tuple[str, ...] = ()


def _hash_files(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted((Path(p) for p in paths), key=lambda p: p.as_posix().lower()):
        if not path.is_file():
            raise FileNotFoundError(path)
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def build_dataset_identity(*, source: str, symbol: str, version: str, paths: Iterable[str | Path]) -> DatasetIdentity:
    file_paths = tuple(Path(p) for p in paths)
    if not source.strip() or not symbol.strip() or not version.strip():
        raise ValueError("source, symbol and version are required")
    if not file_paths:
        raise ValueError("at least one dataset file is required")
    return DatasetIdentity(source.strip(), symbol.strip(), version.strip(), _hash_files(file_paths), tuple(p.name for p in file_paths))


def verify_dataset_identity(identity: DatasetIdentity, paths: Iterable[str | Path]) -> bool:
    return _hash_files(tuple(Path(p) for p in paths)) == identity.sha256
