"""Translate management decisions into governed MODIFY/CLOSE Intents."""
from datetime import datetime
from gold_scalp_trader.domain.enums import ExecutionAction,IntentState,ManagementAction
from gold_scalp_trader.domain.ids import new_id
from gold_scalp_trader.execution.models import ExecutionIntent
from .manager import ManagementDecision
from .models import ManagedTrade
def to_intent(decision:ManagementDecision,trade:ManagedTrade,*,price:float|None,as_of:datetime)->ExecutionIntent|None:
    if decision.action in {ManagementAction.HOLD,ManagementAction.RUNNER}:return None
    action=ExecutionAction.CLOSE if decision.action is ManagementAction.EXIT else ExecutionAction.MODIFY
    return ExecutionIntent(str(new_id("INT")),action,trade.symbol,trade.direction,trade.volume,price if action is ExecutionAction.CLOSE else None,decision.proposed_sl if action is ExecutionAction.MODIFY else None,decision.proposed_tp if action is ExecutionAction.MODIFY else None,IntentState.CREATED,as_of,position_ticket=trade.ticket)
