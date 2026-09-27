from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from gold_scalp_trader.app.cycle import CycleResult
from gold_scalp_trader.domain.enums import StrategyFamily, Timeframe
from gold_scalp_trader.operator.presentation import DashboardData, StrategyBoardRow

if TYPE_CHECKING:
    from gold_scalp_trader.app.runtime import RuntimeResult


def _value(obj, name: str, default=None):
    return default if obj is None else getattr(obj, name, default)


def _enum(value, default: str = "UNKNOWN") -> str:
    return default if value is None else str(getattr(value, "value", value))


def _iso(value) -> str | None:
    return value.isoformat() if hasattr(value, "isoformat") else None


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
    if getattr(timing, "chase_atr", None) is not None:
        parts.append(f"chase {timing.chase_atr:.2f} ATR")
    if getattr(timing, "micro_extension_atr", None) is not None:
        parts.append(f"micro {timing.micro_extension_atr:.2f} ATR")
    return " • ".join(parts)


def _m5_seconds_remaining(result: CycleResult) -> int | None:
    when = result.intelligence.market.captured_at
    if when.tzinfo is None or when.utcoffset() is None:
        return None
    minute_in_block = when.minute % 5
    elapsed = minute_in_block * 60 + when.second
    remaining = 300 - elapsed
    return 0 if remaining == 300 else remaining


def _frame(result: CycleResult, timeframe: Timeframe):
    return result.intelligence.by_timeframe.get(timeframe)


def _structure(result: CycleResult, timeframe: Timeframe) -> str:
    frame = _frame(result, timeframe)
    if frame is None:
        return "UNKNOWN"
    return frame.structure.state.value


def _strategy_rows(result: CycleResult) -> tuple[StrategyBoardRow, ...]:
    rows: dict[str, StrategyBoardRow] = {}
    active = result.isolation.active_family.value if result.isolation.active_family else "UNSET"
    for isolated in result.isolation.candidates:
        candidate = isolated.candidate
        family = candidate.family.value
        rows[family] = (
            family,
            _enum(getattr(isolated, "mode", None), "SHADOW_ONLY"),
            _enum(getattr(candidate, "qualification", None), "UNKNOWN"),
            _enum(getattr(candidate, "direction", None), "NONE"),
            getattr(candidate, "score", None),
            getattr(candidate, "coverage", None),
        )
    ordered: list[StrategyBoardRow] = []
    for family in StrategyFamily:
        ordered.append(
            rows.get(
                family.value,
                (
                    family.value,
                    "ACTIVE_EXECUTION" if family.value == active else "SHADOW_ONLY",
                    "NOT_PRESENT",
                    "NONE",
                    None,
                    None,
                ),
            )
        )
    return tuple(ordered)


def _plan_fields(result: CycleResult) -> dict[str, object]:
    plan = result.trade_plan
    if plan is None:
        return {
            "plan_state": None,
            "plan_direction": None,
            "plan_entry": None,
            "plan_stop": None,
            "plan_primary": None,
            "plan_expansion": None,
            "plan_primary_rr": None,
            "plan_expansion_rr": None,
            "plan_quality": None,
            "plan_invalidation_source": None,
        }
    entry = float(plan.entry_reference)
    stop = float(plan.initial_sl)
    primary = float(plan.primary_target)
    expansion = None if plan.expansion_target is None else float(plan.expansion_target)
    risk_distance = abs(entry - stop)
    primary_rr = None if risk_distance <= 0 else abs(primary - entry) / risk_distance
    expansion_rr = None if expansion is None or risk_distance <= 0 else abs(expansion - entry) / risk_distance
    return {
        "plan_state": "READY",
        "plan_direction": plan.direction.value,
        "plan_entry": entry,
        "plan_stop": stop,
        "plan_primary": primary,
        "plan_expansion": expansion,
        "plan_primary_rr": primary_rr,
        "plan_expansion_rr": expansion_rr,
        "plan_quality": getattr(plan, "quality_score", None),
        "plan_invalidation_source": str(getattr(plan, "invalidation_source", "STRUCTURAL")),
    }


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
        lines = [
            f"{p.direction.value}  Entry {p.entry_reference:.3f}",
            f"SL {p.initial_sl:.3f}  Primary {p.primary_target:.3f}",
        ]
        if p.expansion_target is not None:
            lines.append(f"Expansion {p.expansion_target:.3f}  Gross R {p.gross_r:.2f}")
        else:
            lines.append(f"Gross R {p.gross_r:.2f}")
        plan = "\n".join(lines)

    positions = market.positions
    position_count = None if positions is None else len(positions)
    positions_text = "UNKNOWN" if position_count is None else str(position_count)
    activity = f"Open Gold positions: {positions_text}\n{_timing_text(result)}"
    if result.opportunity is not None:
        activity += (
            f"\nOpportunity: {result.opportunity.state.value} • {result.opportunity.opportunity_id}"
            f"\nEpisode: {result.opportunity.episode_id}"
        )

    m5 = _frame(result, Timeframe.M5)
    quant = None if m5 is None else m5.quant
    board = result.board
    account = market.account
    risk_profile = "NOT EVALUATED" if result.risk is None else result.risk.profile.value
    risk_pct = None if result.risk is None else result.risk.actual_risk_pct
    risk_volume = None if result.risk is None else result.risk.volume
    captured = market.captured_at

    kwargs = _plan_fields(result)
    return DashboardData(
        symbol=market.symbol_spec.symbol,
        bid=market.quote.bid,
        ask=market.quote.ask,
        spread=market.quote.spread,
        market_state=market_state,
        soft_session=result.intelligence.session.label,
        bot_status=result.status,
        detected_setup=detected,
        active_family=active,
        live_action=result.live_action,
        reason=result.reason,
        shadow_setups=shadow,
        risk_text=risk,
        gate_text=result.gate_text,
        news_text="SOFT CONTEXT",
        system_text=result.system_text,
        trade_plan_text=plan,
        activity_text=activity,
        account_balance=account.balance,
        account_equity=account.equity,
        free_margin=account.margin_free,
        buy_score=board.buy.score,
        sell_score=board.sell.score,
        leading_score=board.leading_score,
        evidence_coverage=board.coverage,
        m5_seconds_remaining=_m5_seconds_remaining(result),
        ema20=None if quant is None else quant.ema20,
        ema50=None if quant is None else quant.ema50,
        rsi14=None if quant is None else quant.rsi14,
        atr14=None if quant is None else quant.atr14,
        h4_structure=_structure(result, Timeframe.H4),
        h1_structure=_structure(result, Timeframe.H1),
        m15_structure=_structure(result, Timeframe.M15),
        m5_structure=_structure(result, Timeframe.M5),
        risk_profile=risk_profile,
        risk_pct=risk_pct,
        risk_volume=risk_volume,
        quote_time_utc=_iso(getattr(market.quote, "source_time", None)),
        analysis_time_utc=_iso(captured),
        position_count=position_count,
        live_feed_state="LIVE",
        strategy_board_rows=_strategy_rows(result),
        **kwargs,
    )


def from_runtime(result: "RuntimeResult", market_state: str = "DEMO") -> DashboardData:
    provider = getattr(result, "provider", None)
    hard_state = provider.session.state.value if provider is not None else market_state
    data = from_cycle(result.cycle, market_state=hard_state)

    managed_text = "NONE"
    if result.managed_trade is not None:
        trade = result.managed_trade
        managed_text = (
            f"#{trade.ticket} • {trade.family.value} • {_enum(getattr(trade, 'direction', None), 'OPEN')}\n"
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
    broker_reconcile = "CLEAR"
    if result.intent is not None:
        intent = result.intent
        execution_text = (
            f"{intent.action.value} • {intent.state.value}\n"
            f"Intent {intent.intent_id}\nSend count {intent.send_count}"
        )
        broker_reconcile = intent.state.value
    if result.management_action is not None:
        execution_text += f"\nManager {result.management_action.value}"

    activity = data.activity_text
    news_text = data.news_text
    session_source = None
    session_reason = None
    schedule_verified = None
    news_health = "UNKNOWN"
    if provider is not None:
        activity += (
            f"\nHard Session: {provider.session.state.value} • {provider.session.source}"
            f"\nSession reason: {provider.session.reason}"
        )
        news_text = f"{provider.news.health.value} • {provider.news.source} • SOFT ONLY"
        session_source = provider.session.source
        session_reason = provider.session.reason
        schedule_verified = bool(getattr(provider.session, "schedule_verified", False))
        news_health = provider.news.health.value

    return replace(
        data,
        account_mode="DEMO",
        runtime_role="PRIMARY",
        hard_session_source=session_source,
        hard_session_reason=session_reason,
        schedule_verified=schedule_verified,
        news_health=news_health,
        news_text=news_text,
        activity_text=activity,
        managed_trade_text=managed_text,
        execution_text=execution_text,
        broker_reconcile=broker_reconcile,
        learning_text="Timing + management + actual/shadow evidence active • governed promotion only",
        learning_state="ACTIVE",
        discovery_state="ACTIVE",
        controller_role="LOCAL PRIMARY",
    )
