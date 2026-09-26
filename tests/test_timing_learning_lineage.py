from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

from gold_scalp_trader.domain.enums import Direction, StrategyFamily, TimingOutcome
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.timing_learning import (
    NS,
    episode_key,
    record_runtime_timing,
    summarize_timing_evidence,
)

UTC = timezone.utc


def _result(*, outcome=TimingOutcome.READY_BUY, live_action="ORDER_SENT", wrote=True):
    event_time = datetime(2026, 9, 25, 18, 30, tzinfo=UTC)
    trigger_time = datetime(2026, 9, 25, 18, 35, tzinfo=UTC)
    opportunity = SimpleNamespace(
        family=StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
        direction=Direction.BUY,
        source_event_ids=("M5:BOS:42", "M5:RETEST:43"),
        policy_version="active-v7",
        m5_event_time=event_time,
        preferred_m1_profile="BREAKOUT_RETEST_MICRO_HOLD",
        coverage=0.84,
    )
    timing = SimpleNamespace(
        outcome=outcome,
        reason="fresh M1 refinement supports the surviving M5 thesis",
        trigger_time=trigger_time,
        micro_extension_atr=0.24,
        m5_event_age_seconds=300.0,
        m5_event_age_bars=1,
        trigger_age_seconds=18.0,
        chase_atr=0.17,
        profile="BREAKOUT_RETEST_MICRO_HOLD",
        policy_version="TIMING_TEST_V1",
    )
    market = SimpleNamespace(quote=SimpleNamespace(spread=0.26))
    cycle = SimpleNamespace(
        opportunity=opportunity,
        timing=timing,
        intelligence=SimpleNamespace(market=market),
        status="RISK",
        live_action=live_action,
    )
    return SimpleNamespace(cycle=cycle, wrote_broker=wrote)


def test_timing_episode_key_is_stable_for_same_causal_setup():
    first = _result().cycle.opportunity
    second = _result().cycle.opportunity
    assert episode_key(first) == episode_key(second)


def test_runtime_timing_evidence_is_durable_and_idempotent():
    store = StateStore()
    result = _result()
    first_key = record_runtime_timing(store, result)
    second_key = record_runtime_timing(store, result)

    assert first_key == second_key
    events = store.list_events(NS)
    assert len(events) == 1
    payload = events[0].payload
    assert payload["family"] == StrategyFamily.BREAKOUT_RETEST_CONTINUATION.value
    assert payload["timing_outcome"] == TimingOutcome.READY_BUY.value
    assert payload["timing_policy_version"] == "TIMING_TEST_V1"
    assert payload["strategy_policy_version"] == "active-v7"
    assert payload["trigger_age_seconds"] == 18.0
    assert payload["chase_atr"] == 0.17
    assert payload["broker_write_observed"] is True


def test_timing_research_summary_separates_outcomes_without_granting_authority():
    store = StateStore()
    record_runtime_timing(store, _result())
    record_runtime_timing(
        store,
        _result(outcome=TimingOutcome.WAIT, live_action="WAIT", wrote=False),
    )

    summary = summarize_timing_evidence(store)
    assert summary["samples"] == 2
    assert summary["by_outcome"][TimingOutcome.READY_BUY.value] == 1
    assert summary["by_outcome"][TimingOutcome.WAIT.value] == 1
    assert summary["broker_write_associated_samples"] == 1
