"""Central action-sensitive hard-permission Gate."""
from gold_scalp_trader.domain.enums import ExecutionAction, GateState, RiskDecision
from .models import GateDecision


def evaluate(
    *,
    risk: RiskDecision,
    market_open: bool | None,
    data_ready: bool,
    identity_ready: bool,
    exposure_clear: bool | None,
    persistence_ready: bool,
    controller_ready: bool,
    conflicting_intent: bool,
    action: ExecutionAction = ExecutionAction.OPEN,
) -> GateDecision:
    reasons: list[str] = []

    # Monetary affordability and flat-capacity are OPEN-only authorities.
    # MODIFY/CLOSE manage already-existing exposure and must not be trapped by
    # an entry-only risk/capacity rule.
    if action is ExecutionAction.OPEN and risk is not RiskDecision.PASS:
        reasons.append(f"RISK_{risk.value}")
    if market_open is not True:
        reasons.append("MARKET_UNKNOWN_OR_CLOSED")
    if not data_ready:
        reasons.append("DATA_NOT_READY")
    if not identity_ready:
        reasons.append("IDENTITY_NOT_READY")
    if action is ExecutionAction.OPEN and exposure_clear is not True:
        reasons.append("EXPOSURE_UNKNOWN_OR_OCCUPIED")
    if not persistence_ready:
        reasons.append("PERSISTENCE_NOT_READY")
    if not controller_ready:
        reasons.append("CONTROLLER_NOT_READY")
    if conflicting_intent:
        reasons.append("CONFLICTING_INTENT")

    return GateDecision(
        GateState.ALLOW if not reasons else GateState.BLOCKED,
        tuple(reasons) or ("PASS",),
    )
