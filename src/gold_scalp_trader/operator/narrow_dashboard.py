"""Width-safe English + Roman Urdu PRIMARY dashboard for 64-95 columns."""
from __future__ import annotations

try:
    from wcwidth import wcwidth, wcswidth
except ImportError:  # pragma: no cover
    def wcwidth(char: str) -> int: return 1
    def wcswidth(text: str) -> int: return len(text)

from .presentation import DashboardData


def _num(value: float | None, digits: int = 3) -> str: return "—" if value is None else f"{value:.{digits}f}"
def _money(value: float | None) -> str: return "—" if value is None else f"${value:+.2f}"
def _score(value: float | None) -> str: return "—" if value is None else f"{value * 100:.1f}"
def _roman(action: str) -> str:
    value=action.upper(); return "Kharid" if "BUY" in value else "Farokht" if "SELL" in value else "Intazar"
def _display_width(text: str) -> int:
    value=wcswidth(text); return len(text) if value < 0 else value
def _fit(text: str,width: int)->str:
    if _display_width(text)<=width:return text
    out=[];used=0;target=max(0,width-1)
    for char in text:
        size=max(0,wcwidth(char))
        if used+size>target:break
        out.append(char);used+=size
    return "".join(out)+"…"
def _rule(title:str,width:int,char:str="─")->str:
    label=f" {title} " if title else ""
    return _fit(label,width) if _display_width(label)>=width else label+char*(width-_display_width(label))
def _wrapped(text:str,width:int)->list[str]:
    words=str(text).split();lines=[];cur=""
    for word in words:
        cand=word if not cur else f"{cur} {word}"
        if _display_width(cand)<=width:cur=cand
        else:
            if cur:lines.append(_fit(cur,width))
            cur=_fit(word,width)
    if cur:lines.append(_fit(cur,width))
    return lines or ["—"]


def render_dashboard(data:DashboardData,*,emoji:bool=True,width:int=78,color:bool|None=None)->str:
    del color;width=max(64,min(95,int(width)));e=(lambda x:x) if emoji else (lambda x:"")
    cd="—" if data.m5_seconds_remaining is None else f"{data.m5_seconds_remaining//60:02d}:{data.m5_seconds_remaining%60:02d}"
    today=data.day_safety_pl if data.day_safety_pl is not None else data.bot_realized_pl_today
    lines=[
        _rule(f"{e('🪙')} GoldScalpTraderAI | PRIMARY | {data.account_mode} | {data.bot_status}",width,"═"),
        _fit("M5 thesis · M1 timing · structural routing · governed execution",width),
        _fit(f"{e('🌍')} Market {data.market_state} | Soft Context {data.soft_session} | {data.symbol}",width),
        _fit(f"{e('🔻')} SELL {_num(data.bid)} | {e('🔺')} BUY {_num(data.ask)} | Spread {_num(data.spread)} | M5 {cd}",width),
        _fit(f"{e('🎯')} {data.live_action} | {_roman(data.live_action)} | Gate {data.gate_text}",width),
        _rule(f"{e('📊')} MARKET PICTURE · Market Jaiza",width),
        _fit(f"H4 {data.h4_structure} | H1 {data.h1_structure} | M15 {data.m15_structure} | M5 {data.m5_structure}",width),
        _fit(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)} | RSI {_num(data.rsi14,1)} | ATR {_num(data.atr14)}",width),
        _rule(f"{e('🎯')} CURRENT DECISION · Maujooda Faisla",width),
        _fit(f"Setup {data.detected_setup} | Routed {data.active_family}",width),
        _fit(f"BUY {_score(data.buy_score)} | SELL {_score(data.sell_score)} | Lead {_score(data.leading_score)} | Cov {_score(data.evidence_coverage)}%",width),
    ]
    lines.extend(_wrapped(f"WHY / Wajah: {data.reason}",width));lines.append(_rule(f"{e('📋')} TRADE PLAN · Mansuba",width))
    if data.plan_state is None:lines.append(_fit("WAITING | Entry — | SL — | TP1 — | TP2 — | Sahi mauqay ka intazar",width))
    else:
        lines.append(_fit(f"{data.plan_direction or '—'} | Entry {_num(data.plan_entry)} | SL {_num(data.plan_stop)}",width));lines.append(_fit(f"TP1 {_num(data.plan_primary)} {_num(data.plan_primary_rr,2)}R | TP2 {_num(data.plan_expansion)} {_num(data.plan_expansion_rr,2)}R",width))
    lines.append(_rule(f"{e('👥')} STRATEGY / SETUP BOARD · 1 Routed + 5 Shadow",width))
    if data.strategy_board_rows:
        for family,mode,qualification,direction,score,coverage in data.strategy_board_rows:lines.append(_fit(f"{family.replace('_',' ')} | {mode.replace('_',' ')} | {qualification.replace('_',' ')} | {direction} | {_score(score)}",width))
    else:lines.append(_fit(f"Routed {data.active_family} | Shadow {', '.join(data.shadow_setups) if data.shadow_setups else 'NONE'}",width))
    lines += [_rule(f"{e('🛡️')} RISK & ACCOUNT · Risk aur Account",width),_fit(f"Balance {_money(data.account_balance)} | Equity {_money(data.account_equity)} | Free {_money(data.free_margin)}",width),_fit(f"Profile {data.risk_profile} | Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | Lot {_num(data.risk_volume,2)} | Pos {data.position_count if data.position_count is not None else '—'}/{data.position_capacity}",width),_rule(f"{e('⚙️')} SYSTEM / EXECUTION · Nizam",width),_fit(f"Feed {data.live_feed_state} | Controller {data.controller_role} | Sync {data.broker_reconcile}",width),_fit(f"Today {_money(today)} | Learning {data.learning_state} | Discovery {data.discovery_state}",width)]
    lines.extend(_wrapped(f"Exec: {data.execution_text.replace(chr(10),' • ')}",width))
    if data.managed_trade_text and data.managed_trade_text.upper()!="NONE":lines.append(_rule(f"{e('💼')} OPEN TRADE · Khula Trade",width));lines.extend(_wrapped(data.managed_trade_text.replace(chr(10)," • "),width))
    lines.append(_rule(f"{e('🧠')} LEARNING / DISCOVERY · Seekhna aur Daryaft",width));lines.extend(_wrapped(data.learning_text or "Verified evidence ka intazar",width));lines.extend(_wrapped(f"System: {data.system_text}",width));lines.append(_rule(f"{e('🔒')} Mehfooz amal · Browser SECONDARY · READ ONLY",width,"═"))
    return "\n".join(lines)

__all__=["render_dashboard"]
