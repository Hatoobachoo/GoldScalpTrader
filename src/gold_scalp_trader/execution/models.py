from __future__ import annotations
from dataclasses import dataclass,replace
from datetime import datetime
from gold_scalp_trader.domain.enums import Direction,ExecutionAction,GateState,IntentState
@dataclass(frozen=True,slots=True)
class GateDecision:state:GateState; reasons:tuple[str,...]
@dataclass(frozen=True,slots=True)
class ExecutionIntent:
    intent_id:str; action:ExecutionAction; symbol:str; direction:Direction; volume:float; price:float|None; sl:float|None; tp:float|None; state:IntentState; created_at:datetime; send_count:int=0; broker_ticket:int|None=None; position_ticket:int|None=None; reason:str=""
    def with_state(self,state:IntentState,**changes):return replace(self,state=state,**changes)
@dataclass(frozen=True,slots=True)
class BrokerAck:success_like:bool; rejected:bool; ambiguous:bool; retcode:int|None; order:int|None; deal:int|None; comment:str=""
