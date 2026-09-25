from datetime import datetime,timezone
from types import SimpleNamespace
from gold_scalp_trader.domain.enums import Direction,ExecutionAction,GateState,IntentState
from gold_scalp_trader.execution.controller import acquire
from gold_scalp_trader.execution.models import ExecutionIntent,GateDecision
from gold_scalp_trader.execution.mt5_writer import Mt5Writer
from gold_scalp_trader.execution.service import execute_once
from gold_scalp_trader.persistence.store import StateStore
UTC=timezone.utc
class FakeApi:
    TRADE_ACTION_DEAL=1; ORDER_TYPE_BUY=0; ORDER_TYPE_SELL=1; TRADE_RETCODE_DONE=10009
    def __init__(self):self.calls=0
    def order_send(self,request):self.calls+=1; return SimpleNamespace(retcode=10009,order=123,deal=456,comment="done")
def intent():return ExecutionIntent("INT-1",ExecutionAction.OPEN,"XAUUSDm",Direction.BUY,.01,100,99,102,IntentState.CREATED,datetime.now(tz=UTC))
def test_persist_before_single_send_and_ack_stays_unresolved_until_reconcile():
    store=StateStore(); lease=acquire(store,"1:XAU","A"); api=FakeApi(); out=execute_once(store=store,intent=intent(),gate=GateDecision(GateState.ALLOW,("PASS",)),lease=lease,writer=Mt5Writer(api),precheck_passed=True); assert api.calls==1 and out.send_count==1 and out.state is IntentState.ACCEPTED_UNKNOWN
def test_precheck_failure_sends_zero_times():
    store=StateStore(); lease=acquire(store,"1:XAU","A"); api=FakeApi(); out=execute_once(store=store,intent=intent(),gate=GateDecision(GateState.ALLOW,("PASS",)),lease=lease,writer=Mt5Writer(api),precheck_passed=False); assert api.calls==0 and out.send_count==0 and out.state is IntentState.FAILED
