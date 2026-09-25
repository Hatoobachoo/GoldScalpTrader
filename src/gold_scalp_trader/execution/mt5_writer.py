"""SOLE raw irreversible MetaTrader 5 write boundary; action-specific and retry-free."""
from __future__ import annotations
from typing import Any
from gold_scalp_trader.domain.enums import ExecutionAction
from .models import BrokerAck,ExecutionIntent
class Mt5Writer:
    def __init__(self,api:Any):self.api=api
    def build_request(self,intent:ExecutionIntent)->dict:
        if intent.action is ExecutionAction.OPEN:
            r={"action":getattr(self.api,"TRADE_ACTION_DEAL",1),"symbol":intent.symbol,"volume":intent.volume,"sl":intent.sl or 0.0,"tp":intent.tp or 0.0,"comment":intent.intent_id[:28],"type":getattr(self.api,"ORDER_TYPE_BUY",0) if intent.direction.value=="BUY" else getattr(self.api,"ORDER_TYPE_SELL",1)}
            if intent.price is not None:r["price"]=intent.price
            return r
        if intent.position_ticket is None:raise ValueError(f"{intent.action.value} requires position_ticket")
        if intent.action is ExecutionAction.MODIFY:return {"action":getattr(self.api,"TRADE_ACTION_SLTP",6),"position":intent.position_ticket,"symbol":intent.symbol,"sl":intent.sl or 0.0,"tp":intent.tp or 0.0,"comment":intent.intent_id[:28]}
        r={"action":getattr(self.api,"TRADE_ACTION_DEAL",1),"position":intent.position_ticket,"symbol":intent.symbol,"volume":intent.volume,"comment":intent.intent_id[:28],"type":getattr(self.api,"ORDER_TYPE_SELL",1) if intent.direction.value=="BUY" else getattr(self.api,"ORDER_TYPE_BUY",0)}
        if intent.price is not None:r["price"]=intent.price
        return r
    def send_once(self,intent:ExecutionIntent)->BrokerAck:
        try:raw=self.api.order_send(self.build_request(intent))
        except Exception as exc:return BrokerAck(False,False,True,None,None,None,f"transport exception: {type(exc).__name__}")
        if raw is None:return BrokerAck(False,False,True,None,None,None,"order_send returned None")
        ret=getattr(raw,"retcode",None); order=getattr(raw,"order",None); deal=getattr(raw,"deal",None); comment=str(getattr(raw,"comment","") or ""); success={getattr(self.api,"TRADE_RETCODE_DONE",10009),getattr(self.api,"TRADE_RETCODE_PLACED",10008),getattr(self.api,"TRADE_RETCODE_DONE_PARTIAL",10010)}
        if ret in success:return BrokerAck(True,False,False,ret,order,deal,comment)
        if ret is None:return BrokerAck(False,False,True,None,order,deal,comment)
        return BrokerAck(False,True,False,ret,order,deal,comment)
