"""Family-aware invalidation extension points."""
from gold_scalp_trader.domain.enums import StrategyFamily
def preferred_invalidation_source(family:StrategyFamily)->tuple[str,...]:
    if family is StrategyFamily.BREAKOUT_RETEST_CONTINUATION: return ("M5_RETEST_FAILURE","M15_STRUCTURE","H1_STRUCTURE")
    if family is StrategyFamily.LIQUIDITY_SWEEP_REVERSAL: return ("M5_SWEEP_EXTREME","M5_STRUCTURE","M15_STRUCTURE")
    if family is StrategyFamily.FAILED_BREAKOUT_REVERSAL: return ("M5_FAILED_BREAK_EXTREME","M5_STRUCTURE","M15_STRUCTURE")
    return ("M5_STRUCTURE","M15_STRUCTURE","H1_STRUCTURE")
