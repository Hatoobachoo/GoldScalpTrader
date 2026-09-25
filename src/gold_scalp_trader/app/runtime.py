from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from gold_scalp_trader.app.cycle import CycleResult,run_cycle
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import Direction,ExecutionAction,GateState,IntentState,RiskDecision,RuntimeMode
from gold_scalp_trader.domain.ids import new_id
from gold_scalp_trader.execution.checks import broker_order_check,evaluate as local_precheck
from gold_scalp_trader.execution.controller import acquire
from gold_scalp_trader.execution.gate import evaluate as gate_eval
from gold_scalp_trader.execution.intent_store import save
from gold_scalp_trader.execution.models import ExecutionIntent
from gold_scalp_trader.execution.mt5_writer import Mt5Writer
from gold_scalp_trader.execution.reconcile import open_matches
from gold_scalp_trader.execution.service import execute_once
from gold_scalp_trader.market_data.mt5_reader import Mt5Reader
from gold_scalp_trader.persistence.store import StateStore
@dataclass(frozen=True,slots=True)
class RuntimeResult:cycle:CycleResult; wrote_broker:bool=False; intent:ExecutionIntent|None=None
def run_read_cycle(settings:Settings,api)->RuntimeResult:
    market=Mt5Reader(settings,api).read().snapshot; return RuntimeResult(run_cycle(market,settings,target_risk_pct=settings.target_risk_percent),False,None)
def run_guarded_demo_cycle(settings:Settings,api,store:StateStore,*,market_open:bool,holder:str="local-primary")->RuntimeResult:
    if settings.mode is not RuntimeMode.DEMO or not settings.demo_write_enabled:raise PermissionError("explicit DEMO mode/confirmation required")
    if settings.real_write_enabled:raise PermissionError("REAL write path is disabled in this release")
    market=Mt5Reader(settings,api).read().snapshot; cycle=run_cycle(market,settings,target_risk_pct=settings.target_risk_percent)
    if cycle.trade_plan is None or cycle.risk is None or cycle.risk.decision is not RiskDecision.PASS or cycle.risk.volume is None:return RuntimeResult(cycle,False,None)
    exposure_clear=market.positions==() if market.positions is not None else None; scope=f"{market.account.login}:{market.account.server}:{market.symbol_spec.symbol}"; lease=acquire(store,scope,holder)
    gate=gate_eval(risk=cycle.risk.decision,market_open=market_open,data_ready=True,identity_ready=True,exposure_clear=exposure_clear,persistence_ready=store.integrity_check(),controller_ready=True,conflicting_intent=False)
    if gate.state is not GateState.ALLOW:return RuntimeResult(cycle,False,None)
    p=cycle.trade_plan; price=market.quote.ask if p.direction is Direction.BUY else market.quote.bid; intent=ExecutionIntent(str(new_id("INT")),ExecutionAction.OPEN,market.symbol_spec.symbol,p.direction,cycle.risk.volume,price,p.initial_sl,p.primary_target,IntentState.CREATED,datetime.now(tz=timezone.utc)); writer=Mt5Writer(api); local=local_precheck(market.account,market.symbol_spec,market.quote,intent.volume); broker=broker_order_check(api,writer.build_request(intent)); out=execute_once(store=store,intent=intent,gate=gate,lease=lease,writer=writer,precheck_passed=local.passed and broker.passed)
    if out.state is IntentState.ACCEPTED_UNKNOWN:
        fresh=Mt5Reader(settings,api).read().snapshot; match=open_matches(out,fresh.positions)
        if match is not None:out=out.with_state(IntentState.ACCEPTED_VERIFIED,broker_ticket=match.ticket,reason="OPEN_RECONCILED"); save(store,out)
    return RuntimeResult(cycle,out.send_count==1,out)
