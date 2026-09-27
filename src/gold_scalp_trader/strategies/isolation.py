"""Production strategy routing plus research/shadow family isolation.

Production does not choose a family by score and does not depend on a manually
configured ACTIVE_STRATEGY_FAMILY.  All six families prove their own causal
setup first.  The production router then resolves the qualified structural
families in deterministic semantic priority, while every non-routed family
remains SHADOW_ONLY for attribution and research.

A legacy explicit-family ``apply`` seam is retained for isolated research/tests;
it is not used by the canonical production cycle.
"""
from __future__ import annotations

from dataclasses import dataclass

from gold_scalp_trader.domain.enums import Direction, StrategyFamily, StrategyMode
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
    candidates: tuple[IsolatedCandidate, ...]
    reason: str


# Structural/event semantics outrank generic continuation.  This mirrors the
# mature Swing production principle: classifier/structure first; family score is
# explanatory evidence, never the production family selector.
_PRODUCTION_PRIORITY: tuple[StrategyFamily, ...] = (
    StrategyFamily.FAILED_BREAKOUT_REVERSAL,
    StrategyFamily.LIQUIDITY_SWEEP_REVERSAL,
    StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
    StrategyFamily.COMPRESSION_EXPANSION,
    StrategyFamily.BREAKOUT_EXPANSION,
    StrategyFamily.TREND_PULLBACK_CONTINUATION,
)


def route(registry: SetupRegistry) -> IsolationResult:
    """Route exactly one qualified production family or fail closed.

    Scores never decide the winner. If qualified structural families disagree
    on direction, production declines to choose and all families remain shadow.
    """

    qualified = tuple(candidate for candidate in registry.candidates if candidate.qualified)
    if not qualified:
        return IsolationResult(
            active_family=None,
            live_candidate=None,
            candidates=tuple(IsolatedCandidate(c, StrategyMode.SHADOW_ONLY) for c in registry.candidates),
            reason="NO_QUALIFIED_STRUCTURAL_SETUP",
        )

    directions = {candidate.direction for candidate in qualified if candidate.direction is not Direction.NONE}
    if len(directions) != 1:
        return IsolationResult(
            active_family=None,
            live_candidate=None,
            candidates=tuple(IsolatedCandidate(c, StrategyMode.SHADOW_ONLY) for c in registry.candidates),
            reason="OPPOSING_QUALIFIED_STRUCTURAL_SETUPS",
        )

    by_family = {candidate.family: candidate for candidate in qualified}
    live = next((by_family[family] for family in _PRODUCTION_PRIORITY if family in by_family), None)
    if live is None:  # defensive: every current StrategyFamily is in the priority table
        return IsolationResult(
            active_family=None,
            live_candidate=None,
            candidates=tuple(IsolatedCandidate(c, StrategyMode.SHADOW_ONLY) for c in registry.candidates),
            reason="QUALIFIED_FAMILY_UNROUTABLE",
        )

    isolated = tuple(
        IsolatedCandidate(
            candidate,
            StrategyMode.ACTIVE_EXECUTION if candidate.candidate_id == live.candidate_id else StrategyMode.SHADOW_ONLY,
        )
        for candidate in registry.candidates
    )
    return IsolationResult(
        active_family=live.family,
        live_candidate=live,
        candidates=isolated,
        reason="ROUTED_FAMILY_SETUP_QUALIFIED",
    )


def apply(registry: SetupRegistry, active_family: StrategyFamily | None) -> IsolationResult:
    """Legacy explicit-family isolation for research/compatibility only."""

    isolated = tuple(
        IsolatedCandidate(
            candidate,
            StrategyMode.ACTIVE_EXECUTION
            if active_family is not None and candidate.family is active_family
            else StrategyMode.SHADOW_ONLY,
        )
        for candidate in registry.candidates
    )
    live = next(
        (
            item.candidate
            for item in isolated
            if item.mode is StrategyMode.ACTIVE_EXECUTION and item.candidate.qualified
        ),
        None,
    )
    reason = (
        "ACTIVE_STRATEGY_FAMILY_UNSET"
        if active_family is None
        else "ACTIVE_FAMILY_SETUP_NOT_PRESENT"
        if live is None
        else "ACTIVE_FAMILY_SETUP_QUALIFIED"
    )
    return IsolationResult(active_family, live, isolated, reason)
