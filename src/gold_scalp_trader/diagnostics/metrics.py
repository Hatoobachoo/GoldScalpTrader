"""Small deterministic metrics primitives."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StageTiming:
    stage: str
    elapsed_ms: float

    def __post_init__(self) -> None:
        if self.elapsed_ms < 0:
            raise ValueError("elapsed_ms cannot be negative")
