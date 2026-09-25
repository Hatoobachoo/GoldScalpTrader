from pathlib import Path
import pytest
from gold_scalp_trader.persistence.store import StateStore,StateIntegrityError
def test_store_idempotent_and_conflict_safe(tmp_path:Path):
    s=StateStore(tmp_path/"state.db"); s.put("n","k",{"x":1},allow_replace=False); s.put("n","k",{"x":1},allow_replace=False)
    with pytest.raises(StateIntegrityError):s.put("n","k",{"x":2},allow_replace=False)
    assert s.integrity_check(); s.close()
