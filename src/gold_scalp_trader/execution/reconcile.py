from gold_scalp_trader.domain.market import PositionFacts
from .models import ExecutionIntent
def open_matches(intent:ExecutionIntent,positions:tuple[PositionFacts,...]|None)->PositionFacts|None:
    if positions is None:return None
    candidates=[p for p in positions if p.symbol==intent.symbol and p.direction is intent.direction and abs(p.volume-intent.volume)<=1e-8]; return candidates[0] if len(candidates)==1 else None
