"""One-active/five-shadow strategy-isolation controller."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.enums import StrategyFamily,StrategyMode
from gold_scalp_trader.domain.models import SetupCandidate
from .setup_detector import SetupRegistry

@dataclass(frozen=True, slots=True)
class IsolatedCandidate:
    candidate: SetupCandidate
    mode: StrategyMode

@dataclass(frozen=True, slots=True)
class IsolationResult:
    active_family: StrategyFamily | None
    live_candidate: SetupCandidate | None
    candidates: tuple[IsolatedCandidate,...]
    reason: str

def apply(registry: SetupRegistry,active_family: StrategyFamily | None)->IsolationResult:
    isolated=tuple(IsolatedCandidate(c,StrategyMode.ACTIVE_EXECUTION if active_family is not None and c.family is active_family else StrategyMode.SHADOW_ONLY) for c in registry.candidates)
    live=next((x.candidate for x in isolated if x.mode is StrategyMode.ACTIVE_EXECUTION and x.candidate.qualified),None)
    reason="ACTIVE_STRATEGY_FAMILY_UNSET" if active_family is None else "ACTIVE_FAMILY_SETUP_NOT_PRESENT" if live is None else "ACTIVE_FAMILY_SETUP_QUALIFIED"
    return IsolationResult(active_family,live,isolated,reason)
