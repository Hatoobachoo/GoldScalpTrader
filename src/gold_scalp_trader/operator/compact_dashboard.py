"""Crash-safe compact primary terminal dashboard fallback."""
from __future__ import annotations

from textwrap import wrap

from .presentation import DashboardData


def _num(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}%"


def _urdu_action(action: str) -> str:
    upper = action.upper()
    if "BUY" in upper:
        return "خرید"
    if "SELL" in upper:
        return "فروخت"
    return "انتظار"


def _fit(text: str, width: int) -> str:
    return text if len(text) <= width else text[: max(1, width - 1)] + "…"


def _rule(title: str, width: int, char: str = "─") -> str:
    label = f" {title} " if title else ""
    return _fit(label, width) + char * max(0, width - len(label))


def _wrapped(prefix: str, text: str, width: int) -> list[str]:
    room = max(16, width - len(prefix))
    pieces = wrap(str(text), room, break_long_words=False, break_on_hyphens=False) or ["—"]
    return [_fit((prefix if idx == 0 else " " * len(prefix)) + piece, width) for idx, piece in enumerate(pieces)]


def render_dashboard(data: DashboardData, *, emoji: bool = True, width: int = 78, color: bool | None = None) -> str:
    del color
    width = max(64, min(160, int(width)))
    e = (lambda x: x) if emoji else (lambda x: "")
    shadows = ", ".join(data.shadow_setups) if data.shadow_setups else "NONE"
    lines = [
        _rule(f"{e('🪙')} GoldScalpTraderAI | PRIMARY SCALPING FLOOR | {data.bot_status}", width, "═"),
        _fit(f"{e('🌍')} Market {data.market_state} | Session {data.soft_session} | {data.symbol}", width),
        _fit(f"{e('🔻')} SELL {_num(data.bid)} | {e('🔺')} BUY {_num(data.ask)} | Spread {_num(data.spread)} | M5 {data.m5_seconds_remaining if data.m5_seconds_remaining is not None else '—'}s", width),
        _fit(f"{e('🎯')} Action {data.live_action} ({_urdu_action(data.live_action)}) | Gate {data.gate_text}", width),
        _rule(f"{e('📊')} MARKET ANALYSIS", width),
        _fit(f"H4 {data.h4_structure} | H1 {data.h1_structure} | M15 {data.m15_structure} | M5 {data.m5_structure}", width),
        _fit(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)} | RSI {_num(data.rsi14,1)} | ATR {_num(data.atr14)}", width),
        _rule(f"{e('🧠')} CURRENT DECISION", width),
        _fit(f"Setup {data.detected_setup} | Active {data.active_family}", width),
        _fit(f"BUY {_pct(data.buy_score)} | SELL {_pct(data.sell_score)} | Lead {_pct(data.leading_score)} | Coverage {_pct(data.evidence_coverage)}", width),
    ]
    lines.extend(_wrapped("WHY: ", data.reason, width))
    lines += [
        _rule(f"{e('📋')} TRADE PLAN", width),
        *_wrapped("", data.trade_plan_text.replace("\n", " • "), width),
        _rule(f"{e('🛡️')} RISK / ACCOUNT", width),
        _fit(f"Balance {_num(data.account_balance,2)} | Equity {_num(data.account_equity,2)} | Free {_num(data.free_margin,2)}", width),
        _fit(f"Profile {data.risk_profile} | Risk {_pct(None if data.risk_pct is None else data.risk_pct/100)} | Lot {_num(data.risk_volume,2)}", width),
        _rule(f"{e('⚙️')} EXECUTION / TRADE", width),
        *_wrapped("Exec: ", data.execution_text.replace("\n", " • "), width),
        *_wrapped("Trade: ", data.managed_trade_text.replace("\n", " • "), width),
        _rule(f"{e('👥')} SHADOW / LEARNING / SYSTEM", width),
        *_wrapped("Shadow: ", shadows + " • RESEARCH ONLY", width),
        *_wrapped("Learning: ", data.learning_text, width),
        *_wrapped("System: ", data.system_text, width),
        _rule(f"{e('🔒')} محفوظ عمل • منظم تجارت • Browser = SECONDARY", width, "═"),
    ]
    return "\n".join(lines)
