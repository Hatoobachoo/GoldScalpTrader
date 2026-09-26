"""Durable risk-day state transitions and strict persistence helpers.

The state is account/scope context, not broker permission by itself. A UTC
risk-day profile is fixed for that day; restart never resolves it again from
current equity. Unknown financial history must be handled by the caller as
UNKNOWN rather than silently creating a fresh day.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from typing import Any

from gold_scalp_trader.config import PRESERVED_RISK_BANDS
from gold_scalp_trader.domain.enums import RiskProfile
from gold_scalp_trader.persistence.store import StateStore, StateIntegrityError

UTC = timezone.utc
RISK_STATE_NS = "risk_state"


@dataclass(frozen=True, slots=True)
class RiskState:
    risk_day_utc: str
    day_start_equity: float
    profile: RiskProfile
    aggressive_mode: bool = False
    account_safety_pl: float = 0.0
    consecutive_losses: int = 0
    cooldown_until: datetime | None = None
    loss_locked: bool = False
    manual_reset_count: int = 0
    cycle_reference_equity: float | None = None
    same_episode_reentry_used: bool = False


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


def initial(day_start_equity: float, as_of: datetime, *, aggressive_mode: bool = False) -> RiskState:
    from .engine import resolve_profile

    _require_aware(as_of, "as_of")
    if day_start_equity <= 0:
        raise ValueError("DayStartEquity must be positive")
    return RiskState(
        as_of.astimezone(UTC).date().isoformat(),
        day_start_equity,
        resolve_profile(day_start_equity),
        aggressive_mode=aggressive_mode,
        cycle_reference_equity=day_start_equity,
    )


def rollover(
    previous: RiskState,
    day_start_equity: float,
    as_of: datetime,
    *,
    aggressive_mode: bool,
) -> RiskState:
    """Create the next UTC risk-day state without erasing global loss context."""
    fresh = initial(day_start_equity, as_of, aggressive_mode=aggressive_mode)
    return replace(
        fresh,
        consecutive_losses=previous.consecutive_losses,
        cooldown_until=previous.cooldown_until,
        same_episode_reentry_used=previous.same_episode_reentry_used,
    )


def with_account_safety_pl(
    state: RiskState,
    current_equity: float,
    net_non_trading_cash_flow: float,
) -> RiskState:
    from gold_scalp_trader.market_data.activity import account_safety_pl

    pl = account_safety_pl(
        current_equity=current_equity,
        day_start_equity=state.day_start_equity,
        net_non_trading_cash_flow=net_non_trading_cash_flow,
    )
    threshold = (
        16.0
        if state.aggressive_mode
        else PRESERVED_RISK_BANDS[state.profile.value].daily_loss_lock_pct
    )
    loss_pct = max(0.0, -pl / state.day_start_equity * 100.0)
    return replace(
        state,
        account_safety_pl=pl,
        loss_locked=state.loss_locked or loss_pct >= threshold,
    )


def record_closed_trade(
    state: RiskState,
    realized_result: float,
    closed_at: datetime,
    *,
    cooldown_minutes: int = 30,
) -> RiskState:
    """Update the global consecutive-loss policy from one verified full close.

    Positive result resets the streak. Negative result increments it. A true
    breakeven (zero) is neither a win nor a loss and therefore does not create a
    false loss streak.
    """
    _require_aware(closed_at, "closed_at")
    if realized_result > 0:
        return replace(state, consecutive_losses=0)
    if realized_result == 0:
        return state

    losses = state.consecutive_losses + 1
    cooldown = state.cooldown_until
    if losses >= 3:
        duration = max(30, int(cooldown_minutes))
        candidate = closed_at + timedelta(minutes=duration)
        cooldown = candidate if cooldown is None or candidate > cooldown else cooldown
    return replace(state, consecutive_losses=losses, cooldown_until=cooldown)


def cooldown_released(
    state: RiskState,
    as_of: datetime,
    *,
    context_healthy: bool,
    unresolved_lifecycle: bool,
) -> bool:
    _require_aware(as_of, "as_of")
    if state.cooldown_until is None:
        return True
    return (
        as_of >= state.cooldown_until
        and context_healthy
        and not unresolved_lifecycle
    )


def consume_same_episode_reentry(state: RiskState) -> RiskState:
    if state.same_episode_reentry_used:
        raise PermissionError("same-episode re-entry already used")
    return replace(state, same_episode_reentry_used=True)


def manual_daily_loss_reset(
    state: RiskState,
    *,
    enabled: bool,
    operator_confirmed: bool,
    current_verified_equity: float,
) -> RiskState:
    if not enabled:
        raise PermissionError("manual daily-loss reset capability is disabled")
    if not operator_confirmed:
        raise PermissionError("operator confirmation required")
    if not state.loss_locked:
        raise ValueError("manual reset is only legal from LOSS_LOCKED")
    if state.manual_reset_count >= 1:
        raise PermissionError("manual daily-loss reset already used this UTC risk day")
    if current_verified_equity <= 0:
        raise ValueError("current verified equity must be positive")
    return replace(
        state,
        loss_locked=False,
        manual_reset_count=state.manual_reset_count + 1,
        cycle_reference_equity=current_verified_equity,
    )


def _payload(state: RiskState) -> dict[str, Any]:
    return {
        "risk_day_utc": state.risk_day_utc,
        "day_start_equity": state.day_start_equity,
        "profile": state.profile.value,
        "aggressive_mode": state.aggressive_mode,
        "account_safety_pl": state.account_safety_pl,
        "consecutive_losses": state.consecutive_losses,
        "cooldown_until": None if state.cooldown_until is None else state.cooldown_until.isoformat(),
        "loss_locked": state.loss_locked,
        "manual_reset_count": state.manual_reset_count,
        "cycle_reference_equity": state.cycle_reference_equity,
        "same_episode_reentry_used": state.same_episode_reentry_used,
    }


def _from_payload(payload: dict[str, Any]) -> RiskState:
    try:
        cooldown_raw = payload.get("cooldown_until")
        cooldown = None if cooldown_raw is None else datetime.fromisoformat(str(cooldown_raw))
        if cooldown is not None:
            _require_aware(cooldown, "cooldown_until")
        state = RiskState(
            risk_day_utc=str(payload["risk_day_utc"]),
            day_start_equity=float(payload["day_start_equity"]),
            profile=RiskProfile(str(payload["profile"])),
            aggressive_mode=bool(payload.get("aggressive_mode", False)),
            account_safety_pl=float(payload.get("account_safety_pl", 0.0)),
            consecutive_losses=int(payload.get("consecutive_losses", 0)),
            cooldown_until=cooldown,
            loss_locked=bool(payload.get("loss_locked", False)),
            manual_reset_count=int(payload.get("manual_reset_count", 0)),
            cycle_reference_equity=(
                None
                if payload.get("cycle_reference_equity") is None
                else float(payload["cycle_reference_equity"])
            ),
            same_episode_reentry_used=bool(payload.get("same_episode_reentry_used", False)),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise StateIntegrityError("risk state is corrupt/incomplete") from exc

    if state.day_start_equity <= 0 or state.consecutive_losses < 0 or state.manual_reset_count < 0:
        raise StateIntegrityError("risk state contains invalid values")
    return state


def save(store: StateStore, scope: str, state: RiskState) -> None:
    if not scope:
        raise ValueError("risk-state scope is required")
    store.put(RISK_STATE_NS, scope, _payload(state))


def load(store: StateStore, scope: str) -> RiskState | None:
    if not scope:
        raise ValueError("risk-state scope is required")
    record = store.get(RISK_STATE_NS, scope)
    return None if record is None else _from_payload(record.payload)
