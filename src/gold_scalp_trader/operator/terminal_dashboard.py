"""Primary terminal dashboard.

This is the normal operator surface, modelled after the GoldSwingTrader
terminal-first architecture.  It is presentation-only: it formats immutable
DashboardData and never imports Risk, Gate, MT5 writer or strategy authority.
"""
from __future__ import annotations

from shutil import get_terminal_size
from textwrap import wrap

from .presentation import DashboardData

NARROW_TERMINAL_MAX_WIDTH = 95
MIN_WIDTH = 64
MAX_WIDTH = 140


def render(data: DashboardData, *, width: int | None = None) -> str:
    """Render one complete operator frame.

    Width <=95 uses a stacked layout; wider terminals get a denser two-column
    floor.  Missing/error/closed states remain visible rather than suppressing
    the dashboard.
    """

    actual = width or get_terminal_size((100, 30)).columns
    actual = max(MIN_WIDTH, min(MAX_WIDTH, int(actual)))
    return _render_narrow(data, actual) if actual <= NARROW_TERMINAL_MAX_WIDTH else _render_wide(data, actual)


def _num(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _one_line(value: str) -> str:
    return " • ".join(part.strip() for part in value.splitlines() if part.strip()) or "—"


def _rule(title: str, width: int, char: str = "─") -> str:
    if not title:
        return char * width
    label = f" {title} "
    if len(label) >= width:
        return label[:width]
    return label + char * (width - len(label))


def _fit(text: str, width: int) -> str:
    text = str(text)
    if len(text) <= width:
        return text
    return text[: max(1, width - 1)] + "…"


def _wrapped(prefix: str, text: str, width: int) -> list[str]:
    available = max(16, width - len(prefix))
    chunks = wrap(str(text), width=available, break_long_words=False, break_on_hyphens=False) or ["—"]
    out = [prefix + chunks[0]]
    indent = " " * len(prefix)
    out.extend(indent + chunk for chunk in chunks[1:])
    return [_fit(line, width) for line in out]


def _status_line(data: DashboardData) -> str:
    quote = f"SELL {_num(data.bid)} | BUY {_num(data.ask)} | Spread {_num(data.spread)}"
    return f"Market {data.market_state} | Session {data.soft_session} | {data.symbol} | {quote}"


def _render_narrow(data: DashboardData, width: int) -> str:
    width = max(MIN_WIDTH, min(NARROW_TERMINAL_MAX_WIDTH, width))
    shadows = ", ".join(data.shadow_setups) if data.shadow_setups else "NONE"
    lines: list[str] = [
        _rule(f"GOLD SCALP TRADER | {data.bot_status}", width, "═"),
        _fit(_status_line(data), width),
        _rule("CURRENT DECISION", width),
        _fit(f"Setup {data.detected_setup} | Active {data.active_family}", width),
        _fit(f"Action {data.live_action} | Gate {data.gate_text}", width),
    ]
    lines.extend(_wrapped("WHY: ", data.reason, width))
    lines.extend(
        [
            _rule("TIMING / ACTIVITY", width),
            *_wrapped("", _one_line(data.activity_text), width),
            _rule("TRADE PLAN", width),
            *_wrapped("", _one_line(data.trade_plan_text), width),
            _rule("RISK / EXECUTION", width),
            *_wrapped("Risk: ", data.risk_text, width),
            *_wrapped("Exec: ", _one_line(data.execution_text), width),
            _rule("MANAGED TRADE", width),
            *_wrapped("", _one_line(data.managed_trade_text), width),
            _rule("SHADOW / LEARNING / SYSTEM", width),
            *_wrapped("Shadow: ", shadows + " • RESEARCH ONLY", width),
            *_wrapped("Learning: ", _one_line(data.learning_text), width),
            *_wrapped("News: ", data.news_text, width),
            *_wrapped("System: ", data.system_text, width),
            _rule("Ctrl+C = safe local stop | browser dashboard is secondary", width, "═"),
        ]
    )
    return "\n".join(lines)


def _box(title: str, body: list[str], width: int) -> list[str]:
    inner = max(8, width - 2)
    top_label = f" {title} "
    top = "┌" + top_label + "─" * max(0, inner - len(top_label)) + "┐"
    rows = [top]
    for raw in body:
        pieces = wrap(str(raw), width=inner, break_long_words=False, break_on_hyphens=False) or [""]
        for piece in pieces:
            rows.append("│" + piece.ljust(inner)[:inner] + "│")
    rows.append("└" + "─" * inner + "┘")
    return rows


def _merge(left: list[str], right: list[str], gap: int = 2) -> list[str]:
    left_w = max(len(line) for line in left)
    height = max(len(left), len(right))
    l = left + [" " * left_w] * (height - len(left))
    r = right + [""] * (height - len(right))
    return [l[i].ljust(left_w) + " " * gap + r[i] for i in range(height)]


def _render_wide(data: DashboardData, width: int) -> str:
    width = max(96, min(MAX_WIDTH, width))
    gap = 2
    left_w = (width - gap) // 2
    right_w = width - gap - left_w
    shadows = ", ".join(data.shadow_setups) if data.shadow_setups else "NONE"

    header = [
        _rule(f"GOLD SCALP TRADER | PRIMARY TERMINAL DASHBOARD | {data.bot_status}", width, "═"),
        _fit(_status_line(data), width),
    ]
    decision = _box(
        "CURRENT DECISION",
        [
            f"Setup  {data.detected_setup}",
            f"Active {data.active_family}",
            f"Action {data.live_action}",
            f"Gate   {data.gate_text}",
            f"Why    {data.reason}",
        ],
        left_w,
    )
    timing = _box(
        "TIMING / ACTIVITY",
        [
            _one_line(data.activity_text),
            f"News {data.news_text}",
        ],
        right_w,
    )
    plan = _box("TRADE PLAN", [_one_line(data.trade_plan_text)], left_w)
    risk = _box(
        "RISK / EXECUTION",
        [f"Risk {data.risk_text}", f"Execution {_one_line(data.execution_text)}"],
        right_w,
    )
    managed = _box("MANAGED TRADE", [_one_line(data.managed_trade_text)], left_w)
    system = _box(
        "SHADOW / LEARNING / SYSTEM",
        [
            f"Shadow {shadows} • RESEARCH ONLY",
            f"Learning {_one_line(data.learning_text)}",
            f"System {data.system_text}",
        ],
        right_w,
    )
    footer = _rule("Ctrl+C = safe local stop | graphical/browser dashboard = SECONDARY", width, "═")
    return "\n".join([*header, *_merge(decision, timing, gap), *_merge(plan, risk, gap), *_merge(managed, system, gap), footer])


def render_error(title: str, exc: Exception, *, width: int | None = None) -> str:
    """Render a fail-visible primary frame when normal runtime facts are unavailable."""

    data = DashboardData(
        symbol="XAUUSD",
        bid=None,
        ask=None,
        spread=None,
        market_state="UNKNOWN",
        soft_session="UNKNOWN",
        bot_status="SAFETY BLOCK / DEGRADED",
        detected_setup="UNAVAILABLE",
        active_family="UNAVAILABLE",
        live_action="WAIT",
        reason=f"{title}: {type(exc).__name__}: {exc}",
        shadow_setups=(),
        risk_text="NOT EVALUATED",
        gate_text="NOT EVALUATED",
        news_text="UNKNOWN • SOFT ONLY",
        system_text="DASHBOARD ALIVE • TRADING FAIL-CLOSED • NO BROKER WRITE FROM FAILED CYCLE",
        trade_plan_text="NOT AVAILABLE",
        managed_trade_text="UNKNOWN",
        execution_text="NO BROKER ACTION FROM FAILED CYCLE",
        activity_text="Runtime/startup facts unavailable",
        learning_text="PAUSED until runtime health recovers",
    )
    return render(data, width=width)


__all__ = ["NARROW_TERMINAL_MAX_WIDTH", "render", "render_error"]
