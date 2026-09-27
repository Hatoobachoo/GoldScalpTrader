"""GoldSwing live-floor composition adapted for GoldScalpTrader.

Presentation-only. This renderer consumes the canonical Scalp dashboard DTO and
never recalculates strategy, risk, routing, session authority, or broker writes.
The structure intentionally follows GoldSwingTrader's actual live_dashboard.py:
top market/action strip, market/setup cards, current decision, trade plan,
strategy floor, three-column risk/activity/system row, managed trade, and footer.
"""
from __future__ import annotations

from math import isfinite
import re
import sys

from .presentation import DashboardData


def render_dashboard(
    data: DashboardData,
    *,
    emoji: bool = True,
    width: int = 120,
    color: bool | None = None,
) -> str:
    """Render the primary wide terminal using the Swing floor hierarchy."""
    width = min(180, max(96, int(width)))
    color_enabled = sys.stdout.isatty() if color is None else color
    m = _markers(emoji)

    market = _badge(data.market_state, color_enabled)
    feed = _badge(data.live_feed_state, color_enabled)
    action = _paint(data.live_action, _decision_color(data.live_action), color_enabled)
    gate = _paint(_short_state(data.gate_text), _status_color(data.gate_text), color_enabled)
    today_pl = data.day_safety_pl if data.day_safety_pl is not None else data.bot_realized_pl_today

    lines = [
        _top_border(
            f"{m['gold']} GoldScalpTraderAI  •  PRIMARY LIVE SCALPING FLOOR  •  "
            f"{m['shield']} {data.account_mode}  •  {m['crown']} {data.runtime_role}",
            width,
        ),
        _box_row(
            f"{m['market']} Market {market}   {m['gold']} {data.symbol}   "
            f"{m['sell']} SELL {_paint(_num(data.bid), 'red', color_enabled)}   "
            f"{m['buy']} BUY {_paint(_num(data.ask), 'green', color_enabled)}   "
            f"{m['spread']} Spread {_num(data.spread)}   "
            f"{m['candle']} M5 {_countdown(data.m5_seconds_remaining)}",
            width,
        ),
        _box_row(
            f"{m['decision']} Action {action} / {_roman_action(data.live_action)}   "
            f"{m['news']} News {_short_state(data.news_health)}   "
            f"{m['execution']} Gate {gate}   "
            f"{m['money']} Today {_money(today_pl)}   "
            f"{m['plug']} Feed {feed}",
            width,
        ),
        _bottom_border(width),
        "",
    ]

    half = _half_width(width)
    market_card = _card(
        f"{m['market']} MARKET PICTURE · Market Jaiza",
        _market_rows(data, m, feed),
        half,
    )
    setup_card = _card(
        f"{m['plan']} TRADE SETUP · Setup aur Route",
        _setup_rows(data, m, color_enabled),
        width - half - 2,
    )
    lines.extend(_columns(market_card, setup_card))

    lines.extend([
        "",
        _panel(f"{m['decision']} CURRENT DECISION  |  {action}  |  {_roman_action(data.live_action)}", width),
        _row(
            f"{m['buy']} BUY Desk {_score(data.buy_score)} | "
            f"{m['sell']} SELL Desk {_score(data.sell_score)} | "
            f"{m['target']} Opportunity {_score(data.leading_score)} | "
            f"{m['coverage']} Coverage {_coverage(data.evidence_coverage)}",
            width,
        ),
        _row(
            f"{m['trophy']} Routed {_family(data.active_family)} | "
            f"Detected {_family(data.detected_setup)} | "
            f"{m['clock']} Next M5 {_countdown(data.m5_seconds_remaining)}",
            width,
        ),
        _row(f"{m['message']} Wajah / Reason: {data.reason}", width),
        "",
    ])

    lines.extend(_trade_plan_lines(data, m, color_enabled, width))
    lines.extend(["", _panel(f"{m['strategy']} STRATEGY / SETUP BOARD  |  1 ROUTED + 5 SHADOW", width)])
    lines.extend(_strategy_lines(data, m, color_enabled, width))
    lines.append("")

    third = _third_width(width)
    risk = _card(
        f"{m['risk']} RISK & ACCOUNT · Risk aur Account",
        [
            f"{m['wallet']} Balance {_account_money(data.account_balance)}",
            f"Equity {_account_money(data.account_equity)}   Free {_account_money(data.free_margin)}",
            f"{m['shield']} Profile {_friendly(data.risk_profile)}",
            f"Risk {_risk_pct(data.risk_pct)}   {m['lot']} Lot {_num(data.risk_volume, 2)}",
            f"{m['position']} Position {_count(data.position_count)}/{_count(data.position_capacity)}   Loss {_count(data.loss_streak)}",
            f"State {_friendly(data.risk_text)}",
        ],
        third,
    )
    today = _card(
        f"{m['activity']} TODAY / ACTIVITY · Aaj ki Soorat",
        [
            f"Entries {_count(data.bot_entries_today)}",
            f"Open {_count(data.position_count)}/{_count(data.position_capacity)}",
            f"{m['money']} Today P/L {_money(today_pl)}",
            f"Total Trades {_count(data.bot_total_trades)}",
            f"Cooldown {_friendly(data.cooldown)}",
            f"Hard Session {_friendly(data.market_state)}",
        ],
        third,
    )
    system = _card(
        f"{m['system']} SYSTEM / EXECUTION · Nizam aur Ijazat",
        [
            f"{m['plug']} Feed {_friendly(data.live_feed_state)}",
            f"{m['execution']} Gate {_friendly(data.gate_text)}",
            f"Controller {_friendly(data.controller_role)}",
            f"Broker Sync {_friendly(data.broker_reconcile)}",
            f"Schedule {'VERIFIED' if data.schedule_verified else 'UNVERIFIED' if data.schedule_verified is False else 'UNKNOWN'}",
            f"Exec {_one_line(data.execution_text)}",
        ],
        width - (2 * third) - 4,
    )
    if width >= 120:
        lines.extend(_three_columns(risk, today, system))
    else:
        lines.extend(risk + [""] + today + [""] + system)

    if data.managed_trade_text and data.managed_trade_text.upper() not in {"NONE", "UNKNOWN"}:
        lines.extend([
            "",
            _panel(f"{m['trade']} OPEN / MANAGED TRADE · Khula Trade", width),
            _row(_one_line(data.managed_trade_text), width),
        ])

    lines.extend([
        "",
        _panel(f"{m['learning']} LEARNING / DISCOVERY · Seekhna aur Daryaft", width),
        _row(
            f"{m['brain']} Learning {_friendly(data.learning_state)} | "
            f"{m['discovery']} Discovery {_friendly(data.discovery_state)} | "
            f"Candidate {data.candidate or 'NONE'}",
            width,
        ),
        _row(f"{m['message']} {_one_line(data.learning_text) or 'Verified evidence ka intazar'}", width),
        _row(f"{m['health']} System: {_one_line(data.system_text)}", width),
        _row("Browser = SECONDARY read-only projection · no BUY / SELL / MODIFY / CLOSE controls", width),
        _row("Sahi mauqa · sahi risk · phir hi trade.", width),
        _bottom_border(width),
    ])
    return "\n".join(lines)


def _market_rows(data: DashboardData, m: dict[str, str], feed: str) -> list[str]:
    return [
        f"H4  {_trend_icon(data.h4_structure)} {_friendly(data.h4_structure)}",
        f"H1  {_trend_icon(data.h1_structure)} {_friendly(data.h1_structure)}",
        f"M15 {_trend_icon(data.m15_structure)} {_friendly(data.m15_structure)}",
        f"M5  {_trend_icon(data.m5_structure)} {_friendly(data.m5_structure)}",
        f"{m['indicator']} EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)}",
        f"{m['rsi']} RSI {_num(data.rsi14, 1)} | {m['atr']} ATR {_num(data.atr14)}",
        f"{m['spread']} Spread {_num(data.spread)} | {m['plug']} Feed {feed}",
    ]


def _setup_rows(data: DashboardData, m: dict[str, str], color: bool) -> list[str]:
    direction = data.plan_direction or data.live_action
    return [
        f"{m['compass']} Bias       {_paint(_friendly(direction), _decision_color(direction), color)}",
        f"Detected   {_family(data.detected_setup)}",
        f"Routed     {_family(data.active_family)}",
        f"{m['entry']} Entry      {_num(data.plan_entry)}",
        f"{m['stop']} SL         {_num(data.plan_stop)}",
        f"{m['target']} TP1        {_num(data.plan_primary)}   {_r(data.plan_primary_rr)}",
        f"{m['rocket']} TP2        {_num(data.plan_expansion)}   {_r(data.plan_expansion_rr)}",
        f"State      {_friendly(data.plan_state or 'WAITING')}",
    ]


def _trade_plan_lines(data: DashboardData, m: dict[str, str], color: bool, width: int) -> list[str]:
    state = data.plan_state or "WAITING"
    title_state = _paint(state, _status_color(state), color)
    lines = [_panel(f"{m['plan']} TRADE PLAN  |  {title_state}", width)]
    if data.plan_state is None:
        lines.append(_row("No governed trade plan yet · valid setup aur timing ka intazar.", width))
        lines.append(_row(f"Plan facts: {_one_line(data.trade_plan_text)}", width))
        return lines
    lines.append(_row(
        f"{m['entry']} Entry {_num(data.plan_entry)} | {m['stop']} SL {_num(data.plan_stop)} | "
        f"{m['target']} TP1 {_num(data.plan_primary)} {_r(data.plan_primary_rr)} | "
        f"{m['rocket']} TP2 {_num(data.plan_expansion)} {_r(data.plan_expansion_rr)}",
        width,
    ))
    lines.append(_row(
        f"Direction {_friendly(data.plan_direction or 'UNKNOWN')} | Quality {_num(data.plan_quality, 1)} | "
        f"Invalidation {_friendly(data.plan_invalidation_source or 'STRUCTURAL')}",
        width,
    ))
    return lines


def _strategy_lines(data: DashboardData, m: dict[str, str], color: bool, width: int) -> list[str]:
    if not data.strategy_board_rows:
        return [_row("Strategy facts unavailable · koi score invent nahi hoga.", width)]
    lines = [_row(f"{'#':>2}  {'FAMILY':<32} {'MODE':<15} {'SIGNAL':<21} {'SCORE':>8} {'COV':>8}", width)]
    for idx, (family, mode, qualification, direction, score, coverage) in enumerate(data.strategy_board_rows, 1):
        signal = f"{_friendly(qualification)} / {_friendly(direction)}"
        raw = f"{idx:>2}  {_family(family):<32.32} {_friendly(mode):<15.15} {signal:<21.21} {_score(score):>8} {_coverage(coverage):>8}"
        style = "green" if "ACTIVE" in mode.upper() or "ROUTED" in mode.upper() else "magenta"
        lines.append(_row(_paint(raw, style, color), width))
    lines.append(_row("Scores = research/diagnostic facts only; production family selection structural routing se hoti hai.", width))
    return lines


def _markers(emoji: bool) -> dict[str, str]:
    if not emoji:
        return {k: "" for k in "gold market sell buy spread candle decision news execution money plug shield crown plan strategy risk wallet lot position activity system trade learning brain discovery message health target trophy clock coverage indicator rsi atr compass entry stop rocket".split()}
    return {
        "gold":"🪙","market":"🌍","sell":"🔻","buy":"🔺","spread":"↔","candle":"🕯","decision":"🎯",
        "news":"📰","execution":"🚦","money":"💰","plug":"🔌","shield":"🛡️","crown":"👑","plan":"📋",
        "strategy":"🧭","risk":"🛡️","wallet":"💳","lot":"📦","position":"📌","activity":"📈","system":"⚙️",
        "trade":"💼","learning":"🧠","brain":"🧠","discovery":"🔎","message":"💬","health":"❤️","target":"🎯",
        "trophy":"🏆","clock":"⏱","coverage":"🧩","indicator":"📐","rsi":"📊","atr":"📏","compass":"🧭",
        "entry":"📍","stop":"🛑","rocket":"🚀",
    }


def _top_border(title: str, width: int) -> str:
    inner = max(1, width - 2)
    clean = _truncate_visible(title, inner - 2)
    return "╔" + f" {clean} ".ljust(inner, "═") + "╗"


def _bottom_border(width: int) -> str:
    return "╚" + "═" * (width - 2) + "╝"


def _box_row(text: str, width: int) -> str:
    return "║" + _pad_visible(" " + text, width - 2) + "║"


def _panel(title: str, width: int) -> str:
    inner = width - 2
    return "┌" + _pad_visible(f" {title} ", inner, fill="─") + "┐"


def _row(text: str, width: int) -> str:
    return "│" + _pad_visible(" " + text, width - 2) + "│"


def _card(title: str, rows: list[str], width: int) -> list[str]:
    width = max(24, width)
    out = [_panel(title, width)]
    out.extend(_row(row, width) for row in rows)
    out.append("└" + "─" * (width - 2) + "┘")
    return out


def _columns(left: list[str], right: list[str]) -> list[str]:
    rows = max(len(left), len(right))
    lw = max((_visible_len(x) for x in left), default=0)
    rw = max((_visible_len(x) for x in right), default=0)
    return [
        _pad_visible(left[i] if i < len(left) else "", lw) + "  " + _pad_visible(right[i] if i < len(right) else "", rw)
        for i in range(rows)
    ]


def _three_columns(a: list[str], b: list[str], c: list[str]) -> list[str]:
    rows = max(len(a), len(b), len(c))
    widths = [max((_visible_len(x) for x in col), default=0) for col in (a, b, c)]
    out: list[str] = []
    for i in range(rows):
        parts = []
        for col, w in zip((a, b, c), widths):
            parts.append(_pad_visible(col[i] if i < len(col) else "", w))
        out.append("  ".join(parts))
    return out


def _half_width(width: int) -> int:
    return (width - 2) // 2


def _third_width(width: int) -> int:
    return max(30, (width - 4) // 3)


_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _visible_len(value: str) -> int:
    return len(_ANSI.sub("", value))


def _truncate_visible(value: str, width: int) -> str:
    if _visible_len(value) <= width:
        return value
    plain = _ANSI.sub("", value)
    return plain[: max(0, width - 1)] + "…"


def _pad_visible(value: str, width: int, fill: str = " ") -> str:
    value = _truncate_visible(value, width)
    return value + fill * max(0, width - _visible_len(value))


def _paint(value: str, color: str, enabled: bool) -> str:
    if not enabled:
        return value
    codes = {"red":"91","green":"92","yellow":"93","cyan":"96","magenta":"95","blue":"94","white":"97"}
    return f"\x1b[{codes.get(color, '97')}m{value}\x1b[0m"


def _badge(value: object, color: bool) -> str:
    text = _friendly(value)
    return _paint(text, _status_color(text), color)


def _status_color(value: object) -> str:
    u = str(value).upper()
    if any(x in u for x in ("BLOCK", "FAIL", "ERROR", "DEGRADED", "FAULT", "SELL")):
        return "red"
    if any(x in u for x in ("READY", "PASS", "HEALTHY", "ACTIVE", "LIVE", "OPEN", "BUY", "CLEAR")):
        return "green"
    if any(x in u for x in ("WAIT", "UNKNOWN", "CLOSED", "PRE_CLOSE", "NOT EVALUATED", "IDLE")):
        return "yellow"
    return "cyan"


def _decision_color(value: object) -> str:
    u = str(value).upper()
    return "green" if "BUY" in u else "red" if "SELL" in u else "yellow"


def _roman_action(value: object) -> str:
    u = str(value).upper()
    return "Kharid" if "BUY" in u else "Farokht" if "SELL" in u else "Intazar"


def _trend_icon(value: object) -> str:
    u = str(value).upper()
    if "BULL" in u or "UP" in u:
        return "▲"
    if "BEAR" in u or "DOWN" in u:
        return "▼"
    return "▶"


def _friendly(value: object) -> str:
    if value is None:
        return "—"
    text = str(value).strip()
    return text.replace("_", " ") if text else "—"


def _short_state(value: object) -> str:
    text = _friendly(value)
    for sep in (" • ", " | ", ":"):
        if sep in text:
            return text.split(sep, 1)[0]
    return text


def _family(value: object) -> str:
    return _friendly(value).title()


def _one_line(value: object) -> str:
    return " ".join(str(value or "").split())


def _num(value: float | None, digits: int = 3) -> str:
    if value is None or not isfinite(value):
        return "—"
    return f"{value:.{digits}f}"


def _money(value: float | None) -> str:
    if value is None or not isfinite(value):
        return "—"
    return f"${value:+.2f}"


def _account_money(value: float | None) -> str:
    if value is None or not isfinite(value):
        return "—"
    return f"${value:,.2f}"


def _score(value: float | None) -> str:
    if value is None or not isfinite(value):
        return "—"
    display = value * 100.0 if -1.0 <= value <= 1.0 else value
    return f"{display:.1f}"


def _coverage(value: float | None) -> str:
    if value is None or not isfinite(value):
        return "—"
    display = value * 100.0 if 0.0 <= value <= 1.0 else value
    return f"{display:.1f}%"


def _risk_pct(value: float | None) -> str:
    if value is None or not isfinite(value):
        return "—"
    return f"{value:.2f}%"


def _r(value: float | None) -> str:
    return "—" if value is None or not isfinite(value) else f"{value:.2f}R"


def _count(value: int | None) -> str:
    return "—" if value is None else str(value)


def _countdown(seconds: int | None) -> str:
    if seconds is None:
        return "—"
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


__all__ = ["render_dashboard"]
