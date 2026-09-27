"""Crash-safe compact PRIMARY terminal fallback with Roman Urdu cues.

The compact renderer is the last-resort presentation path. It must preserve the
same critical operator hierarchy as the Rich/narrow floors even when Rich is
unavailable or another presentation renderer fails. Presentation only; no
trading authority.
"""
from __future__ import annotations

from textwrap import wrap

from .presentation import DashboardData


def _num(v: float | None, d: int = 3) -> str:
    return "—" if v is None else f"{v:.{d}f}"


def _money(v: float | None) -> str:
    return "—" if v is None else f"${v:+.2f}"


def _score(v: float | None) -> str:
    return "—" if v is None else f"{v * 100:.1f}"


def _roman(action: str) -> str:
    upper = action.upper()
    return "Kharid" if "BUY" in upper else "Farokht" if "SELL" in upper else "Intazar"


def _fit(text: str, width: int) -> str:
    return text if len(text) <= width else text[: max(1, width - 1)] + "…"


def _rule(title: str, width: int, char: str = "-") -> str:
    label = f" {title} " if title else ""
    return _fit(label, width) if len(label) >= width else label + char * max(0, width - len(label))


def _wrapped(prefix: str, text: str, width: int) -> list[str]:
    room = max(16, width - len(prefix))
    parts = wrap(str(text), room, break_long_words=False, break_on_hyphens=False) or ["—"]
    return [
        _fit((prefix if index == 0 else " " * len(prefix)) + part, width)
        for index, part in enumerate(parts)
    ]


def render_dashboard(
    data: DashboardData,
    *,
    emoji: bool = True,
    width: int = 78,
    color: bool | None = None,
) -> str:
    del color
    width = max(64, min(180, int(width)))
    e = (lambda value: value) if emoji else (lambda value: "")
    countdown = (
        "—"
        if data.m5_seconds_remaining is None
        else f"{data.m5_seconds_remaining // 60:02d}:{data.m5_seconds_remaining % 60:02d}"
    )
    today = data.day_safety_pl if data.day_safety_pl is not None else data.bot_realized_pl_today

    lines = [
        _rule(f"{e('🪙')} GoldScalpTraderAI | PRIMARY LIVE SCALPING FLOOR | {data.bot_status}", width, "="),
        _fit("M5 thesis · M1 timing · structural routing · governed execution", width),
        _fit(f"{e('🌍')} Market {data.market_state} | Soft Context {data.soft_session} | {data.symbol}", width),
        _fit(f"{e('🔻')} SELL {_num(data.bid)} | {e('🔺')} BUY {_num(data.ask)} | Spread {_num(data.spread)} | M5 {countdown}", width),
        _fit(f"{e('🎯')} {data.live_action} | {_roman(data.live_action)} | Gate {data.gate_text}", width),
        _rule(f"{e('📊')} MARKET PICTURE · Market Jaiza", width),
        _fit(f"H4 {data.h4_structure} | H1 {data.h1_structure} | M15 {data.m15_structure} | M5 {data.m5_structure}", width),
        _fit(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)} | RSI {_num(data.rsi14, 1)} | ATR {_num(data.atr14)}", width),
        _rule(f"{e('👥')} TRADE SETUP · Setup aur Route", width),
        _fit(f"Detected {data.detected_setup} | Routed {data.active_family}", width),
        _fit(f"Timing {data.activity_text.replace(chr(10), ' • ')}", width),
        _rule(f"{e('🎯')} CURRENT DECISION · Maujooda Faisla", width),
        _fit(f"Setup {data.detected_setup} | Routed {data.active_family}", width),
        _fit(f"BUY {_score(data.buy_score)} | SELL {_score(data.sell_score)} | Lead {_score(data.leading_score)} | Coverage {_score(data.evidence_coverage)}%", width),
    ]
    lines.extend(_wrapped("WHY / Wajah: ", data.reason, width))

    lines.append(_rule(f"{e('📋')} TRADE PLAN · Mansuba", width))
    if data.plan_state is None:
        lines.append(_fit("WAITING | Entry — | SL — | TP1 — | TP2 — | Sahi mauqay ka intazar", width))
    else:
        lines.append(
            _fit(
                f"{data.plan_direction or '—'} | Entry {_num(data.plan_entry)} | SL {_num(data.plan_stop)} | "
                f"TP1 {_num(data.plan_primary)} | TP2 {_num(data.plan_expansion)}",
                width,
            )
        )

    lines.append(_rule(f"{e('👥')} STRATEGY / SETUP BOARD", width))
    if data.strategy_board_rows:
        for family, mode, qualification, direction, score, coverage in data.strategy_board_rows:
            lines.append(
                _fit(
                    f"{family.replace('_', ' ')} | {mode.replace('_', ' ')} | "
                    f"{qualification.replace('_', ' ')} | {direction} | {_score(score)}",
                    width,
                )
            )
    else:
        lines.append(_fit("Strategy facts unavailable — koi score invent nahi hoga.", width))

    lines.extend(
        [
            _rule(f"{e('🛡️')} RISK & ACCOUNT · Risk aur Account", width),
            _fit(
                f"Balance {_money(data.account_balance)} | Equity {_money(data.account_equity)} | "
                f"Free {_money(data.free_margin)}",
                width,
            ),
            _fit(
                f"Profile {data.risk_profile} | Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | "
                f"Lot {_num(data.risk_volume, 2)} | Pos {data.position_count if data.position_count is not None else '—'}/{data.position_capacity}",
                width,
            ),
            _rule(f"{e('📈')} TODAY / ACTIVITY · Aaj", width),
            _fit(
                f"Today {_money(today)} | Entries {data.entries_today if data.entries_today is not None else '—'} | "
                f"Trades {data.trades_total if data.trades_total is not None else '—'} | Cooldown {data.cooldown_state}",
                width,
            ),
            _fit(f"Hard Session {data.market_state} | Soft Context {data.soft_session}", width),
            _rule(f"{e('⚙️')} SYSTEM / EXECUTION · Nizam", width),
            _fit(
                f"Feed {data.live_feed_state} | Controller {data.controller_role} | Sync {data.broker_reconcile}",
                width,
            ),
        ]
    )
    lines.extend(_wrapped("Exec: ", data.execution_text.replace("\n", " • "), width))

    if data.managed_trade_text and data.managed_trade_text.upper() != "NONE":
        lines.append(_rule(f"{e('💼')} OPEN / MANAGED TRADE · Khula Trade", width))
        lines.extend(_wrapped("", data.managed_trade_text.replace("\n", " • "), width))

    lines.append(_rule(f"{e('🧠')} LEARNING / DISCOVERY · Seekhna aur Daryaft", width))
    lines.extend(_wrapped("Learning: ", data.learning_text or "Verified evidence ka intazar", width))
    lines.extend(_wrapped("System: ", data.system_text, width))
    lines.append(
        _rule(
            f"{e('🔒')} Mehfooz risk · Mehfooz amal · Browser SECONDARY · no broker controls",
            width,
            "=",
        )
    )
    return "\n".join(lines)


__all__ = ["render_dashboard"]
