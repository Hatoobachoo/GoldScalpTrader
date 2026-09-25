"""Market-first setup registry and immutable policy attribution."""
from __future__ import annotations

from dataclasses import dataclass, replace

from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot

from .floor import StrategyPolicy, detect_all


@dataclass(frozen=True, slots=True)
class SetupRegistry:
    candidates: tuple[SetupCandidate, ...]

    @property
    def qualified(self) -> tuple[SetupCandidate, ...]:
        return tuple(candidate for candidate in self.candidates if candidate.qualified)

    @property
    def has_any(self) -> bool:
        return bool(self.qualified)


def detect(snapshot: IntelligenceSnapshot, policy: StrategyPolicy | None = None) -> SetupRegistry:
    """Detect market setups without consulting active-family live eligibility."""

    resolved = policy or StrategyPolicy()
    candidates = tuple(
        replace(candidate, policy_version=resolved.version)
        if candidate.policy_version is None
        else candidate
        for candidate in detect_all(snapshot, resolved)
    )
    return SetupRegistry(candidates)
