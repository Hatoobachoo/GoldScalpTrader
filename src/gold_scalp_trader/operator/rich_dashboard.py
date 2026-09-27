"""Rich PRIMARY VS Code trading floor with English + Roman Urdu cues.

Presentation only. The renderer follows the mature Swing operator hierarchy
while keeping GoldScalp-specific M5 thesis, M1 timing and structural routing.
Any Rich failure falls back to the compact renderer.
"""
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
    RICH_AVAILABLE = False
else:
    RICH_AVAILABLE = True


def _num(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _money(value: float | None) -> str:
    return "—" if value is None else f"${value:+.2f}"


def _score(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}"


def _roman_action(action: str) -> str:
    upper = str(action).upper()
    if "BUY" in upper:
        return "Kharid"
    if "SELL" in upper:
        return "Farokht"
    return "Intazar"


def _status_style(value: object) -> str:
    upper = str(value).upper()
    if any(x in upper for x in ("OPEN", "READY", "PASS", "BUY", "HEALTHY", "ACTIVE", "LIVE", "CLEAR")):
        return "bold bright_green"
    if any(x in upper for x in ("SELL", "BLOCK", "FAIL", "ERROR", "DEGRADED", "FAULT")):
        return "bold bright_red"
    if any(x in upper for x in ("WAIT", "UNKNOWN", "CLOSED", "PRE_CLOSE", "NOT EVALUATED", "IDLE")):
        return "bold yellow"
    return "bright_cyan"


def _family(value: str) -> str:
    return str(value).replace("_", " ").title()


def _line(*parts: tuple[str, str | None]) -> Text:
    text = Text()
    for value, style in parts:
        text.append(str(value), style=style)
    return text


def _countdown(seconds: int | None) -> str:
    return "—" if seconds is None else f"{seconds // 60:02d}:{seconds % 60:02d}"


def _trend_icon(value: str) -> str:
    upper = str(value).upper()
    if "BULL" in upper or "UP" in upper:
        return "↗"
    if "BEAR" in upper or "DOWN" in upper:
        return "↘"
    return "↔"


def render_dashboard(data: DashboardData, *, emoji: bool = True, width: int = 120, color: bool | None = None) -> str:
    if not RICH_AVAILABLE:
        return fallback.render_dashboard(data, emoji=emoji, width=width, color=color)
    try:
        return _render(data, emoji=emoji, width=width, color=color)
    except Exception:
        return fallback.render_dashboard(data, emoji=emoji, width=width, color=color)


def _m(emoji: bool) -> dict[str, str]:
    return {
        "gold": "🪙" if emoji else "[GOLD]", "market": "🌍" if emoji else "[MKT]",
        "sell": "🔻" if emoji else "SELL", "buy": "🔺" if emoji else "BUY",
        "clock": "⏱" if emoji else "[TIME]", "decision": "🎯" if emoji else "[DEC]",
        "news": "📰" if emoji else "[NEWS]", "gate": "🚦" if emoji else "[GATE]",
        "chart": "📊" if emoji else "[AN]", "plan": "📋" if emoji else "[PLAN]",
        "risk": "🛡️" if emoji else "[RISK]", "activity": "📈" if emoji else "[ACT]",
        "system": "🩺" if emoji else "[SYS]", "trade": "💼" if emoji else "[TRADE]",
        "learn": "🧠" if emoji else "[LEARN]", "shadow": "👥" if emoji else "[SHADOW]",
        "lock": "🔒" if emoji else "[SAFE]", "target": "🎯" if emoji else "[TP]",
        "entry": "📍" if emoji else "[ENTRY]", "stop": "🛑" if emoji else "[SL]",
        "rocket": "🚀" if emoji else "[TP2]", "wallet": "👛" if emoji else "[BAL]",
    }


def _render(data: DashboardData, *, emoji: bool, width: int, color: bool | None) -> str:
    width = min(200, max(96, int(width)))
    stream = StringIO()
    color_enabled = sys.stdout.isatty() if color is None else color
    console = Console(file=stream, width=width, force_terminal=color_enabled,
                      color_system="truecolor" if color_enabled else None,
                      highlight=False, markup=False, emoji=emoji, legacy_windows=False,
                      soft_wrap=False)
    m = _m(emoji)
    items: list[Any] = [_identity_header(data, m), _market_strip(data, m)]

    pair = Table.grid(expand=True, padding=(0, 1)); pair.add_column(ratio=1); pair.add_column(ratio=1)
    pair.add_row(_market_panel(data, m), _setup_panel(data, m)); items.append(pair)
    items += [_decision_panel(data, m), _trade_plan_panel(data, m), _strategy_panel(data, m)]

    lower = Table.grid(expand=True, padding=(0, 1)); lower.add_column(ratio=1); lower.add_column(ratio=1); lower.add_column(ratio=1)
    lower.add_row(_risk_panel(data, m), _activity_panel(data, m), _system_panel(data, m)); items.append(lower)

    if data.managed_trade_text and data.managed_trade_text.upper() != "NONE":
        items.append(Panel(Text(data.managed_trade_text), title=f"{m['trade']} OPEN / MANAGED TRADE · Khula Trade",
                           border_style="bright_green", box=box.ROUNDED))
    items.append(_learning_panel(data, m))
    console.print(Group(*items)); return stream.getvalue().rstrip("\n")


def _identity_header(data: DashboardData, m: dict[str, str]) -> Any:
    body = Table.grid(expand=True); body.add_column(ratio=2); body.add_column(ratio=1, justify="right")
    body.add_row(
        _line((f"{m['gold']} GoldScalpTraderAI", "bold bright_yellow"),
              ("  •  PRIMARY LIVE SCALPING FLOOR", "bold bright_cyan")),
        _line((data.account_mode, "bold bright_green"), ("  •  ", None),
              (data.runtime_role, "bold bright_magenta"), ("  •  ", None),
              (data.bot_status, _status_style(data.bot_status))),
    )
    body.add_row(Text("M5 thesis · M1 timing · structural routing · governed execution", style="bright_cyan"),
                 Text("Tez faisla · Mehfooz risk · Discipline pehle", style="bright_yellow"))
    return Panel(body, border_style="bright_yellow", box=box.DOUBLE, padding=(0, 1))


def _market_strip(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(ratio=1); grid.add_column(ratio=1); grid.add_column(ratio=1); grid.add_column(ratio=1)
    grid.add_row(
        _line((f"{m['market']} Market ", None), (data.market_state, _status_style(data.market_state)),
              ("  · Soft Context ", None), (data.soft_session, "bright_cyan")),
        _line((f"{m['gold']} {data.symbol}  ", "bright_yellow"),
              (f"{m['sell']} {_num(data.bid)}  {m['buy']} {_num(data.ask)}", None)),
        _line((f"Spread {_num(data.spread)}  · {m['clock']} M5 {_countdown(data.m5_seconds_remaining)}", None)),
        _line((f"{m['decision']} ", None), (data.live_action, _status_style(data.live_action)),
              (f" · {_roman_action(data.live_action)}  {m['gate']} ", None),
              (data.gate_text, _status_style(data.gate_text))),
    )
    return Panel(grid, border_style="bright_cyan", box=box.ROUNDED, padding=(0, 1))


def _market_panel(data: DashboardData, m: dict[str, str]) -> Any:
    g = Table.grid(expand=True); g.add_column()
    for tf, value in (("H4",data.h4_structure),("H1",data.h1_structure),("M15",data.m15_structure),("M5",data.m5_structure)):
        g.add_row(Text(f"{tf:<3} {_trend_icon(value)} {value}"))
    g.add_row(Text(f"EMA20 {_num(data.ema20)}  |  EMA50 {_num(data.ema50)}"))
    g.add_row(Text(f"RSI {_num(data.rsi14,1)}  |  ATR {_num(data.atr14)}  |  Spread {_num(data.spread)}"))
    return Panel(g, title=f"{m['chart']} MARKET PICTURE · Market Jaiza", border_style="bright_cyan", box=box.ROUNDED)


def _setup_panel(data: DashboardData, m: dict[str, str]) -> Any:
    g=Table.grid(expand=True); g.add_column()
    g.add_row(Text(f"Detected Setup    {_family(data.detected_setup)}"))
    g.add_row(Text(f"Routed Family     {_family(data.active_family)}"))
    g.add_row(Text(f"Shadow Qualified  {', '.join(_family(x) for x in data.shadow_setups) if data.shadow_setups else 'NONE'}"))
    g.add_row(Text(f"Timing            {data.activity_text.replace(chr(10),' • ')}"))
    g.add_row(_line(("Plan State        ",None),(data.plan_state or "WAITING",_status_style(data.plan_state or "WAITING"))))
    return Panel(g,title=f"{m['shadow']} TRADE SETUP · Setup aur Route",border_style="bright_magenta",box=box.ROUNDED)


def _decision_panel(data: DashboardData, m: dict[str,str]) -> Any:
    g=Table.grid(expand=True);g.add_column()
    g.add_row(Text(f"{m['buy']} BUY {_score(data.buy_score)}  |  {m['sell']} SELL {_score(data.sell_score)}  |  Lead {_score(data.leading_score)}  |  Coverage {_score(data.evidence_coverage)}%"))
    g.add_row(Text(f"Setup {_family(data.detected_setup)}  |  Routed {_family(data.active_family)}"))
    g.add_row(Text(f"WHY / Wajah: {data.reason}"))
    return Panel(g,title=_line((f"{m['decision']} CURRENT DECISION  |  ",None),(data.live_action,_status_style(data.live_action)),(f"  |  {_roman_action(data.live_action)}","bright_yellow")),border_style=_status_style(data.live_action),box=box.ROUNDED)


def _trade_plan_panel(data: DashboardData,m:dict[str,str])->Any:
    if data.plan_state is None:
        return Panel(Text(f"{m['entry']} Entry —  |  {m['stop']} SL —  |  {m['target']} TP1 —  |  {m['rocket']} TP2 —\nSahi M5 opportunity ka intazar"),title=f"{m['plan']} TRADE PLAN · Mansuba | WAITING",border_style="yellow",box=box.ROUNDED)
    body=Text(f"{m['entry']} Entry {_num(data.plan_entry)} | {m['stop']} SL {_num(data.plan_stop)} | {m['target']} TP1 {_num(data.plan_primary)} ({_num(data.plan_primary_rr,2)}R) | {m['rocket']} TP2 {_num(data.plan_expansion)} ({_num(data.plan_expansion_rr,2)}R)\nDirection {data.plan_direction or '—'} | Invalidation {data.plan_invalidation_source or 'STRUCTURAL'} | Quality {_num(data.plan_quality,1)}")
    return Panel(body,title=f"{m['plan']} TRADE PLAN · Mansuba | {data.plan_state}",border_style="bright_yellow",box=box.ROUNDED)


def _strategy_panel(data:DashboardData,m:dict[str,str])->Any:
    if not data.strategy_board_rows:
        return Panel(Text("Strategy facts unavailable — koi score invent nahi hoga."),title=f"{m['shadow']} STRATEGY / SETUP BOARD",border_style="bright_magenta",box=box.ROUNDED)
    t=Table(box=box.SIMPLE_HEAD,expand=True,pad_edge=False);t.add_column("Strategy",ratio=3);t.add_column("Mode",ratio=2);t.add_column("Qual",ratio=2);t.add_column("Dir",ratio=1);t.add_column("Score",justify="right");t.add_column("Cov",justify="right")
    for family,mode,qualification,direction,score,coverage in data.strategy_board_rows:
        t.add_row(_family(family),mode.replace("_"," "),qualification.replace("_"," "),direction,_score(score),_score(coverage)+("%" if coverage is not None else ""))
    return Panel(t,title=f"{m['shadow']} STRATEGY / SETUP BOARD · 1 Routed + 5 Shadow",border_style="bright_magenta",box=box.ROUNDED)


def _risk_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"{m['wallet']} Balance {_money(data.account_balance)} | Equity {_money(data.account_equity)}"));g.add_row(Text(f"Free Margin {_money(data.free_margin)}"));g.add_row(Text(f"Profile {data.risk_profile} | Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | Lot {_num(data.risk_volume,2)}"));g.add_row(Text(f"Position {data.position_count if data.position_count is not None else '—'}/{data.position_capacity} | Loss Streak {data.loss_streak if data.loss_streak is not None else '—'}"));g.add_row(_line(("Risk State ",None),(data.risk_state,_status_style(data.risk_state))))
    return Panel(g,title=f"{m['risk']} RISK & ACCOUNT · Risk aur Account",border_style="bright_blue",box=box.ROUNDED)


def _activity_panel(data:DashboardData,m:dict[str,str])->Any:
    today=data.day_safety_pl if data.day_safety_pl is not None else data.bot_realized_pl_today;g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"Entries Today {data.entries_today if data.entries_today is not None else '—'}"));g.add_row(Text(f"Today P/L {_money(today)}"));g.add_row(Text(f"Total Trades {data.trades_total if data.trades_total is not None else '—'}"));g.add_row(Text(f"Cooldown {data.cooldown_state}"));g.add_row(Text(f"Hard Session {data.market_state} | Soft {data.soft_session}"))
    return Panel(g,title=f"{m['activity']} TODAY / ACTIVITY · Aaj",border_style="bright_green",box=box.ROUNDED)


def _system_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(_line(("Feed ",None),(data.live_feed_state,_status_style(data.live_feed_state))));g.add_row(_line(("Gate ",None),(data.gate_text,_status_style(data.gate_text))));g.add_row(Text(f"Controller {data.controller_role}"));g.add_row(Text(f"Broker Sync {data.broker_reconcile}"));g.add_row(Text(f"Exec {data.execution_text.replace(chr(10),' • ')}"))
    return Panel(g,title=f"{m['system']} SYSTEM / EXECUTION · Nizam",border_style="bright_cyan",box=box.ROUNDED)


def _learning_panel(data:DashboardData,m:dict[str,str])->Any:
    g=Table.grid(expand=True);g.add_column();g.add_row(Text(f"{m['learn']} Learning {data.learning_state}  |  Discovery {data.discovery_state}  |  Candidate {data.candidate_state}"));g.add_row(Text(data.learning_text or "Verified evidence ka intazar"));g.add_row(Text(f"System: {data.system_text}"));g.add_row(Text("Browser = SECONDARY read-only · no BUY/SELL/MODIFY/CLOSE controls",style="dim"));g.add_row(Text("Sahi mauqa, sahi risk, phir hi trade.",style="bright_yellow"))
    return Panel(g,title=f"{m['learn']} LEARNING / DISCOVERY · Seekhna aur Daryaft",border_style="bright_magenta",box=box.ROUNDED)


__all__=["render_dashboard"]
