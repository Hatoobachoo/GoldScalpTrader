from datetime import datetime,timezone
from types import SimpleNamespace
from gold_scalp_trader.domain.enums import Direction,ExecutionAction,IntentState
from gold_scalp_trader.domain.market import PositionFacts
from gold_scalp_trader.execution.models import ExecutionIntent
from gold_scalp_trader.execution.mt5_writer import Mt5Writer
from gold_scalp_trader.execution.reconcile import close_matches,modify_matches
UTC=timezone.utc
def intent(action):return ExecutionIntent("I",action,"XAUUSDm",Direction.BUY,.01,None,100,102,IntentState.CREATED,datetime.now(tz=UTC),position_ticket=77)
def test_modify_and_close_requests_target_exact_ticket():
    api=SimpleNamespace(TRADE_ACTION_SLTP=6,TRADE_ACTION_DEAL=1,ORDER_TYPE_SELL=1,ORDER_TYPE_BUY=0);w=Mt5Writer(api);assert w.build_request(intent(ExecutionAction.MODIFY))["position"]==77;assert w.build_request(intent(ExecutionAction.CLOSE))["position"]==77
def test_action_specific_reconciliation():
    p=PositionFacts(77,"XAUUSDm",Direction.BUY,.01,101,100,102,1,"");assert modify_matches(intent(ExecutionAction.MODIFY),(p,)) is True;assert close_matches(intent(ExecutionAction.CLOSE),(p,)) is False;assert close_matches(intent(ExecutionAction.CLOSE),()) is True;assert close_matches(intent(ExecutionAction.CLOSE),None) is None
