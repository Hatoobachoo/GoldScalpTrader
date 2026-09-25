"""SOLE raw irreversible MetaTrader 5 write boundary; action-specific and retry-free."""
from __future__ import annotations
from typing import Any
from gold_scalp_trader.domain.enums import ExecutionAction
from .models import BrokerAck, ExecutionIntent


class Mt5Writer:
    def __init__(self, api: Any, *, magic: int | None = None, comment_prefix: str = "GST"):
        self.api = api
        self.magic = magic
        self.comment_prefix = comment_prefix

    def _comment(self, intent: ExecutionIntent) -> str:
        base = f"{self.comment_prefix}:{intent.intent_id}" if self.comment_prefix else intent.intent_id
        return base[:31]

    def build_request(self, intent: ExecutionIntent) -> dict:
        common = {"comment": self._comment(intent)}
        if self.magic is not None:
            common["magic"] = self.magic

        if intent.action is ExecutionAction.OPEN:
            request = {
                "action": getattr(self.api, "TRADE_ACTION_DEAL", 1),
                "symbol": intent.symbol,
                "volume": intent.volume,
                "sl": intent.sl or 0.0,
                "tp": intent.tp or 0.0,
                "type": getattr(self.api, "ORDER_TYPE_BUY", 0)
                if intent.direction.value == "BUY"
                else getattr(self.api, "ORDER_TYPE_SELL", 1),
                **common,
            }
            if intent.price is not None:
                request["price"] = intent.price
            return request

        if intent.position_ticket is None:
            raise ValueError(f"{intent.action.value} requires position_ticket")

        if intent.action is ExecutionAction.MODIFY:
            return {
                "action": getattr(self.api, "TRADE_ACTION_SLTP", 6),
                "position": intent.position_ticket,
                "symbol": intent.symbol,
                "sl": intent.sl or 0.0,
                "tp": intent.tp or 0.0,
                **common,
            }

        request = {
            "action": getattr(self.api, "TRADE_ACTION_DEAL", 1),
            "position": intent.position_ticket,
            "symbol": intent.symbol,
            "volume": intent.volume,
            "type": getattr(self.api, "ORDER_TYPE_SELL", 1)
            if intent.direction.value == "BUY"
            else getattr(self.api, "ORDER_TYPE_BUY", 0),
            **common,
        }
        if intent.price is not None:
            request["price"] = intent.price
        return request

    def send_once(self, intent: ExecutionIntent) -> BrokerAck:
        try:
            raw = self.api.order_send(self.build_request(intent))
        except Exception as exc:
            return BrokerAck(False, False, True, None, None, None, f"transport exception: {type(exc).__name__}")
        if raw is None:
            return BrokerAck(False, False, True, None, None, None, "order_send returned None")
        ret = getattr(raw, "retcode", None)
        order = getattr(raw, "order", None)
        deal = getattr(raw, "deal", None)
        comment = str(getattr(raw, "comment", "") or "")
        success = {
            getattr(self.api, "TRADE_RETCODE_DONE", 10009),
            getattr(self.api, "TRADE_RETCODE_PLACED", 10008),
            getattr(self.api, "TRADE_RETCODE_DONE_PARTIAL", 10010),
        }
        if ret in success:
            return BrokerAck(True, False, False, ret, order, deal, comment)
        if ret is None:
            return BrokerAck(False, False, True, None, order, deal, comment)
        return BrokerAck(False, True, False, ret, order, deal, comment)
