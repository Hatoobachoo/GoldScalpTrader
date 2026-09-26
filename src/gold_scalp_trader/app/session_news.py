"""Typed broker-session and News-context provider boundary.

Session facts are hard-authority inputs; News facts are soft context only. This
module performs no broker action and never infers session safety from News.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from gold_scalp_trader.domain.enums import MarketState, ProviderHealth
from gold_scalp_trader.intelligence.news import NewsEvent

UTC = timezone.utc
MAX_PROVIDER_FILE_BYTES = 1_000_000
SUPPORTED_SCHEMA_VERSION = 1


class ProviderContractError(ValueError):
    pass


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProviderContractError(f"{name} must be timezone-aware")
    return value.astimezone(UTC)


def _dt(value: Any, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ProviderContractError(f"invalid {name}") from exc
    return _aware(parsed, name)


def _optional_dt(value: Any, name: str) -> datetime | None:
    return None if value in (None, "") else _dt(value, name)


@dataclass(frozen=True, slots=True)
class BrokerScope:
    account_login: int
    server: str
    symbol: str


@dataclass(frozen=True, slots=True)
class BrokerSessionFacts:
    state: MarketState
    source: str = "UNVERIFIED"
    scope: BrokerScope | None = None
    observed_at_utc: datetime | None = None
    valid_until_utc: datetime | None = None
    schedule_verified: bool = False
    tradeable: bool | None = None
    next_close_utc: datetime | None = None
    close_kind: str | None = None
    reopened_at_utc: datetime | None = None
    reopen_kind: str | None = None
    clean_completed_m5_since_reopen: int = 0
    weekend_gap_assessed: bool | None = None
    execution_normalized: bool | None = None
    unresolved_gap_or_reconciliation: bool = False
    special_schedule_context: str | None = None
    reason: str = ""

    @property
    def hard_new_entry_allowed(self) -> bool:
        return (
            self.state is MarketState.OPEN
            and self.schedule_verified
            and self.tradeable is True
            and not self.unresolved_gap_or_reconciliation
        )


@dataclass(frozen=True, slots=True)
class NewsContextFacts:
    health: ProviderHealth
    source: str = "NONE"
    fetched_at_utc: datetime | None = None
    events: tuple[NewsEvent, ...] = ()
    reason: str = ""

    @property
    def hard_trading_permission(self) -> None:
        return None


@dataclass(frozen=True, slots=True)
class ProviderSnapshot:
    session: BrokerSessionFacts
    news: NewsContextFacts


def unknown_snapshot(reason: str = "PROVIDER_UNAVAILABLE") -> ProviderSnapshot:
    return ProviderSnapshot(
        BrokerSessionFacts(MarketState.UNKNOWN, reason=reason),
        NewsContextFacts(ProviderHealth.UNAVAILABLE, reason=reason),
    )


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.stat().st_size > MAX_PROVIDER_FILE_BYTES:
        raise ProviderContractError("provider file exceeds bounded size")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProviderContractError("provider file is unreadable/corrupt") from exc
    if not isinstance(payload, dict):
        raise ProviderContractError("provider payload must be an object")
    if payload.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        raise ProviderContractError("unsupported provider schema version")
    return payload


def _scope(payload: dict[str, Any], expected: BrokerScope) -> BrokerScope:
    raw = payload.get("scope")
    if not isinstance(raw, dict):
        raise ProviderContractError("provider scope missing")
    try:
        actual = BrokerScope(int(raw["account_login"]), str(raw["server"]), str(raw["symbol"]))
    except (KeyError, TypeError, ValueError) as exc:
        raise ProviderContractError("provider scope is corrupt/incomplete") from exc
    if actual != expected:
        raise ProviderContractError("provider scope does not match connected account/server/symbol")
    return actual


def _session(payload: dict[str, Any], provider: str, scope: BrokerScope, as_of: datetime) -> BrokerSessionFacts:
    raw = payload.get("session")
    if not isinstance(raw, dict):
        return BrokerSessionFacts(MarketState.UNKNOWN, provider, scope, reason="SESSION_FACTS_MISSING")
    observed = _dt(raw.get("observed_at_utc"), "session.observed_at_utc")
    valid_until = _dt(raw.get("valid_until_utc"), "session.valid_until_utc")
    if valid_until < observed:
        raise ProviderContractError("session validity ends before observation")
    verified = raw.get("schedule_verified") is True
    if as_of > valid_until:
        return BrokerSessionFacts(
            MarketState.UNKNOWN, provider, scope, observed, valid_until, verified,
            reason="SESSION_FACTS_EXPIRED",
        )
    try:
        state = MarketState(str(raw.get("market_state", "UNKNOWN")).upper())
    except ValueError as exc:
        raise ProviderContractError("invalid session market_state") from exc
    tradeable_raw = raw.get("tradeable")
    tradeable = tradeable_raw if isinstance(tradeable_raw, bool) else None
    unresolved = bool(raw.get("unresolved_gap_or_reconciliation", False))
    if not verified:
        state = MarketState.UNKNOWN
    elif state is MarketState.OPEN and tradeable is not True:
        state = MarketState.UNKNOWN
    return BrokerSessionFacts(
        state=state,
        source=provider,
        scope=scope,
        observed_at_utc=observed,
        valid_until_utc=valid_until,
        schedule_verified=verified,
        tradeable=tradeable,
        next_close_utc=_optional_dt(raw.get("next_close_utc"), "session.next_close_utc"),
        close_kind=None if raw.get("close_kind") is None else str(raw.get("close_kind")),
        reopened_at_utc=_optional_dt(raw.get("reopened_at_utc"), "session.reopened_at_utc"),
        reopen_kind=None if raw.get("reopen_kind") is None else str(raw.get("reopen_kind")),
        clean_completed_m5_since_reopen=max(0, int(raw.get("clean_completed_m5_since_reopen", 0))),
        weekend_gap_assessed=(raw.get("weekend_gap_assessed") if isinstance(raw.get("weekend_gap_assessed"), bool) else None),
        execution_normalized=(raw.get("execution_normalized") if isinstance(raw.get("execution_normalized"), bool) else None),
        unresolved_gap_or_reconciliation=unresolved,
        special_schedule_context=(None if raw.get("special_schedule_context") is None else str(raw.get("special_schedule_context"))),
        reason="PASS" if state is not MarketState.UNKNOWN else "SESSION_FACTS_UNVERIFIED",
    )


def _news(payload: dict[str, Any], provider: str, as_of: datetime, ttl_seconds: int) -> NewsContextFacts:
    raw = payload.get("news")
    if not isinstance(raw, dict):
        return NewsContextFacts(ProviderHealth.UNAVAILABLE, provider, reason="NEWS_CONTEXT_MISSING")
    try:
        health = ProviderHealth(str(raw.get("provider_health", "UNKNOWN")).upper())
    except ValueError as exc:
        raise ProviderContractError("invalid News provider health") from exc
    fetched = _optional_dt(raw.get("fetched_at_utc"), "news.fetched_at_utc")
    if fetched is not None and (as_of - fetched).total_seconds() > ttl_seconds:
        health = ProviderHealth.STALE
    events: list[NewsEvent] = []
    for item in raw.get("events", ()):
        if not isinstance(item, dict):
            raise ProviderContractError("News event must be an object")
        try:
            events.append(
                NewsEvent(
                    event_id=str(item["provider_event_id"]),
                    title=str(item["title"]),
                    currency=str(item.get("currency", "")),
                    scheduled_at=_dt(item["scheduled_at_utc"], "news.event.scheduled_at_utc"),
                    tier=str(item.get("impact", item.get("tier", "OTHER"))),
                    provider=provider,
                )
            )
        except KeyError as exc:
            raise ProviderContractError("News event is incomplete") from exc
    return NewsContextFacts(health, provider, fetched, tuple(events), "PASS" if health is ProviderHealth.VERIFIED else health.value)


def load_scoped_file(
    path: str | Path,
    *,
    account_login: int,
    server: str,
    symbol: str,
    as_of_utc: datetime,
    news_ttl_seconds: int = 1800,
) -> ProviderSnapshot:
    as_of = _aware(as_of_utc, "as_of_utc")
    if news_ttl_seconds <= 0:
        raise ValueError("news_ttl_seconds must be positive")
    try:
        payload = _load_json(Path(path))
    except FileNotFoundError:
        return unknown_snapshot("PROVIDER_FILE_NOT_FOUND")
    provider = str(payload.get("provider", "SCOPED_FILE"))
    expected = BrokerScope(account_login, server, symbol)
    actual = _scope(payload, expected)
    return ProviderSnapshot(
        _session(payload, provider, actual, as_of),
        _news(payload, provider, as_of, news_ttl_seconds),
    )
