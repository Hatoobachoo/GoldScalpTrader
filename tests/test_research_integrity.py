from pathlib import Path
import pytest
from gold_scalp_trader.research.datasets import build_dataset_identity, verify_dataset_identity
from gold_scalp_trader.research.stress import StressScenario, apply_execution_stress
from gold_scalp_trader.research.validation import HoldoutUse, ValidationWindows, consume_holdout


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


def test_execution_stress_is_explicit_and_deterministic():
    result = apply_execution_stress(base_spread=0.20, base_slippage_allowance=0.05, scenario=StressScenario(1.5, 0.03, 120, 0.10))
    assert result.spread == pytest.approx(0.30)
    assert result.slippage_allowance == pytest.approx(0.08)
    assert result.latency_ms == 120
    assert result.adverse_entry_drift == pytest.approx(0.10)
