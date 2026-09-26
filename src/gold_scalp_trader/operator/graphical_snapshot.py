from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from gold_scalp_trader.app.cycle import CycleResult
from gold_scalp_trader.operator.presentation import DashboardData

if TYPE_CHECKING:
    from gold_scalp_trader.app.runtime import RuntimeResult


def _timing_text(result: CycleResult) -> str:
    if result.timing is None:
        return "Timing: NOT EVALUATED"
    timing = result.timing
    parts = [f"Timing: {timing.outcome.value}"]
    if timing.profile:
        parts.append(timing.profile)
    if timing.m5_event_age_bars is not None:
        parts.append(f"M5 age {timing.m5_event_age_bars} bars")
    if timing.trigger_age_seconds is not None:
        parts.append(f"M1 age {timing.trigger_age_seconds:.1f}s")
    return " • ".join(parts)


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
    activity = f"Open Gold positions: {positions}\n{_timing_text(result)}"
    if result.opportunity is not None:
        activity += (
            f"\nOpportunity: {result.opportunity.state.value} • {result.opportunity.opportunity_id}"
            f"\nEpisode: {result.opportunity.episode_id}"
        )
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
        activity_text=activity,
    )


def from_runtime(result: "RuntimeResult", market_state: str = "DEMO") -> DashboardData:
    provider = getattr(result, "provider", None)
    hard_state = provider.session.state.value if provider is not None else market_state
    data = from_cycle(result.cycle, market_state=hard_state)
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
        if trade.timing_profile is not None:
            managed_text += f"\nTiming {trade.timing_profile} • {trade.timing_policy_version or 'UNKNOWN'}"
        if trade.trigger_age_seconds is not None:
            managed_text += f" • trigger {trade.trigger_age_seconds:.1f}s"

    execution_text = "IDLE"
    if result.intent is not None:
        intent = result.intent
        execution_text = (
            f"{intent.action.value} • {intent.state.value}\n"
            f"Intent {intent.intent_id}\nSend count {intent.send_count}"
        )
    if result.management_action is not None:
        execution_text += f"\nManager {result.management_action.value}"

    activity = data.activity_text
    news_text = data.news_text
    if provider is not None:
        activity += (
            f"\nHard Session: {provider.session.state.value} • {provider.session.source}"
            f"\nSession reason: {provider.session.reason}"
        )
        news_text = f"{provider.news.health.value} • {provider.news.source} • SOFT ONLY"

    return replace(
        data,
        news_text=news_text,
        activity_text=activity,
        managed_trade_text=managed_text,
        execution_text=execution_text,
        learning_text="Timing + management + actual/shadow evidence active • governed promotion only",
    )
