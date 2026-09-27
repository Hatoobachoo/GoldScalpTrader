import pytest

from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore
from gold_scalp_trader.research.candidate_registry import NS as CANDIDATE_NS, runtime_activation_allowed, load
from gold_scalp_trader.research.discovery import DiscoveryPolicy, SUPPRESSION_NS, run_discovery
from gold_scalp_trader.research.episode_journal import EpisodeRecord, append as append_episode
from gold_scalp_trader.research.learning import LearningObservation, save
from gold_scalp_trader.research.promotion import Candidate, PromotionStage, advance
from gold_scalp_trader.research.triggers import classify_learning_episodes


def test_learning_is_idempotent_but_conflicting_source_is_integrity_error():
    s = StateStore()
    a = LearningObservation("trade:1", "BREAKOUT_RETEST", "v1", 1.2, .9, .7)
    save(s, a)
    save(s, a)
    with pytest.raises(StateIntegrityError):
        save(s, LearningObservation("trade:1", "BREAKOUT_RETEST", "v1", 2.0, .9, .7))


def test_candidate_cannot_self_promote_to_production():
    c = Candidate("C1", "ENTRY_POLICY", {"x": 1}, PromotionStage.APPROVAL_REQUIRED, rollback_target="champion-v1")
    with pytest.raises(PermissionError):
        advance(c, PromotionStage.PRODUCTION, evidence_id="ev", operator_approved=False)
    assert advance(c, PromotionStage.PRODUCTION, evidence_id="ev", operator_approved=True).stage is PromotionStage.PRODUCTION


def test_verified_learning_drives_bounded_discovery_without_runtime_authority():
    store = StateStore()
    for index in range(5):
        save(
            store,
            LearningObservation(
                source_id=f"managed-trade:T{index}",
                family="BREAKOUT_RETEST_CONTINUATION",
                policy_version="v1",
                realized_r=0.25,
                observed_mfe_r=2.0,
                observed_capture_efficiency=0.25,
                observed_giveback_r=0.25,
            ),
        )

    assert classify_learning_episodes(store) == 10  # actual + weak-capture per verified close
    assert classify_learning_episodes(store) == 0   # content-addressed/idempotent triggers

    status = run_discovery(store, DiscoveryPolicy(min_independent_episodes=5))
    assert status.state == "HEALTHY"
    assert status.eligible_clusters == 1
    assert status.candidates == 1
    assert status.suppressed == 0

    rows = store.list_records(CANDIDATE_NS)
    assert len(rows) == 1
    candidate = load(store, rows[0].key)
    assert candidate is not None
    assert candidate.candidate.kind == "EXIT_POLICY"
    assert candidate.candidate.semantics["parent_family"] == "BREAKOUT_RETEST_CONTINUATION"
    assert len(candidate.candidate.semantics["sources"]) == 5
    assert runtime_activation_allowed(candidate) is False
    assert rows[0].payload["runtime_authority"] == "NONE"
    assert rows[0].payload["broker_authority"] == "NONE"


def test_fault_clusters_are_durably_suppressed_not_invented_as_strategy():
    store = StateStore()
    for index in range(5):
        append_episode(
            store,
            EpisodeRecord(
                episode_id=f"FAULT-{index}",
                evidence_class="SYSTEM_OR_BROKER_FAULT",
                active_family="BREAKOUT_RETEST_CONTINUATION",
                shadow_families=(),
                outcome_r=None,
                reason="BROKER_READ_FAILURE",
            ),
        )

    status = run_discovery(store, DiscoveryPolicy(min_independent_episodes=5))
    assert status.state == "HEALTHY"
    assert status.candidates == 0
    assert status.suppressed == 1
    suppressions = store.list_records(SUPPRESSION_NS)
    assert len(suppressions) == 1
    assert suppressions[0].payload["reason"] == "BROKER_OR_SYSTEM_FAULT_IS_NOT_STRATEGY_EVIDENCE"
    assert store.list_records(CANDIDATE_NS) == ()
