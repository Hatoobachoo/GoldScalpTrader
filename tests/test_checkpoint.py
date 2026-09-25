from pathlib import Path
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.persistence.checkpoint import export_checkpoint,restore_checkpoint
def test_checkpoint_roundtrip(tmp_path:Path):
    a=StateStore(); a.put("risk","current",{"x":1}); p=export_checkpoint(a,tmp_path/"cp.json",("risk",)); b=StateStore(); restore_checkpoint(p,b); assert b.get("risk","current").payload=={"x":1}
