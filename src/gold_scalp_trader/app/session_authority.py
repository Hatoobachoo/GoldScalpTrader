"""Hard broker-session authority resolver for guarded DEMO runtime.

Session facts are hard authority inputs. News remains soft context only. The
resolver is read-only and has no broker-write capability.

A scoped provider file remains the strongest explicit authority. When that file
is absent, current MT5 broker facts may prove *present* tradeability without
fabricating a future schedule: a fresh quote plus an explicit symbol trade mode
can establish OPEN / PRE_CLOSE / CLOSED for the current cycle. Stale or unknown
broker facts remain UNKNOWN and fail closed.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from gold_scalp_trader.app.session_news import (
    BrokerSessionFacts,
    NewsContextFacts,
    ProviderContractError,
    ProviderSnapshot,
    load_scoped_file,
    unknown_snapshot,
)
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import ExecutionAction, MarketState, ProviderHealth
from gold_scalp_trader.domain.market import MarketSnapshot

UTC = timezone.utc

# MetaTrader 5 SYMBOL_TRADE_MODE values.  Keep the normalization local to this
# read-only authority module so analytical/strategy code never depends on MT5.
_TRADE_DISABLED = 0
_TRADE_LONG_ONLY = 1
_TRADE_SHORT_ONLY = 2
_TRADE_CLOSE_ONLY = 3
_TRADE_FULL = 4


def provider_path(settings: Settings) -> Path:
    """Keep local Session/News facts beside the ignored runtime state DB."""
    return Path(settings.state_db_path).parent / "session_news.json"


def _saturday_floor(as_of_utc: datetime) -> ProviderSnapshot | None:
    """Return a conservative Saturday CLOSED floor, never a fabricated OPEN."""
    as_of = as_of_utc.astimezone(UTC)
    if as_of.weekday() != 5:
        return None
    return ProviderSnapshot(
        session=BrokerSessionFacts(
            state=MarketState.CLOSED,
            source="BUILTIN_SATURDAY_FLOOR",
            observed_at_utc=as_of,
            valid_until_utc=as_of + timedelta(hours=1),
            schedule_verified=False,
            tradeable=False,
            reason="SATURDAY_MARKET_CLOSED_FLOOR",
        ),
        news=NewsContextFacts(
            health=ProviderHealth.UNAVAILABLE,
            source="NONE",
            reason="NEWS_PROVIDER_NOT_CONFIGURED",
        ),
    )


def _normalized_trade_mode(value: int | str | None) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value in {
            _TRADE_DISABLED, _TRADE_LONG_ONLY, _TRADE_SHORT_ONLY,
            _TRADE_CLOSE_ONLY, _TRADE_FULL,
        } else None
    if value is None:
        return None
    text = str(value).strip().upper().replace(" ", "_").replace("-", "_")
    names = {
        "0": _TRADE_DISABLED,
        "DISABLED": _TRADE_DISABLED,
        "SYMBOL_TRADE_MODE_DISABLED": _TRADE_DISABLED,
        "1": _TRADE_LONG_ONLY,
        "LONGONLY": _TRADE_LONG_ONLY,
        "LONG_ONLY": _TRADE_LONG_ONLY,
        "SYMBOL_TRADE_MODE_LONGONLY": _TRADE_LONG_ONLY,
        "2": _TRADE_SHORT_ONLY,
        "SHORTONLY": _TRADE_SHORT_ONLY,
        "SHORT_ONLY": _TRADE_SHORT_ONLY,
        "SYMBOL_TRADE_MODE_SHORTONLY": _TRADE_SHORT_ONLY,
        "3": _TRADE_CLOSE_ONLY,
        "CLOSEONLY": _TRADE_CLOSE_ONLY,
        "CLOSE_ONLY": _TRADE_CLOSE_ONLY,
        "SYMBOL_TRADE_MODE_CLOSEONLY": _TRADE_CLOSE_ONLY,
        "4": _TRADE_FULL,
        "FULL": _TRADE_FULL,
        "SYMBOL_TRADE_MODE_FULL": _TRADE_FULL,
    }
    return names.get(text)


def _live_mt5_floor(settings: Settings, market: MarketSnapshot) -> ProviderSnapshot:
    """Prove current broker tradeability from normalized MT5 read facts.

    This is deliberately *not* a guessed future schedule.  It only grants the
    current cycle when the broker quote is fresh and symbol trade mode is
    explicit.  The normal execution layer still performs its independent fresh
    broker/order checks before any write.
    """
    now = market.captured_at.astimezone(UTC)
    quote_age = market.quote.age_seconds
    if quote_age < -2.0 or quote_age > settings.max_quote_age_seconds:
        return unknown_snapshot("MT5_LIVE_SESSION_QUOTE_STALE")

    mode = _normalized_trade_mode(market.symbol_spec.trade_mode)
    if mode is None:
        return unknown_snapshot("MT5_LIVE_SESSION_TRADE_MODE_UNKNOWN")

    scope_source = "MT5_LIVE_BROKER_EVIDENCE"
    valid_until = now + timedelta(seconds=settings.max_quote_age_seconds)
    if mode == _TRADE_DISABLED:
        session = BrokerSessionFacts(
            state=MarketState.CLOSED,
            source=scope_source,
            observed_at_utc=market.quote.source_time,
            valid_until_utc=valid_until,
            schedule_verified=True,
            tradeable=False,
            reason="MT5_SYMBOL_TRADE_DISABLED",
        )
    elif mode == _TRADE_CLOSE_ONLY:
        session = BrokerSessionFacts(
            state=MarketState.PRE_CLOSE,
            source=scope_source,
            observed_at_utc=market.quote.source_time,
            valid_until_utc=valid_until,
            schedule_verified=True,
            tradeable=True,
            reason="MT5_SYMBOL_CLOSE_ONLY",
        )
    else:
        session = BrokerSessionFacts(
            state=MarketState.OPEN,
            source=scope_source,
            observed_at_utc=market.quote.source_time,
            valid_until_utc=valid_until,
            schedule_verified=True,
            tradeable=True,
            reason="MT5_FRESH_QUOTE_AND_TRADE_MODE",
        )

    return ProviderSnapshot(
        session=session,
        news=NewsContextFacts(
            health=ProviderHealth.UNAVAILABLE,
            source="NONE",
            reason="NEWS_PROVIDER_NOT_CONFIGURED",
        ),
    )


def resolve(settings: Settings, market: MarketSnapshot) -> ProviderSnapshot:
    """Resolve exact scoped Session/News facts for one immutable market snapshot."""
    path = provider_path(settings)
    if path.is_file():
        try:
            return load_scoped_file(
                path,
                account_login=market.account.login,
                server=market.account.server,
                symbol=market.symbol_spec.symbol,
                as_of_utc=market.captured_at,
                news_ttl_seconds=settings.context_cache_ttl_seconds,
            )
        except ProviderContractError as exc:
            return unknown_snapshot(f"SESSION_PROVIDER_CONTRACT_ERROR:{exc}")

    saturday = _saturday_floor(market.captured_at)
    if saturday is not None:
        return saturday
    return _live_mt5_floor(settings, market)


def action_allowed(snapshot: ProviderSnapshot, action: ExecutionAction) -> bool:
    """Return hard Session permission for an action; News never participates."""
    session = snapshot.session
    if action is ExecutionAction.OPEN:
        return session.hard_new_entry_allowed
    return (
        session.schedule_verified
        and session.tradeable is True
        and session.state in {MarketState.OPEN, MarketState.PRE_CLOSE}
        and not session.unresolved_gap_or_reconciliation
    )


def preclose_flatten_due(session: BrokerSessionFacts, as_of_utc: datetime) -> bool:
    """Apply preserved T-10 daily / T-30 weekend mandatory flatten thresholds."""
    if session.state is not MarketState.PRE_CLOSE or session.next_close_utc is None:
        return False
    seconds = (session.next_close_utc - as_of_utc.astimezone(UTC)).total_seconds()
    if seconds < 0:
        return False
    kind = (session.close_kind or "").upper()
    threshold = 30 * 60 if "WEEKEND" in kind or "FRIDAY" in kind else 10 * 60
    return seconds <= threshold
