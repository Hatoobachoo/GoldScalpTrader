"""Crash-safe compact PRIMARY terminal dashboard fallback.

This is the last-resort renderer.  It keeps the same operator hierarchy and key
English/Urdu cues without Rich/ANSI dependencies.  Presentation only.
"""
from __future__ import annotations

from textwrap import wrap

from .presentation import DashboardData


def _num(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _money(value: float | None) -> str:
    return "—" if value is None else f"${value:+.2f}"


def _score(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}"


def _urdu_action(action: str) -> str:
    upper = action.upper()
    if "BUY" in upper:
        return "خرید"
    if "SELL" in upper:
        return "فروخت"
    return "انتظار"


def _fit(text: str, width: int) -> str:
    return text if len(text) <= width else text[: max(1, width - 1)] + "…"


def _rule(title: str, width: int, char: str = "-") -> str:
    label = f" {title} " if title else ""
    if len(label) >= width:
        return _fit(label, width)
    return label + char * max(0, width - len(label))


def _wrapped(prefix: str, text: str, width: int) -> list[str]:
    room = max(16, width - len(prefix))
    pieces = wrap(str(text), room, break_long_words=False, break_on_hyphens=False) or ["—"]
    return [_fit((prefix if idx == 0 else " " * len(prefix)) + piece, width) for idx, piece in enumerate(pieces)]


def render_dashboard(data: DashboardData, *, emoji: bool = True, width: int = 78, color: bool | None = None) -> str:
    del color
    width = max(64, min(180, int(width)))
    e = (lambda x: x) if emoji else (lambda x: "")
    countdown = "—" if data.m5_seconds_remaining is None else f"{data.m5_seconds_remaining // 60:02d}:{data.m5_seconds_remaining % 60:02d}"
    shadows = ", ".join(data.shadow_setups) if data.shadow_setups else "NONE"
    lines = [
        _rule(f"{e('🪙')} GoldScalpTraderAI | PRIMARY LIVE SCALPING FLOOR | {data.bot_status}", width, "="),
        _fit(f"{e('🌍')} Market {data.market_state} | Session {data.soft_session} | {data.symbol}", width),
        _fit(f"{e('🔻')} SELL {_num(data.bid)} | {e('🔺')} BUY {_num(data.ask)} | Spread {_num(data.spread)} | M5 {countdown}", width),
        _fit(f"{e('🎯')} Action {data.live_action} ({_urdu_action(data.live_action)}) | Gate {data.gate_text}", width),
        _fit("M5 thesis • M1 timing • محفوظ عمل • منظم تجارت", width),
        _rule(f"{e('📊')} MARKET PICTURE / مارکیٹ", width),
        _fit(f"H4 {data.h4_structure} | H1 {data.h1_structure} | M15 {data.m15_structure} | M5 {data.m5_structure}", width),
        _fit(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)} | RSI {_num(data.rsi14,1)} | ATR {_num(data.atr14)}", width),
        _rule(f"{e('🎯')} CURRENT DECISION / موجودہ فیصلہ", width),
        _fit(f"Setup {data.detected_setup} | Active {data.active_family}", width),
        _fit(f"BUY {_score(data.buy_score)} | SELL {_score(data.sell_score)} | Lead {_score(data.leading_score)} | Coverage {_score(data.evidence_coverage)}%", width),
    ]
    lines.extend(_wrapped("WHY / وجہ: ", data.reason, width))
    lines.append(_rule(f"{e('📋')} TRADE PLAN / تجارتی منصوبہ", width))
    if data.plan_state is None:
        lines.append(_fit("WAITING | Entry — | SL — | TP1 — | TP2 —", width))
    else:
        lines.append(_fit(f"{data.plan_direction or '—'} | Entry {_num(data.plan_entry)} | SL {_num(data.plan_stop)} | TP1 {_num(data.plan_primary)} | TP2 {_num(data.plan_expansion)}", width))
    lines.append(_rule(f"{e('👥')} STRATEGY ISOLATION", width))
    if data.strategy_board_rows:
        for family, mode, qualification, direction, score, coverage in data.strategy_board_rows:
            lines.append(_fit(f"{family.replace('_',' ')} | {mode.replace('_',' ')} | {qualification.replace('_',' ')} | {direction} | {_score(score)}", width))
    else:
        lines.append(_fit(f"ACTIVE {data.active_family} | SHADOW {shadows}", width))
    lines += [
        _rule(f"{e('🛡️')} RISK & ACCOUNT", width),
        _fit(f"Balance {_money(data.account_balance)} | Equity {_money(data.account_equity)} | Free {_money(data.free_margin)}", width),
        _fit(f"Profile {data.risk_profile} | Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | Lot {_num(data.risk_volume,2)} | Pos {data.position_count if data.position_count is not None else '—'}/{data.position_capacity}", width),
        _rule(f"{e('⚙️')} SYSTEM / EXECUTION", width),
        _fit(f"Feed {data.live_feed_state} | Controller {data.controller_role} | Sync {data.broker_reconcile}", width),
    ]
    lines.extend(_wrapped("Exec: ", data.execution_text.replace("\n", " • "), width))
    if data.managed_trade_text and data.managed_trade_text.upper() != "NONE":
        lines.append(_rule(f"{e('💼')} OPEN TRADE / کھلی پوزیشن", width))
        lines.extend(_wrapped("", data.managed_trade_text.replace("\n", " • "), width))
    lines.append(_rule(f"{e('🧠')} LEARNING / DISCOVERY", width))
    lines.extend(_wrapped("Learning: ", data.learning_text or "Waiting for verified evidence", width))
    lines.extend(_wrapped("System: ", data.system_text, width))
    lines.append(_rule(f"{e('🔒')} محفوظ عمل • Browser SECONDARY • no broker controls", width, "="))
    return "\n".join(lines)


__all__ = ["render_dashboard"]
