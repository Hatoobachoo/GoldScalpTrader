"""Hard Risk permission composition; News is intentionally absent."""
from datetime import datetime
from gold_scalp_trader.domain.enums import RiskDecision
from .engine import RiskEvaluation
from .state import RiskState
def permission(evaluation:RiskEvaluation,state:RiskState,as_of:datetime)->tuple[RiskDecision,str]:
    if state.loss_locked:return RiskDecision.BLOCK,"DAILY_LOSS_LOCK"
    if state.cooldown_until is not None and as_of<state.cooldown_until:return RiskDecision.BLOCK,"CONSECUTIVE_LOSS_COOLDOWN"
    return evaluation.decision,evaluation.reason
