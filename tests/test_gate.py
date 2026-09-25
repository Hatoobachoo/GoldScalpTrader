from gold_scalp_trader.domain.enums import GateState,RiskDecision
from gold_scalp_trader.execution.gate import evaluate
def test_gate_requires_all_hard_authorities_and_has_no_news_input():
    assert evaluate(risk=RiskDecision.PASS,market_open=True,data_ready=True,identity_ready=True,exposure_clear=True,persistence_ready=True,controller_ready=True,conflicting_intent=False).state is GateState.ALLOW
    assert evaluate(risk=RiskDecision.PASS,market_open=None,data_ready=True,identity_ready=True,exposure_clear=True,persistence_ready=True,controller_ready=True,conflicting_intent=False).state is GateState.BLOCKED
