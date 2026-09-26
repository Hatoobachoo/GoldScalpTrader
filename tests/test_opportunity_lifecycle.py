from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from gold_scalp_trader.app.cycle import CycleResult
from gold_scalp_trader.app.opportunity_lifecycle import load, mark_triggered, stabilize_cycle
from gold_scalp_trader.decisions.opportunity import Opportunity
from gold_scalp_trader.domain.enums import Direction, OpportunityState, StrategyFamily, TimingOutcome
from gold_scalp_trader.persistence.store import StateStore

UTC = timezone.utc


def _opp(when: datetime, *, oid="OPP-RANDOM", eid="EP-RANDOM"):
    return Opportunity(
        oid,
        eid,
        StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
        Direction.BUY,
        when,
        when,
        OpportunityState.ARMED,
        ("M5:BOS:42", "M5:RETEST:43"),
        .8,
        ("qualified",),
        policy_version="v1",
        m5_event_time=when - timedelta(minutes=5),
        preferred_m1_profile="RETEST",
        coverage=.9,
    )


def _cycle(when: datetime, opportunity: Opportunity, outcome: TimingOutcome):
    timing = SimpleNamespace(outcome=outcome, trigger_time=when)
    market = SimpleNamespace(captured_at=when)
    return CycleResult(
        intelligence=SimpleNamespace(market=market),
        registry=SimpleNamespace(),
        isolation=SimpleNamespace(),
        board=SimpleNamespace(),
        opportunity=opportunity,
        timing=timing,
        trade_plan=None,
        quality=None,
        risk=None,
        live_action="WAIT",
        status="TIMING",
        reason="timing",
    )


def test_same_causal_opportunity_keeps_identity_across_wait_ready_and_restart():
    store = StateStore()
    when = datetime(2026, 9, 28, 10, 0, tzinfo=UTC)
    first = stabilize_cycle(store, "scope", _cycle(when, _opp(when), TimingOutcome.WAIT))
    assert first.opportunity.state is OpportunityState.WAITING
    oid = first.opportunity.opportunity_id
    eid = first.opportunity.episode_id

    second_fresh = _opp(when + timedelta(minutes=1), oid="NEW-RANDOM", eid="NEW-EP")
    second_fresh = Opportunity(
        second_fresh.opportunity_id,
        second_fresh.episode_id,
        second_fresh.family,
        second_fresh.direction,
        second_fresh.created_at,
        second_fresh.updated_at,
        second_fresh.state,
        second_fresh.source_event_ids,
        second_fresh.score,
        second_fresh.reasons,
        policy_version="v1",
        m5_event_time=when - timedelta(minutes=5),
        preferred_m1_profile="RETEST",
        coverage=.9,
    )
    second = stabilize_cycle(
        store,
        "scope",
        _cycle(when + timedelta(minutes=1), second_fresh, TimingOutcome.READY_BUY),
    )
    assert second.opportunity.opportunity_id == oid
    assert second.opportunity.episode_id == eid
    assert second.opportunity.state is OpportunityState.READY
    assert load(store, "scope").opportunity_id == oid


def test_triggered_same_causal_episode_cannot_rearm_from_new_random_ids():
    store = StateStore()
    when = datetime(2026, 9, 28, 10, 0, tzinfo=UTC)
    ready = stabilize_cycle(store, "scope", _cycle(when, _opp(when), TimingOutcome.READY_BUY))
    triggered = mark_triggered(store, "scope", ready)
    assert triggered.opportunity.state is OpportunityState.TRIGGERED

    fresh_random = _opp(when + timedelta(minutes=1), oid="OTHER", eid="OTHER-EP")
    fresh_random = Opportunity(
        fresh_random.opportunity_id,
        fresh_random.episode_id,
        fresh_random.family,
        fresh_random.direction,
        fresh_random.created_at,
        fresh_random.updated_at,
        fresh_random.state,
        fresh_random.source_event_ids,
        fresh_random.score,
        fresh_random.reasons,
        policy_version="v1",
        m5_event_time=when - timedelta(minutes=5),
        preferred_m1_profile="RETEST",
        coverage=.9,
    )
    blocked = stabilize_cycle(
        store,
        "scope",
        _cycle(when + timedelta(minutes=1), fresh_random, TimingOutcome.READY_BUY),
    )
    assert blocked.opportunity.state is OpportunityState.TRIGGERED
    assert blocked.trade_plan is None
    assert blocked.risk is None
    assert "AWAIT_FRESH_CAUSAL_SETUP" in blocked.reason
