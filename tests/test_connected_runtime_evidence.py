from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

from gold_scalp_trader.diagnostics.connected_runtime_evidence import session_payload, summarize_local_research
from gold_scalp_trader.domain.enums import MarketState
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.runtime_evidence import MANAGEMENT_NS, SHADOW_NS
from gold_scalp_trader.research.timing_learning import NS as TIMING_NS

UTC = timezone.utc


def test_connected_runtime_evidence_summarizes_only_durable_local_facts(tmp_path) -> None:
    store = StateStore(tmp_path / "state.sqlite3")
    try:
        store.append_event(TIMING_NS, "t1", {"broker_write_observed": False})
        store.append_event(TIMING_NS, "t2", {"broker_write_observed": True})
        store.append_event(MANAGEMENT_NS, "m1", {"action": "HOLD"})
        store.append_event(SHADOW_NS, "s1", {"qualified": True})
        store.append_event(SHADOW_NS, "s2", {"qualified": False})
        assert summarize_local_research(store) == {
            "timing_samples": 2,
            "timing_broker_write_associated_samples": 1,
            "management_samples": 1,
            "shadow_samples": 2,
            "qualified_shadow_samples": 1,
        }
    finally:
        store.close()


def test_session_payload_preserves_hard_authority_truth_without_recomputing() -> None:
    now = datetime(2026, 9, 26, 12, 0, tzinfo=UTC)
    session = SimpleNamespace(
        state=MarketState.PRE_CLOSE,
        source="TEST",
        schedule_verified=True,
        tradeable=True,
        reason="TEST_PRECLOSE",
        observed_at_utc=now,
        valid_until_utc=now,
        next_close_utc=now,
        close_kind="WEEKEND",
        unresolved_gap_or_reconciliation=False,
        hard_new_entry_allowed=False,
    )
    payload = session_payload(SimpleNamespace(session=session))
    assert payload["state"] == "PRE_CLOSE"
    assert payload["schedule_verified"] is True
    assert payload["tradeable"] is True
    assert payload["hard_new_entry_allowed"] is False
    assert payload["reason"] == "TEST_PRECLOSE"
