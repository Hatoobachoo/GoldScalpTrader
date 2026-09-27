"""Width-safe bilingual primary dashboard for terminals below 96 columns."""
from __future__ import annotations

try:
    from wcwidth import wcwidth, wcswidth
except ImportError:  # optional dependency; renderer remains available
    def wcwidth(char: str) -> int:
        return 1
    def wcswidth(text: str) -> int:
        return len(text)

from .presentation import DashboardData


def _num(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _score(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}"


def _action_urdu(action: str) -> str:
    value = action.upper()
    return "خرید" if "BUY" in value else "فروخت" if "SELL" in value else "انتظار"


def _display_width(text: str) -> int:
    value = wcswidth(text)
    return len(text) if value < 0 else value


def _fit(text: str, width: int) -> str:
    if _display_width(text) <= width:
        return text
    target = max(0, width - 1)
    out: list[str] = []
    used = 0
    for char in text:
        size = max(0, wcwidth(char))
        if used + size > target:
            break
        out.append(char)
        used += size
    return "".join(out) + "…"


def _rule(title: str, width: int, char: str = "─") -> str:
    label = f" {title} " if title else ""
    if _display_width(label) >= width:
        return _fit(label, width)
    return label + char * (width - _display_width(label))


def _wrap_words(text: str, width: int) -> list[str]:
    words = str(text).split()
    if not words:
        return ["—"]
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if _display_width(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(_fit(current, width))
            current = _fit(word, width)
    if current:
        lines.append(_fit(current, width))
    return lines


def render_dashboard(data: DashboardData, *, emoji: bool = True, width: int = 78, color: bool | None = None) -> str:
    del color
    width = max(64, min(95, int(width)))
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
        "learn": "🧠" if emoji else "[LEARN]",
        "lock": "🔒" if emoji else "[SAFE]",
    }
    seconds = "—" if data.m5_seconds_remaining is None else f"{data.m5_seconds_remaining//60:02d}:{data.m5_seconds_remaining%60:02d}"
    lines = [
        _rule(f"{m['gold']} GoldScalpTraderAI | PRIMARY | {data.bot_status}", width, "═"),
        _fit(f"{m['market']} Market {data.market_state} | Session {data.soft_session} | {data.symbol}", width),
        _fit(f"{m['sell']} SELL {_num(data.bid)} | {m['buy']} BUY {_num(data.ask)} | Spread {_num(data.spread)}", width),
        _fit(f"{m['clock']} M5 {seconds} | {m['decision']} {data.live_action} ({_action_urdu(data.live_action)}) | Gate {data.gate_text}", width),
        _rule(f"{m['chart']} MARKET / SETUP", width),
        _fit(f"H4 {data.h4_structure} | H1 {data.h1_structure} | M15 {data.m15_structure} | M5 {data.m5_structure}", width),
        _fit(f"EMA20 {_num(data.ema20)} | EMA50 {_num(data.ema50)} | RSI {_num(data.rsi14,1)} | ATR {_num(data.atr14)}", width),
        _fit(f"Setup {data.detected_setup} | Active {data.active_family}", width),
        _fit(f"BUY {_score(data.buy_score)} | SELL {_score(data.sell_score)} | Lead {_score(data.leading_score)} | Cov {_score(data.evidence_coverage)}%", width),
        _rule(f"{m['decision']} CURRENT DECISION / موجودہ فیصلہ", width),
    ]
    lines.extend(_wrap_words(f"WHY: {data.reason}", width))
    lines.append(_rule(f"{m['plan']} TRADE PLAN / تجارتی منصوبہ", width))
    for part in data.trade_plan_text.splitlines() or ["NOT AVAILABLE"]:
        lines.append(_fit(part, width))
    lines += [
        _rule(f"{m['risk']} RISK / ACCOUNT", width),
        _fit(f"Balance {_num(data.account_balance,2)} | Equity {_num(data.account_equity,2)} | Free {_num(data.free_margin,2)}", width),
        _fit(f"Profile {data.risk_profile} | Risk {'—' if data.risk_pct is None else f'{data.risk_pct:.2f}%'} | Lot {_num(data.risk_volume,2)}", width),
        _rule(f"{m['exec']} EXECUTION / MANAGED TRADE", width),
    ]
    for part in (data.execution_text + " | " + data.managed_trade_text).replace("\n", " | ").split(" | "):
        if part.strip():
            lines.append(_fit(part.strip(), width))
    shadows = ", ".join(data.shadow_setups) if data.shadow_setups else "NONE"
    lines += [
        _rule(f"{m['learn']} SHADOW / LEARNING / SYSTEM", width),
        _fit(f"Shadow {shadows} • RESEARCH ONLY", width),
    ]
    lines.extend(_wrap_words(f"Learning: {data.learning_text or 'WAITING FOR VERIFIED EVIDENCE'}", width))
    lines.extend(_wrap_words(f"System: {data.system_text}", width))
    lines.append(_rule(f"{m['lock']} محفوظ عمل • منظم تجارت • Browser SECONDARY", width, "═"))
    return "\n".join(lines)
