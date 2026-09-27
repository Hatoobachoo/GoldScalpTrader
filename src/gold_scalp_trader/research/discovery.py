"""Durable bounded discovery from explicitly classified research episodes.

Discovery is conservative: an ordinary loss, broker fault or hard-safety block
is never silently re-labelled as a strategy defect. Eligible recurring clusters
may create candidates only when every episode carries an immutable approved
source-evidence reference (currently StrategyMemory for automatic live triggers).
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore

from .candidate_registry import load as load_candidate, register_invention
from .episode_journal import NS as EPISODE_NS
from .invention import Recipe, invent

SUPPRESSION_NS = "research_discovery_suppressions"
STATUS_NS = "research_discovery_status"
STATUS_KEY = "CURRENT"


@dataclass(frozen=True, slots=True)
class DiscoveryPolicy:
    min_independent_episodes: int = 5

    def __post_init__(self) -> None:
        if self.min_independent_episodes < 2:
            raise ValueError("discovery requires at least two independent episodes")


@dataclass(frozen=True, slots=True)
class DiscoveryStatus:
    state: str
    eligible_clusters: int
    candidates: int
    suppressed: int
    pending_clusters: int = 0


_ELIGIBLE_RECIPES = {
    "MISSED_MEANINGFUL_MOVE": ("ENTRY_POLICY", ("M5_SETUP",), ("M1_ENTRY_TIMING",), "Improve entry timing on repeated meaningful misses."),
    "TIME_EFFICIENCY_FAILURE": ("ENTRY_POLICY", ("M5_SETUP",), ("M1_ENTRY_TIMING", "EXECUTABLE_COST"), "Reduce repeated adverse entry timing without forcing entries."),
    "PREMATURE_EXIT": ("EXIT_POLICY", ("M5_SETUP",), ("MANAGEMENT_EFFICIENCY",), "Study management timing where verified exits repeatedly leave material opportunity."),
    "WEAK_CAPTURE": ("EXIT_POLICY", ("M5_SETUP",), ("MANAGEMENT_EFFICIENCY", "TARGET_PATH"), "Improve verified capture efficiency while preserving structural invalidation."),
    "FALSE_ENTRY_CLUSTER": ("VARIANT", ("M5_SETUP",), ("M1_ENTRY_TIMING", "TARGET_PATH"), "Study repeated losses that showed minimal favorable excursion before invalidation."),
    "COST_REJECTED_OPPORTUNITY": ("QUALITY_POLICY", ("M5_SETUP",), ("EXECUTABLE_COST",), "Study repeated cost rejects without weakening hard safety."),
    "FALSE_BLOCK_CANDIDATE": ("QUALITY_POLICY", ("M5_SETUP",), ("EXECUTABLE_COST", "TARGET_PATH"), "Study repeated non-safety quality blocks with favorable counterfactual outcomes."),
    "REGIME_DETERIORATION": ("REGIME_POLICY", ("M5_SETUP",), ("SESSION_CONTEXT", "ATR_VOLATILITY"), "Condition strategy evidence on repeated regime deterioration."),
    "CAPACITY_SUPPRESSED_OPPORTUNITY": ("EXIT_POLICY", ("M5_SETUP",), ("MANAGEMENT_EFFICIENCY",), "Study slot-occupancy opportunity cost without allowing extra live positions."),
}

_NEVER_STRATEGY = {
    "SYSTEM_OR_BROKER_FAULT": "BROKER_OR_SYSTEM_FAULT_IS_NOT_STRATEGY_EVIDENCE",
    "HARD_SAFE_BLOCK": "HARD_SAFETY_BLOCK_IS_NOT_OPTIMIZATION_SPACE",
}


def _cluster_key(payload: dict) -> tuple[str, str, tuple[str, ...]]:
    evidence_class = str(payload.get("evidence_class", "UNKNOWN"))
    active_family = str(payload.get("active_family") or "NONE")
    shadows = tuple(sorted(str(x) for x in payload.get("shadow_families", ()) if str(x)))
    return evidence_class, active_family, shadows


def _cluster_id(key: tuple[str, str, tuple[str, ...]]) -> str:
    raw = json.dumps(key, sort_keys=True, separators=(",", ":"))
    return f"CLUSTER-{sha256(raw.encode()).hexdigest()[:24]}"


def _source_ref(payload: dict) -> str | None:
    reason = str(payload.get("reason", ""))
    marker = ";SOURCE="
    if marker not in reason:
        return None
    source = reason.rsplit(marker, 1)[-1].strip()
    return source or None


def _recipe(key: tuple[str, str, tuple[str, ...]]) -> Recipe | None:
    evidence_class, active_family, _ = key
    spec = _ELIGIBLE_RECIPES.get(evidence_class)
    if spec is None:
        return None
    candidate_type, required, supportive, hypothesis = spec
    return Recipe(
        required=required,
        supportive=supportive,
        direction_model="INDEPENDENT_BUY_SELL_CASES",
        timing_model="M5_THESIS_WITH_SUBORDINATE_M1_TIMING",
        candidate_type=candidate_type,
        parent_family=None if active_family == "NONE" else active_family,
        hypothesis=hypothesis,
        version="DISCOVERY_V1",
    )


def _persist_status(store: StateStore, status: DiscoveryStatus) -> None:
    store.put(
        STATUS_NS,
        STATUS_KEY,
        {
            "state": status.state,
            "eligible_clusters": status.eligible_clusters,
            "candidates": status.candidates,
            "suppressed": status.suppressed,
            "pending_clusters": status.pending_clusters,
            "runtime_authority": "NONE",
            "broker_authority": "NONE",
        },
        allow_replace=True,
    )


def _suppress(store: StateStore, cluster_id: str, evidence_class: str, episode_ids: tuple[str, ...], reason: str) -> None:
    if store.get(SUPPRESSION_NS, cluster_id) is None:
        store.put(
            SUPPRESSION_NS,
            cluster_id,
            {
                "cluster_id": cluster_id,
                "evidence_class": evidence_class,
                "episode_ids": list(episode_ids),
                "reason": reason,
                "runtime_authority": "NONE",
                "broker_authority": "NONE",
            },
            allow_replace=False,
        )


def run_discovery(store: StateStore, policy: DiscoveryPolicy | None = None) -> DiscoveryStatus:
    policy = policy or DiscoveryPolicy()
    clusters: dict[tuple[str, str, tuple[str, ...]], list] = {}
    for event in store.list_events(EPISODE_NS):
        clusters.setdefault(_cluster_key(event.payload), []).append(event)

    eligible = candidates = suppressed = pending = 0
    for key, events in clusters.items():
        evidence_class = key[0]
        if evidence_class not in _ELIGIBLE_RECIPES and evidence_class not in _NEVER_STRATEGY:
            continue

        independent_ids = tuple(dict.fromkeys(event.event_key for event in events))
        if len(independent_ids) < policy.min_independent_episodes:
            pending += 1
            continue

        eligible += 1
        cluster_id = _cluster_id(key)
        if evidence_class in _NEVER_STRATEGY:
            _suppress(store, cluster_id, evidence_class, independent_ids, _NEVER_STRATEGY[evidence_class])
            suppressed += 1
            continue

        source_ids = tuple(dict.fromkeys(ref for event in events if (ref := _source_ref(event.payload))))
        if len(source_ids) < policy.min_independent_episodes:
            _suppress(store, cluster_id, evidence_class, independent_ids, "INSUFFICIENT_IMMUTABLE_SOURCE_LINEAGE")
            suppressed += 1
            continue

        recipe = _recipe(key)
        if recipe is None:
            raise StateIntegrityError(f"eligible discovery class has no recipe: {evidence_class}")
        preview = invent(recipe, source_ids)
        if load_candidate(store, preview.candidate_id) is None:
            register_invention(store, recipe, source_ids)
        candidates += 1

    state = "IDLE" if eligible == 0 else "HEALTHY" if eligible == candidates + suppressed else "DEGRADED"
    status = DiscoveryStatus(state, eligible, candidates, suppressed, pending)
    _persist_status(store, status)
    return status


def health(eligible: int, candidates: int, suppressed: int) -> DiscoveryStatus:
    state = "HEALTHY" if eligible == candidates + suppressed else "DEGRADED"
    return DiscoveryStatus(state, eligible, candidates, suppressed)


__all__ = ["DiscoveryPolicy", "DiscoveryStatus", "SUPPRESSION_NS", "STATUS_NS", "health", "run_discovery"]
