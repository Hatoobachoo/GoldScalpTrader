"""Shared immutable analytical DTOs.

The trading documents require family evidence and BUY/SELL cases to remain
explicit rather than collapsing a strategy into one opaque score. These DTOs
carry the minimum lineage needed by setup detection, fusion, timing, dashboard
and research without granting broker authority.
"""
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
class DirectionalCase:
    """One independent directional case inside one strategy family.

    `score` is an explanatory relative quality value, never a probability and
    never a monetary-Risk input. `required_complete` distinguishes a weak case
    from a case that cannot qualify because family-defining evidence is absent.
    """

    direction: Direction
    score: float
    coverage: float
    required_complete: bool
    reasons: tuple[str, ...]
    evidence: tuple[Evidence, ...] = ()

    def __post_init__(self) -> None:
        if self.direction not in {Direction.BUY, Direction.SELL}:
            raise ValueError("DirectionalCase direction must be BUY or SELL")
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("DirectionalCase score must be in [0, 1]")
        if not 0.0 <= self.coverage <= 1.0:
            raise ValueError("DirectionalCase coverage must be in [0, 1]")


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
    # Backward-compatible extensions required by the frozen strategy/fusion
    # contracts. Older fixtures may omit them; live detectors populate them.
    buy_case: DirectionalCase | None = None
    sell_case: DirectionalCase | None = None
    required_evidence_complete: bool | None = None
    m5_event_time: datetime | None = None
    location_quality: str | None = None
    target_room: float | None = None
    preferred_m1_profile: str | None = None
    correlation_ids: tuple[str, ...] = ()
    policy_version: str | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("SetupCandidate score must be in [0, 1]")
        if not 0.0 <= self.coverage <= 1.0:
            raise ValueError("SetupCandidate coverage must be in [0, 1]")
        if self.qualification is SetupQualification.QUALIFIED_BUY and self.direction is not Direction.BUY:
            raise ValueError("QUALIFIED_BUY candidate must have BUY direction")
        if self.qualification is SetupQualification.QUALIFIED_SELL and self.direction is not Direction.SELL:
            raise ValueError("QUALIFIED_SELL candidate must have SELL direction")

    @property
    def qualified(self) -> bool:
        return self.qualification in {
            SetupQualification.QUALIFIED_BUY,
            SetupQualification.QUALIFIED_SELL,
        }
