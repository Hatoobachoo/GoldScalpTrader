"""One-position production-capacity replay helpers.

Shadow hypotheses never consume the real production slot. Active-execution
candidates are accepted chronologically only when the prior accepted position
has already closed. This preserves the documented 0/1 production-capacity rule
without pretending counterfactual shadow P/L is broker P/L.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from gold_scalp_trader.domain.enums import StrategyMode


@dataclass(frozen=True, slots=True)
class ReplayCandidate:
    episode_id: str
    entry_time: datetime
    exit_time: datetime
    mode: StrategyMode = StrategyMode.ACTIVE_EXECUTION

    def __post_init__(self) -> None:
        if not self.episode_id.strip():
            raise ValueError("episode_id is required")
        for name, value in (("entry_time", self.entry_time), ("exit_time", self.exit_time)):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{name} must be timezone-aware")
        if self.exit_time <= self.entry_time:
            raise ValueError("exit_time must be after entry_time")


@dataclass(frozen=True, slots=True)
class CapacityResult:
    episode_id: str
    mode: StrategyMode
    accepted_for_production: bool
    reason: str


def apply_single_position_capacity(candidates: Iterable[ReplayCandidate]) -> tuple[CapacityResult, ...]:
    """Apply the documented one independently-risk-bearing Gold slot.

    Shadow candidates remain valid counterfactual observations but do not occupy
    or wait for the live slot. Active candidates overlapping an already accepted
    production trade are recorded as capacity-suppressed rather than deleted.
    """
    ordered = sorted(tuple(candidates), key=lambda c: (c.entry_time, c.episode_id))
    active_until: datetime | None = None
    out: list[CapacityResult] = []
    for candidate in ordered:
        if candidate.mode is StrategyMode.SHADOW_ONLY:
            out.append(CapacityResult(candidate.episode_id, candidate.mode, False, "SHADOW_COUNTERFACTUAL_NO_PRODUCTION_SLOT"))
            continue
        if candidate.mode is not StrategyMode.ACTIVE_EXECUTION:
            out.append(CapacityResult(candidate.episode_id, candidate.mode, False, "RESEARCH_ONLY_NO_PRODUCTION_SLOT"))
            continue
        if active_until is not None and candidate.entry_time < active_until:
            out.append(CapacityResult(candidate.episode_id, candidate.mode, False, "POSITION_CAPACITY_BLOCKED"))
            continue
        active_until = candidate.exit_time
        out.append(CapacityResult(candidate.episode_id, candidate.mode, True, "PRODUCTION_SLOT_ACCEPTED"))
    return tuple(out)
