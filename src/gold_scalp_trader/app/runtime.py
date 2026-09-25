from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from gold_scalp_trader.app.cycle import CycleResult, run_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import (
    DataQuality,
    Direction,
    ExecutionAction,
    GateState,
    IntentState,
    RiskDecision,
    RuntimeMode,
    Timeframe,
)
from gold_scalp_trader.domain.ids import new_id
from gold_scalp_trader.domain.market import SymbolSpec
from gold_scalp_trader.execution.checks import broker_order_check, evaluate as local_precheck
from gold_scalp_trader.execution.controller import acquire
from gold_scalp_trader.execution.gate import evaluate as gate_eval
from gold_scalp_trader.execution.intent_store import save, unresolved
from gold_scalp_trader.execution.models import ExecutionIntent
from gold_scalp_trader.execution.mt5_writer import Mt5Writer
from gold_scalp_trader.execution.reconcile import open_matches
from gold_scalp_trader.execution.service import execute_once
from gold_scalp_trader.market_data.account_mode import demo_account_verified
from gold_scalp_trader.market_data.mt5_reader import Mt5Reader
from gold_scalp_trader.persistence.store import StateStore


@dataclass(frozen=True, slots=True)
class RuntimeResult:
    cycle: CycleResult
    wrote_broker: bool = False
    intent: ExecutionIntent | None = None


def symbol_allows_open(api, spec: SymbolSpec, direction: Direction) -> bool | None:
    """Normalize MT5 symbol trade mode into opening permission for this direction."""
    mode = spec.trade_mode
    if mode is None:
        return None
    if isinstance(mode, str):
        value = mode.strip().upper()
        if value in {"FULL", "SYMBOL_TRADE_MODE_FULL"}:
            return True
        if direction is Direction.BUY and value in {"LONGONLY", "SYMBOL_TRADE_MODE_LONGONLY"}:
            return True
        if direction is Direction.SELL and value in {"SHORTONLY", "SYMBOL_TRADE_MODE_SHORTONLY"}:
            return True
        return False

    full = getattr(api, "SYMBOL_TRADE_MODE_FULL", 4)
    long_only = getattr(api, "SYMBOL_TRADE_MODE_LONGONLY", 1)
    short_only = getattr(api, "SYMBOL_TRADE_MODE_SHORTONLY", 2)
    if mode == full:
        return True
    if direction is Direction.BUY and mode == long_only:
        return True
    if direction is Direction.SELL and mode == short_only:
        return True
    return False


def _data_ready(cycle: CycleResult, settings: Settings) -> bool:
    market = cycle.intelligence.market
    required = (Timeframe.M1, Timeframe.M5, Timeframe.M15, Timeframe.H1)
    candles_ready = all(market.quality.get(tf) is DataQuality.HEALTHY for tf in required)
    quote_ready = 0.0 <= market.quote.age_seconds <= settings.max_quote_age_seconds
    return candles_ready and quote_ready


def run_read_cycle(settings: Settings, api) -> RuntimeResult:
    market = Mt5Reader(settings, api).read().snapshot
    return RuntimeResult(run_cycle(market, settings, target_risk_pct=settings.target_risk_percent), False, None)


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

    market = Mt5Reader(settings, api).read().snapshot
    if not demo_account_verified(api):
        raise PermissionError("connected MT5 account is not explicitly verified as DEMO")

    cycle = run_cycle(market, settings, target_risk_pct=settings.target_risk_percent)
    cycle = replace(cycle, system_text="DEMO LIVE • DEMO ACCOUNT VERIFIED")

    if (
        cycle.trade_plan is None
        or cycle.risk is None
        or cycle.risk.decision is not RiskDecision.PASS
        or cycle.risk.volume is None
    ):
        return RuntimeResult(cycle, False, None)

    plan = cycle.trade_plan
    exposure_clear = market.positions == () if market.positions is not None else None
    scope = f"{market.account.login}:{market.account.server}:{market.symbol_spec.symbol}"
    conflicting = bool(unresolved(store))

    try:
        lease = acquire(store, scope, holder)
        controller_ready = True
    except RuntimeError:
        lease = None
        controller_ready = False

    broker_open = symbol_allows_open(api, market.symbol_spec, plan.direction)
    effective_market_open = market_open if market_open is not None else broker_open
    identity_ready = (
        market.account.trade_allowed is True
        and market.account.trade_expert is True
        and demo_account_verified(api)
    )

    gate = gate_eval(
        risk=cycle.risk.decision,
        market_open=effective_market_open,
        data_ready=_data_ready(cycle, settings),
        identity_ready=identity_ready,
        exposure_clear=exposure_clear,
        persistence_ready=store.integrity_check(),
        controller_ready=controller_ready,
        conflicting_intent=conflicting,
    )
    cycle = replace(
        cycle,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
        live_action="OPEN_READY" if gate.state is GateState.ALLOW else "WAIT",
        reason=cycle.reason if gate.state is GateState.ALLOW else ", ".join(gate.reasons),
    )
    if gate.state is not GateState.ALLOW or lease is None:
        return RuntimeResult(cycle, False, None)

    price = market.quote.ask if plan.direction is Direction.BUY else market.quote.bid
    intent = ExecutionIntent(
        str(new_id("INT")),
        ExecutionAction.OPEN,
        market.symbol_spec.symbol,
        plan.direction,
        cycle.risk.volume,
        price,
        plan.initial_sl,
        plan.primary_target,
        IntentState.CREATED,
        datetime.now(tz=timezone.utc),
    )
    writer = Mt5Writer(api)
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

    if out.state is IntentState.ACCEPTED_UNKNOWN:
        fresh = Mt5Reader(settings, api).read().snapshot
        match = open_matches(out, fresh.positions)
        if match is not None:
            out = out.with_state(
                IntentState.ACCEPTED_VERIFIED,
                broker_ticket=match.ticket,
                position_ticket=match.ticket,
                reason="OPEN_RECONCILED",
            )
            save(store, out)

    cycle = replace(
        cycle,
        live_action="ORDER_SENT" if out.send_count == 1 else "WAIT",
        reason=out.reason or cycle.reason,
        gate_text=f"{gate.state.value} • {', '.join(gate.reasons)}",
    )
    return RuntimeResult(cycle, out.send_count == 1, out)
