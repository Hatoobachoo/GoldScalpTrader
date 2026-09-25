"""Persist-before-send, one-shot execution service."""
from gold_scalp_trader.domain.enums import GateState,IntentState
from gold_scalp_trader.persistence.store import StateStore
from .controller import ControllerLease,verify
from .intent_store import save
from .models import ExecutionIntent,GateDecision
from .mt5_writer import Mt5Writer
def execute_once(*,store:StateStore,intent:ExecutionIntent,gate:GateDecision,lease:ControllerLease,writer:Mt5Writer,precheck_passed:bool)->ExecutionIntent:
    if intent.send_count!=0 or intent.state not in {IntentState.CREATED,IntentState.APPROVED}:raise RuntimeError("Intent already consumed or illegal state")
    save(store,intent)
    if gate.state is not GateState.ALLOW:
        out=intent.with_state(IntentState.FAILED,reason="GATE_BLOCKED"); save(store,out); return out
    if not verify(store,lease):
        out=intent.with_state(IntentState.FAILED,reason="CONTROLLER_FENCED"); save(store,out); return out
    if not precheck_passed:
        out=intent.with_state(IntentState.FAILED,reason="PRECHECK_FAILED"); save(store,out); return out
    submitting=intent.with_state(IntentState.SUBMITTING,send_count=1); save(store,submitting); ack=writer.send_once(submitting)
    if ack.ambiguous:out=submitting.with_state(IntentState.ACCEPTED_UNKNOWN,reason=ack.comment)
    elif ack.rejected:out=submitting.with_state(IntentState.FAILED,reason=f"BROKER_REJECTED:{ack.retcode}")
    else:out=submitting.with_state(IntentState.ACCEPTED_UNKNOWN,broker_ticket=ack.order or ack.deal,reason="ACK_SUCCESS_RECONCILE_REQUIRED")
    save(store,out); return out
