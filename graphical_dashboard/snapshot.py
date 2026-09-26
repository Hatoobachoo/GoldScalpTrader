"""Read-only atomic browser snapshot for the GoldScalpTrader visual floor."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from gold_scalp_trader.operator.presentation import DashboardData
from gold_scalp_trader.security.financial_secrets import contains_probable_secret

SCHEMA_VERSION = 1
DEFAULT_FILENAME = "dashboard_snapshot.json"


def _value(obj: object | None, name: str, default: Any = None) -> Any:
    return default if obj is None else getattr(obj, name, default)


def _enum(value: object | None, default: str = "UNKNOWN") -> str:
    if value is None:
        return default
    return str(getattr(value, "value", value))


def _candle_row(candle: object) -> dict[str, Any]:
    opened = getattr(candle, "open_time", None)
    return {
        "time_utc": opened.isoformat() if hasattr(opened, "isoformat") else str(opened),
        "open": float(getattr(candle, "open")),
        "high": float(getattr(candle, "high")),
        "low": float(getattr(candle, "low")),
        "close": float(getattr(candle, "close")),
        "tick_volume": int(getattr(candle, "tick_volume", 0)),
    }


def _chart_payload(candles_by_tf: Mapping[str, tuple]) -> dict[str, list[dict[str, Any]]]:
    charts: dict[str, list[dict[str, Any]]] = {}
    for timeframe in ("M1", "M5", "M15", "H1", "H4"):
        rows = candles_by_tf.get(timeframe, ())
        charts[timeframe] = [_candle_row(item) for item in rows[-80:]]
    return charts


def _intelligence_payload(runtime_result: object | None) -> tuple[dict[str, Any], dict[str, Any]]:
    cycle = _value(runtime_result, "cycle")
    intelligence = _value(cycle, "intelligence")
    by_timeframe = _value(intelligence, "by_timeframe", {}) or {}
    structure: dict[str, Any] = {}
    indicators: dict[str, Any] = {}
    for timeframe, frame in by_timeframe.items():
        tf = _enum(timeframe)
        report = _value(frame, "structure")
        quant = _value(frame, "quant")
        structure[tf] = {
            "state": _enum(_value(report, "state")),
            "break": _enum(_value(report, "break_event"), "NONE"),
            "direction": _enum(_value(report, "break_direction"), "NONE"),
        }
        indicators[tf] = {
            "ema20": _value(quant, "ema20"),
            "ema50": _value(quant, "ema50"),
            "rsi": _value(quant, "rsi14"),
            "atr": _value(quant, "atr14"),
            "flow": _value(quant, "ema_flow"),
            "volatility": _value(quant, "volatility_state"),
        }
    return structure, indicators


def _plan_payload(runtime_result: object | None) -> dict[str, Any]:
    cycle = _value(runtime_result, "cycle")
    plan = _value(cycle, "trade_plan")
    if plan is None:
        return {"exists": False}
    return {
        "exists": True,
        "id": _value(plan, "trade_plan_id"),
        "direction": _enum(_value(plan, "direction"), "WAIT"),
        "entry": _value(plan, "entry_reference"),
        "stop": _value(plan, "initial_sl"),
        "primary": _value(plan, "primary_target"),
        "expansion": _value(plan, "expansion_target"),
        "gross_r": _value(plan, "gross_r"),
        "policy_version": _value(plan, "policy_version"),
    }


def _timing_payload(runtime_result: object | None) -> dict[str, Any]:
    cycle = _value(runtime_result, "cycle")
    timing = _value(cycle, "timing")
    opportunity = _value(cycle, "opportunity")
    return {
        "outcome": _enum(_value(timing, "outcome"), "NOT_EVALUATED"),
        "profile": _value(timing, "profile"),
        "policy_version": _value(timing, "policy_version"),
        "trigger_age_seconds": _value(timing, "trigger_age_seconds"),
        "m5_event_age_bars": _value(timing, "m5_event_age_bars"),
        "chase_atr": _value(timing, "chase_atr"),
        "micro_extension_atr": _value(timing, "micro_extension_atr"),
        "opportunity_id": _value(opportunity, "opportunity_id"),
        "episode_id": _value(opportunity, "episode_id"),
        "opportunity_state": _enum(_value(opportunity, "state"), "NONE"),
    }


def _risk_payload(runtime_result: object | None) -> dict[str, Any]:
    cycle = _value(runtime_result, "cycle")
    risk = _value(cycle, "risk")
    return {
        "decision": _enum(_value(risk, "decision"), "NOT_EVALUATED"),
        "risk_pct": _value(risk, "actual_risk_pct"),
        "volume": _value(risk, "volume"),
        "reason": _value(risk, "reason"),
    }


def _session_payload(runtime_result: object | None, data: DashboardData) -> dict[str, Any]:
    provider = _value(runtime_result, "provider")
    session = _value(provider, "session")
    news = _value(provider, "news")
    return {
        "hard_state": _enum(_value(session, "state"), data.market_state),
        "schedule_verified": bool(_value(session, "schedule_verified", False)),
        "tradeable": _value(session, "tradeable"),
        "source": _value(session, "source"),
        "reason": _value(session, "reason"),
        "soft_session": data.soft_session,
        "news_health": _enum(_value(news, "health"), "UNKNOWN"),
        "news_source": _value(news, "source"),
    }


def _management_payload(runtime_result: object | None) -> dict[str, Any] | None:
    trade = _value(runtime_result, "managed_trade")
    if trade is None:
        return None
    return {
        "ticket": _value(trade, "ticket"),
        "family": _enum(_value(trade, "family")),
        "direction": _enum(_value(trade, "direction")),
        "entry": _value(trade, "entry"),
        "stop": _value(trade, "current_sl"),
        "primary": _value(trade, "primary_target"),
        "expansion": _value(trade, "expansion_target"),
        "timing_profile": _value(trade, "timing_profile"),
        "timing_policy_version": _value(trade, "timing_policy_version"),
        "manager_action": _enum(_value(runtime_result, "management_action"), "HOLD"),
    }


def _market_payload(runtime_result: object | None, data: DashboardData) -> dict[str, Any]:
    cycle = _value(runtime_result, "cycle")
    intelligence = _value(cycle, "intelligence")
    market = _value(intelligence, "market")
    account = _value(market, "account")
    quote = _value(market, "quote")
    quote_time = _value(quote, "source_time")
    return {
        "symbol": data.symbol,
        "state": data.market_state,
        "bid": data.bid,
        "ask": data.ask,
        "spread": data.spread,
        "quote_time_utc": quote_time.isoformat() if hasattr(quote_time, "isoformat") else None,
        "balance": _value(account, "balance"),
        "equity": _value(account, "equity"),
        "free_margin": _value(account, "margin_free"),
    }


def build_snapshot(
    data: DashboardData,
    candles_by_tf: Mapping[str, tuple],
    *,
    runtime_result: object | None = None,
    generated_at_utc: datetime | None = None,
) -> dict[str, Any]:
    """Build a browser-only projection. No trading permission is created here."""
    generated = generated_at_utc or datetime.now(timezone.utc)
    if generated.tzinfo is None or generated.utcoffset() is None:
        raise ValueError("generated_at_utc must be timezone-aware")
    structure, indicators = _intelligence_payload(runtime_result)
    cycle = _value(runtime_result, "cycle")
    isolation = _value(cycle, "isolation")
    shadow = tuple(data.shadow_setups)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": generated.astimezone(timezone.utc).isoformat(),
        "project": "GoldScalpTraderAI",
        "mode": "DEMO",
        "market": _market_payload(runtime_result, data),
        "session": _session_payload(runtime_result, data),
        "structure": structure,
        "indicators": indicators,
        "charts": _chart_payload(candles_by_tf),
        "decision": {
            "bot_status": data.bot_status,
            "setup": data.detected_setup,
            "active_family": data.active_family,
            "action": data.live_action,
            "reason": data.reason,
            "gate": data.gate_text,
            "system": data.system_text,
        },
        "timing": _timing_payload(runtime_result),
        "plan": _plan_payload(runtime_result),
        "risk": _risk_payload(runtime_result),
        "execution": {"text": data.execution_text, "activity": data.activity_text},
        "management": _management_payload(runtime_result),
        "learning": {"text": data.learning_text},
        "news": {"text": data.news_text},
        "shadows": list(shadow),
        "shadow_count": len(shadow),
        "isolation_active_family": _enum(_value(isolation, "active_family"), data.active_family),
    }
    encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False)
    if contains_probable_secret(encoded):
        raise ValueError("unsafe presentation snapshot")
    return payload


def publish_snapshot(path: Path, payload: dict[str, Any]) -> None:
    """Atomically replace one JSON frame so browser readers never see partial data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    if contains_probable_secret(text):
        raise ValueError("unsafe presentation snapshot")
    try:
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
