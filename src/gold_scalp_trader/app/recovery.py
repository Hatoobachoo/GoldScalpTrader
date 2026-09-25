from dataclasses import dataclass
from gold_scalp_trader.execution.intent_store import unresolved
from gold_scalp_trader.persistence.store import StateStore
@dataclass(frozen=True,slots=True)
class RecoveryStatus:ready:bool; reason:str; unresolved_intents:int
def inspect(store:StateStore)->RecoveryStatus:
    p=unresolved(store); return RecoveryStatus(not p,"READY" if not p else "RECONCILE_INTENTS",len(p))
