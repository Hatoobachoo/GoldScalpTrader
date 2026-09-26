from datetime import datetime, timezone
from gold_scalp_trader.domain.enums import Direction, StrategyFamily
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.management.store import load, save
from gold_scalp_trader.persistence.store import StateStore


def test_managed_trade_roundtrip_preserves_original_family_r_and_timing_lineage():
    now = datetime(2026, 9, 26, 10, 0, tzinfo=timezone.utc)
    trade = ManagedTrade(
        "T",
        7,
        "XAUUSDm",
        Direction.BUY,
        0.01,
        100,
        99,
        99,
        102,
        104,
        StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
        "v3",
        1.0,
        now,
        opportunity_id="OPP-1",
        episode_id="EP-1",
        trade_plan_id="PLAN-1",
        entry_reference=99.8,
        m5_source_event_ids=("M5-A", "M5-B"),
        m5_event_time=now,
        timing_profile="BREAKOUT_RETEST",
        timing_policy_version="TIMING-V2",
        timing_trigger_time=now,
        m5_event_age_seconds=60.0,
        m5_event_age_bars=1,
        trigger_age_seconds=4.0,
        chase_atr=0.18,
        micro_extension_atr=0.22,
    )
    store = StateStore()
    save(store, "scope", trade)
    assert load(store, "scope") == trade


def test_legacy_managed_trade_payload_loads_without_fabricating_timing_lineage():
    store = StateStore()
    store.put(
        "managed_trade",
        "scope",
        {
            "trade_id": "T",
            "ticket": 7,
            "symbol": "XAUUSDm",
            "direction": "BUY",
            "volume": 0.01,
            "entry": 100,
            "original_sl": 99,
            "current_sl": 99,
            "primary_target": 102,
            "expansion_target": None,
            "family": "BREAKOUT_RETEST_CONTINUATION",
            "policy_version": "v3",
            "original_r_price": 1.0,
            "opened_at": None,
        },
    )
    trade = load(store, "scope")
    assert trade is not None
    assert trade.opportunity_id is None
    assert trade.timing_profile is None
    assert trade.m5_source_event_ids == ()
