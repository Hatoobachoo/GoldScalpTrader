"""Crash-safe verified-close queue and exactly-once actual learning processor."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore

from .learning import LearningObservation, save as save_observation

QUEUE = "closed_trade_learning_queue"


@dataclass(frozen=True, slots=True)
class LearningProcessResult:
    processed: int
    pending: int
    failed: int
    errors: tuple[str, ...] = ()


def enqueue(store: StateStore, trade_id: str, payload: dict) -> None:
    store.put(QUEUE, trade_id, payload, allow_replace=False)


def consume(store: StateStore, trade_id: str) -> None:
    store.delete(QUEUE, trade_id)


def pending(store: StateStore) -> int:
    return len(store.list_records(QUEUE))


def _optional_float(payload: dict[str, Any], name: str) -> float | None:
    value = payload.get(name)
    return None if value is None else float(value)


def _optional_int(payload: dict[str, Any], name: str) -> int | None:
    value = payload.get(name)
    return None if value is None else int(value)


def _optional_str(payload: dict[str, Any], name: str) -> str | None:
    value = payload.get(name)
    return None if value is None else str(value)


def _observation(trade_id: str, payload: dict[str, Any]) -> LearningObservation:
    try:
        family = str(payload["family"])
        policy = str(payload["policy_version"])
        ticket = int(payload["position_ticket"])
        symbol = str(payload["symbol"])
        origin = str(payload["close_origin"])
        closed_at = str(payload["closed_at"])
    except (KeyError, TypeError, ValueError) as exc:
        raise StateIntegrityError(f"learning source {trade_id} is incomplete") from exc
    if not family or not policy or ticket <= 0 or not symbol or not closed_at:
        raise StateIntegrityError(f"learning source {trade_id} contains invalid identity")

    tags = ("ACTUAL_ACTIVE", f"CLOSE_ORIGIN:{origin}", f"SYMBOL:{symbol}")
    return LearningObservation(
        source_id=f"managed-trade:{trade_id}",
        family=family,
        policy_version=policy,
        realized_r=_optional_float(payload, "realized_r"),
        entry_efficiency=_optional_float(payload, "entry_efficiency"),
        capture_efficiency=_optional_float(payload, "capture_efficiency"),
        net_money=_optional_float(payload, "net_money"),
        close_origin=origin,
        position_ticket=ticket,
        symbol=symbol,
        opened_at=_optional_str(payload, "opened_at"),
        closed_at=closed_at,
        opportunity_id=_optional_str(payload, "opportunity_id"),
        episode_id=_optional_str(payload, "episode_id"),
        trade_plan_id=_optional_str(payload, "trade_plan_id"),
        entry_reference=_optional_float(payload, "entry_reference"),
        m5_source_event_ids=tuple(str(x) for x in payload.get("m5_source_event_ids", ())),
        m5_event_time=_optional_str(payload, "m5_event_time"),
        timing_profile=_optional_str(payload, "timing_profile"),
        timing_policy_version=_optional_str(payload, "timing_policy_version"),
        timing_trigger_time=_optional_str(payload, "timing_trigger_time"),
        m5_event_age_seconds=_optional_float(payload, "m5_event_age_seconds"),
        m5_event_age_bars=_optional_int(payload, "m5_event_age_bars"),
        trigger_age_seconds=_optional_float(payload, "trigger_age_seconds"),
        chase_atr=_optional_float(payload, "chase_atr"),
        micro_extension_atr=_optional_float(payload, "micro_extension_atr"),
        initial_risk_money=_optional_float(payload, "initial_risk_money"),
        entry_reference_drift_r=_optional_float(payload, "entry_reference_drift_r"),
        observed_mfe_r=_optional_float(payload, "observed_mfe_r"),
        observed_mae_r=_optional_float(payload, "observed_mae_r"),
        observed_capture_efficiency=_optional_float(payload, "observed_capture_efficiency"),
        observed_giveback_r=_optional_float(payload, "observed_giveback_r"),
        opportunity_to_entry_seconds=_optional_float(payload, "opportunity_to_entry_seconds"),
        ready_to_entry_seconds=_optional_float(payload, "ready_to_entry_seconds"),
        trigger_to_entry_seconds=_optional_float(payload, "trigger_to_entry_seconds"),
        m5_event_to_entry_seconds=_optional_float(payload, "m5_event_to_entry_seconds"),
        time_to_first_protect_seconds=_optional_float(payload, "time_to_first_protect_seconds"),
        time_to_first_trail_seconds=_optional_float(payload, "time_to_first_trail_seconds"),
        time_to_observed_primary_target_seconds=_optional_float(payload, "time_to_observed_primary_target_seconds"),
        time_to_observed_expansion_target_seconds=_optional_float(payload, "time_to_observed_expansion_target_seconds"),
        time_to_observed_mfe_seconds=_optional_float(payload, "time_to_observed_mfe_seconds"),
        management_samples=int(payload.get("management_samples", 0) or 0),
        tags=tags,
    )


def process_pending(store: StateStore, *, limit: int | None = None) -> LearningProcessResult:
    records = store.list_records(QUEUE)
    selected = records if limit is None else records[: max(0, limit)]
    processed = 0
    errors: list[str] = []
    for record in selected:
        trade_id = record.key
        try:
            observation = _observation(trade_id, record.payload)
            save_observation(store, observation)
            consume(store, trade_id)
            processed += 1
        except (StateIntegrityError, TypeError, ValueError) as exc:
            errors.append(f"{trade_id}:{exc}")
    return LearningProcessResult(processed, pending(store), len(errors), tuple(errors))
