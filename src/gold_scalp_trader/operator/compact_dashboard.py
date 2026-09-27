"""Crash-safe compact PRIMARY terminal fallback with Roman Urdu cues."""
from __future__ import annotations
from textwrap import wrap
from .presentation import DashboardData

def _num(v:float|None,d:int=3)->str:return "—" if v is None else f"{v:.{d}f}"
def _money(v:float|None)->str:return "—" if v is None else f"${v:+.2f}"
def _score(v:float|None)->str:return "—" if v is None else f"{v*100:.1f}"
def _roman(a:str)->str:
    u=a.upper();return "Kharid" if "BUY" in u else "Farokht" if "SELL" in u else "Intazar"
def _fit(t:str,w:int)->str:return t if len(t)<=w else t[:max(1,w-1)]+"…"
def _rule(t:str,w:int,c:str="-")->str:
    x=f" {t} " if t else "";return _fit(x,w) if len(x)>=w else x+c*max(0,w-len(x))
def _wrapped(p:str,t:str,w:int)->list[str]:
    room=max(16,w-len(p));parts=wrap(str(t),room,break_long_words=False,break_on_hyphens=False) or ["—"];return [_fit((p if i==0 else " "*len(p))+x,w) for i,x in enumerate(parts)]

def render_dashboard(data:DashboardData,*,emoji:bool=True,width:int=78,color:bool|None=None)->str:
    del color;width=max(64,min(180,int(width)));e=(lambda x:x) if emoji else (lambda x:"");cd="—" if data.m5_seconds_remaining is None else f"{data.m5_seconds_remaining//60:02d}:{data.m5_seconds_remaining%60:02d}"
    lines=[_rule(f"{e('🪙')} GoldScalpTraderAI | PRIMARY LIVE SCALPING FLOOR | {data.bot_status}",width,"="),_fit("M5 thesis · M1 timing · structural routing · governed execution",width),_fit(f"{e('🌍')} Market {data.market_state} | Soft Context {data.soft_session} | {data.symbol}",width),_fit(f"{e('🔻')} SELL {_num(data.bid)} | {e('🔺')} BUY {_num(data.ask)} | Spread {_num(data.spread)} | M5 {cd}",width),_fit(f"{e('🎯')} {data.live_action} | {_roman(data.live_action)} | Gate {data.gate_text}",width),_rule(f"{e('📊')} MARKET PICTURE · Market Jaiza",width),_fit(f"H4 {data.h4_structure} | H1 {data.h1_structure} | M15 {data.m15_structure} | M5 {data.m5_structure}",width),_fit(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)} | RSI {_num(data.rsi14,1)} | ATR {_num(data.atr14)}",width),_rule(f"{e('🎯')} CURRENT DECISION · Maujooda Faisla",width),_fit(f"Setup {data.detected_setup} | Routed {data.active_family}",width),_fit(f"BUY {_score(data.buy_score)} | SELL {_score(data.sell_score)} | Lead {_score(data.leading_score)} | Coverage {_score(data.evidence_coverage)}%",width)]
    lines.extend(_wrapped("WHY / Wajah: ",data.reason,width));lines.append(_rule(f"{e('📋')} TRADE PLAN · Mansuba",width))
    if data.plan_state is None:lines.append(_fit("WAITING | Entry — | SL — | TP1 — | TP2 — | Sahi mauqay ka intazar",width))
    else:lines.append(_fit(f"{data.plan_direction or '—'} | Entry {_num(data.plan_entry)} | SL {_num(data.plan_stop)} | TP1 {_num(data.plan_primary)} | TP2 {_num(data.plan_expansion)}",width))
    lines.append(_rule(f"{e('👥')} STRATEGY / SETUP BOARD",width))
    for family,mode,qualification,direction,score,coverage in data.strategy_board_rows:lines.append(_fit(f"{family.replace('_',' ')} | {mode.replace('_',' ')} | {qualification.replace('_',' ')} | {direction} | {_score(score)}",width))
    lines += [_rule(f"{e('🛡️')} RISK & ACCOUNT · Risk aur Account",width),_fit(f"Balance {_money(data.account_balance)} | Equity {_money(data.account_equity)} | Free {_money(data.free_margin)}",width),_fit(f"Profile {data.risk_profile} | Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | Lot {_num(data.risk_volume,2)}",width),_rule(f"{e('⚙️')} SYSTEM / EXECUTION · Nizam",width),_fit(f"Feed {data.live_feed_state} | Controller {data.controller_role} | Sync {data.broker_reconcile}",width)]
    lines.extend(_wrapped("Exec: ",data.execution_text.replace("\n"," • "),width));lines.append(_rule(f"{e('🧠')} LEARNING / DISCOVERY · Seekhna aur Daryaft",width));lines.extend(_wrapped("Learning: ",data.learning_text or "Verified evidence ka intazar",width));lines.extend(_wrapped("System: ",data.system_text,width));lines.append(_rule(f"{e('🔒')} Mehfooz amal · Browser SECONDARY · no broker controls",width,"="));return "\n".join(lines)

__all__=["render_dashboard"]
