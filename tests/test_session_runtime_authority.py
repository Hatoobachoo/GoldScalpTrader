from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from types import SimpleNamespace

from gold_scalp_trader.app.session_authority import action_allowed, preclose_flatten_due, resolve
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import ExecutionAction, MarketState

UTC = timezone.utc


def _market(tmp_path, when: datetime, *, trade_mode=4, quote_age_seconds=1.0):
    return SimpleNamespace(
        captured_at=when,
        account=SimpleNamespace(login=7, server="demo"),
        symbol_spec=SimpleNamespace(symbol="XAUUSDm", trade_mode=trade_mode),
        quote=SimpleNamespace(
            age_seconds=quote_age_seconds,
            source_time=when - timedelta(seconds=max(0.0, quote_age_seconds)),
        ),
    )


def _settings(tmp_path):
    return Settings(state_db_path=str(tmp_path / "state.sqlite3"), max_quote_age_seconds=10.0)


def _write(tmp_path, when: datetime, state: str, *, next_close=None, close_kind=None):
    payload = {
        "schema_version": 1,
        "provider": "TEST_SCHEDULE",
        "scope": {"account_login": 7, "server": "demo", "symbol": "XAUUSDm"},
        "session": {
            "observed_at_utc": (when - timedelta(minutes=1)).isoformat(),
            "valid_until_utc": (when + timedelta(minutes=30)).isoformat(),
            "schedule_verified": True,
            "tradeable": state in {"OPEN", "PRE_CLOSE"},
            "market_state": state,
            "next_close_utc": None if next_close is None else next_close.isoformat(),
            "close_kind": close_kind,
            "unresolved_gap_or_reconciliation": False,
        },
        "news": {"provider_health": "UNAVAILABLE", "events": []},
    }
    (tmp_path / "session_news.json").write_text(json.dumps(payload), encoding="utf-8")


def test_weekday_missing_provider_uses_fresh_live_mt5_tradeability(tmp_path):
    when = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when, trade_mode=4, quote_age_seconds=1.0))
    assert snapshot.session.state is MarketState.OPEN
    assert snapshot.session.source == "MT5_LIVE_BROKER_EVIDENCE"
    assert snapshot.session.schedule_verified is True
    assert snapshot.session.tradeable is True
    assert action_allowed(snapshot, ExecutionAction.OPEN) is True
    assert snapshot.news.hard_trading_permission is None


def test_weekday_missing_provider_stale_quote_is_unknown_and_fails_closed(tmp_path):
    when = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when, trade_mode=4, quote_age_seconds=30.0))
    assert snapshot.session.state is MarketState.UNKNOWN
    assert snapshot.session.reason == "MT5_LIVE_SESSION_QUOTE_STALE"
    assert action_allowed(snapshot, ExecutionAction.OPEN) is False


def test_weekday_missing_provider_unknown_trade_mode_is_unknown(tmp_path):
    when = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when, trade_mode=None))
    assert snapshot.session.state is MarketState.UNKNOWN
    assert snapshot.session.reason == "MT5_LIVE_SESSION_TRADE_MODE_UNKNOWN"
    assert action_allowed(snapshot, ExecutionAction.OPEN) is False


def test_live_mt5_close_only_maps_preclose_and_blocks_new_open(tmp_path):
    when = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when, trade_mode=3))
    assert snapshot.session.state is MarketState.PRE_CLOSE
    assert action_allowed(snapshot, ExecutionAction.OPEN) is False
    assert action_allowed(snapshot, ExecutionAction.CLOSE) is True
    assert action_allowed(snapshot, ExecutionAction.MODIFY) is True


def test_live_mt5_disabled_maps_closed_and_blocks_all_new_open(tmp_path):
    when = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when, trade_mode=0))
    assert snapshot.session.state is MarketState.CLOSED
    assert snapshot.session.tradeable is False
    assert action_allowed(snapshot, ExecutionAction.OPEN) is False


def test_saturday_missing_provider_is_visible_closed_floor(tmp_path):
    when = datetime(2026, 9, 26, 12, 0, tzinfo=UTC)
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when))
    assert snapshot.session.state is MarketState.CLOSED
    assert snapshot.session.source == "BUILTIN_SATURDAY_FLOOR"
    assert action_allowed(snapshot, ExecutionAction.OPEN) is False


def test_verified_scoped_file_overrides_live_fallback_and_news_is_irrelevant(tmp_path):
    when = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    _write(tmp_path, when, "OPEN")
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when, trade_mode=0))
    assert snapshot.session.state is MarketState.OPEN
    assert snapshot.session.source == "TEST_SCHEDULE"
    assert action_allowed(snapshot, ExecutionAction.OPEN) is True
    assert snapshot.news.hard_trading_permission is None


def test_preclose_blocks_open_allows_management_and_enforces_flatten_threshold(tmp_path):
    when = datetime(2026, 9, 28, 16, 51, tzinfo=UTC)
    _write(tmp_path, when, "PRE_CLOSE", next_close=when + timedelta(minutes=9), close_kind="DAILY")
    snapshot = resolve(_settings(tmp_path), _market(tmp_path, when))
    assert action_allowed(snapshot, ExecutionAction.OPEN) is False
    assert action_allowed(snapshot, ExecutionAction.CLOSE) is True
    assert action_allowed(snapshot, ExecutionAction.MODIFY) is True
    assert preclose_flatten_due(snapshot.session, when) is True


def test_scope_mismatch_becomes_unknown_not_permission(tmp_path):
    when = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    _write(tmp_path, when, "OPEN")
    market = _market(tmp_path, when)
    market.account.login = 8
    snapshot = resolve(_settings(tmp_path), market)
    assert snapshot.session.state is MarketState.UNKNOWN
    assert action_allowed(snapshot, ExecutionAction.OPEN) is False
