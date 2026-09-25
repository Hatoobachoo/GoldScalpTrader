from datetime import datetime, timezone
from types import SimpleNamespace

from gold_scalp_trader.config import Settings
from gold_scalp_trader.market_data.mt5_reader import Mt5Reader

UTC = timezone.utc


class Api:
    DEAL_TYPE_BUY = 0
    DEAL_TYPE_SELL = 1
    DEAL_ENTRY_IN = 0
    DEAL_ENTRY_OUT = 1
    DEAL_ENTRY_INOUT = 2
    DEAL_ENTRY_OUT_BY = 3

    def history_deals_get(self, date_from, date_to, position=None):
        return [
            SimpleNamespace(
                ticket=10,
                position_id=position,
                symbol="XAUUSDm",
                type=1,
                entry=1,
                volume=0.01,
                profit=5.0,
                commission=-0.1,
                swap=0.0,
                fee=0.0,
                magic=560501,
                time=int(datetime(2026, 9, 25, 12, 5, tzinfo=UTC).timestamp()),
                time_msc=0,
                comment="close",
            )
        ]


def test_position_deal_history_is_normalized_for_close_proof():
    reader = Mt5Reader(Settings(), Api())
    deals = reader.read_position_deals(
        88,
        from_time=datetime(2026, 9, 25, 12, 0, tzinfo=UTC),
        to_time=datetime(2026, 9, 25, 12, 10, tzinfo=UTC),
    )
    assert deals is not None
    assert len(deals) == 1
    assert deals[0].position_id == 88
    assert deals[0].entry_role == "OUT"
    assert deals[0].deal_type == "SELL"
    assert deals[0].net_money == 4.9
