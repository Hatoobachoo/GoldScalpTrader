from dataclasses import dataclass
from .fusion import DecisionBoard
from .opportunity import Opportunity
from .timing import TimingDecision
from .trade_plan import TradePlan
from .executable_quality import ExecutableQuality
@dataclass(frozen=True,slots=True)
class DecisionSnapshot:
    board:DecisionBoard; opportunity:Opportunity|None; timing:TimingDecision|None; trade_plan:TradePlan|None; executable_quality:ExecutableQuality|None
