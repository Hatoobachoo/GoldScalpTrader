"""Canonical governed runtime composition.

This module is the only public DEMO execution composition owner. Hard Session
permission comes from the scoped Session authority; callers cannot override it.
Durable Risk-day state is reconciled before any new OPEN can reach the Gate.
News and research remain read-only context.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from gold_scalp_trader.app import runtime_core as core
from gold_scalp_trader.app.cycle import CycleResult, run_cycle
from gold_scalp_trader.app.opportunity_lifecycle import mark_triggered, stabilize_cycle
from gold_scalp_trader.app.session_authority import (
    action_allowed as session_action_allowed,
    preclose_flatten_due,
    resolve as resolve_session_news,
)
from gold_scalp_trader.app.session_news import ProviderSnapshot
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import (
    Direction,
    ExecutionAction,
    GateState,
    IntentState,
    ManagementAction,
    RiskDecision,
    RuntimeMode,
)
from gold_scalp_trader.domain.ids import new_id
from gold_scalp_trader.execution.gate import evaluate as gate_eval
from gold_scalp_trader.execution.models import ExecutionIntent
from gold_scalp_trader.execution.service import execute_once
from gold_scalp_trader.management.execution import to_intent as management_to_intent
from gold_scalp_trader.management.manager import ManagementDecision
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.management.store import load as load_managed
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.risk.engine import evaluate as monetary_risk_eval
from gold_scalp_trader.risk.runtime import RiskAuthority, prepare as prepare_risk_authority

symbol_allows_action = core.symbol_allows_action
symbol_allows_open = core.symbol_allows_open
OPEN_CONTEXT_NS = core.OPEN_CONTEXT_NS


@dataclass(frozen=True, slots=True)
class RuntimeResult:
    cycle: CycleResult
    wrote_broker: bool = False
    intent: ExecutionIntent | None = None
    managed_trade: ManagedTrade | None = None
    management_action: ManagementAction | None = None
    provider: ProviderSnapshot | None = None


def _wrap(result: core.RuntimeResult, provider: ProviderSnapshot) -> RuntimeResult:
    return RuntimeResult(
        result.cycle,
        result.wrote_broker,
        result.intent,
        result.managed_trade,
        result.management_action,
        provider,
    )


def _session_permission(
    provider: ProviderSnapshot,
    action: ExecutionAction,
    broker_allowed: bool | None,
) -> bool:
    """Hard Session + broker capability; no caller-supplied override exists."""
    return session_action_allowed(provider, action) and broker_allowed is True


def _apply_durable_open_risk(
    cycle: CycleResult,
    settings: Settings,
    authority: RiskAuthority,
) -> CycleResult:
    """Bind monetary sizing to the durable UTC Risk-day authority.

    Analytical cycles intentionally do not invent DayStartEquity. A live OPEN
    can only receive a monetary RiskEvaluation after the durable authority has
    reconciled account activity, loss lock and cooldown state.
    """
    if cycle.trade_plan is None:
        return cycle
    if authority.state is None or authority.decision is not RiskDecision.PASS:
        return replace(
            cycle,
            risk=None,
            status="RISK",
            live_action="WAIT",
            reason=authority.reason,
        )

    market = cycle.intelligence.market
    evaluated = monetary_risk_eval(
        cycle.trade_plan,
        market.account,
        market.symbol_spec,
        day_start_equity=authority.state.day_start_equity,
        target_risk_pct=settings.target_risk_percent,
        aggressive_mode=authority.state.aggressive_mode,
    )
    return replace(
        cycle,
        risk=evaluated,
        status="RISK",
        live_action=(
            "READY_FOR_HARD_AUTHORITIES"
            if evaluated.decision is RiskDecision.PASS
            else "WAIT"
        ),
        reason=evaluated.reason,
    )


def run_read_cycle(settings: Settings, api) -> RuntimeResult:
    market = core.Mt5Reader(settings, api).read().snapshot
    provider = resolve_session_news(settings, market)
    cycle = run_cycle(market, settings, target_risk_pct=settings.target_risk_percent)
    return RuntimeResult(cycle, provider=provider)


def _forced_preclose_flatten(
    settings: Settings,
    api,
    reader,
    store: StateStore,
    market,
    cycle: CycleResult,
    scope: str,
    trade: ManagedTrade,
    provider: ProviderSnapshot,
    *,
    holder: str,
) -> RuntimeResult:
    """Submit one governed CLOSE when preserved PRE_CLOSE flatten is due."""
    if market.positions is None:
        return RuntimeResult(
            replace(cycle, status="MANAGEMENT", live_action="WAIT", reason="POSITION_DATA_UNAVAILABLE"),
            managed_trade=trade,
            management_action=ManagementAction.HOLD,
            provider=provider,
        )
    position = next((item for item in market.positions if item.ticket == trade.ticket), None)
    if position is None:
        if core._try_archive_missing_managed(settings, reader, store, market, scope, trade):
            return RuntimeResult(
                replace(
                    cycle,
                    status="CLOSED",
                    live_action="CLOSE_VERIFIED",
                    reason="EXACT_BROKER_EXIT_DEALS_VERIFIED",
                ),
                managed_trade=None,
                management_action=ManagementAction.EXIT,
                provider=provider,
            )
        return RuntimeResult(
            replace(
                cycle,
                status="MANAGEMENT",
                live_action="WAIT",
                reason="KNOWN_POSITION_MISSING_REQUIRES_EXACT_DEAL_PROOF",
            ),
            managed_trade=trade,
            management_action=ManagementAction.HOLD,
            provider=provider,
        )
    if (
        position.symbol != trade.symbol
        or position.direction is not trade.direction
        or position.magic != settings.bot_magic
        or abs(position.volume - trade.volume) > 1e-8
    ):
        return RuntimeResult(
            replace(
                cycle,
                status="MANAGEMENT",
                live_action="WAIT",
                reason="PRE_CLOSE_POSITION_RECONCILIATION_REQUIRED",
            ),
            managed_trade=trade,
            management_action=ManagementAction.HOLD,
            provider=provider,
        )

    decision = ManagementDecision(ManagementAction.EXIT, "PRE_CLOSE_MANDATORY_FLATTEN")
    price = market.quote.bid if trade.direction is Direction.BUY else market.quote.ask
    intent = management_to_intent(decision, trade, price=price, as_of=market.captured_at)
    if intent is None:
        return RuntimeResult(cycle, managed_trade=trade, management_action=ManagementAction.EXIT, provider=provider)

    try:
        lease = core.acquire(store, scope, holder)
        controller_ready = True
    except RuntimeError:
        lease = None
        controller_ready = False

    broker_allowed = core.symbol_allows_action(api, market.symbol_spec, trade.direction, ExecutionAction.CLOSE)
    session_ok = _session_permission(provider, ExecutionAction.CLOSE, broker_allowed)
    gate = gate_eval(
        risk=RiskDecision.PASS,
        market_open=session_ok,
        data_ready=core._management_data_ready(market, settings, ExecutionAction.CLOSE),
        identity_ready=core._identity_ready(market, api),
        exposure_clear=False,
        persistence_ready=store.integrity_check(),
        controller_ready=controller_ready,
        conflicting_intent=bool(core.unresolved(store)),
        action=ExecutionAction.CLOSE,
    )
    cycle = replace(
        cycle,
        status="MANAGEMENT",
        live_action="MANAGE_EXIT" if gate.state is GateState.ALLOW else "WAIT",
        reason=decision.reason if gate.state is GateState.ALLOW else ", ".join(gate.reasons),
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
        system_text="DEMO LIVE • PRE_CLOSE • GOVERNED FLATTEN",
    )
    if gate.state is not GateState.ALLOW or lease is None:
        return RuntimeResult(cycle, managed_trade=trade, management_action=ManagementAction.EXIT, provider=provider)

    writer = core._writer(settings, api)
    local = core.local_precheck(market.account, market.symbol_spec, market.quote, intent.volume)
    broker = core.broker_order_check(api, writer.build_request(intent))
    out = execute_once(
        store=store,
        intent=intent,
        gate=gate,
        lease=lease,
        writer=writer,
        precheck_passed=local.passed and broker.passed,
    )
    current: ManagedTrade | None = trade
    if out.state is IntentState.ACCEPTED_UNKNOWN:
        try:
            fresh = reader.read().snapshot
            if core.close_matches(out, fresh.positions) is True:
                out = out.with_state(IntentState.ACCEPTED_VERIFIED, reason="CLOSE_POSITION_ABSENCE_RECONCILED")
                core.save_intent(store, out)
                if core._try_archive_missing_managed(settings, reader, store, fresh, scope, trade):
                    current = None
        except core.Mt5ReadError:
            pass
    cycle = replace(
        cycle,
        live_action="CLOSE_SENT" if out.send_count == 1 else "WAIT",
        reason=out.reason or cycle.reason,
    )
    return RuntimeResult(cycle, out.send_count == 1, out, current, ManagementAction.EXIT, provider)


def run_guarded_demo_cycle(
    settings: Settings,
    api,
    store: StateStore,
    *,
    holder: str = "local-primary",
) -> RuntimeResult:
    """Run the sole public guarded DEMO execution cycle.

    Hard Session permission and durable Risk state are resolved internally.
    Tests must mock those providers rather than inject broker permission flags.
    """
    if settings.mode is not RuntimeMode.DEMO or not settings.demo_write_enabled:
        raise PermissionError("explicit DEMO mode/confirmation required")
    if settings.real_write_enabled:
        raise PermissionError("REAL write path is disabled in this release")

    reader = core.Mt5Reader(settings, api)
    market = reader.read().snapshot
    if not core.demo_account_verified(api):
        raise PermissionError("connected MT5 account is not explicitly verified as DEMO")

    provider = resolve_session_news(settings, market)
    # Structural/quality analysis first. Monetary sizing is deliberately deferred
    # until durable Risk-day authority has been reconciled below.
    cycle = run_cycle(market, settings, target_risk_pct=None)
    cycle = replace(
        cycle,
        system_text=f"DEMO LIVE • {provider.session.state.value} • DEMO ACCOUNT VERIFIED",
    )
    scope = core._scope(market)
    cycle = stabilize_cycle(store, scope, cycle)

    managed, reconciled_intent = core._reconcile_unresolved_intents(settings, store, market, scope)
    if core.unresolved(store):
        return RuntimeResult(
            replace(
                cycle,
                status="EXECUTION",
                live_action="WAIT",
                reason="UNRESOLVED_INTENT_RECONCILIATION_REQUIRED",
                system_text="DEMO LIVE • RECONCILING INTENT • NO RESEND",
            ),
            intent=reconciled_intent,
            managed_trade=managed,
            provider=provider,
        )

    managed = load_managed(store, scope)
    if managed is not None:
        if preclose_flatten_due(provider.session, market.captured_at):
            return _forced_preclose_flatten(
                settings,
                api,
                reader,
                store,
                market,
                cycle,
                scope,
                managed,
                provider,
                holder=holder,
            )
        management_allowed = _session_permission(
            provider,
            ExecutionAction.MODIFY,
            core.symbol_allows_action(api, market.symbol_spec, managed.direction, ExecutionAction.MODIFY),
        )
        return _wrap(
            core._run_managed_demo_cycle(
                settings,
                api,
                reader,
                store,
                market,
                cycle,
                scope,
                managed,
                authority_allowed=management_allowed,
                holder=holder,
            ),
            provider,
        )

    if market.positions is not None and any(p.magic == settings.bot_magic for p in market.positions):
        return RuntimeResult(
            replace(
                cycle,
                status="RECOVERY",
                live_action="WAIT",
                reason="ORPHAN_BOT_MAGIC_POSITION_REQUIRES_RECOVERY",
                system_text="DEMO LIVE • ORPHAN EXPOSURE • NO ADOPTION",
            ),
            provider=provider,
        )

    risk_authority = prepare_risk_authority(
        store,
        scope,
        reader,
        market,
        settings,
        unresolved_lifecycle=False,
    )
    cycle = _apply_durable_open_risk(cycle, settings, risk_authority)

    if (
        risk_authority.decision is not RiskDecision.PASS
        or cycle.trade_plan is None
        or cycle.risk is None
        or cycle.risk.decision is not RiskDecision.PASS
        or cycle.risk.volume is None
    ):
        return RuntimeResult(cycle, provider=provider)

    plan = cycle.trade_plan
    exposure_clear = market.positions == () if market.positions is not None else None
    try:
        lease = core.acquire(store, scope, holder)
        controller_ready = True
    except RuntimeError:
        lease = None
        controller_ready = False

    broker_open = core.symbol_allows_open(api, market.symbol_spec, plan.direction)
    session_open = _session_permission(provider, ExecutionAction.OPEN, broker_open)
    gate = gate_eval(
        risk=cycle.risk.decision,
        market_open=session_open,
        data_ready=core._data_ready(cycle, settings),
        identity_ready=core._identity_ready(market, api),
        exposure_clear=exposure_clear,
        persistence_ready=store.integrity_check(),
        controller_ready=controller_ready,
        conflicting_intent=bool(core.unresolved(store)),
        action=ExecutionAction.OPEN,
    )
    cycle = replace(
        cycle,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
        live_action="OPEN_READY" if gate.state is GateState.ALLOW else "WAIT",
        reason=cycle.reason if gate.state is GateState.ALLOW else ", ".join(gate.reasons),
    )
    if gate.state is not GateState.ALLOW or lease is None:
        return RuntimeResult(cycle, provider=provider)

    price = market.quote.ask if plan.direction is Direction.BUY else market.quote.bid
    intent = ExecutionIntent(
        str(new_id("INT")),
        ExecutionAction.OPEN,
        market.symbol_spec.symbol,
        plan.direction,
        cycle.risk.volume,
        price,
        plan.initial_sl,
        plan.expansion_target or plan.primary_target,
        IntentState.CREATED,
        datetime.now(tz=timezone.utc),
    )
    core._save_open_context(store, intent, cycle, settings)
    writer = core._writer(settings, api)
    local = core.local_precheck(market.account, market.symbol_spec, market.quote, intent.volume)
    broker = core.broker_order_check(api, writer.build_request(intent))
    out = execute_once(
        store=store,
        intent=intent,
        gate=gate,
        lease=lease,
        writer=writer,
        precheck_passed=local.passed and broker.passed,
    )
    if out.send_count == 1:
        cycle = mark_triggered(store, scope, cycle)
    if out.state is IntentState.FAILED:
        store.delete(OPEN_CONTEXT_NS, intent.intent_id)

    current_managed: ManagedTrade | None = None
    if out.state is IntentState.ACCEPTED_UNKNOWN:
        try:
            fresh = reader.read().snapshot
            current_managed, reconciled = core._reconcile_unresolved_intents(settings, store, fresh, scope)
            if reconciled is not None and reconciled.intent_id == out.intent_id:
                out = reconciled
        except core.Mt5ReadError:
            pass

    cycle = replace(
        cycle,
        live_action="ORDER_SENT" if out.send_count == 1 else "WAIT",
        reason=out.reason or cycle.reason,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
    )
    return RuntimeResult(cycle, out.send_count == 1, out, current_managed, provider=provider)
