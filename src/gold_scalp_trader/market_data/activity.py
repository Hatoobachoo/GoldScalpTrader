"""Broker activity normalization and account-safety accounting.

This module separates bot performance, external/manual trading and non-trading
cash flow. Missing broker history is represented as UNKNOWN rather than zero.
It contains no broker-write authority.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from typing import Iterable
from gold_scalp_trader.domain.enums import DataQuality, Direction

@dataclass(frozen=True, slots=True)
class DealFacts:
    ticket:int; position_id:int|None; symbol:str; direction:Direction|None; volume:float; profit:float; commission:float; swap:float; fee:float; magic:int|None; entry_role:str; deal_type:str; time_utc:datetime; comment:str=""
    @property
    def net_money(self)->float:return self.profit+self.commission+self.swap+self.fee

@dataclass(frozen=True, slots=True)
class ActivitySummary:
    quality:DataQuality; bot_entries:int|None=None; bot_realized:float|None=None; external_realized:float|None=None; external_open_positions:int|None=None; net_non_trading_cash_flow:float|None=None; reason:str=""

def classify_deals(deals:Iterable[DealFacts]|None,*,bot_magic:int,external_open_positions:int|None=None)->ActivitySummary:
    if deals is None:return ActivitySummary(DataQuality.UNKNOWN,reason="DEAL_HISTORY_UNAVAILABLE")
    bot_positions:set[int]=set(); bot_realized=0.0; external_realized=0.0; non_trading_cash=0.0
    for deal in deals:
        if not all(isfinite(v) for v in (deal.volume,deal.profit,deal.commission,deal.swap,deal.fee)):return ActivitySummary(DataQuality.CORRUPT,reason="NON_FINITE_DEAL_VALUE")
        role=deal.entry_role.upper(); dtype=deal.deal_type.upper(); is_trade=dtype in {"BUY","SELL","TRADE"}; is_cash=dtype in {"BALANCE","CREDIT","DEBIT","BONUS","INTEREST","DIVIDEND","TAX"}; is_bot=deal.magic==bot_magic
        if is_trade:
            if is_bot and role in {"IN","INOUT"} and deal.position_id is not None:bot_positions.add(deal.position_id)
            if role in {"OUT","OUT_BY","INOUT"}:
                if is_bot:bot_realized+=deal.net_money
                else:external_realized+=deal.net_money
        elif is_cash:non_trading_cash+=deal.net_money
        elif abs(deal.net_money)>1e-12:return ActivitySummary(DataQuality.UNKNOWN,reason=f"UNCLASSIFIED_MONETARY_DEAL:{dtype}")
    return ActivitySummary(DataQuality.HEALTHY,len(bot_positions),bot_realized,external_realized,external_open_positions,non_trading_cash,"PASS")

def account_safety_pl(*,current_equity:float,day_start_equity:float,net_non_trading_cash_flow:float)->float:
    if day_start_equity<=0:raise ValueError("DayStartEquity must be positive")
    if not all(isfinite(v) for v in (current_equity,day_start_equity,net_non_trading_cash_flow)):raise ValueError("account-safety inputs must be finite")
    return current_equity-day_start_equity-net_non_trading_cash_flow
