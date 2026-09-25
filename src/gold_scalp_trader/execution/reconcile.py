"""Action-specific broker reconciliation helpers."""
from gold_scalp_trader.domain.market import PositionFacts
from .models import ExecutionIntent
def open_matches(intent:ExecutionIntent,positions:tuple[PositionFacts,...]|None)->PositionFacts|None:
    if positions is None:return None
    c=[p for p in positions if p.symbol==intent.symbol and p.direction is intent.direction and abs(p.volume-intent.volume)<=1e-8]; return c[0] if len(c)==1 else None
def modify_matches(intent:ExecutionIntent,positions:tuple[PositionFacts,...]|None,*,tolerance:float=1e-8)->bool|None:
    if positions is None:return None
    if intent.position_ticket is None:return False
    p=next((p for p in positions if p.ticket==intent.position_ticket),None)
    if p is None:return False
    return (intent.sl is None or (p.sl is not None and abs(p.sl-intent.sl)<=tolerance)) and (intent.tp is None or (p.tp is not None and abs(p.tp-intent.tp)<=tolerance))
def close_matches(intent:ExecutionIntent,positions:tuple[PositionFacts,...]|None)->bool|None:
    if positions is None:return None
    if intent.position_ticket is None:return False
    return next((p for p in positions if p.ticket==intent.position_ticket),None) is None
