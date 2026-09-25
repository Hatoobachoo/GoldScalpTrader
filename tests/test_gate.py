from gold_scalp_trader.domain.enums import ExecutionAction, GateState, RiskDecision
from gold_scalp_trader.execution.gate import evaluate


def test_gate_requires_all_hard_authorities_and_has_no_news_input():
    assert evaluate(
        risk=RiskDecision.PASS,
        market_open=True,
        data_ready=True,
        identity_ready=True,
        exposure_clear=True,
        persistence_ready=True,
        controller_ready=True,
        conflicting_intent=False,
    ).state is GateState.ALLOW
    assert evaluate(
        risk=RiskDecision.PASS,
        market_open=None,
        data_ready=True,
        identity_ready=True,
        exposure_clear=True,
        persistence_ready=True,
        controller_ready=True,
        conflicting_intent=False,
    ).state is GateState.BLOCKED


def test_management_actions_are_not_blocked_by_entry_only_risk_or_capacity():
    close_gate = evaluate(
        risk=RiskDecision.BLOCK,
        market_open=True,
        data_ready=True,
        identity_ready=True,
        exposure_clear=False,
        persistence_ready=True,
        controller_ready=True,
        conflicting_intent=False,
        action=ExecutionAction.CLOSE,
    )
    modify_gate = evaluate(
        risk=RiskDecision.UNKNOWN,
        market_open=True,
        data_ready=True,
        identity_ready=True,
        exposure_clear=False,
        persistence_ready=True,
        controller_ready=True,
        conflicting_intent=False,
        action=ExecutionAction.MODIFY,
    )
    assert close_gate.state is GateState.ALLOW
    assert modify_gate.state is GateState.ALLOW
