"""Durable risk-day state transitions with preserved normal/aggressive semantics."""
from __future__ import annotations
from dataclasses import dataclass,replace
from datetime import datetime,timedelta,timezone
from gold_scalp_trader.config import PRESERVED_RISK_BANDS
from gold_scalp_trader.domain.enums import RiskProfile
@dataclass(frozen=True,slots=True)
class RiskState:
    risk_day_utc:str; day_start_equity:float; profile:RiskProfile; aggressive_mode:bool=False; account_safety_pl:float=0.0; consecutive_losses:int=0; cooldown_until:datetime|None=None; loss_locked:bool=False; manual_reset_count:int=0; cycle_reference_equity:float|None=None; same_episode_reentry_used:bool=False
def initial(day_start_equity:float,as_of:datetime,*,aggressive_mode:bool=False)->RiskState:
    from .engine import resolve_profile
    if as_of.tzinfo is None:raise ValueError("as_of must be timezone-aware")
    return RiskState(as_of.astimezone(timezone.utc).date().isoformat(),day_start_equity,resolve_profile(day_start_equity),aggressive_mode=aggressive_mode,cycle_reference_equity=day_start_equity)
def with_account_safety_pl(state:RiskState,current_equity:float,net_non_trading_cash_flow:float)->RiskState:
    from gold_scalp_trader.market_data.activity import account_safety_pl
    pl=account_safety_pl(current_equity=current_equity,day_start_equity=state.day_start_equity,net_non_trading_cash_flow=net_non_trading_cash_flow); threshold=16.0 if state.aggressive_mode else PRESERVED_RISK_BANDS[state.profile.value].daily_loss_lock_pct; loss_pct=max(0.0,-pl/state.day_start_equity*100.0); return replace(state,account_safety_pl=pl,loss_locked=state.loss_locked or loss_pct>=threshold)
def record_closed_trade(state:RiskState,realized_r:float,closed_at:datetime)->RiskState:
    if closed_at.tzinfo is None:raise ValueError("closed_at must be timezone-aware")
    if realized_r>0:return replace(state,consecutive_losses=0)
    losses=state.consecutive_losses+1; cooldown=state.cooldown_until
    if losses>=3:
        candidate=closed_at+timedelta(minutes=30); cooldown=candidate if cooldown is None or candidate>cooldown else cooldown
    return replace(state,consecutive_losses=losses,cooldown_until=cooldown)
def cooldown_released(state:RiskState,as_of:datetime,*,context_healthy:bool,unresolved_lifecycle:bool)->bool:
    if state.cooldown_until is None:return True
    return as_of>=state.cooldown_until and context_healthy and not unresolved_lifecycle
def consume_same_episode_reentry(state:RiskState)->RiskState:
    if state.same_episode_reentry_used:raise PermissionError("same-episode re-entry already used")
    return replace(state,same_episode_reentry_used=True)
def manual_daily_loss_reset(state:RiskState,*,enabled:bool,operator_confirmed:bool,current_verified_equity:float)->RiskState:
    if not enabled:raise PermissionError("manual daily-loss reset capability is disabled")
    if not operator_confirmed:raise PermissionError("operator confirmation required")
    if not state.loss_locked:raise ValueError("manual reset is only legal from LOSS_LOCKED")
    if state.manual_reset_count>=1:raise PermissionError("manual daily-loss reset already used this UTC risk day")
    if current_verified_equity<=0:raise ValueError("current verified equity must be positive")
    return replace(state,loss_locked=False,manual_reset_count=state.manual_reset_count+1,cycle_reference_equity=current_verified_equity)
