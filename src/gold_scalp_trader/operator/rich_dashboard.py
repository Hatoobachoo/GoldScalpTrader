"""Rich-based bilingual PRIMARY VS Code trading floor.

Presentation only.  This renderer deliberately mirrors the mature GoldSwing
operator hierarchy while adapting the facts to GoldScalp's M5 thesis, subordinate
M1 timing and one-active/five-shadow strategy-isolation architecture.  Any Rich
failure falls back to the compact renderer; UI failure can never stop trading.
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


def _pct(value: float | None, *, scale: bool = False) -> str:
    if value is None:
        return "—"
    shown = value * 100 if scale else value
    return f"{shown:.1f}%"


def _score(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}"


def _count(value: int | None) -> str:
    return "—" if value is None else str(value)


def _urdu(action: str) -> str:
    upper = str(action).upper()
    if "BUY" in upper:
        return "خرید"
    if "SELL" in upper:
        return "فروخت"
    return "انتظار"


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
    return value.replace("_", " ").title()


def _line(*parts: tuple[str, str | None]) -> Text:
    text = Text()
    for value, style in parts:
        text.append(str(value), style=style)
    return text


def _countdown(seconds: int | None) -> str:
    if seconds is None:
        return "—"
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def _trend_icon(value: str) -> str:
    upper = value.upper()
    if "BULL" in upper or "UP" in upper:
        return "↗"
    if "BEAR" in upper or "DOWN" in upper:
        return "↘"
    return "↔"


def render_dashboard(
    data: DashboardData,
    *,
    emoji: bool = True,
    width: int = 120,
    color: bool | None = None,
) -> str:
    if not RICH_AVAILABLE:
        return fallback.render_dashboard(data, emoji=emoji, width=width, color=color)
    try:
        return _render(data, emoji=emoji, width=width, color=color)
    except Exception:
        return fallback.render_dashboard(data, emoji=emoji, width=width, color=color)


def _markers(emoji: bool) -> dict[str, str]:
    return {
        "gold": "🪙" if emoji else "[GOLD]",
        "market": "🌍" if emoji else "[MKT]",
        "sell": "🔻" if emoji else "SELL",
        "buy": "🔺" if emoji else "BUY",
        "spread": "📏" if emoji else "[SPR]",
        "clock": "⏱" if emoji else "[TIME]",
        "decision": "🎯" if emoji else "[DEC]",
        "news": "📰" if emoji else "[NEWS]",
        "gate": "🚦" if emoji else "[GATE]",
        "chart": "📊" if emoji else "[AN]",
        "plan": "📋" if emoji else "[PLAN]",
        "risk": "🛡️" if emoji else "[RISK]",
        "account": "💰" if emoji else "[ACCT]",
        "activity": "📈" if emoji else "[ACT]",
        "system": "🩺" if emoji else "[SYS]",
        "trade": "💼" if emoji else "[TRADE]",
        "learn": "🧠" if emoji else "[LEARN]",
        "shadow": "👥" if emoji else "[SHADOW]",
        "lock": "🔒" if emoji else "[SAFE]",
        "target": "🎯" if emoji else "[TP]",
        "entry": "📍" if emoji else "[ENTRY]",
        "stop": "🛑" if emoji else "[SL]",
        "rocket": "🚀" if emoji else "[TP2]",
        "wallet": "👛" if emoji else "[BAL]",
        "brain": "🧠" if emoji else "[AI]",
        "search": "🔎" if emoji else "[DISC]",
    }


def _render(data: DashboardData, *, emoji: bool, width: int, color: bool | None) -> str:
    width = min(200, max(96, int(width)))
    color_enabled = sys.stdout.isatty() if color is None else color
    stream = StringIO()
    console = Console(
        file=stream,
        width=width,
        force_terminal=color_enabled,
        color_system="truecolor" if color_enabled else None,
        highlight=False,
        markup=False,
        emoji=emoji,
        legacy_windows=False,
        soft_wrap=False,
    )
    m = _markers(emoji)
    renderables: list[Any] = [_header(data, m)]

    pair = Table.grid(expand=True, padding=(0, 1))
    pair.add_column(ratio=1)
    pair.add_column(ratio=1)
    pair.add_row(_market_panel(data, m), _setup_panel(data, m))
    renderables.append(pair)

    renderables.append(_decision_panel(data, m))
    renderables.append(_trade_plan_panel(data, m))
    renderables.append(_strategy_panel(data, m))

    lower = Table.grid(expand=True, padding=(0, 1))
    lower.add_column(ratio=1)
    lower.add_column(ratio=1)
    lower.add_column(ratio=1)
    lower.add_row(_risk_panel(data, m), _activity_panel(data, m), _system_panel(data, m))
    renderables.append(lower)

    if data.managed_trade_text and data.managed_trade_text.upper() != "NONE":
        renderables.append(
            Panel(
                Text(data.managed_trade_text),
                title=f"{m['trade']} OPEN / MANAGED TRADE  •  کھلی پوزیشن",
                border_style="bright_green",
                box=box.ROUNDED,
            )
        )

    renderables.append(_learning_panel(data, m))
    console.print(Group(*renderables))
    return stream.getvalue().rstrip("\n")


def _header(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(
        _line(
            (f"{m['market']} Market ", None), (data.market_state, _status_style(data.market_state)),
            ("   Session ", None), (data.soft_session, "bright_cyan"),
            (f"   {m['gold']} {data.symbol}", "bright_yellow"),
            (f"   {m['sell']} SELL ", None), (_num(data.bid), "bright_red"),
            (f"   {m['buy']} BUY ", None), (_num(data.ask), "bright_green"),
        )
    )
    grid.add_row(
        _line(
            (f"{m['spread']} Spread {_num(data.spread)}   {m['clock']} M5 {_countdown(data.m5_seconds_remaining)}   ", None),
            (f"{m['decision']} Action ", None), (data.live_action, _status_style(data.live_action)),
            (f" ({_urdu(data.live_action)})   {m['news']} News ", None), (data.news_health, _status_style(data.news_health)),
            (f"   {m['gate']} Gate ", None), (data.gate_text, _status_style(data.gate_text)),
        )
    )
    grid.add_row(
        _line(
            ("M5 thesis • M1 subordinate timing • 1 Active + 5 Shadow   ", "bright_cyan"),
            ("تیز فیصلہ • محفوظ عمل • منظم تجارت", "bright_yellow"),
        )
    )
    title = _line(
        (f"{m['gold']} GoldScalpTraderAI  •  PRIMARY LIVE SCALPING FLOOR  •  ", "bold bright_yellow"),
        (data.account_mode, "bold bright_green"), ("  •  ", None),
        (data.runtime_role, "bold bright_magenta"), ("  •  ", None),
        (data.bot_status, _status_style(data.bot_status)),
    )
    return Panel(grid, title=title, border_style="bright_yellow", box=box.DOUBLE, padding=(0, 1))


def _market_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    for tf, value in (("H4", data.h4_structure), ("H1", data.h1_structure), ("M15", data.m15_structure), ("M5", data.m5_structure)):
        grid.add_row(Text(f"{tf:<3} {_trend_icon(value)} {value}"))
    grid.add_row(Text(f"EMA20 {_num(data.ema20)}  |  EMA50 {_num(data.ema50)}"))
    grid.add_row(Text(f"RSI {_num(data.rsi14, 1)}  |  ATR {_num(data.atr14)}"))
    grid.add_row(_line(("Feed ", None), (data.live_feed_state, _status_style(data.live_feed_state)), ("  |  Spread ", None), (_num(data.spread), "bright_cyan")))
    return Panel(grid, title=f"{m['chart']} MARKET PICTURE / مارکیٹ", border_style="bright_cyan", box=box.ROUNDED)


def _setup_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"Detected Setup   {_family(data.detected_setup)}"))
    grid.add_row(Text(f"Active Family    {_family(data.active_family)}"))
    grid.add_row(Text(f"Shadow Qualified {', '.join(_family(x) for x in data.shadow_setups) if data.shadow_setups else 'NONE'}"))
    grid.add_row(Text(f"Timing           {data.activity_text.replace(chr(10), ' • ')}"))
    grid.add_row(_line(("Plan State       ", None), (data.plan_state or "WAITING", _status_style(data.plan_state or "WAITING"))))
    return Panel(grid, title=f"{m['shadow']} TRADE SETUP / سیٹ اپ", border_style="bright_magenta", box=box.ROUNDED)


def _decision_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"{m['buy']} BUY Desk {_score(data.buy_score)}  |  {m['sell']} SELL Desk {_score(data.sell_score)}  |  Lead {_score(data.leading_score)}  |  Coverage {_score(data.evidence_coverage)}%"))
    grid.add_row(Text(f"{m['target']} Setup {_family(data.detected_setup)}  |  Active {_family(data.active_family)}"))
    grid.add_row(Text(f"WHY / وجہ: {data.reason}"))
    title = _line((f"{m['decision']} CURRENT DECISION  |  ", None), (data.live_action, _status_style(data.live_action)), (f"  |  {_urdu(data.live_action)}", "bright_yellow"))
    return Panel(grid, title=title, border_style=_status_style(data.live_action), box=box.ROUNDED)


def _trade_plan_panel(data: DashboardData, m: dict[str, str]) -> Any:
    if data.plan_state is None:
        body = Text(f"{m['entry']} Entry —  |  {m['stop']} SL —  |  {m['target']} TP1 —  |  {m['rocket']} TP2 —\nWaiting for qualifying M5 opportunity / درست موقع کا انتظار")
        return Panel(body, title=f"{m['plan']} TRADE PLAN / تجارتی منصوبہ  |  WAITING", border_style="yellow", box=box.ROUNDED)
    body = Text(
        f"{m['entry']} Entry {_num(data.plan_entry)}  |  {m['stop']} SL {_num(data.plan_stop)}  |  "
        f"{m['target']} TP1 {_num(data.plan_primary)} ({_num(data.plan_primary_rr, 2)}R)  |  "
        f"{m['rocket']} TP2 {_num(data.plan_expansion)} ({_num(data.plan_expansion_rr, 2)}R)\n"
        f"Direction {data.plan_direction or '—'}  |  Invalidation {data.plan_invalidation_source or 'STRUCTURAL'}  |  Quality {_num(data.plan_quality, 1)}"
    )
    return Panel(body, title=f"{m['plan']} TRADE PLAN / تجارتی منصوبہ  |  {data.plan_state}", border_style="bright_yellow", box=box.ROUNDED)


def _strategy_panel(data: DashboardData, m: dict[str, str]) -> Any:
    if not data.strategy_board_rows:
        body = Text("Strategy Isolation facts unavailable — dashboard will not invent family scores.")
        return Panel(body, title=f"{m['shadow']} STRATEGY ISOLATION  •  1 ACTIVE + 5 SHADOW", border_style="bright_magenta", box=box.ROUNDED)
    table = Table(box=box.SIMPLE_HEAD, expand=True, pad_edge=False)
    table.add_column("Strategy", ratio=3)
    table.add_column("Mode", ratio=2)
    table.add_column("Qual", ratio=2)
    table.add_column("Dir", ratio=1)
    table.add_column("Score", justify="right")
    table.add_column("Cov", justify="right")
    for family, mode, qualification, direction, score, coverage in data.strategy_board_rows:
        table.add_row(_family(family), mode.replace("_", " "), qualification.replace("_", " "), direction, _score(score), _score(coverage) + ("%" if coverage is not None else ""))
    return Panel(table, title=f"{m['shadow']} STRATEGY ISOLATION  •  ACTIVE EXECUTION vs SHADOW RESEARCH", border_style="bright_magenta", box=box.ROUNDED)


def _risk_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"{m['wallet']} Balance {_money(data.account_balance)}  |  Equity {_money(data.account_equity)}"))
    grid.add_row(Text(f"Free Margin {_money(data.free_margin)}"))
    grid.add_row(Text(f"Profile {data.risk_profile}  |  Risk {_pct(data.risk_pct)}  |  Lot {_num(data.risk_volume, 2)}"))
    grid.add_row(Text(f"Position {_count(data.position_count)}/{_count(data.position_capacity)}  |  Loss Streak {_count(data.loss_streak)}"))
    grid.add_row(_line(("Risk State ", None), (data.risk_text, _status_style(data.risk_text))))
    return Panel(grid, title=f"{m['risk']} RISK & ACCOUNT / رسک", border_style="bright_blue", box=box.ROUNDED)


def _activity_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"Entries Today {_count(data.bot_entries_today)}"))
    grid.add_row(Text(f"Today P/L {_money(data.day_safety_pl if data.day_safety_pl is not None else data.bot_realized_pl_today)}"))
    grid.add_row(Text(f"Total Trades {_count(data.bot_total_trades)}"))
    grid.add_row(Text(f"Cooldown {data.cooldown}"))
    grid.add_row(Text(f"Hard Session {data.market_state}  |  Schedule {'VERIFIED' if data.schedule_verified else 'UNKNOWN'}"))
    return Panel(grid, title=f"{m['activity']} TODAY / ACTIVITY", border_style="bright_green", box=box.ROUNDED)


def _system_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(_line(("Feed ", None), (data.live_feed_state, _status_style(data.live_feed_state))))
    grid.add_row(_line(("Gate ", None), (data.gate_text, _status_style(data.gate_text))))
    grid.add_row(Text(f"Controller {data.controller_role}"))
    grid.add_row(Text(f"Broker Sync {data.broker_reconcile}"))
    grid.add_row(Text(f"Exec {data.execution_text.replace(chr(10), ' • ')}"))
    return Panel(grid, title=f"{m['system']} SYSTEM / EXECUTION", border_style="bright_cyan", box=box.ROUNDED)


def _learning_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"{m['brain']} Learning {data.learning_state}  |  {m['search']} Discovery {data.discovery_state}  |  Candidate {data.candidate or 'NONE'}"))
    grid.add_row(Text(f"{data.learning_text or 'Waiting for verified evidence'}"))
    grid.add_row(Text(f"System: {data.system_text}"))
    grid.add_row(Text("Browser dashboard = SECONDARY read-only projection • no BUY/SELL/MODIFY/CLOSE controls", style="dim"))
    grid.add_row(Text("محفوظ عمل • منظم تجارت • سیکھنا حفاظت کو کبھی بائی پاس نہیں کرے گا", style="bright_yellow"))
    return Panel(grid, title=f"{m['learn']} LEARNING / DISCOVERY / BACKUP", border_style="bright_magenta", box=box.ROUNDED)


__all__ = ["RICH_AVAILABLE", "render_dashboard"]
