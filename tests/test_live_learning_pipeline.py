import pytest
from gold_scalp_trader.persistence.store import StateIntegrityError,StateStore
from gold_scalp_trader.research.learning import LearningObservation,load,save
from gold_scalp_trader.research.live_learning import enqueue,pending,process_pending
def payload():return {"trade_id":"TRD-1","position_ticket":123,"symbol":"XAUUSDm","family":"BREAKOUT_RETEST_CONTINUATION","policy_version":"v1","opened_at":"2026-09-26T10:00:00+00:00","closed_at":"2026-09-26T10:20:00+00:00","close_origin":"BOT","net_money":2.5}
def test_verified_close_queue_becomes_exactly_once_actual_memory():
    store=StateStore(); enqueue(store,"TRD-1",payload()); result=process_pending(store); assert result.processed==1 and result.failed==0 and result.pending==0; obs=load(store,"managed-trade:TRD-1"); assert obs is not None; assert obs.family=="BREAKOUT_RETEST_CONTINUATION"; assert obs.net_money==2.5; assert obs.realized_r is None; assert "ACTUAL_ACTIVE" in obs.tags; second=process_pending(store); assert second.processed==0
def test_missing_metrics_are_not_fabricated():
    store=StateStore(); enqueue(store,"TRD-1",payload()); process_pending(store); obs=load(store,"managed-trade:TRD-1"); assert obs is not None; assert obs.entry_efficiency is None; assert obs.capture_efficiency is None; assert obs.realized_r is None
def test_conflicting_existing_memory_preserves_queue():
    store=StateStore(); enqueue(store,"TRD-1",payload()); save(store,LearningObservation("managed-trade:TRD-1","OTHER","vX",net_money=-99)); result=process_pending(store); assert result.processed==0 and result.failed==1 and pending(store)==1
def test_incomplete_source_remains_pending():
    store=StateStore(); enqueue(store,"TRD-BAD",{"trade_id":"TRD-BAD"}); result=process_pending(store); assert result.failed==1; assert pending(store)==1
