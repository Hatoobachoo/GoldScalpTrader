"""Hard Risk permission composition; News is intentionally absent."""
from datetime import datetime
from gold_scalp_trader.domain.enums import RiskDecision
from .engine import RiskEvaluation
from .state import RiskState,cooldown_released
def permission(evaluation:RiskEvaluation,state:RiskState,as_of:datetime,*,context_healthy:bool=True,unresolved_lifecycle:bool=False)->tuple[RiskDecision,str]:
    if state.loss_locked:return RiskDecision.BLOCK,"DAILY_LOSS_LOCK"
    if not cooldown_released(state,as_of,context_healthy=context_healthy,unresolved_lifecycle=unresolved_lifecycle):return RiskDecision.BLOCK,"CONSECUTIVE_LOSS_COOLDOWN"
    return evaluation.decision,evaluation.reason
