from __future__ import annotations
from gold_scalp_trader.operator.presentation import DashboardData
from gold_scalp_trader.app.cycle import CycleResult
def from_cycle(result:CycleResult,market_state:str="UNKNOWN")->DashboardData:
    m=result.intelligence.market; qualified=[c.family.value for c in result.registry.qualified]; detected=", ".join(qualified) if qualified else "NO VALID SETUP"; active=result.isolation.active_family.value if result.isolation.active_family else "UNSET"; shadow=tuple(x.candidate.family.value for x in result.isolation.candidates if x.candidate.qualified and x.candidate is not result.isolation.live_candidate)
    risk="NOT EVALUATED" if result.risk is None else f"{result.risk.decision.value} • {result.risk.actual_risk_pct if result.risk.actual_risk_pct is not None else '—'}%"
    return DashboardData(m.symbol_spec.symbol,m.quote.bid,m.quote.ask,m.quote.spread,market_state,result.intelligence.session.label,result.status,detected,active,result.live_action,result.reason,shadow,risk,result.gate_text,"SOFT CONTEXT",result.system_text)
