"""Durable, research-only timing evidence from governed DEMO runtime cycles.

This module has no broker authority. It records stable, deduplicated timing
facts so later governed research can measure entry timing efficiency without
changing live TimingPolicy, Risk, Gate, strategy isolation, or REAL release
boundaries.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from typing import Any

from gold_scalp_trader.persistence.store import StateStore

NS = "timing_decision_evidence"
SCHEMA_VERSION = 1


def _value(value: Any) -> str | None:
    if value is None:
        return None
    return str(getattr(value, "value", value))


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    isoformat = getattr(value, "isoformat", None)
    return isoformat() if callable(isoformat) else str(value)


def _number(value: Any) -> float | None:
    return None if value is None else round(float(value), 6)


def _canonical_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(raw.encode("utf-8")).hexdigest()


def episode_key(opportunity: Any) -> str:
    """Stable causal episode fingerprint independent of transient Opportunity IDs."""
    payload = {
        "family": _value(getattr(opportunity, "family", None)),
        "direction": _value(getattr(opportunity, "direction", None)),
        "source_event_ids": sorted(str(x) for x in getattr(opportunity, "source_event_ids", ()) or ()),
        "strategy_policy_version": getattr(opportunity, "policy_version", None),
        "m5_event_time": _iso(getattr(opportunity, "m5_event_time", None)),
        "timing_profile": getattr(opportunity, "preferred_m1_profile", None),
    }
    return f"TEP-{_canonical_hash(payload)[:20]}"


def evidence_payload(result: Any) -> dict[str, Any] | None:
    """Normalize one meaningful timing decision into immutable research evidence."""
    cycle = getattr(result, "cycle", None)
    if cycle is None:
        return None
    opportunity = getattr(cycle, "opportunity", None)
    timing = getattr(cycle, "timing", None)
    if opportunity is None or timing is None:
        return None

    market = getattr(getattr(cycle, "intelligence", None), "market", None)
    quote = getattr(market, "quote", None)
    return {
        "schema_version": SCHEMA_VERSION,
        "episode_key": episode_key(opportunity),
        "family": _value(getattr(opportunity, "family", None)),
        "direction": _value(getattr(opportunity, "direction", None)),
        "source_event_ids": sorted(str(x) for x in getattr(opportunity, "source_event_ids", ()) or ()),
        "strategy_policy_version": getattr(opportunity, "policy_version", None),
        "m5_event_time": _iso(getattr(opportunity, "m5_event_time", None)),
        "coverage": _number(getattr(opportunity, "coverage", None)),
        "timing_outcome": _value(getattr(timing, "outcome", None)),
        "timing_reason": str(getattr(timing, "reason", "")),
        "timing_profile": getattr(timing, "profile", None),
        "timing_policy_version": getattr(timing, "policy_version", None),
        "trigger_time": _iso(getattr(timing, "trigger_time", None)),
        "m5_event_age_seconds": _number(getattr(timing, "m5_event_age_seconds", None)),
        "m5_event_age_bars": getattr(timing, "m5_event_age_bars", None),
        "trigger_age_seconds": _number(getattr(timing, "trigger_age_seconds", None)),
        "chase_atr": _number(getattr(timing, "chase_atr", None)),
        "micro_extension_atr": _number(getattr(timing, "micro_extension_atr", None)),
        "spread": _number(getattr(quote, "spread", None)),
        "cycle_status": str(getattr(cycle, "status", "")),
        "live_action": str(getattr(cycle, "live_action", "")),
        "broker_write_observed": bool(getattr(result, "wrote_broker", False)),
    }


def record_runtime_timing(store: StateStore, result: Any) -> str | None:
    """Append one deduplicated immutable timing fact; repeated identical cycles are idempotent."""
    payload = evidence_payload(result)
    if payload is None:
        return None
    event_key = f"TIM-{_canonical_hash(payload)}"
    store.append_event(NS, event_key, payload)
    return event_key


def summarize_timing_evidence(store: StateStore) -> dict[str, Any]:
    """Small governed-research summary; it grants no trading or promotion authority."""
    events = store.list_events(NS)
    outcomes = Counter(str(event.payload.get("timing_outcome", "UNKNOWN")) for event in events)
    families = Counter(str(event.payload.get("family", "UNKNOWN")) for event in events)
    profiles = Counter(str(event.payload.get("timing_profile") or "UNKNOWN") for event in events)
    return {
        "samples": len(events),
        "by_outcome": dict(sorted(outcomes.items())),
        "by_family": dict(sorted(families.items())),
        "by_profile": dict(sorted(profiles.items())),
        "broker_write_associated_samples": sum(
            1 for event in events if event.payload.get("broker_write_observed") is True
        ),
    }
