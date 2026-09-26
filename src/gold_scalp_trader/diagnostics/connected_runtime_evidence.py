"""Read-only summaries for connected DEMO Session and learning evidence.

This module has no MT5 dependency and no broker authority. It only summarizes
already-durable local evidence for certification/operator visibility.
"""
from __future__ import annotations

from typing import Any

from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.runtime_evidence import MANAGEMENT_NS, SHADOW_NS
from gold_scalp_trader.research.timing_learning import NS as TIMING_NS


def summarize_local_research(store: StateStore) -> dict[str, int]:
    """Return honest counts for the three governed runtime-research streams."""
    timing = store.list_events(TIMING_NS)
    management = store.list_events(MANAGEMENT_NS)
    shadows = store.list_events(SHADOW_NS)
    return {
        "timing_samples": len(timing),
        "timing_broker_write_associated_samples": sum(
            1 for event in timing if event.payload.get("broker_write_observed") is True
        ),
        "management_samples": len(management),
        "shadow_samples": len(shadows),
        "qualified_shadow_samples": sum(
            1 for event in shadows if event.payload.get("qualified") is True
        ),
    }


def session_payload(provider_snapshot: Any) -> dict[str, object]:
    """Normalize hard Session facts without granting or recomputing authority."""
    session = provider_snapshot.session
    state = getattr(session.state, "value", session.state)
    return {
        "state": str(state),
        "source": str(session.source),
        "schedule_verified": bool(session.schedule_verified),
        "tradeable": session.tradeable,
        "reason": str(session.reason),
        "observed_at_utc": session.observed_at_utc.isoformat() if session.observed_at_utc else None,
        "valid_until_utc": session.valid_until_utc.isoformat() if session.valid_until_utc else None,
        "next_close_utc": session.next_close_utc.isoformat() if session.next_close_utc else None,
        "close_kind": session.close_kind,
        "unresolved_gap_or_reconciliation": bool(session.unresolved_gap_or_reconciliation),
        "hard_new_entry_allowed": bool(session.hard_new_entry_allowed),
    }
