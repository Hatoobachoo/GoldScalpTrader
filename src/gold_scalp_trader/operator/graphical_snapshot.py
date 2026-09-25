from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from gold_scalp_trader.app.cycle import CycleResult
from gold_scalp_trader.operator.presentation import DashboardData

if TYPE_CHECKING:
    from gold_scalp_trader.app.runtime import RuntimeResult


def from_cycle(result: CycleResult, market_state: str = "UNKNOWN") -> DashboardData:
    market = result.intelligence.market
    qualified = [candidate.family.value for candidate in result.registry.qualified]
    detected = ", ".join(qualified) if qualified else "NO VALID SETUP"
    active = result.isolation.active_family.value if result.isolation.active_family else "UNSET"
    shadow = tuple(
        item.candidate.family.value
        for item in result.isolation.candidates
        if item.candidate.qualified and item.candidate is not result.isolation.live_candidate
    )
    risk = (
        "NOT EVALUATED"
        if result.risk is None
        else f"{result.risk.decision.value} • {result.risk.actual_risk_pct if result.risk.actual_risk_pct is not None else '—'}%"
    )
    plan = "NOT AVAILABLE"
    if result.trade_plan is not None:
        p = result.trade_plan
        plan = (
            f"{p.direction.value}  Entry {p.entry_reference:.3f}\n"
            f"SL {p.initial_sl:.3f}  Primary {p.primary_target:.3f}\n"
            f"Expansion {p.expansion_target:.3f}  Gross R {p.gross_r:.2f}"
            if p.expansion_target is not None
            else (
                f"{p.direction.value}  Entry {p.entry_reference:.3f}\n"
                f"SL {p.initial_sl:.3f}  Primary {p.primary_target:.3f}\n"
                f"Gross R {p.gross_r:.2f}"
            )
        )
    positions = "UNKNOWN" if market.positions is None else str(len(market.positions))
    return DashboardData(
        market.symbol_spec.symbol,
        market.quote.bid,
        market.quote.ask,
        market.quote.spread,
        market_state,
        result.intelligence.session.label,
        result.status,
        detected,
        active,
        result.live_action,
        result.reason,
        shadow,
        risk,
        result.gate_text,
        "SOFT CONTEXT",
        result.system_text,
        trade_plan_text=plan,
        activity_text=f"Open Gold positions: {positions}",
    )


def from_runtime(result: "RuntimeResult", market_state: str = "DEMO") -> DashboardData:
    data = from_cycle(result.cycle, market_state=market_state)
    managed_text = "NONE"
    if result.managed_trade is not None:
        trade = result.managed_trade
        managed_text = (
            f"#{trade.ticket} • {trade.family.value}\n"
            f"Entry {trade.entry:.3f}  SL {trade.current_sl:.3f}\n"
            f"Primary {trade.primary_target:.3f}"
        )
        if trade.expansion_target is not None:
            managed_text += f"  Expansion {trade.expansion_target:.3f}"

    execution_text = "IDLE"
    if result.intent is not None:
        intent = result.intent
        execution_text = (
            f"{intent.action.value} • {intent.state.value}\n"
            f"Intent {intent.intent_id}\nSend count {intent.send_count}"
        )
    if result.management_action is not None:
        execution_text += f"\nManager {result.management_action.value}"

    return replace(
        data,
        managed_trade_text=managed_text,
        execution_text=execution_text,
        learning_text="Actual / shadow evidence collection active",
    )
