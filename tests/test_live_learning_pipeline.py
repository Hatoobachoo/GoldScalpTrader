import pytest
from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore
from gold_scalp_trader.research.learning import LearningObservation, load, save
from gold_scalp_trader.research.live_learning import enqueue, pending, process_pending


def payload():
    return {
        "trade_id": "TRD-1",
        "position_ticket": 123,
        "symbol": "XAUUSDm",
        "family": "BREAKOUT_RETEST_CONTINUATION",
        "policy_version": "v1",
        "opened_at": "2026-09-26T10:00:00+00:00",
        "closed_at": "2026-09-26T10:20:00+00:00",
        "close_origin": "BOT",
        "net_money": 2.5,
        "opportunity_id": "OPP-1",
        "episode_id": "EP-1",
        "trade_plan_id": "PLAN-1",
        "entry_reference": 4600.0,
        "m5_source_event_ids": ["M5-A"],
        "m5_event_time": "2026-09-26T09:55:00+00:00",
        "timing_profile": "BREAKOUT_RETEST",
        "timing_policy_version": "TIMING-V2",
        "timing_trigger_time": "2026-09-26T09:59:00+00:00",
        "m5_event_age_seconds": 300.0,
        "m5_event_age_bars": 1,
        "trigger_age_seconds": 8.0,
        "chase_atr": 0.18,
        "micro_extension_atr": 0.22,
    }


def test_verified_close_queue_becomes_exactly_once_actual_memory():
    store = StateStore()
    enqueue(store, "TRD-1", payload())
    result = process_pending(store)
    assert result.processed == 1 and result.failed == 0 and result.pending == 0
    obs = load(store, "managed-trade:TRD-1")
    assert obs is not None
    assert obs.family == "BREAKOUT_RETEST_CONTINUATION"
    assert obs.net_money == 2.5
    assert obs.realized_r is None
    assert "ACTUAL_ACTIVE" in obs.tags
    second = process_pending(store)
    assert second.processed == 0


def test_timing_lineage_survives_exactly_once_learning_ingestion():
    store = StateStore()
    enqueue(store, "TRD-1", payload())
    process_pending(store)
    obs = load(store, "managed-trade:TRD-1")
    assert obs is not None
    assert obs.opportunity_id == "OPP-1"
    assert obs.episode_id == "EP-1"
    assert obs.trade_plan_id == "PLAN-1"
    assert obs.entry_reference == 4600.0
    assert obs.m5_source_event_ids == ("M5-A",)
    assert obs.timing_profile == "BREAKOUT_RETEST"
    assert obs.timing_policy_version == "TIMING-V2"
    assert obs.trigger_age_seconds == 8.0
    assert obs.chase_atr == 0.18


def test_missing_metrics_are_not_fabricated():
    store = StateStore()
    enqueue(store, "TRD-1", payload())
    process_pending(store)
    obs = load(store, "managed-trade:TRD-1")
    assert obs is not None
    assert obs.entry_efficiency is None
    assert obs.capture_efficiency is None
    assert obs.realized_r is None
    assert obs.observed_mfe_r is None
    assert obs.observed_capture_efficiency is None


def test_provable_efficiency_metrics_survive_learning_ingestion():
    store = StateStore()
    enriched = payload()
    enriched.update(
        {
            "initial_risk_money": 5.0,
            "realized_r": 0.5,
            "entry_reference_drift_r": 0.1,
            "observed_mfe_r": 1.25,
            "observed_mae_r": -0.4,
            "observed_capture_efficiency": 0.4,
            "observed_giveback_r": 0.75,
            "opportunity_to_entry_seconds": 300.0,
            "ready_to_entry_seconds": 45.0,
            "trigger_to_entry_seconds": 12.0,
            "m5_event_to_entry_seconds": 600.0,
            "time_to_first_protect_seconds": 240.0,
            "time_to_first_trail_seconds": 480.0,
            "time_to_observed_primary_target_seconds": 540.0,
            "time_to_observed_expansion_target_seconds": None,
            "time_to_observed_mfe_seconds": 510.0,
            "management_samples": 8,
        }
    )
    enqueue(store, "TRD-1", enriched)
    process_pending(store)
    obs = load(store, "managed-trade:TRD-1")
    assert obs is not None
    assert obs.realized_r == pytest.approx(0.5)
    assert obs.entry_reference_drift_r == pytest.approx(0.1)
    assert obs.observed_mfe_r == pytest.approx(1.25)
    assert obs.observed_mae_r == pytest.approx(-0.4)
    assert obs.observed_capture_efficiency == pytest.approx(0.4)
    assert obs.ready_to_entry_seconds == pytest.approx(45.0)
    assert obs.time_to_first_trail_seconds == pytest.approx(480.0)
    assert obs.management_samples == 8
    assert obs.capture_efficiency is None


def test_conflicting_existing_memory_preserves_queue():
    store = StateStore()
    enqueue(store, "TRD-1", payload())
    save(store, LearningObservation("managed-trade:TRD-1", "OTHER", "vX", net_money=-99))
    result = process_pending(store)
    assert result.processed == 0 and result.failed == 1 and pending(store) == 1


def test_incomplete_source_remains_pending():
    store = StateStore()
    enqueue(store, "TRD-BAD", {"trade_id": "TRD-BAD"})
    result = process_pending(store)
    assert result.failed == 1
    assert pending(store) == 1
