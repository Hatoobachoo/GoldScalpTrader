from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from gold_scalp_trader.domain.enums import (
    Direction,
    ManagementAction,
    SetupQualification,
    StrategyFamily,
    StrategyMode,
    Timeframe,
)
from gold_scalp_trader.domain.market import Candle, Quote, SymbolSpec
from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.runtime_evidence import (
    MANAGEMENT_NS,
    SHADOW_NS,
    measure_trade_efficiency,
    record_runtime_research,
    summarize_runtime_evidence,
    trade_path_summary,
)
from gold_scalp_trader.research.timing_learning import NS as TIMING_NS
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
        symbol_spec=SymbolSpec(
            "XAUUSDm", 3, 0.001, 0.01, 1.0, 0.01, 200.0, 0.01, 0, 0
        ),
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
    assert management["initial_risk_money"] == pytest.approx(1.0)
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


def _efficiency_trade() -> ManagedTrade:
    opened = datetime(2026, 9, 26, 10, 5, tzinfo=UTC)
    return ManagedTrade(
        "TRD-EFF", 99, "XAUUSDm", Direction.BUY, .01, 101.0, 99.0, 99.0, 105.0, 107.0,
        StrategyFamily.BREAKOUT_RETEST_CONTINUATION, "v3", 2.0, opened,
        opportunity_id="OPP-EFF", episode_id="EP-EFF", trade_plan_id="PLAN-EFF",
        entry_reference=100.8,
        m5_event_time=datetime(2026, 9, 26, 9, 55, tzinfo=UTC),
        timing_trigger_time=datetime(2026, 9, 26, 10, 4, tzinfo=UTC),
    )


def test_post_trade_efficiency_uses_only_durable_observed_path():
    store = StateStore()
    trade = _efficiency_trade()
    store.append_event(
        TIMING_NS,
        "TIM-WAIT",
        {
            "opportunity_id": "OPP-EFF",
            "opportunity_created_at": "2026-09-26T10:00:00+00:00",
            "timing_decision_at": "2026-09-26T10:01:00+00:00",
            "timing_outcome": "WAIT",
        },
    )
    store.append_event(
        TIMING_NS,
        "TIM-READY",
        {
            "opportunity_id": "OPP-EFF",
            "opportunity_created_at": "2026-09-26T10:00:00+00:00",
            "timing_decision_at": "2026-09-26T10:03:00+00:00",
            "timing_outcome": "READY_BUY",
        },
    )
    for key, minutes, open_r, action in (
        ("M1", 2, -0.25, "HOLD"),
        ("M2", 5, 1.00, "PROTECT"),
        ("M3", 10, 2.00, "TRAIL"),
        ("M4", 13, 1.40, "HOLD"),
    ):
        store.append_event(
            MANAGEMENT_NS,
            key,
            {
                "trade_id": trade.trade_id,
                "captured_at_utc": (trade.opened_at + timedelta(minutes=minutes)).isoformat(),
                "action": action,
                "open_r": open_r,
                "initial_risk_money": 10.0,
            },
        )

    result = measure_trade_efficiency(
        store,
        trade,
        closed_at=datetime(2026, 9, 26, 10, 20, tzinfo=UTC),
        net_money=15.0,
    )
    assert result.realized_r == pytest.approx(1.5)
    assert result.entry_reference_drift_r == pytest.approx(0.1)
    assert result.observed_mfe_r == pytest.approx(2.0)
    assert result.observed_mae_r == pytest.approx(-0.25)
    assert result.observed_capture_efficiency == pytest.approx(0.75)
    assert result.observed_giveback_r == pytest.approx(0.5)
    assert result.opportunity_to_entry_seconds == pytest.approx(300.0)
    assert result.ready_to_entry_seconds == pytest.approx(120.0)
    assert result.trigger_to_entry_seconds == pytest.approx(60.0)
    assert result.m5_event_to_entry_seconds == pytest.approx(600.0)
    assert result.time_to_first_protect_seconds == pytest.approx(300.0)
    assert result.time_to_first_trail_seconds == pytest.approx(600.0)
    assert result.time_to_observed_primary_target_seconds == pytest.approx(600.0)
    assert result.time_to_observed_expansion_target_seconds is None
    assert result.time_to_observed_mfe_seconds == pytest.approx(600.0)
    assert result.management_samples == 4


def test_efficiency_never_invents_missing_path_metrics():
    store = StateStore()
    trade = _efficiency_trade()
    result = measure_trade_efficiency(
        store,
        trade,
        closed_at=datetime(2026, 9, 26, 10, 20, tzinfo=UTC),
        net_money=15.0,
    )
    assert result.initial_risk_money is None
    assert result.realized_r is None
    assert result.observed_mfe_r is None
    assert result.observed_mae_r is None
    assert result.observed_capture_efficiency is None
    assert result.management_samples == 0
