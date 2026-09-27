"""Derive conservative research-trigger episodes from verified StrategyMemory.

Thresholds here only decide whether an observation is worth researching. They do
not modify live strategy/Risk/Gate/management behavior and cannot create broker
authority. Every derived episode retains the immutable StrategyMemory source ID.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from gold_scalp_trader.persistence.store import StateStore

from .episode_journal import EpisodeRecord, NS as EPISODE_NS, append as append_episode
from .learning import NS as LEARNING_NS, load as load_learning


@dataclass(frozen=True, slots=True)
class TriggerPolicy:
    meaningful_mfe_r: float = 1.0
    weak_capture_max: float = 0.50
    material_giveback_r: float = 1.0
    adverse_entry_drift_r: float = 0.50
    false_entry_max_mfe_r: float = 0.25
    false_entry_loss_r: float = -0.75

    def __post_init__(self) -> None:
        if self.meaningful_mfe_r <= 0 or self.material_giveback_r <= 0 or self.adverse_entry_drift_r <= 0:
            raise ValueError("research trigger thresholds must be positive where applicable")
        if not 0 <= self.weak_capture_max <= 1:
            raise ValueError("weak_capture_max must be within 0..1")
        if self.false_entry_max_mfe_r < 0 or self.false_entry_loss_r >= 0:
            raise ValueError("false-entry research thresholds are invalid")


def _event_id(source_id: str, evidence_class: str) -> str:
    digest = sha256(f"{source_id}|{evidence_class}".encode()).hexdigest()[:24]
    return f"EP-{digest}"


def _append(store: StateStore, obs, evidence_class: str, reason: str) -> bool:
    event_id = _event_id(obs.source_id, evidence_class)
    existing = next((x for x in store.list_events(EPISODE_NS) if x.event_key == event_id), None)
    if existing is not None:
        return False
    append_episode(
        store,
        EpisodeRecord(
            episode_id=event_id,
            evidence_class=evidence_class,
            active_family=obs.family,
            shadow_families=(),
            outcome_r=obs.realized_r,
            reason=f"{reason};SOURCE={obs.source_id}",
        ),
    )
    return True


def classify_learning_episodes(store: StateStore, policy: TriggerPolicy | None = None) -> int:
    """Append idempotent actual/trigger episodes from verified learning memory."""
    policy = policy or TriggerPolicy()
    added = 0
    for row in store.list_records(LEARNING_NS):
        obs = load_learning(store, row.key)
        if obs is None:
            continue
        added += int(_append(store, obs, "ACTUAL_ACTIVE_TRADE", "VERIFIED_ACTIVE_CLOSE"))

        if (
            obs.observed_mfe_r is not None
            and obs.observed_mfe_r >= policy.meaningful_mfe_r
            and obs.observed_capture_efficiency is not None
            and obs.observed_capture_efficiency <= policy.weak_capture_max
        ):
            added += int(_append(store, obs, "WEAK_CAPTURE", "LOW_CAPTURE_AFTER_MEANINGFUL_MFE"))

        if obs.observed_giveback_r is not None and obs.observed_giveback_r >= policy.material_giveback_r:
            added += int(_append(store, obs, "PREMATURE_EXIT", "MATERIAL_OBSERVED_GIVEBACK"))

        if obs.entry_reference_drift_r is not None and obs.entry_reference_drift_r >= policy.adverse_entry_drift_r:
            added += int(_append(store, obs, "TIME_EFFICIENCY_FAILURE", "MATERIAL_ADVERSE_ENTRY_DRIFT"))

        if (
            obs.realized_r is not None
            and obs.realized_r <= policy.false_entry_loss_r
            and obs.observed_mfe_r is not None
            and obs.observed_mfe_r <= policy.false_entry_max_mfe_r
        ):
            added += int(_append(store, obs, "FALSE_ENTRY_CLUSTER", "LOSS_WITH_MINIMAL_FAVORABLE_EXCURSION"))
    return added


__all__ = ["TriggerPolicy", "classify_learning_episodes"]
