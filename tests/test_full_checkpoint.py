from pathlib import Path

from gold_scalp_trader.persistence.checkpoint import export_checkpoint, restore_checkpoint
from gold_scalp_trader.persistence.store import StateStore


def test_full_checkpoint_preserves_records_and_events(tmp_path: Path):
    a = StateStore()
    a.put("risk", "current", {"x": 1})
    a.put("candidate_stage_evidence", "stage-1", {"candidate": "C1", "target": "SHADOW"})
    a.append_event("journal", "e1", {"y": 2})
    a.append_event("shadow_counterfactual_outcomes", "cf-1", {"net_r": 1.2, "broker_authority": "NONE"})
    p = export_checkpoint(a, tmp_path / "full.json")

    b = StateStore()
    restore_checkpoint(p, b)
    assert b.get("risk", "current").payload == {"x": 1}
    assert b.get("candidate_stage_evidence", "stage-1").payload["target"] == "SHADOW"
    assert b.list_events("journal")[0].payload == {"y": 2}
    counterfactual = b.list_events("shadow_counterfactual_outcomes")[0].payload
    assert counterfactual["net_r"] == 1.2
    assert counterfactual["broker_authority"] == "NONE"
