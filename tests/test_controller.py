from datetime import datetime,timedelta,timezone
import pytest
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.execution.controller import acquire,verify
UTC=timezone.utc
def test_controller_fences_second_holder_until_expiry():
    s=StateStore(); now=datetime.now(tz=UTC); a=acquire(s,"acct:sym","A",now,30); assert verify(s,a,now)
    with pytest.raises(RuntimeError):acquire(s,"acct:sym","B",now+timedelta(seconds=5),30)
    b=acquire(s,"acct:sym","B",now+timedelta(seconds=31),30); assert b.epoch>a.epoch
