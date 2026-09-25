"""Market-first setup registry."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot
from .floor import StrategyPolicy, detect_all

@dataclass(frozen=True, slots=True)
class SetupRegistry:
    candidates: tuple[SetupCandidate, ...]
    @property
    def qualified(self) -> tuple[SetupCandidate, ...]:
        return tuple(c for c in self.candidates if c.qualified)
    @property
    def has_any(self) -> bool:
        return bool(self.qualified)

def detect(snapshot: IntelligenceSnapshot, policy: StrategyPolicy | None=None) -> SetupRegistry:
    return SetupRegistry(detect_all(snapshot,policy))
