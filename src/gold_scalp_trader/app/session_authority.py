"""Hard broker-session authority resolver for guarded DEMO runtime.

Session facts are hard authority inputs. News remains soft context only. The
resolver is read-only and has no broker-write capability.
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
    return unknown_snapshot("SESSION_PROVIDER_FILE_NOT_FOUND")


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
