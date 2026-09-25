from datetime import datetime, timezone

from gold_scalp_trader.domain.enums import Direction, ExecutionAction, IntentState
from gold_scalp_trader.execution.models import ExecutionIntent
from gold_scalp_trader.execution.mt5_writer import Mt5Writer


class Api:
    TRADE_ACTION_DEAL = 1
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1


def test_writer_stamps_magic_and_comment_prefix():
    intent = ExecutionIntent(
        "INT-123456789",
        ExecutionAction.OPEN,
        "XAUUSDm",
        Direction.BUY,
        0.01,
        100.0,
        99.0,
        102.0,
        IntentState.CREATED,
        datetime.now(tz=timezone.utc),
    )
    request = Mt5Writer(Api(), magic=560501, comment_prefix="GST").build_request(intent)
    assert request["magic"] == 560501
    assert request["comment"].startswith("GST:INT-")
    assert len(request["comment"]) <= 31
