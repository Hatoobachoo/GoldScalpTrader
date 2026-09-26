from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from gold_scalp_trader.app.runtime import run_guarded_demo_cycle, symbol_allows_open
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import Direction, RuntimeMode, StrategyFamily
from gold_scalp_trader.persistence.store import StateStore

UTC = timezone.utc


class Api:
    TIMEFRAME_M1 = 1
    TIMEFRAME_M5 = 5
    TIMEFRAME_M15 = 15
    TIMEFRAME_H1 = 60
    TIMEFRAME_H4 = 240
    TRADE_ACTION_DEAL = 1
    TRADE_ACTION_SLTP = 6
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    TRADE_RETCODE_DONE = 10009
    ACCOUNT_TRADE_MODE_DEMO = 0
    SYMBOL_TRADE_MODE_LONGONLY = 1
    SYMBOL_TRADE_MODE_SHORTONLY = 2
    SYMBOL_TRADE_MODE_FULL = 4

    def __init__(self, account_trade_mode=0):
        self.sent = 0
        self.opened = False
        self.account_trade_mode = account_trade_mode
        self.last_request = None

    def account_info(self):
        return SimpleNamespace(
            login=7,
            server="demo",
            currency="USD",
            balance=1000,
            equity=1000,
            margin_free=1000,
            trade_allowed=True,
            trade_expert=True,
            trade_mode=self.account_trade_mode,
        )

    def symbol_info(self, symbol):
        if symbol != "XAUUSDm":
            return None
        return SimpleNamespace(
            digits=3,
            point=.001,
            trade_tick_size=.001,
            trade_tick_value=1,
            volume_min=.01,
            volume_max=200,
            volume_step=.01,
            trade_stops_level=0,
            trade_freeze_level=0,
            trade_mode=4,
            filling_mode=1,
        )

    def symbol_info_tick(self, symbol):
        return SimpleNamespace(bid=100, ask=100.02, time=int(datetime.now(tz=UTC).timestamp()))

    def copy_rates_from_pos(self, symbol, timeframe, start, count):
        now = int(datetime.now(tz=UTC).timestamp())
        step = {1: 60, 5: 300, 15: 900, 60: 3600, 240: 14400}[timeframe]
        rows = []
        n = min(count, 80)
        for i in range(n):
            timestamp = now - (n - i) * step
            price = 100 + (i * .02)
            rows.append(
                {
                    "time": timestamp,
                    "open": price - .01,
                    "high": price + .08,
                    "low": price - .08,
                    "close": price + .01,
                    "tick_volume": 10,
                    "real_volume": 0,
                }
            )
        return rows

    def positions_get(self, symbol=None):
        if not self.opened or self.last_request is None:
            return []
        return [
            SimpleNamespace(
                ticket=88,
                symbol="XAUUSDm",
                type=0,
                volume=float(self.last_request.get("volume", .01)),
                price_open=float(self.last_request.get("price", 100.02)),
                sl=float(self.last_request.get("sl", 99.0)),
                tp=float(self.last_request.get("tp", 101.0)),
                magic=int(self.last_request.get("magic", 0)),
                comment=str(self.last_request.get("comment", "")),
            )
        ]

    def order_check(self, request):
        return SimpleNamespace(retcode=0)

    def order_send(self, request):
        self.sent += 1
        self.last_request = dict(request)
        self.opened = True
        return SimpleNamespace(retcode=10009, order=88, deal=99, comment="done")


def _settings():
    return Settings(
        mode=RuntimeMode.DEMO,
        active_strategy_family=StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
        target_risk_percent=1.0,
        demo_trading_confirm="YES_I_APPROVE_DEMO",
    )


def test_demo_path_never_writes_without_a_complete_trade_setup():
    api = Api()
    result = run_guarded_demo_cycle(_settings(), api, StateStore(), market_open=True)
    assert api.sent in {0, 1}
    if api.sent == 1:
        assert result.intent is not None
        assert result.intent.state.value == "ACCEPTED_VERIFIED"
        assert result.managed_trade is not None
        assert result.managed_trade.ticket == 88
        assert api.last_request["magic"] == _settings().bot_magic

        assert result.cycle.opportunity is not None
        assert result.cycle.trade_plan is not None
        assert result.cycle.timing is not None
        trade = result.managed_trade
        opportunity = result.cycle.opportunity
        plan = result.cycle.trade_plan
        timing = result.cycle.timing
        assert trade.opportunity_id == opportunity.opportunity_id
        assert trade.episode_id == opportunity.episode_id
        assert trade.trade_plan_id == plan.trade_plan_id
        assert trade.entry_reference == plan.entry_reference
        assert trade.m5_source_event_ids == opportunity.source_event_ids
        assert trade.m5_event_time == opportunity.m5_event_time
        assert trade.timing_profile == timing.profile
        assert trade.timing_policy_version == timing.policy_version
        assert trade.timing_trigger_time == timing.trigger_time
        assert trade.m5_event_age_seconds == timing.m5_event_age_seconds
        assert trade.m5_event_age_bars == timing.m5_event_age_bars
        assert trade.trigger_age_seconds == timing.trigger_age_seconds
        assert trade.chase_atr == timing.chase_atr
        assert trade.micro_extension_atr == timing.micro_extension_atr


def test_non_demo_account_is_hard_refused():
    api = Api(account_trade_mode=2)
    with pytest.raises(PermissionError, match="DEMO"):
        run_guarded_demo_cycle(_settings(), api, StateStore(), market_open=True)
    assert api.sent == 0


def test_symbol_open_capability_is_direction_aware():
    api = Api()
    assert symbol_allows_open(api, SimpleNamespace(trade_mode=4), Direction.BUY) is True
    assert symbol_allows_open(api, SimpleNamespace(trade_mode=1), Direction.BUY) is True
    assert symbol_allows_open(api, SimpleNamespace(trade_mode=1), Direction.SELL) is False
    assert symbol_allows_open(api, SimpleNamespace(trade_mode=None), Direction.BUY) is None
