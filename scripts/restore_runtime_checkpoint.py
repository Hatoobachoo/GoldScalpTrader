from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.persistence.checkpoint import restore_checkpoint
if len(sys.argv)!=3:raise SystemExit("usage: restore_runtime_checkpoint.py CHECKPOINT TARGET_DB")
store=StateStore(sys.argv[2]); restore_checkpoint(sys.argv[1],store); print("Checkpoint restored; fresh MT5 reconciliation is still required.")
