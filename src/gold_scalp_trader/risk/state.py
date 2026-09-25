"""Risk-day, daily-lock, loss-streak, cooldown and same-episode re-entry state."""
from __future__ import annotations
from dataclasses import dataclass,replace
from datetime import datetime,timedelta,timezone
from gold_scalp_trader.config import PRESERVED_RISK_BANDS
from gold_scalp_trader.domain.enums import RiskProfile
@dataclass(frozen=True,slots=True)
class RiskState:
    risk_day_utc:str; day_start_equity:float; profile:RiskProfile; account_safety_pl:float=0.0; consecutive_losses:int=0; cooldown_until:datetime|None=None; loss_locked:bool=False; same_episode_reentry_used:bool=False
def initial(day_start_equity:float,as_of:datetime)->RiskState:
    from .engine import resolve_profile
    return RiskState(as_of.astimezone(timezone.utc).date().isoformat(),day_start_equity,resolve_profile(day_start_equity))
def with_account_safety_pl(state:RiskState,current_equity:float,net_non_trading_cash_flow:float)->RiskState:
    pl=current_equity-state.day_start_equity-net_non_trading_cash_flow; band=PRESERVED_RISK_BANDS[state.profile.value]; loss_pct=max(0.0,-pl/state.day_start_equity*100.0)
    return replace(state,account_safety_pl=pl,loss_locked=state.loss_locked or loss_pct>=band.daily_loss_lock_pct)
def record_closed_trade(state:RiskState,realized_r:float,closed_at:datetime)->RiskState:
    if realized_r>0:return replace(state,consecutive_losses=0)
    losses=state.consecutive_losses+1; cooldown=state.cooldown_until
    if losses>=3:
        candidate=closed_at+timedelta(minutes=30); cooldown=candidate if cooldown is None or candidate>cooldown else cooldown
    return replace(state,consecutive_losses=losses,cooldown_until=cooldown)
