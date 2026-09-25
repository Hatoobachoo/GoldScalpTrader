"""Persistent analytical Opportunity identity and lifecycle primitives."""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from gold_scalp_trader.domain.enums import Direction, OpportunityState, StrategyFamily
from gold_scalp_trader.domain.ids import new_id

from .fusion import DecisionBoard


@dataclass(frozen=True, slots=True)
class Opportunity:
    opportunity_id: str
    episode_id: str
    family: StrategyFamily
    direction: Direction
    created_at: datetime
    updated_at: datetime
    state: OpportunityState
    source_event_ids: tuple[str, ...]
    score: float
    reasons: tuple[str, ...]
    policy_version: str | None = None
    m5_event_time: datetime | None = None
    preferred_m1_profile: str | None = None
    coverage: float | None = None
    last_timing_event: datetime | None = None


def create(board: DecisionBoard, as_of: datetime) -> Opportunity | None:
    candidate = board.candidate
    if candidate is None or board.recommendation != "ARM" or board.leading_direction is Direction.NONE:
        return None
    return Opportunity(
        opportunity_id=str(new_id("OPP")),
        episode_id=str(new_id("EP")),
        family=candidate.family,
        direction=board.leading_direction,
        created_at=as_of,
        updated_at=as_of,
        state=OpportunityState.ARMED,
        source_event_ids=candidate.source_event_ids,
        score=board.leading_score or candidate.score,
        reasons=candidate.reasons,
        policy_version=candidate.policy_version,
        m5_event_time=candidate.m5_event_time,
        preferred_m1_profile=candidate.preferred_m1_profile,
        coverage=board.coverage or candidate.coverage,
    )


def transition(
    opportunity: Opportunity,
    state: OpportunityState,
    as_of: datetime,
    reason: str,
    *,
    timing_event: datetime | None = None,
) -> Opportunity:
    legal = {
        OpportunityState.ARMED: {
            OpportunityState.WAITING,
            OpportunityState.READY,
            OpportunityState.MISSED,
            OpportunityState.INVALIDATED,
        },
        OpportunityState.WAITING: {
            OpportunityState.READY,
            OpportunityState.MISSED,
            OpportunityState.INVALIDATED,
        },
        OpportunityState.READY: {
            OpportunityState.WAITING,
            OpportunityState.TRIGGERED,
            OpportunityState.MISSED,
            OpportunityState.INVALIDATED,
        },
    }
    if opportunity.state in {
        OpportunityState.MISSED,
        OpportunityState.INVALIDATED,
        OpportunityState.TRIGGERED,
    }:
        raise ValueError("terminal Opportunity identity cannot transition")
    if state not in legal.get(opportunity.state, set()):
        raise ValueError(f"illegal opportunity transition {opportunity.state}->{state}")
    return replace(
        opportunity,
        state=state,
        updated_at=as_of,
        reasons=(*opportunity.reasons, reason),
        last_timing_event=timing_event or opportunity.last_timing_event,
    )
