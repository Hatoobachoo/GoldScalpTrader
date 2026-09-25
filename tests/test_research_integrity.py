from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from gold_scalp_trader.domain.enums import StrategyMode, Timeframe
from gold_scalp_trader.domain.market import Candle
from gold_scalp_trader.research.ablation import compare_feature
from gold_scalp_trader.research.datasets import build_dataset_identity, verify_dataset_identity
from gold_scalp_trader.research.evidence import build_evidence_identity
from gold_scalp_trader.research.management_replay import ReplayCandidate, apply_single_position_capacity
from gold_scalp_trader.research.metrics import summarize
from gold_scalp_trader.research.outcomes import ResearchOutcome
from gold_scalp_trader.research.packages import verify_evidence_package, write_evidence_package
from gold_scalp_trader.research.replay import chronological_points
from gold_scalp_trader.research.stress import StressScenario, apply_execution_stress
from gold_scalp_trader.research.validation import HoldoutUse, ValidationWindows, consume_holdout, walk_forward_folds

UTC = timezone.utc


def _candle(tf: Timeframe, minute: int, price: float = 100.0) -> Candle:
    return Candle(tf, datetime(2026, 1, 2, 10, minute, tzinfo=UTC), price, price + 1, price - 1, price + 0.25)


def test_dataset_identity_detects_change(tmp_path: Path):
    p = tmp_path / "M5.csv"
    p.write_text("time,open,high,low,close\n1,1,2,0,1.5\n", encoding="utf-8")
    identity = build_dataset_identity(source="fixture", symbol="XAUUSDm", version="v1", paths=[p])
    assert verify_dataset_identity(identity, [p])
    p.write_text("time,open,high,low,close\n1,1,3,0,1.5\n", encoding="utf-8")
    assert not verify_dataset_identity(identity, [p])


def test_holdout_is_one_shot_and_windows_do_not_overlap():
    ValidationWindows(0, 100, 100, 150, 150, 200)
    used = consume_holdout(HoldoutUse("candidate-hash", "dataset-hash"))
    assert used.consumed
    with pytest.raises(ValueError, match="one-shot"):
        consume_holdout(used)
    with pytest.raises(ValueError, match="chronological"):
        ValidationWindows(0, 100, 90, 150, 150, 200)


def test_walk_forward_folds_never_enter_final_holdout_region():
    folds = walk_forward_folds(development_count=180, train_size=100, validation_size=20, step_size=20)
    assert [(f.train_start, f.train_end, f.validation_start, f.validation_end) for f in folds] == [
        (0, 100, 100, 120),
        (0, 120, 120, 140),
        (0, 140, 140, 160),
        (0, 160, 160, 180),
    ]
    assert all(f.validation_end <= 180 for f in folds)


def test_execution_stress_is_explicit_and_deterministic():
    result = apply_execution_stress(base_spread=0.20, base_slippage_allowance=0.05, scenario=StressScenario(1.5, 0.03, 120, 0.10))
    assert result.spread == pytest.approx(0.30)
    assert result.slippage_allowance == pytest.approx(0.08)
    assert result.latency_ms == 120
    assert result.adverse_entry_drift == pytest.approx(0.10)


def test_multitimeframe_replay_excludes_unclosed_m1_bar():
    m5 = (_candle(Timeframe.M5, 0), _candle(Timeframe.M5, 5), _candle(Timeframe.M5, 10))
    m1 = tuple(_candle(Timeframe.M1, minute) for minute in range(0, 12))
    points = tuple(chronological_points({Timeframe.M5: m5, Timeframe.M1: m1}, warmup=2))
    assert len(points) == 2
    first = points[0]
    assert first.as_of == datetime(2026, 1, 2, 10, 10, tzinfo=UTC)
    assert first.candles[Timeframe.M5] == m5[:2]
    assert first.candles[Timeframe.M1][-1].open_time.minute == 9
    assert all(candle.close_time <= first.as_of for candle in first.candles[Timeframe.M1])


def test_replay_rejects_non_chronological_series():
    with pytest.raises(ValueError, match="strictly chronological"):
        tuple(chronological_points({Timeframe.M5: (_candle(Timeframe.M5, 5), _candle(Timeframe.M5, 0))}, warmup=1))


def test_single_position_capacity_preserves_shadow_counterfactuals():
    base = datetime(2026, 1, 2, 10, 0, tzinfo=UTC)
    rows = (
        ReplayCandidate("A", base, base + timedelta(minutes=10)),
        ReplayCandidate("SHADOW", base + timedelta(minutes=2), base + timedelta(minutes=4), StrategyMode.SHADOW_ONLY),
        ReplayCandidate("B", base + timedelta(minutes=5), base + timedelta(minutes=7)),
        ReplayCandidate("C", base + timedelta(minutes=10), base + timedelta(minutes=15)),
    )
    result = {row.episode_id: row for row in apply_single_position_capacity(rows)}
    assert result["A"].accepted_for_production
    assert result["SHADOW"].reason == "SHADOW_COUNTERFACTUAL_NO_PRODUCTION_SLOT"
    assert result["B"].reason == "POSITION_CAPACITY_BLOCKED"
    assert result["C"].accepted_for_production


def test_metrics_keep_opportunity_capture_separate_from_win_rate():
    rows = (
        ResearchOutcome("1", "FAMILY", StrategyMode.ACTIVE_EXECUTION, True, True, net_r=1.0, entry_efficiency=0.9),
        ResearchOutcome("2", "FAMILY", StrategyMode.ACTIVE_EXECUTION, True, True, net_r=-0.5, entry_efficiency=0.7),
        ResearchOutcome("3", "FAMILY", StrategyMode.ACTIVE_EXECUTION, True, False, reason="MISSED"),
    )
    metrics = summarize(rows)
    assert metrics.net_r == pytest.approx(0.5)
    assert metrics.average_r == pytest.approx(0.25)
    assert metrics.win_rate == pytest.approx(0.5)
    assert metrics.profit_factor == pytest.approx(2.0)
    assert metrics.opportunity_capture_rate == pytest.approx(2 / 3)
    assert metrics.average_entry_efficiency == pytest.approx(0.8)


def test_shadow_outcome_cannot_claim_broker_execution():
    with pytest.raises(ValueError, match="cannot be marked as broker executed"):
        ResearchOutcome("x", "FAMILY", StrategyMode.SHADOW_ONLY, True, True, net_r=1.0)


def test_ablation_reports_edge_and_recall_tradeoff_without_creating_policy():
    result = compare_feature(
        "RSI_CONTEXT",
        full_net_r=5.0,
        without_feature_net_r=4.5,
        full_opportunity_recall=0.72,
        without_feature_opportunity_recall=0.80,
    )
    assert result.marginal_net_r == pytest.approx(0.5)
    assert result.recall_delta == pytest.approx(-0.08)


def test_evidence_package_is_write_new_and_detects_tamper(tmp_path: Path):
    evidence = build_evidence_identity(
        candidate_fingerprint="candidate-v1",
        dataset_sha256="dataset-sha",
        code_revision="abc123",
        config_fingerprint="cfg-v1",
        policy_version="policy-v1",
        execution_realism="M1_REFINEMENT_REPLAY",
    )
    metrics = summarize((ResearchOutcome("1", "FAMILY", StrategyMode.ACTIVE_EXECUTION, True, True, net_r=0.4),))
    package = write_evidence_package(tmp_path, package_id="pkg-001", evidence=evidence, metrics=metrics, limitations=("bar-based execution",))
    assert verify_evidence_package(package)
    with pytest.raises(FileExistsError):
        write_evidence_package(tmp_path, package_id="pkg-001", evidence=evidence, metrics=metrics)
    (package / "metrics.json").write_text("{}\n", encoding="utf-8")
    assert not verify_evidence_package(package)
