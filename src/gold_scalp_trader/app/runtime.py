from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone

from gold_scalp_trader.app.cycle import CycleResult, run_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import (
    DataQuality,
    Direction,
    ExecutionAction,
    GateState,
    IntentState,
    ManagementAction,
    RiskDecision,
    RuntimeMode,
    Timeframe,
)
from gold_scalp_trader.domain.ids import new_id
from gold_scalp_trader.domain.market import MarketSnapshot, PositionFacts, SymbolSpec
from gold_scalp_trader.execution.checks import broker_order_check, evaluate as local_precheck
from gold_scalp_trader.execution.controller import acquire
from gold_scalp_trader.execution.gate import evaluate as gate_eval
from gold_scalp_trader.execution.intent_store import load as load_intent
from gold_scalp_trader.execution.intent_store import save as save_intent
from gold_scalp_trader.execution.intent_store import unresolved
from gold_scalp_trader.execution.models import ExecutionIntent
from gold_scalp_trader.execution.mt5_writer import Mt5Writer
from gold_scalp_trader.execution.reconcile import close_matches, modify_matches, open_matches
from gold_scalp_trader.execution.service import execute_once
from gold_scalp_trader.management.closure import archive_verified_close, complete_exit_proved
from gold_scalp_trader.management.execution import to_intent as management_to_intent
from gold_scalp_trader.management.manager import evaluate as management_eval
from gold_scalp_trader.management.models import ManagedTrade
from gold_scalp_trader.management.store import load as load_managed
from gold_scalp_trader.management.store import save as save_managed
from gold_scalp_trader.market_data.account_mode import demo_account_verified
from gold_scalp_trader.market_data.mt5_reader import Mt5Reader, Mt5ReadError
from gold_scalp_trader.persistence.store import StateStore

OPEN_CONTEXT_NS = "open_intent_context"


@dataclass(frozen=True, slots=True)
class RuntimeResult:
    cycle: CycleResult
    wrote_broker: bool = False
    intent: ExecutionIntent | None = None
    managed_trade: ManagedTrade | None = None
    management_action: ManagementAction | None = None


def symbol_allows_action(
    api,
    spec: SymbolSpec,
    direction: Direction,
    action: ExecutionAction,
) -> bool | None:
    """Normalize MT5 symbol trade mode for OPEN/MODIFY/CLOSE.

    OPEN respects long/short/close-only restrictions. Exposure-reducing CLOSE
    and protective MODIFY are allowed for any non-disabled trade mode and still
    face broker `order_check` before send.
    """
    mode = spec.trade_mode
    if mode is None:
        return None

    if isinstance(mode, str):
        value = mode.strip().upper()
        disabled = value in {"DISABLED", "SYMBOL_TRADE_MODE_DISABLED"}
        if disabled:
            return False
        if action is not ExecutionAction.OPEN:
            return True
        if value in {"FULL", "SYMBOL_TRADE_MODE_FULL"}:
            return True
        if direction is Direction.BUY and value in {"LONGONLY", "SYMBOL_TRADE_MODE_LONGONLY"}:
            return True
        if direction is Direction.SELL and value in {"SHORTONLY", "SYMBOL_TRADE_MODE_SHORTONLY"}:
            return True
        return False

    disabled = getattr(api, "SYMBOL_TRADE_MODE_DISABLED", 0)
    full = getattr(api, "SYMBOL_TRADE_MODE_FULL", 4)
    long_only = getattr(api, "SYMBOL_TRADE_MODE_LONGONLY", 1)
    short_only = getattr(api, "SYMBOL_TRADE_MODE_SHORTONLY", 2)
    if mode == disabled:
        return False
    if action is not ExecutionAction.OPEN:
        return True
    if mode == full:
        return True
    if direction is Direction.BUY and mode == long_only:
        return True
    if direction is Direction.SELL and mode == short_only:
        return True
    return False


def symbol_allows_open(api, spec: SymbolSpec, direction: Direction) -> bool | None:
    return symbol_allows_action(api, spec, direction, ExecutionAction.OPEN)


def _scope(market: MarketSnapshot) -> str:
    return f"{market.account.login}:{market.account.server}:{market.symbol_spec.symbol}"


def _quote_ready(market: MarketSnapshot, settings: Settings) -> bool:
    return 0.0 <= market.quote.age_seconds <= settings.max_quote_age_seconds


def _data_ready(cycle: CycleResult, settings: Settings) -> bool:
    market = cycle.intelligence.market
    required = (Timeframe.M1, Timeframe.M5, Timeframe.M15, Timeframe.H1)
    candles_ready = all(market.quality.get(tf) is DataQuality.HEALTHY for tf in required)
    return candles_ready and _quote_ready(market, settings)


def _management_data_ready(
    market: MarketSnapshot,
    settings: Settings,
    action: ExecutionAction,
) -> bool:
    if not _quote_ready(market, settings) or market.positions_quality is not DataQuality.HEALTHY:
        return False
    if action is ExecutionAction.CLOSE:
        return True
    return market.quality.get(Timeframe.M5) is DataQuality.HEALTHY


def _identity_ready(market: MarketSnapshot, api) -> bool:
    return (
        market.account.trade_allowed is True
        and market.account.trade_expert is True
        and demo_account_verified(api)
    )


def _writer(settings: Settings, api) -> Mt5Writer:
    return Mt5Writer(
        api,
        magic=settings.bot_magic,
        comment_prefix=settings.bot_comment_prefix,
    )


def _save_open_context(
    store: StateStore,
    intent: ExecutionIntent,
    cycle: CycleResult,
    settings: Settings,
) -> None:
    if cycle.trade_plan is None or cycle.opportunity is None:
        raise ValueError("OPEN context requires TradePlan and Opportunity")
    plan = cycle.trade_plan
    store.put(
        OPEN_CONTEXT_NS,
        intent.intent_id,
        {
            "family": cycle.opportunity.family.value,
            "policy_version": settings.active_strategy_policy_version,
            "primary_target": plan.primary_target,
            "expansion_target": plan.expansion_target,
            "opened_at": intent.created_at.isoformat(),
        },
    )


def _managed_from_verified_open(
    store: StateStore,
    settings: Settings,
    intent: ExecutionIntent,
    position: PositionFacts,
) -> ManagedTrade:
    context_record = store.get(OPEN_CONTEXT_NS, intent.intent_id)
    context = context_record.payload if context_record is not None else {}
    family = settings.active_strategy_family
    if context.get("family"):
        from gold_scalp_trader.domain.enums import StrategyFamily

        family = StrategyFamily(str(context["family"]))
    if family is None:
        raise ValueError("active strategy family unavailable for verified OPEN")

    original_sl = intent.sl if intent.sl is not None else position.sl
    if original_sl is None:
        raise ValueError("verified OPEN has no structural stop")
    current_sl = position.sl if position.sl is not None else original_sl
    primary_target_raw = context.get("primary_target", intent.tp)
    if primary_target_raw is None:
        raise ValueError("verified OPEN has no target lineage")
    expansion_raw = context.get("expansion_target")
    opened_raw = context.get("opened_at")
    opened_at = datetime.fromisoformat(str(opened_raw)) if opened_raw else intent.created_at
    original_r = abs(position.price_open - original_sl)
    if original_r <= 0:
        raise ValueError("verified OPEN has invalid original R geometry")

    trade = ManagedTrade(
        trade_id=str(new_id("TRD")),
        ticket=position.ticket,
        symbol=position.symbol,
        direction=position.direction,
        volume=position.volume,
        entry=position.price_open,
        original_sl=original_sl,
        current_sl=current_sl,
        primary_target=float(primary_target_raw),
        expansion_target=None if expansion_raw is None else float(expansion_raw),
        family=family,
        policy_version=str(context.get("policy_version", settings.active_strategy_policy_version)),
        original_r_price=original_r,
        opened_at=opened_at,
    )
    store.delete(OPEN_CONTEXT_NS, intent.intent_id)
    return trade


def _verified_close_intent_id(store: StateStore, ticket: int) -> str | None:
    matches: list[ExecutionIntent] = []
    for record in store.list_records("execution_intents"):
        intent = load_intent(store, record.key)
        if (
            intent is not None
            and intent.action is ExecutionAction.CLOSE
            and intent.position_ticket == ticket
            and intent.state is IntentState.ACCEPTED_VERIFIED
        ):
            matches.append(intent)
    if not matches:
        return None
    matches.sort(key=lambda item: item.created_at)
    return matches[-1].intent_id


def _try_archive_missing_managed(
    settings: Settings,
    reader: Mt5Reader,
    store: StateStore,
    market: MarketSnapshot,
    scope: str,
    trade: ManagedTrade,
) -> bool:
    if market.positions is None:
        return False
    if any(position.ticket == trade.ticket for position in market.positions):
        return False
    from_time = trade.opened_at or (market.captured_at - timedelta(days=7))
    deals = reader.read_position_deals(
        trade.ticket,
        from_time=from_time - timedelta(minutes=5),
        to_time=market.captured_at + timedelta(minutes=1),
    )
    if deals is None or not complete_exit_proved(deals, trade):
        return False
    archive_verified_close(
        store,
        scope,
        trade,
        deals,
        bot_magic=settings.bot_magic,
        close_intent_id=_verified_close_intent_id(store, trade.ticket),
        reason="BROKER_EXIT_DEALS_VERIFIED",
    )
    return True


def _reconcile_unresolved_intents(
    settings: Settings,
    store: StateStore,
    market: MarketSnapshot,
    scope: str,
) -> tuple[ManagedTrade | None, ExecutionIntent | None]:
    managed = load_managed(store, scope)
    last: ExecutionIntent | None = None
    for intent in unresolved(store):
        if intent.symbol != market.symbol_spec.symbol:
            continue
        out = intent
        if intent.action is ExecutionAction.OPEN:
            match = open_matches(intent, market.positions, magic=settings.bot_magic)
            if match is not None:
                out = intent.with_state(
                    IntentState.ACCEPTED_VERIFIED,
                    broker_ticket=match.ticket,
                    position_ticket=match.ticket,
                    reason="OPEN_RECONCILED",
                )
                save_intent(store, out)
                if managed is None:
                    managed = _managed_from_verified_open(store, settings, out, match)
                    save_managed(store, scope, managed)
        elif intent.action is ExecutionAction.MODIFY:
            matched = modify_matches(intent, market.positions)
            if matched is True:
                out = intent.with_state(IntentState.ACCEPTED_VERIFIED, reason="MODIFY_RECONCILED")
                save_intent(store, out)
                if managed is not None and intent.sl is not None:
                    managed = replace(managed, current_sl=intent.sl)
                    save_managed(store, scope, managed)
        elif intent.action is ExecutionAction.CLOSE:
            matched = close_matches(intent, market.positions)
            if matched is True:
                out = intent.with_state(IntentState.ACCEPTED_VERIFIED, reason="CLOSE_POSITION_ABSENCE_RECONCILED")
                save_intent(store, out)
                # ManagedTrade is deliberately retained until exact exit-deal
                # volume proof is available.
        last = out
    return managed, last


def _bars_in_trade(trade: ManagedTrade, market: MarketSnapshot) -> int:
    if trade.opened_at is None:
        return 0
    return sum(1 for candle in market.series(Timeframe.M5) if candle.close_time > trade.opened_at)


def run_read_cycle(settings: Settings, api) -> RuntimeResult:
    market = Mt5Reader(settings, api).read().snapshot
    return RuntimeResult(
        run_cycle(market, settings, target_risk_pct=settings.target_risk_percent),
        False,
        None,
    )


def _run_managed_demo_cycle(
    settings: Settings,
    api,
    reader: Mt5Reader,
    store: StateStore,
    market: MarketSnapshot,
    cycle: CycleResult,
    scope: str,
    trade: ManagedTrade,
    *,
    market_open: bool | None,
    holder: str,
) -> RuntimeResult:
    if market.positions is None:
        cycle = replace(
            cycle,
            status="MANAGEMENT",
            live_action="WAIT",
            reason="POSITION_DATA_UNAVAILABLE",
            system_text="DEMO LIVE • MANAGED TRADE • RECONCILING",
        )
        return RuntimeResult(cycle, False, None, trade, ManagementAction.HOLD)

    position = next((item for item in market.positions if item.ticket == trade.ticket), None)
    if position is None:
        if _try_archive_missing_managed(settings, reader, store, market, scope, trade):
            cycle = replace(
                cycle,
                status="CLOSED",
                live_action="CLOSE_VERIFIED",
                reason="EXACT_BROKER_EXIT_DEALS_VERIFIED",
                system_text="DEMO LIVE • TRADE CLOSED • LEARNING QUEUED",
            )
            return RuntimeResult(cycle, False, None, None, ManagementAction.EXIT)
        cycle = replace(
            cycle,
            status="MANAGEMENT",
            live_action="WAIT",
            reason="KNOWN_POSITION_MISSING_REQUIRES_EXACT_DEAL_PROOF",
            system_text="DEMO LIVE • MANAGED TRADE • RECONCILING CLOSE",
        )
        return RuntimeResult(cycle, False, None, trade, ManagementAction.HOLD)

    if (
        position.symbol != trade.symbol
        or position.direction is not trade.direction
        or position.magic != settings.bot_magic
    ):
        cycle = replace(
            cycle,
            status="MANAGEMENT",
            live_action="WAIT",
            reason="MANAGED_POSITION_OWNERSHIP_MISMATCH",
            system_text="DEMO LIVE • OWNERSHIP RECONCILIATION REQUIRED",
        )
        return RuntimeResult(cycle, False, None, trade, ManagementAction.HOLD)

    if abs(position.volume - trade.volume) > 1e-8:
        cycle = replace(
            cycle,
            status="MANAGEMENT",
            live_action="WAIT",
            reason="PARTIAL_VOLUME_CHANGE_REQUIRES_RECONCILIATION",
            system_text="DEMO LIVE • VOLUME RECONCILIATION REQUIRED",
        )
        return RuntimeResult(cycle, False, None, trade, ManagementAction.HOLD)

    decision = management_eval(trade, cycle.intelligence, _bars_in_trade(trade, market))
    cycle = replace(
        cycle,
        status="MANAGEMENT",
        live_action=f"MANAGE_{decision.action.value}",
        reason=decision.reason,
        system_text=f"DEMO LIVE • MANAGED TRADE • {decision.action.value}",
    )
    if decision.action in {ManagementAction.HOLD, ManagementAction.RUNNER}:
        return RuntimeResult(cycle, False, None, trade, decision.action)

    close_price = None
    if decision.action is ManagementAction.EXIT:
        close_price = market.quote.bid if trade.direction is Direction.BUY else market.quote.ask
    intent = management_to_intent(
        decision,
        trade,
        price=close_price,
        as_of=market.captured_at,
    )
    if intent is None:
        return RuntimeResult(cycle, False, None, trade, decision.action)

    try:
        lease = acquire(store, scope, holder)
        controller_ready = True
    except RuntimeError:
        lease = None
        controller_ready = False

    broker_allowed = symbol_allows_action(api, market.symbol_spec, trade.direction, intent.action)
    effective_market_open = market_open if market_open is not None else broker_allowed
    gate = gate_eval(
        risk=RiskDecision.PASS,
        market_open=effective_market_open,
        data_ready=_management_data_ready(market, settings, intent.action),
        identity_ready=_identity_ready(market, api),
        exposure_clear=False,
        persistence_ready=store.integrity_check(),
        controller_ready=controller_ready,
        conflicting_intent=bool(unresolved(store)),
        action=intent.action,
    )
    cycle = replace(
        cycle,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
        live_action=f"MANAGE_{decision.action.value}" if gate.state is GateState.ALLOW else "WAIT",
        reason=decision.reason if gate.state is GateState.ALLOW else ", ".join(gate.reasons),
    )
    if gate.state is not GateState.ALLOW or lease is None:
        return RuntimeResult(cycle, False, None, trade, decision.action)

    writer = _writer(settings, api)
    local = local_precheck(market.account, market.symbol_spec, market.quote, intent.volume)
    broker = broker_order_check(api, writer.build_request(intent))
    out = execute_once(
        store=store,
        intent=intent,
        gate=gate,
        lease=lease,
        writer=writer,
        precheck_passed=local.passed and broker.passed,
    )

    current_trade = trade
    if out.state is IntentState.ACCEPTED_UNKNOWN:
        try:
            fresh = reader.read().snapshot
            if out.action is ExecutionAction.MODIFY and modify_matches(out, fresh.positions) is True:
                out = out.with_state(IntentState.ACCEPTED_VERIFIED, reason="MODIFY_RECONCILED")
                save_intent(store, out)
                if out.sl is not None:
                    current_trade = replace(current_trade, current_sl=out.sl)
                    save_managed(store, scope, current_trade)
            elif out.action is ExecutionAction.CLOSE and close_matches(out, fresh.positions) is True:
                out = out.with_state(IntentState.ACCEPTED_VERIFIED, reason="CLOSE_POSITION_ABSENCE_RECONCILED")
                save_intent(store, out)
                if _try_archive_missing_managed(settings, reader, store, fresh, scope, current_trade):
                    current_trade = None  # type: ignore[assignment]
        except Mt5ReadError:
            # The one irreversible send has already happened. Preserve UNKNOWN
            # and let the next cycle reconcile; never resend blindly.
            pass

    cycle = replace(
        cycle,
        live_action=(
            "MODIFY_SENT"
            if intent.action is ExecutionAction.MODIFY and out.send_count == 1
            else "CLOSE_SENT"
            if intent.action is ExecutionAction.CLOSE and out.send_count == 1
            else "WAIT"
        ),
        reason=out.reason or cycle.reason,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
    )
    return RuntimeResult(cycle, out.send_count == 1, out, current_trade, decision.action)


def run_guarded_demo_cycle(
    settings: Settings,
    api,
    store: StateStore,
    *,
    market_open: bool | None = None,
    holder: str = "local-primary",
) -> RuntimeResult:
    if settings.mode is not RuntimeMode.DEMO or not settings.demo_write_enabled:
        raise PermissionError("explicit DEMO mode/confirmation required")
    if settings.real_write_enabled:
        raise PermissionError("REAL write path is disabled in this release")

    reader = Mt5Reader(settings, api)
    market = reader.read().snapshot
    if not demo_account_verified(api):
        raise PermissionError("connected MT5 account is not explicitly verified as DEMO")

    cycle = run_cycle(market, settings, target_risk_pct=settings.target_risk_percent)
    cycle = replace(cycle, system_text="DEMO LIVE • DEMO ACCOUNT VERIFIED")
    scope = _scope(market)

    managed, reconciled_intent = _reconcile_unresolved_intents(settings, store, market, scope)
    if unresolved(store):
        cycle = replace(
            cycle,
            status="EXECUTION",
            live_action="WAIT",
            reason="UNRESOLVED_INTENT_RECONCILIATION_REQUIRED",
            system_text="DEMO LIVE • RECONCILING INTENT • NO RESEND",
        )
        return RuntimeResult(cycle, False, reconciled_intent, managed)

    managed = load_managed(store, scope)
    if managed is not None:
        return _run_managed_demo_cycle(
            settings,
            api,
            reader,
            store,
            market,
            cycle,
            scope,
            managed,
            market_open=market_open,
            holder=holder,
        )

    # A bot-magic position without durable ManagedTrade lineage is never
    # silently adopted. Recovery evidence must resolve it explicitly.
    if market.positions is not None and any(position.magic == settings.bot_magic for position in market.positions):
        cycle = replace(
            cycle,
            status="RECOVERY",
            live_action="WAIT",
            reason="ORPHAN_BOT_MAGIC_POSITION_REQUIRES_RECOVERY",
            system_text="DEMO LIVE • ORPHAN EXPOSURE • NO ADOPTION",
        )
        return RuntimeResult(cycle, False, None, None)

    if (
        cycle.trade_plan is None
        or cycle.risk is None
        or cycle.risk.decision is not RiskDecision.PASS
        or cycle.risk.volume is None
    ):
        return RuntimeResult(cycle, False, None, None)

    plan = cycle.trade_plan
    exposure_clear = market.positions == () if market.positions is not None else None
    conflicting = bool(unresolved(store))

    try:
        lease = acquire(store, scope, holder)
        controller_ready = True
    except RuntimeError:
        lease = None
        controller_ready = False

    broker_open = symbol_allows_open(api, market.symbol_spec, plan.direction)
    effective_market_open = market_open if market_open is not None else broker_open
    gate = gate_eval(
        risk=cycle.risk.decision,
        market_open=effective_market_open,
        data_ready=_data_ready(cycle, settings),
        identity_ready=_identity_ready(market, api),
        exposure_clear=exposure_clear,
        persistence_ready=store.integrity_check(),
        controller_ready=controller_ready,
        conflicting_intent=conflicting,
        action=ExecutionAction.OPEN,
    )
    cycle = replace(
        cycle,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
        live_action="OPEN_READY" if gate.state is GateState.ALLOW else "WAIT",
        reason=cycle.reason if gate.state is GateState.ALLOW else ", ".join(gate.reasons),
    )
    if gate.state is not GateState.ALLOW or lease is None:
        return RuntimeResult(cycle, False, None, None)

    price = market.quote.ask if plan.direction is Direction.BUY else market.quote.bid
    broker_tp = plan.expansion_target or plan.primary_target
    intent = ExecutionIntent(
        str(new_id("INT")),
        ExecutionAction.OPEN,
        market.symbol_spec.symbol,
        plan.direction,
        cycle.risk.volume,
        price,
        plan.initial_sl,
        broker_tp,
        IntentState.CREATED,
        datetime.now(tz=timezone.utc),
    )
    _save_open_context(store, intent, cycle, settings)
    writer = _writer(settings, api)
    local = local_precheck(market.account, market.symbol_spec, market.quote, intent.volume)
    broker = broker_order_check(api, writer.build_request(intent))
    out = execute_once(
        store=store,
        intent=intent,
        gate=gate,
        lease=lease,
        writer=writer,
        precheck_passed=local.passed and broker.passed,
    )
    if out.state is IntentState.FAILED:
        store.delete(OPEN_CONTEXT_NS, intent.intent_id)

    current_managed: ManagedTrade | None = None
    if out.state is IntentState.ACCEPTED_UNKNOWN:
        try:
            fresh = reader.read().snapshot
            current_managed, reconciled = _reconcile_unresolved_intents(settings, store, fresh, scope)
            if reconciled is not None and reconciled.intent_id == out.intent_id:
                out = reconciled
        except Mt5ReadError:
            # Send already consumed. Preserve ACCEPTED_UNKNOWN and reconcile on
            # the next cycle rather than raising into a misleading no-write path.
            pass

    cycle = replace(
        cycle,
        live_action="ORDER_SENT" if out.send_count == 1 else "WAIT",
        reason=out.reason or cycle.reason,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
    )
    return RuntimeResult(cycle, out.send_count == 1, out, current_managed)
