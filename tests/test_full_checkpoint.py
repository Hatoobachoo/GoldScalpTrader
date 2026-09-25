from pathlib import Path
from gold_scalp_trader.persistence.checkpoint import export_checkpoint,restore_checkpoint
from gold_scalp_trader.persistence.store import StateStore
def test_full_checkpoint_preserves_records_and_events(tmp_path:Path):
    a=StateStore();a.put("risk","current",{"x":1});a.append_event("journal","e1",{"y":2});p=export_checkpoint(a,tmp_path/"full.json");b=StateStore();restore_checkpoint(p,b);assert b.get("risk","current").payload=={"x":1};assert b.list_events("journal")[0].payload=={"y":2}
