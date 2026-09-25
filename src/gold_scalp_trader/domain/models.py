"""Shared immutable analytical DTOs."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .enums import Direction, EvidenceRole, SetupQualification, StrategyFamily


@dataclass(frozen=True, slots=True)
class Evidence:
    code: str
    role: EvidenceRole
    value: float | str | bool | None
    source_id: str
    observed_at: datetime
    explanation: str = ""


@dataclass(frozen=True, slots=True)
class SetupCandidate:
    candidate_id: str
    family: StrategyFamily
    qualification: SetupQualification
    direction: Direction
    score: float
    coverage: float
    source_event_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    evidence: tuple[Evidence, ...] = ()

    @property
    def qualified(self) -> bool:
        return self.qualification in {
            SetupQualification.QUALIFIED_BUY,
            SetupQualification.QUALIFIED_SELL,
        }
