from dataclasses import dataclass
from gold_scalp_trader.domain.enums import ManagementAction,Timeframe
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot
from .models import ManagedTrade
@dataclass(frozen=True,slots=True)
class ManagementDecision:action:ManagementAction; reason:str; proposed_sl:float|None=None; proposed_tp:float|None=None
def evaluate(trade:ManagedTrade,snapshot:IntelligenceSnapshot,bars_in_trade:int)->ManagementDecision:
    m5=snapshot.by_timeframe.get(Timeframe.M5)
    if m5 is None:return ManagementDecision(ManagementAction.HOLD,"M5 management context unavailable")
    price=snapshot.market.quote.bid if trade.direction.value=="BUY" else snapshot.market.quote.ask; open_r=(price-trade.entry)/trade.original_r_price if trade.direction.value=="BUY" else (trade.entry-price)/trade.original_r_price
    if open_r<=-1:return ManagementDecision(ManagementAction.EXIT,"structural/original risk exhausted")
    if bars_in_trade>=6 and open_r<.25:return ManagementDecision(ManagementAction.EXIT,"TIME_EFFICIENCY_FAILURE")
    if open_r>=1 and trade.current_sl==trade.original_sl:
        proposed=max(trade.current_sl,trade.entry) if trade.direction.value=="BUY" else min(trade.current_sl,trade.entry); return ManagementDecision(ManagementAction.PROTECT,"earned protection after >=1R",proposed)
    return ManagementDecision(ManagementAction.HOLD,"thesis remains active")
