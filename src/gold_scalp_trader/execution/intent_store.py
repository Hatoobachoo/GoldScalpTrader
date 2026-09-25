from __future__ import annotations
from datetime import datetime
from gold_scalp_trader.domain.enums import Direction,ExecutionAction,IntentState
from gold_scalp_trader.persistence.store import StateStore
from .models import ExecutionIntent
NS="execution_intents"
def save(store:StateStore,intent:ExecutionIntent)->None:store.put(NS,intent.intent_id,{"intent_id":intent.intent_id,"action":intent.action.value,"symbol":intent.symbol,"direction":intent.direction.value,"volume":intent.volume,"price":intent.price,"sl":intent.sl,"tp":intent.tp,"state":intent.state.value,"created_at":intent.created_at.isoformat(),"send_count":intent.send_count,"broker_ticket":intent.broker_ticket,"reason":intent.reason})
def load(store:StateStore,intent_id:str)->ExecutionIntent|None:
    r=store.get(NS,intent_id)
    if r is None:return None
    p=r.payload; return ExecutionIntent(str(p["intent_id"]),ExecutionAction(p["action"]),str(p["symbol"]),Direction(p["direction"]),float(p["volume"]),None if p["price"] is None else float(p["price"]),None if p["sl"] is None else float(p["sl"]),None if p["tp"] is None else float(p["tp"]),IntentState(p["state"]),datetime.fromisoformat(p["created_at"]),int(p["send_count"]),None if p["broker_ticket"] is None else int(p["broker_ticket"]),str(p["reason"]))
def unresolved(store:StateStore)->tuple[ExecutionIntent,...]:
    out=[]
    for r in store.list_records(NS):
        x=load(store,r.key)
        if x and x.state in {IntentState.SUBMITTING,IntentState.ACCEPTED_UNKNOWN}:out.append(x)
    return tuple(out)
