from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from gold_scalp_trader.domain.enums import (
    Direction,
    ManagementAction,
    SetupQualification,
    StrategyFamily,
    StrategyMode,
    Timeframe,
)
from gold_scalp_trader.domain.market import Candle, Quote
from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.runtime_evidence import (
    MANAGEMENT_NS,
    SHADOW_NS,
    record_runtime_research,
    summarize_runtime_evidence,
    trade_path_summary,
)
from gold_scalp_trader.strategies.isolation import IsolatedCandidate, IsolationResult

UTC = timezone.utc


def _result():
    now = datetime(2026, 9, 26, 10, 0, tzinfo=UTC)
    candles = tuple(
        Candle(Timeframe.M5, now - timedelta(minutes=5 * (3 - i)), 100, 101, 99, 100.5)
        for i in range(3)
    )
    market = SimpleNamespace(
        captured_at=now,
        quote=Quote(101.0, 101.2, now, now),
        series=lambda tf: candles if tf is Timeframe.M5 else (),
    )
    active = SetupCandidate(
        "A",
        StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
        SetupQualification.QUALIFIED_BUY,
        Direction.BUY,
        .8,
        .9,
        ("M5-A",),
        ("active",),
    )
    shadow = SetupCandidate(
        "S",
        StrategyFamily.LIQUIDITY_SWEEP_REVERSAL,
        SetupQualification.QUALIFIED_SELL,
        Direction.SELL,
        .7,
        .8,
        ("M5-S",),
        ("shadow",),
        m5_event_time=now - timedelta(minutes=5),
        preferred_m1_profile="SWEEP_RECLAIM",
        policy_version="shadow-v1",
    )
    isolation = IsolationResult(
        active.family,
        active,
        (
            IsolatedCandidate(active, StrategyMode.ACTIVE_EXECUTION),
            IsolatedCandidate(shadow, StrategyMode.SHADOW_ONLY),
        ),
        "ACTIVE_FAMILY_SETUP_QUALIFIED",
    )
    trade = ManagedTrade(
        "TRD-1", 88, "XAUUSDm", Direction.BUY, .01, 100, 99, 99, 102, 104,
        StrategyFamily.BREAKOUT_RETEST_CONTINUATION, "v1", 1.0,
        now - timedelta(minutes=12), opportunity_id="OPP-1", episode_id="EP-1",
        trade_plan_id="PLAN-1", timing_profile="RETEST", timing_policy_version="T1",
    )
    cycle = SimpleNamespace(
        intelligence=SimpleNamespace(market=market),
        isolation=isolation,
        reason="earned protection after >=1R",
    )
    return SimpleNamespace(cycle=cycle, managed_trade=trade, management_action=ManagementAction.PROTECT)


def test_runtime_research_records_management_and_shadow_without_live_authority():
    store = StateStore()
    result = _result()
    first = record_runtime_research(store, result)
    second = record_runtime_research(store, result)
    assert first == second
    assert len(store.list_events(MANAGEMENT_NS)) == 1
    assert len(store.list_events(SHADOW_NS)) == 1
    management = store.list_events(MANAGEMENT_NS)[0].payload
    assert management["trade_id"] == "TRD-1"
    assert management["action"] == "PROTECT"
    assert management["open_r"] == 1.0
    shadow = store.list_events(SHADOW_NS)[0].payload
    assert shadow["shadow_family"] == StrategyFamily.LIQUIDITY_SWEEP_REVERSAL.value
    assert shadow["qualified"] is True
    assert "broker_write" not in shadow
    assert "risk_decision" not in shadow


def test_trade_path_and_runtime_summary_are_descriptive_only():
    store = StateStore()
    record_runtime_research(store, _result())
    path = trade_path_summary(store, "TRD-1")
    assert path["samples"] == 1
    assert path["max_favorable_r"] == 1.0
    summary = summarize_runtime_evidence(store)
    assert summary["management_samples"] == 1
    assert summary["shadow_samples"] == 1
    assert summary["qualified_shadow_samples"] == 1
