"""Crash-safe active Opportunity identity for guarded runtime.

This layer does not create setups or broker authority. It stabilizes the
identity/state of an already-qualified M5 Opportunity across repeated runtime
cycles and restart, and prevents terminal same-causal episodes from silently
re-arming until a genuinely fresh causal setup appears.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from gold_scalp_trader.app.cycle import CycleResult
from gold_scalp_trader.decisions.opportunity import Opportunity, transition
from gold_scalp_trader.domain.enums import OpportunityState, TimingOutcome
from gold_scalp_trader.persistence.store import StateStore

NS = "active_opportunity"
HISTORY_NS = "opportunity_lifecycle"


def _payload(opportunity: Opportunity) -> dict[str, object]:
    return {
        "opportunity_id": opportunity.opportunity_id,
        "episode_id": opportunity.episode_id,
        "family": opportunity.family.value,
        "direction": opportunity.direction.value,
        "created_at": opportunity.created_at.isoformat(),
        "updated_at": opportunity.updated_at.isoformat(),
        "state": opportunity.state.value,
        "source_event_ids": list(opportunity.source_event_ids),
        "score": opportunity.score,
        "reasons": list(opportunity.reasons),
        "policy_version": opportunity.policy_version,
        "m5_event_time": None if opportunity.m5_event_time is None else opportunity.m5_event_time.isoformat(),
        "preferred_m1_profile": opportunity.preferred_m1_profile,
        "coverage": opportunity.coverage,
        "last_timing_event": None if opportunity.last_timing_event is None else opportunity.last_timing_event.isoformat(),
    }


def _dt(value) -> datetime | None:
    return None if value in (None, "") else datetime.fromisoformat(str(value))


def _from_payload(payload: dict) -> Opportunity:
    from gold_scalp_trader.domain.enums import Direction, StrategyFamily

    return Opportunity(
        opportunity_id=str(payload["opportunity_id"]),
        episode_id=str(payload["episode_id"]),
        family=StrategyFamily(str(payload["family"])),
        direction=Direction(str(payload["direction"])),
        created_at=datetime.fromisoformat(str(payload["created_at"])),
        updated_at=datetime.fromisoformat(str(payload["updated_at"])),
        state=OpportunityState(str(payload["state"])),
        source_event_ids=tuple(str(x) for x in payload.get("source_event_ids", ())),
        score=float(payload["score"]),
        reasons=tuple(str(x) for x in payload.get("reasons", ())),
        policy_version=None if payload.get("policy_version") is None else str(payload["policy_version"]),
        m5_event_time=_dt(payload.get("m5_event_time")),
        preferred_m1_profile=None if payload.get("preferred_m1_profile") is None else str(payload["preferred_m1_profile"]),
        coverage=None if payload.get("coverage") is None else float(payload["coverage"]),
        last_timing_event=_dt(payload.get("last_timing_event")),
    )


def load(store: StateStore, scope: str) -> Opportunity | None:
    record = store.get(NS, scope)
    return None if record is None else _from_payload(record.payload)


def save(store: StateStore, scope: str, opportunity: Opportunity) -> None:
    store.put(NS, scope, _payload(opportunity))
    store.append_event(
        HISTORY_NS,
        f"{opportunity.opportunity_id}:{opportunity.state.value}:{opportunity.updated_at.isoformat()}",
        _payload(opportunity),
    )


def _causal_identity(opportunity: Opportunity) -> tuple[object, ...]:
    return (
        opportunity.family,
        opportunity.direction,
        tuple(sorted(opportunity.source_event_ids)),
        opportunity.policy_version,
        opportunity.m5_event_time,
    )


def _state_for_cycle(cycle: CycleResult) -> OpportunityState:
    timing = cycle.timing
    if timing is None:
        return OpportunityState.ARMED
    if timing.outcome is TimingOutcome.WAIT:
        return OpportunityState.WAITING
    if timing.outcome in {TimingOutcome.READY_BUY, TimingOutcome.READY_SELL}:
        return OpportunityState.READY
    if timing.outcome is TimingOutcome.MISSED:
        return OpportunityState.MISSED
    return OpportunityState.INVALIDATED


def stabilize_cycle(store: StateStore, scope: str, cycle: CycleResult) -> CycleResult:
    fresh = cycle.opportunity
    current = load(store, scope)

    if fresh is None:
        if current is not None and current.state not in {
            OpportunityState.TRIGGERED,
            OpportunityState.MISSED,
            OpportunityState.INVALIDATED,
        }:
            terminal = transition(current, OpportunityState.INVALIDATED, cycle.intelligence.market.captured_at, "ACTIVE_M5_SETUP_NO_LONGER_QUALIFIED")
            save(store, scope, terminal)
        return cycle

    same = current is not None and _causal_identity(current) == _causal_identity(fresh)
    if same and current.state in {
        OpportunityState.TRIGGERED,
        OpportunityState.MISSED,
        OpportunityState.INVALIDATED,
    }:
        # Same causal episode is terminal. A new random in-memory ID must never
        # re-arm it; only a fresh causal M5 identity may create a new episode.
        return replace(
            cycle,
            opportunity=current,
            trade_plan=None,
            quality=None,
            risk=None,
            live_action="WAIT",
            status="OPPORTUNITY",
            reason=f"OPPORTUNITY_{current.state.value}_AWAIT_FRESH_CAUSAL_SETUP",
        )

    if same:
        base = replace(
            fresh,
            opportunity_id=current.opportunity_id,
            episode_id=current.episode_id,
            created_at=current.created_at,
            state=current.state,
            reasons=current.reasons,
            last_timing_event=current.last_timing_event,
        )
    else:
        if current is not None and current.state not in {
            OpportunityState.TRIGGERED,
            OpportunityState.MISSED,
            OpportunityState.INVALIDATED,
        }:
            old = transition(current, OpportunityState.INVALIDATED, cycle.intelligence.market.captured_at, "SUPERSEDED_BY_FRESH_CAUSAL_SETUP")
            save(store, scope, old)
        base = fresh

    target = _state_for_cycle(cycle)
    if base.state is not target:
        if base.state is OpportunityState.ARMED and target is OpportunityState.ARMED:
            updated = base
        else:
            updated = transition(
                base,
                target,
                cycle.intelligence.market.captured_at,
                f"TIMING_{cycle.timing.outcome.value}" if cycle.timing is not None else "M5_ARMED",
                timing_event=None if cycle.timing is None else cycle.timing.trigger_time,
            )
    else:
        updated = replace(base, updated_at=cycle.intelligence.market.captured_at)
    save(store, scope, updated)

    plan = cycle.trade_plan
    if plan is not None and plan.opportunity_id != updated.opportunity_id:
        plan = replace(plan, opportunity_id=updated.opportunity_id)
    return replace(cycle, opportunity=updated, trade_plan=plan)


def mark_triggered(store: StateStore, scope: str, cycle: CycleResult) -> CycleResult:
    opportunity = cycle.opportunity
    if opportunity is None:
        return cycle
    current = load(store, scope) or opportunity
    if current.state is OpportunityState.TRIGGERED:
        return replace(cycle, opportunity=current)
    if current.state is not OpportunityState.READY:
        raise ValueError("only READY Opportunity may become TRIGGERED")
    triggered = transition(
        current,
        OpportunityState.TRIGGERED,
        cycle.intelligence.market.captured_at,
        "IRREVERSIBLE_OPEN_SEND_CONSUMED",
        timing_event=None if cycle.timing is None else cycle.timing.trigger_time,
    )
    save(store, scope, triggered)
    return replace(cycle, opportunity=triggered)
