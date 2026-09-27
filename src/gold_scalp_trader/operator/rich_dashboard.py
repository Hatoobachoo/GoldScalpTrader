"""GoldSwing-derived Rich PRIMARY terminal floor adapted for GoldScalpTrader."""
from __future__ import annotations
from io import StringIO
import sys
from typing import Any
from . import compact_dashboard as fallback
from .presentation import DashboardData

try:
    from rich import box
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:  # pragma: no cover
    RICH_AVAILABLE=False
else:
    RICH_AVAILABLE=True


def _num(v:float|None,d:int=3)->str:return "—" if v is None else f"{v:.{d}f}"
def _money(v:float|None)->str:return "—" if v is None else f"${v:+.2f}"
def _score(v:float|None)->str:return "—" if v is None else f"{v*100:.1f}"
def _pct(v:float|None)->str:return "—" if v is None else f"{v*100:.1f}%"
def _family(v:str)->str:return str(v).replace("_"," ").title()
def _roman(a:str)->str:
    u=str(a).upper();return "Kharid" if "BUY" in u else "Farokht" if "SELL" in u else "Intazar"
def _status(v:object)->str:
    u=str(v).upper()
    if any(x in u for x in ("OPEN","READY","PASS","BUY","HEALTHY","ACTIVE","LIVE","CLEAR")):return "bold bright_green"
    if any(x in u for x in ("SELL","BLOCK","FAIL","ERROR","DEGRADED","FAULT")):return "bold bright_red"
    if any(x in u for x in ("WAIT","UNKNOWN","CLOSED","PRE_CLOSE","NOT EVALUATED","IDLE")):return "bold yellow"
    return "bright_cyan"
def _line(*parts:tuple[str,str|None])->Text:
    t=Text()
    for value,style in parts:t.append(str(value),style=style)
    return t
def _countdown(s:int|None)->str:return "—" if s is None else f"{s//60:02d}:{s%60:02d}"
def _trend(v:str)->str:
    u=str(v).upper();return "▲" if "BULL" in u or "UP" in u else "▼" if "BEAR" in u or "DOWN" in u else "▶"
def _m(emoji:bool)->dict[str,str]:
    return {"gold":"🪙" if emoji else "[GOLD]","market":"🌍" if emoji else "[MKT]","sell":"🔻" if emoji else "SELL","buy":"🔺" if emoji else "BUY","clock":"⏱" if emoji else "[TIME]","decision":"🎯" if emoji else "[DEC]","news":"📰" if emoji else "[NEWS]","gate":"🚦" if emoji else "[GATE]","chart":"📊" if emoji else "[AN]","plan":"📋" if emoji else "[PLAN]","risk":"🛡️" if emoji else "[RISK]","activity":"📈" if emoji else "[ACT]","system":"⚙️" if emoji else "[SYS]","trade":"💼" if emoji else "[TRADE]","learn":"🧠" if emoji else "[LEARN]","shadow":"👥" if emoji else "[SHADOW]","entry":"📍" if emoji else "[ENTRY]","stop":"🛑" if emoji else "[SL]","target":"🎯" if emoji else "[TP]","rocket":"🚀" if emoji else "[TP2]","wallet":"💰" if emoji else "[BAL]"}


def render_dashboard(data:DashboardData,*,emoji:bool=True,width:int=120,color:bool|None=None)->str:
    if not RICH_AVAILABLE:return fallback.render_dashboard(data,emoji=emoji,width=width,color=color)
    try:return _render(data,emoji=emoji,width=width,color=color)
    except Exception:return fallback.render_dashboard(data,emoji=emoji,width=width,color=color)


def _render(data:DashboardData,*,emoji:bool,width:int,color:bool|None)->str:
    width=min(200,max(96,int(width)));stream=StringIO();ce=sys.stdout.isatty() if color is None else color
    console=Console(file=stream,width=width,force_terminal=ce,color_system="truecolor" if ce else None,highlight=False,markup=False,emoji=emoji,legacy_windows=False,soft_wrap=False);m=_m(emoji);items:list[Any]=[_header(data,m)]
    market=_market_panel(data,m);setup=_setup_panel(data,m)
    pair=Table.grid(expand=True,padding=(0,1));pair.add_column(ratio=1);pair.add_column(ratio=1);pair.add_row(market,setup);items.append(pair)
    items.extend((_decision_panel(data,m),_trade_plan_panel(data,m),_strategy_panel(data,m)))
    lower=Table.grid(expand=True,padding=(0,1));lower.add_column(ratio=1);lower.add_column(ratio=1);lower.add_column(ratio=1);lower.add_row(_risk_panel(data,m),_today_panel(data,m),_system_panel(data,m));items.append(lower)
    if data.managed_trade_text and data.managed_trade_text.upper()!="NONE":items.append(Panel(Text(data.managed_trade_text),title=f"{m['trade']} OPEN / MANAGED TRADE · Khula Trade",border_style="bright_green",box=box.ROUNDED))
    items.append(_footer(data,m));console.print(Group(*items));return stream.getvalue().rstrip("\n")


def _header(data:DashboardData,m:dict[str,str])->Any:
    today=data.day_safety_pl if data.day_safety_pl is not None else data.bot_realized_pl_today
    g=Table.grid(expand=True);g.add_column()
    g.add_row(_line((f"{m['market']} Market ",None),(data.market_state,_status(data.market_state)),("   Soft Context ",None),(data.soft_session,"bright_cyan"),(f"   {m['gold']} {data.symbol}","bright_yellow"),(f"   {m['sell']} SELL ",None),(_num(data.bid),"bright_red"),(f"   {m['buy']} BUY ",None),(_num(data.ask),"bright_green")))
    g.add_row(_line((f"Spread {_num(data.spread)}",None),(f"   {m['clock']} M5 {_countdown(data.m5_seconds_remaining)}",None),(f"   {m['decision']} Action ",None),(data.live_action,_status(data.live_action)),(f" / {_roman(data.live_action)}", "bright_yellow"),(f"   {m['news']} News {data.news_health}",None),(f"   {m['gate']} Gate ",None),(data.gate_text,_status(data.gate_text))))
    g.add_row(_line((f"{m['wallet']} Today {_money(today)}",None),("   M5 thesis · M1 timing · structural routing · disciplined execution", "bright_cyan"),("   Mehfooz risk", "bright_yellow")))
    title=_line((f"{m['gold']} GoldScalpTraderAI  •  PRIMARY LIVE SCALPING FLOOR  •  ","bold bright_yellow"),(data.account_mode,"bold bright_green"),("  •  ",None),(data.runtime_role,"bold bright_magenta"),("  •  ",None),(data.bot_status,_status(data.bot_status)))
    return Panel(g,title=title,border_style="bright_yellow",box=box.DOUBLE,padding=(0,1))


def _market_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column()
    for tf,v in (("H4",data.h4_structure),("H1",data.h1_structure),("M15",data.m15_structure),("M5",data.m5_structure)):g.add_row(Text(f"{tf:<3} {_trend(v)} {v}"))
    g.add_row(Text(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)}"));g.add_row(Text(f"RSI {_num(data.rsi14,1)} | ATR {_num(data.atr14)} | Spread {_num(data.spread)}"));g.add_row(Text(f"Feed {data.live_feed_state} | Hard Session {data.market_state}"))
    return Panel(g,title=f"{m['chart']} MARKET PICTURE · Market Jaiza",border_style="bright_cyan",box=box.ROUNDED)


def _setup_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"Detected Setup   {_family(data.detected_setup)}"));g.add_row(Text(f"Routed Family    {_family(data.active_family)}"));g.add_row(Text(f"Timing           {data.activity_text.replace(chr(10),' • ')}"));g.add_row(Text(f"Entry            {_num(data.plan_entry)}"));g.add_row(Text(f"Stop Loss        {_num(data.plan_stop)}"));g.add_row(Text(f"Target           {_num(data.plan_primary)}"));g.add_row(_line(("Plan Status      ",None),(data.plan_state or "WAITING",_status(data.plan_state or "WAITING"))))
    return Panel(g,title=f"{m['plan']} TRADE SETUP · Setup aur Route",border_style="bright_yellow",box=box.ROUNDED)


def _decision_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"{m['buy']} BUY Desk {_score(data.buy_score)} | {m['sell']} SELL Desk {_score(data.sell_score)} | Opportunity {_score(data.leading_score)} | Coverage {_pct(data.evidence_coverage)}"));g.add_row(Text(f"{m['shadow']} Lead {_family(data.active_family)} | Detected {_family(data.detected_setup)}"));g.add_row(Text(f"Wajah: {data.reason}"));g.add_row(Text(f"Next M5 {_countdown(data.m5_seconds_remaining)}"));title=_line((f"{m['decision']} CURRENT DECISION  |  ",None),(data.live_action,_status(data.live_action)),(f"  |  {_roman(data.live_action)}","bright_yellow"));return Panel(g,title=title,border_style=_status(data.live_action),box=box.ROUNDED)


def _trade_plan_panel(data:DashboardData,m:dict[str,str])->Any:
    if data.plan_state is None:return Panel(Text("No trade plan yet — Entry / SL / TP1 / TP2 valid setup ke baad nazar ayenge."),title=f"{m['plan']} TRADE PLAN | WAITING",border_style="yellow",box=box.ROUNDED)
    body=Text(f"{m['entry']} Entry {_num(data.plan_entry)} | {m['stop']} SL {_num(data.plan_stop)} | {m['target']} TP1 {_num(data.plan_primary)} ({_num(data.plan_primary_rr,2)}R) | {m['rocket']} TP2 {_num(data.plan_expansion)} ({_num(data.plan_expansion_rr,2)}R) | Invalidation {data.plan_invalidation_source or 'STRUCTURAL'}")
    return Panel(body,title=f"{m['plan']} TRADE PLAN | {data.plan_state} | Quality {_num(data.plan_quality,1)}",border_style=_status(data.plan_state),box=box.ROUNDED)


def _strategy_panel(data:DashboardData,m:dict[str,str])->Any:
    if not data.strategy_board_rows:return Panel(Text("Strategy facts unavailable — koi score invent nahi hoga."),title=f"{m['shadow']} STRATEGY / SETUP BOARD",border_style="bright_magenta",box=box.ROUNDED)
    t=Table(box=box.SIMPLE_HEAD,expand=True,pad_edge=False);t.add_column("#",justify="right");t.add_column("Strategy",ratio=3);t.add_column("Mode",ratio=2);t.add_column("Signal",ratio=2);t.add_column("Score",justify="right");t.add_column("Cov",justify="right")
    for i,(family,mode,qual,direction,score,cov) in enumerate(data.strategy_board_rows,1):t.add_row(str(i),_family(family),mode.replace("_"," "),f"{qual.replace('_',' ')} / {direction}",_score(score),_pct(cov))
    return Panel(t,title=f"{m['shadow']} STRATEGY / SETUP BOARD · 1 Routed + 5 Shadow",border_style="bright_magenta",box=box.ROUNDED)


def _risk_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"Balance {_money(data.account_balance)}"));g.add_row(Text(f"Equity {_money(data.account_equity)}"));g.add_row(Text(f"Free Margin {_money(data.free_margin)}"));g.add_row(Text(f"Profile {data.risk_profile}"));g.add_row(Text(f"Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | Lot {_num(data.risk_volume,2)}"));g.add_row(Text(f"Position {data.position_count if data.position_count is not None else '—'}/{data.position_capacity} | Loss Streak {data.loss_streak if data.loss_streak is not None else '—'}"));g.add_row(_line(("Risk State ",None),(data.risk_text,_status(data.risk_text))));return Panel(g,title=f"{m['risk']} RISK & ACCOUNT · Risk aur Account",border_style="bright_blue",box=box.ROUNDED)


def _today_panel(data:DashboardData,m:dict[str,str])->Any:
    today=data.day_safety_pl if data.day_safety_pl is not None else data.bot_realized_pl_today;g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"Entries Today {data.bot_entries_today if data.bot_entries_today is not None else '—'}"));g.add_row(Text(f"Today P/L {_money(today)}"));g.add_row(Text(f"Total Trades {data.bot_total_trades if data.bot_total_trades is not None else '—'}"));g.add_row(Text(f"Cooldown {data.cooldown}"));g.add_row(Text(f"Hard Session {data.market_state}"));g.add_row(Text(f"Soft Context {data.soft_session}"));return Panel(g,title=f"{m['activity']} TODAY / ACTIVITY · Aaj",border_style="bright_green",box=box.ROUNDED)


def _system_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(_line(("Feed ",None),(data.live_feed_state,_status(data.live_feed_state))));g.add_row(_line(("Gate ",None),(data.gate_text,_status(data.gate_text))));g.add_row(Text(f"Controller {data.controller_role}"));g.add_row(Text(f"Broker Sync {data.broker_reconcile}"));g.add_row(Text(f"Exec {data.execution_text.replace(chr(10),' • ')}"));g.add_row(Text(f"Schedule {'VERIFIED' if data.schedule_verified else 'UNVERIFIED'}"));return Panel(g,title=f"{m['system']} SYSTEM / EXECUTION · Nizam",border_style="bright_cyan",box=box.ROUNDED)


def _footer(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"{m['learn']} Learning {data.learning_state} | Discovery {data.discovery_state} | Candidate {data.candidate or 'NONE'}"));g.add_row(Text(data.learning_text or "Verified evidence ka intazar"));g.add_row(Text(f"System: {data.system_text}"));g.add_row(Text("Browser = SECONDARY read-only · no BUY/SELL/MODIFY/CLOSE controls",style="dim"));g.add_row(Text("Sahi mauqa · sahi risk · phir hi trade.",style="bright_yellow"));return Panel(g,title=f"{m['learn']} LEARNING / DISCOVERY · Seekhna aur Daryaft",border_style="bright_magenta",box=box.ROUNDED)

__all__=["render_dashboard"]
