"""Rich-based bilingual primary terminal dashboard.

Presentation only. Any import/render failure falls back to the compact renderer,
so a UI problem can never stop the trading process.
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
except ImportError:
    RICH_AVAILABLE = False
else:
    RICH_AVAILABLE = True


def _num(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _score(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}"


def _urdu(action: str) -> str:
    value = action.upper()
    return "خرید" if "BUY" in value else "فروخت" if "SELL" in value else "انتظار"


def _status_style(value: str) -> str:
    upper = str(value).upper()
    if any(x in upper for x in ("OPEN", "READY", "PASS", "BUY", "HEALTHY", "SCANNING")):
        return "bold bright_green"
    if any(x in upper for x in ("SELL", "BLOCK", "FAIL", "ERROR", "DEGRADED")):
        return "bold bright_red"
    if any(x in upper for x in ("WAIT", "UNKNOWN", "CLOSED", "PRE_CLOSE", "NOT EVALUATED")):
        return "bold yellow"
    return "bright_cyan"


def render_dashboard(data: DashboardData, *, emoji: bool = True, width: int = 120, color: bool | None = None) -> str:
    if not RICH_AVAILABLE:
        return fallback.render_dashboard(data, emoji=emoji, width=width, color=color)
    try:
        return _render(data, emoji=emoji, width=width, color=color)
    except Exception:
        return fallback.render_dashboard(data, emoji=emoji, width=width, color=color)


def _render(data: DashboardData, *, emoji: bool, width: int, color: bool | None) -> str:
    width = min(180, max(96, int(width)))
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
    m = {
        "gold": "🪙" if emoji else "[GOLD]",
        "market": "🌍" if emoji else "[MKT]",
        "sell": "🔻" if emoji else "SELL",
        "buy": "🔺" if emoji else "BUY",
        "clock": "⏱" if emoji else "[TIME]",
        "decision": "🎯" if emoji else "[DEC]",
        "chart": "📊" if emoji else "[AN]",
        "plan": "📋" if emoji else "[PLAN]",
        "risk": "🛡️" if emoji else "[RISK]",
        "exec": "⚙️" if emoji else "[EXEC]",
        "trade": "💼" if emoji else "[TRADE]",
        "learn": "🧠" if emoji else "[LEARN]",
        "system": "🩺" if emoji else "[SYS]",
        "shadow": "👥" if emoji else "[SHADOW]",
        "lock": "🔒" if emoji else "[SAFE]",
    }
    seconds = "—" if data.m5_seconds_remaining is None else f"{data.m5_seconds_remaining//60:02d}:{data.m5_seconds_remaining%60:02d}"
    renderables: list[Any] = [_header(data, m, seconds)]

    market = _market_panel(data, m)
    setup = _setup_panel(data, m)
    pair = Table.grid(expand=True, padding=(0, 1))
    pair.add_column(ratio=1)
    pair.add_column(ratio=1)
    pair.add_row(market, setup)
    renderables.append(pair)

    renderables.append(_decision_panel(data, m))
    renderables.append(_trade_plan_panel(data, m))

    lower = Table.grid(expand=True, padding=(0, 1))
    lower.add_column(ratio=1)
    lower.add_column(ratio=1)
    lower.add_column(ratio=1)
    lower.add_row(_risk_panel(data, m), _execution_panel(data, m), _system_panel(data, m))
    renderables.append(lower)

    if data.managed_trade_text and data.managed_trade_text != "NONE":
        renderables.append(Panel(Text(data.managed_trade_text), title=f"{m['trade']} OPEN / MANAGED TRADE", border_style="bright_green", box=box.ROUNDED))

    footer = Text.assemble(
        (f"{m['lock']} PRIMARY TERMINAL • محفوظ عمل • منظم تجارت", "bold bright_cyan"),
        ("  •  Browser dashboard = SECONDARY  •  Ctrl+C = safe local stop", "dim"),
    )
    renderables.append(Panel(footer, border_style="bright_cyan", box=box.ROUNDED, padding=(0, 1)))
    console.print(Group(*renderables))
    return stream.getvalue().rstrip("\n")


def _header(data: DashboardData, m: dict[str, str], seconds: str) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text.assemble(
        (f"{m['market']} Market ", None), (data.market_state, _status_style(data.market_state)),
        ("   Session ", None), (data.soft_session, "bright_cyan"),
        (f"   {m['gold']} {data.symbol}", "bright_yellow"),
        (f"   {m['sell']} SELL ", None), (_num(data.bid), "bright_red"),
        (f"   {m['buy']} BUY ", None), (_num(data.ask), "bright_green"),
    ))
    grid.add_row(Text.assemble(
        (f"Spread {_num(data.spread)}   {m['clock']} M5 {seconds}   {m['decision']} Action ", None),
        (data.live_action, _status_style(data.live_action)),
        (f" ({_urdu(data.live_action)})   Gate ", None),
        (data.gate_text, _status_style(data.gate_text)),
    ))
    grid.add_row(Text("تیز فیصلہ • محفوظ عمل • نظم و ضبط کے ساتھ مسلسل بہتری", style="bright_yellow"))
    title = Text.assemble(
        (f"{m['gold']} GoldScalpTraderAI  •  PRIMARY LIVE SCALPING FLOOR  •  ", "bold bright_yellow"),
        (data.bot_status, _status_style(data.bot_status)),
    )
    return Panel(grid, title=title, border_style="bright_yellow", box=box.DOUBLE, padding=(0, 1))


def _market_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"H4 {data.h4_structure} | H1 {data.h1_structure} | M15 {data.m15_structure} | M5 {data.m5_structure}"))
    grid.add_row(Text(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)}"))
    grid.add_row(Text(f"RSI {_num(data.rsi14,1)} | ATR {_num(data.atr14)}"))
    grid.add_row(Text(f"News {data.news_text}"))
    return Panel(grid, title=f"{m['chart']} MARKET ANALYSIS / مارکیٹ", border_style="bright_cyan", box=box.ROUNDED)


def _setup_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"Setup   {data.detected_setup}"))
    grid.add_row(Text(f"Active  {data.active_family}"))
    grid.add_row(Text(f"Shadows {', '.join(data.shadow_setups) if data.shadow_setups else 'NONE'}"))
    grid.add_row(Text(f"Timing  {data.activity_text.replace(chr(10), ' • ')}"))
    return Panel(grid, title=f"{m['shadow']} SETUP / TIMING", border_style="bright_magenta", box=box.ROUNDED)


def _decision_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(
        f"{m['buy']} BUY {_score(data.buy_score)} | {m['sell']} SELL {_score(data.sell_score)} | "
        f"Lead {_score(data.leading_score)} | Coverage {_score(data.evidence_coverage)}%"
    ))
    grid.add_row(Text(f"WHY: {data.reason}"))
    title = Text.assemble(
        (f"{m['decision']} CURRENT DECISION  |  ", None),
        (data.live_action, _status_style(data.live_action)),
        (f"  |  {_urdu(data.live_action)}", "bright_yellow"),
    )
    return Panel(grid, title=title, border_style=_status_style(data.live_action), box=box.ROUNDED)


def _trade_plan_panel(data: DashboardData, m: dict[str, str]) -> Any:
    return Panel(Text(data.trade_plan_text), title=f"{m['plan']} TRADE PLAN / تجارتی منصوبہ", border_style="bright_yellow", box=box.ROUNDED)


def _risk_panel(data: DashboardData, m: dict[str, str]) -> Any:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text(f"Balance {_num(data.account_balance,2)} | Equity {_num(data.account_equity,2)}"))
    grid.add_row(Text(f"Free Margin {_num(data.free_margin,2)}"))
    grid.add_row(Text(f"Profile {data.risk_profile} | Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | Lot {_num(data.risk_volume,2)}"))
    grid.add_row(Text(f"State {data.risk_text}"))
    return Panel(grid, title=f"{m['risk']} ACCOUNT & RISK", border_style="bright_blue", box=box.ROUNDED)


def _execution_panel(data: DashboardData, m: dict[str, str]) -> Any:
    body = Text(f"{data.execution_text}\n\n{data.managed_trade_text}")
    return Panel(body, title=f"{m['exec']} EXECUTION / TRADE", border_style="bright_green", box=box.ROUNDED)


def _system_panel(data: DashboardData, m: dict[str, str]) -> Any:
    body = Text(
        f"Learning  {data.learning_text or 'WAITING FOR VERIFIED EVIDENCE'}\n"
        f"System    {data.system_text}\n"
        f"Authority Browser secondary / read-only"
    )
    return Panel(body, title=f"{m['system']} LEARNING / SYSTEM", border_style="bright_cyan", box=box.ROUNDED)
