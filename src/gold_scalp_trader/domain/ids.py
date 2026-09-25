"""Stable typed identifiers used by lifecycle records."""
from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class EntityId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("identifier cannot be empty")

    def __str__(self) -> str:
        return self.value


def new_id(prefix: str) -> EntityId:
    clean = prefix.strip().upper().replace(" ", "_")
    if not clean:
        raise ValueError("prefix cannot be empty")
    return EntityId(f"{clean}-{uuid4().hex}")
