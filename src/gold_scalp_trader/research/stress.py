from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class StressScenario:spread_multiplier:float=1.0; slippage_add:float=0.0; latency_ms:int=0
