"""Live risk-day authority for guarded DEMO execution."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone
from gold_scalp_trader.config import Settings
from gold_scalp_trader.domain.enums import DataQuality,RiskDecision,Timeframe
from gold_scalp_trader.domain.market import MarketSnapshot
from gold_scalp_trader.market_data.activity import ActivitySummary,classify_deals
from gold_scalp_trader.market_data.mt5_reader import Mt5Reader
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.live_learning import QUEUE as LEARNING_QUEUE_NS
from .state import RiskState,cooldown_released,initial,load,record_closed_trade,rollover,save,with_account_safety_pl
UTC=timezone.utc; CLOSURE_RECEIPT_NS="managed_trade_closure_receipt"; RISK_CLOSE_APPLIED_NS="risk_close_applied"
@dataclass(frozen=True,slots=True)
class RiskAuthority:
    state:RiskState|None; decision:RiskDecision; reason:str; net_non_trading_cash_flow:float|None=None
def utc_day_start(as_of:datetime)->datetime:
    if as_of.tzinfo is None or as_of.utcoffset() is None: raise ValueError("as_of must be timezone-aware")
    utc=as_of.astimezone(UTC); return datetime(utc.year,utc.month,utc.day,tzinfo=UTC)
def market_context_healthy(market:MarketSnapshot,settings:Settings)->bool:
    required=(Timeframe.M1,Timeframe.M5,Timeframe.M15,Timeframe.H1)
    return all(market.quality.get(tf) is DataQuality.HEALTHY for tf in required) and market.positions_quality is DataQuality.HEALTHY and 0.0<=market.quote.age_seconds<=settings.max_quote_age_seconds
def _activity_summary(reader:Mt5Reader,settings:Settings,market:MarketSnapshot)->ActivitySummary:
    return classify_deals(reader.read_deals(from_time=utc_day_start(market.captured_at),to_time=market.captured_at),bot_magic=settings.bot_magic)
def _reconstructed_day_start_equity(market:MarketSnapshot,summary:ActivitySummary)->float|None:
    if summary.quality is not DataQuality.HEALTHY or summary.bot_realized is None or summary.external_realized is None or summary.net_non_trading_cash_flow is None:return None
    value=market.account.equity-summary.bot_realized-summary.external_realized-summary.net_non_trading_cash_flow
    return value if value>0 else None
def _receipt_net_money(store:StateStore,reader:Mt5Reader,payload:dict)->float|None:
    if payload.get("net_money") is not None:return float(payload["net_money"])
    trade_id=str(payload.get("trade_id","")); queued=store.get(LEARNING_QUEUE_NS,trade_id) if trade_id else None
    if queued is not None and queued.payload.get("net_money") is not None:return float(queued.payload["net_money"])
    ticket_raw=payload.get("position_ticket"); closed_raw=payload.get("closed_at")
    if ticket_raw in (None,0) or not closed_raw:return None
    try:ticket=int(ticket_raw); closed_at=datetime.fromisoformat(str(closed_raw))
    except (TypeError,ValueError):return None
    if closed_at.tzinfo is None or closed_at.utcoffset() is None:return None
    deals=reader.read_position_deals(ticket,from_time=closed_at-timedelta(days=7),to_time=closed_at+timedelta(minutes=2))
    if deals is None:return None
    exits=[d for d in deals if d.position_id==ticket and d.entry_role.upper() in {"OUT","OUT_BY","INOUT"} and d.volume>0]
    return None if not exits else sum(d.net_money for d in exits)
def _apply_unprocessed_closes(store:StateStore,reader:Mt5Reader,state:RiskState,settings:Settings):
    pending=[]
    for record in sorted(store.list_records(CLOSURE_RECEIPT_NS),key=lambda r:str(r.payload.get("closed_at",""))):
        trade_id=str(record.payload.get("trade_id",record.key))
        if store.get(RISK_CLOSE_APPLIED_NS,trade_id) is not None:continue
        try:closed_at=datetime.fromisoformat(str(record.payload.get("closed_at")))
        except (TypeError,ValueError):return None,"CLOSE_RECEIPT_TIME_UNKNOWN",[]
        if closed_at.tzinfo is None or closed_at.utcoffset() is None:return None,"CLOSE_RECEIPT_TIME_UNKNOWN",[]
        net=_receipt_net_money(store,reader,record.payload)
        if net is None:return None,f"CLOSE_RESULT_UNKNOWN:{trade_id}",[]
        pending.append((trade_id,net,closed_at))
    updated=state
    for _,net,closed_at in pending:updated=record_closed_trade(updated,net,closed_at,cooldown_minutes=settings.consecutive_loss_cooldown_minutes)
    return updated,None,pending
def prepare(store:StateStore,scope:str,reader:Mt5Reader,market:MarketSnapshot,settings:Settings,*,unresolved_lifecycle:bool)->RiskAuthority:
    if not store.integrity_check():return RiskAuthority(None,RiskDecision.UNKNOWN,"STATESTORE_INTEGRITY_FAILED")
    summary=_activity_summary(reader,settings,market)
    if summary.quality is not DataQuality.HEALTHY or summary.net_non_trading_cash_flow is None:return RiskAuthority(None,RiskDecision.UNKNOWN,summary.reason or "ACCOUNT_ACTIVITY_UNKNOWN")
    current_day=market.captured_at.astimezone(UTC).date().isoformat(); state=load(store,scope)
    if state is None or state.risk_day_utc!=current_day:
        if reader.account_positions_clear() is not True or unresolved_lifecycle:return RiskAuthority(state,RiskDecision.UNKNOWN,"RISK_DAY_BOOTSTRAP_REQUIRES_FLAT_RECONCILED_ACCOUNT",summary.net_non_trading_cash_flow)
        start=_reconstructed_day_start_equity(market,summary)
        if start is None:return RiskAuthority(state,RiskDecision.UNKNOWN,"DAY_START_EQUITY_RECONSTRUCTION_FAILED",summary.net_non_trading_cash_flow)
        state=initial(start,market.captured_at,aggressive_mode=settings.aggressive_small_account) if state is None else rollover(state,start,market.captured_at,aggressive_mode=settings.aggressive_small_account)
    updated,error,pending=_apply_unprocessed_closes(store,reader,state,settings)
    if updated is None:return RiskAuthority(state,RiskDecision.UNKNOWN,error or "CLOSE_RISK_RECONCILIATION_UNKNOWN",summary.net_non_trading_cash_flow)
    updated=with_account_safety_pl(updated,market.account.equity,summary.net_non_trading_cash_flow)
    with store.transaction():
        save(store,scope,updated)
        for trade_id,net,closed_at in pending:store.put(RISK_CLOSE_APPLIED_NS,trade_id,{"trade_id":trade_id,"net_money":net,"closed_at":closed_at.isoformat()},allow_replace=False)
    if updated.loss_locked:return RiskAuthority(updated,RiskDecision.BLOCK,"DAILY_LOSS_LOCKED",summary.net_non_trading_cash_flow)
    healthy=market_context_healthy(market,settings)
    if not cooldown_released(updated,market.captured_at,context_healthy=healthy,unresolved_lifecycle=unresolved_lifecycle):return RiskAuthority(updated,RiskDecision.BLOCK,"CONSECUTIVE_LOSS_COOLDOWN",summary.net_non_trading_cash_flow)
    if not healthy:return RiskAuthority(updated,RiskDecision.UNKNOWN,"RISK_RELEASE_CONTEXT_NOT_HEALTHY",summary.net_non_trading_cash_flow)
    return RiskAuthority(updated,RiskDecision.PASS,"RISK_STATE_PASS",summary.net_non_trading_cash_flow)
