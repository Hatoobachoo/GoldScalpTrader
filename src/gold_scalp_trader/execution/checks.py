from dataclasses import dataclass
from gold_scalp_trader.domain.market import AccountFacts,Quote,SymbolSpec
@dataclass(frozen=True,slots=True)
class PrecheckResult:passed:bool; reasons:tuple[str,...]
def evaluate(account:AccountFacts,spec:SymbolSpec,quote:Quote,volume:float)->PrecheckResult:
    reasons=[]
    if account.trade_allowed is not True:reasons.append("ACCOUNT_TRADING_DISABLED_OR_UNKNOWN")
    if account.trade_expert is not True:reasons.append("ACCOUNT_EXPERT_DISABLED_OR_UNKNOWN")
    if volume<spec.volume_min or volume>spec.volume_max:reasons.append("VOLUME_OUT_OF_RANGE")
    steps=round((volume-spec.volume_min)/spec.volume_step) if volume>=spec.volume_min else -1; normalized=spec.volume_min+max(0,steps)*spec.volume_step
    if abs(normalized-volume)>1e-8:reasons.append("VOLUME_STEP_INVALID")
    if quote.age_seconds< -2:reasons.append("QUOTE_FUTURE_CORRUPT")
    return PrecheckResult(not reasons,tuple(reasons) or ("PASS",))
