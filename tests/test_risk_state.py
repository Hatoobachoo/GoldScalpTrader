from datetime import datetime,timedelta,timezone
import pytest
from gold_scalp_trader.risk.state import initial,manual_daily_loss_reset,record_closed_trade,with_account_safety_pl,consume_same_episode_reentry,cooldown_released
UTC=timezone.utc
def test_aggressive_daily_lock_uses_preserved_16_percent_ceiling():
    s=initial(100,datetime.now(tz=UTC),aggressive_mode=True);assert not with_account_safety_pl(s,85,0).loss_locked;assert with_account_safety_pl(s,84,0).loss_locked
def test_manual_reset_disabled_by_default_and_one_use_when_enabled():
    s=with_account_safety_pl(initial(100,datetime.now(tz=UTC)),87,0)
    with pytest.raises(PermissionError):manual_daily_loss_reset(s,enabled=False,operator_confirmed=True,current_verified_equity=87)
    r=manual_daily_loss_reset(s,enabled=True,operator_confirmed=True,current_verified_equity=87);assert not r.loss_locked and r.manual_reset_count==1
    with pytest.raises(PermissionError):manual_daily_loss_reset(with_account_safety_pl(r,70,0),enabled=True,operator_confirmed=True,current_verified_equity=70)
def test_reentry_and_cooldown_release_require_real_conditions():
    s=initial(100,datetime.now(tz=UTC));s=consume_same_episode_reentry(s)
    with pytest.raises(PermissionError):consume_same_episode_reentry(s)
    t=datetime.now(tz=UTC)
    for i in range(3):s=record_closed_trade(s,-1,t+timedelta(minutes=i))
    assert not cooldown_released(s,s.cooldown_until,context_healthy=False,unresolved_lifecycle=False);assert cooldown_released(s,s.cooldown_until,context_healthy=True,unresolved_lifecycle=False)
