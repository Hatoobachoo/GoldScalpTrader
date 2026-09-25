from datetime import datetime, timedelta, timezone

from gold_scalp_trader.domain.enums import Direction, ManagementAction, StrategyFamily
from gold_scalp_trader.execution.models import ExecutionIntent
from gold_scalp_trader.management.closure import (
    RECEIPT_NS,
    archive_verified_close,
    close_origin,
    complete_exit_proved,
)
from gold_scalp_trader.management.execution import to_intent
from gold_scalp_trader.management.manager import ManagementDecision
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.management.store import load, save
from gold_scalp_trader.market_data.activity import DealFacts
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.live_learning import QUEUE

UTC = timezone.utc


def _trade() -> ManagedTrade:
    opened = datetime(2026, 9, 25, 12, 0, tzinfo=UTC)
    return ManagedTrade(
        "TRD-1",
        88,
        "XAUUSDm",
        Direction.BUY,
        0.01,
        100.0,
        99.0,
        99.0,
        101.0,
        102.0,
        StrategyFamily.TREND_PULLBACK_CONTINUATION,
        "v1",
        1.0,
        opened,
    )


def _exit_deal(volume: float, *, magic: int = 560501, minutes: int = 5) -> DealFacts:
    return DealFacts(
        ticket=900 + minutes,
        position_id=88,
        symbol="XAUUSDm",
        direction=Direction.SELL,
        volume=volume,
        profit=10.0,
        commission=-0.1,
        swap=0.0,
        fee=0.0,
        magic=magic,
        entry_role="OUT",
        deal_type="SELL",
        time_utc=datetime(2026, 9, 25, 12, minutes, tzinfo=UTC),
        comment="close",
    )


def test_managed_trade_store_preserves_open_time():
    store = StateStore()
    trade = _trade()
    save(store, "scope", trade)
    restored = load(store, "scope")
    assert restored == trade
    store.close()


def test_protect_modify_preserves_expansion_tp():
    trade = _trade()
    decision = ManagementDecision(ManagementAction.PROTECT, "earned", proposed_sl=100.0)
    intent = to_intent(
        decision,
        trade,
        price=None,
        as_of=datetime(2026, 9, 25, 12, 6, tzinfo=UTC),
    )
    assert intent is not None
    assert intent.action.value == "MODIFY"
    assert intent.sl == 100.0
    assert intent.tp == 102.0


def test_full_exit_volume_is_required_before_archive():
    trade = _trade()
    partial = (_exit_deal(0.005),)
    full = (_exit_deal(0.01),)
    assert complete_exit_proved(partial, trade) is False
    assert complete_exit_proved(full, trade) is True
    assert close_origin(full, trade, bot_magic=560501) == "BOT"
    assert close_origin((_exit_deal(0.01, magic=0),), trade, bot_magic=560501) == "EXTERNAL"


def test_verified_close_archives_before_clearing_managed_trade():
    store = StateStore()
    trade = _trade()
    save(store, "scope", trade)
    deals = (_exit_deal(0.01),)
    archive_verified_close(
        store,
        "scope",
        trade,
        deals,
        bot_magic=560501,
        close_intent_id="INT-CLOSE-1",
        reason="TEST_CLOSE",
    )
    assert load(store, "scope") is None
    assert store.get(RECEIPT_NS, trade.trade_id) is not None
    assert store.get(QUEUE, trade.trade_id) is not None
    store.close()
