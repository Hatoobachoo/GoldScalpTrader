"""Read-only atomic browser snapshot for the GoldScalpTrader visual floor."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from gold_scalp_trader.domain.enums import StrategyFamily, StrategyMode
from gold_scalp_trader.operator.presentation import DashboardData
from gold_scalp_trader.security.financial_secrets import contains_probable_secret

SCHEMA_VERSION = 2
DEFAULT_FILENAME = "dashboard_snapshot.json"

def _value(obj, name, default=None):
    return default if obj is None else getattr(obj, name, default)

def _enum(value, default="UNKNOWN"):
    return default if value is None else str(getattr(value, "value", value))

def _iso(value):
    return value.isoformat() if hasattr(value, "isoformat") else None

def _candle_row(candle):
    return {
        "time_utc": _iso(getattr(candle, "open_time", None)),
        "close_time_utc": _iso(getattr(candle, "close_time", None)),
        "open": float(getattr(candle, "open")),
        "high": float(getattr(candle, "high")),
        "low": float(getattr(candle, "low")),
        "close": float(getattr(candle, "close")),
        "tick_volume": int(getattr(candle, "tick_volume", 0)),
    }

def _chart_payload(candles_by_tf):
    out = {}
    for tf in ("M1","M5","M15","H1","H4"):
        out[tf] = [_candle_row(x) for x in candles_by_tf.get(tf, ())[-120:]]
    return out

def _intelligence_payload(runtime_result):
    cycle = _value(runtime_result, "cycle")
    intelligence = _value(cycle, "intelligence")
    by_tf = _value(intelligence, "by_timeframe", {}) or {}
    structure, indicators = {}, {}
    for timeframe, frame in by_tf.items():
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

def _plan_payload(runtime_result):
    plan = _value(_value(runtime_result, "cycle"), "trade_plan")
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

def _timing_payload(runtime_result):
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

def _risk_payload(runtime_result):
    risk = _value(_value(runtime_result, "cycle"), "risk")
    return {
        "decision": _enum(_value(risk, "decision"), "NOT_EVALUATED"),
        "profile": _enum(_value(risk, "profile"), "—"),
        "target_risk_pct": _value(risk, "target_risk_pct"),
        "risk_pct": _value(risk, "actual_risk_pct"),
        "risk_money": _value(risk, "actual_risk_money"),
        "volume": _value(risk, "volume"),
        "reason": _value(risk, "reason"),
    }

def _session_payload(runtime_result, data):
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

def _market_payload(runtime_result, data):
    cycle = _value(runtime_result, "cycle")
    market = _value(_value(cycle, "intelligence"), "market")
    account = _value(market, "account")
    quote = _value(market, "quote")
    return {
        "symbol": data.symbol,
        "state": data.market_state,
        "bid": data.bid,
        "ask": data.ask,
        "spread": data.spread,
        "quote_time_utc": _iso(_value(quote, "source_time")),
        "captured_at_utc": _iso(_value(market, "captured_at")),
        "balance": _value(account, "balance"),
        "equity": _value(account, "equity"),
        "free_margin": _value(account, "margin_free"),
        "login": _value(account, "login"),
        "server": _value(account, "server"),
    }

def _decision_payload(runtime_result, data):
    board = _value(_value(runtime_result, "cycle"), "board")
    buy = _value(board, "buy")
    sell = _value(board, "sell")
    return {
        "bot_status": data.bot_status,
        "setup": data.detected_setup,
        "active_family": data.active_family,
        "action": data.live_action,
        "reason": data.reason,
        "gate": data.gate_text,
        "system": data.system_text,
        "buy_score": _value(buy, "score"),
        "sell_score": _value(sell, "score"),
        "leading_score": _value(board, "leading_score"),
        "coverage": _value(board, "coverage"),
        "recommendation": _value(board, "recommendation"),
        "red_team": list(_value(board, "red_team_objections", ()) or ()),
    }

def _management_payload(runtime_result):
    trade = _value(runtime_result, "managed_trade")
    if trade is None:
        return None
    return {
        "trade_id": _value(trade, "trade_id"),
        "ticket": _value(trade, "ticket"),
        "family": _enum(_value(trade, "family")),
        "direction": _enum(_value(trade, "direction")),
        "entry": _value(trade, "entry"),
        "original_stop": _value(trade, "original_sl"),
        "stop": _value(trade, "current_sl"),
        "primary": _value(trade, "primary_target"),
        "expansion": _value(trade, "expansion_target"),
        "volume": _value(trade, "volume"),
        "opened_at": _iso(_value(trade, "opened_at")),
        "manager_action": _enum(_value(runtime_result, "management_action"), "HOLD"),
    }

def _strategy_board(runtime_result, data):
    isolation = _value(_value(runtime_result, "cycle"), "isolation")
    active = _enum(_value(isolation, "active_family"), data.active_family)
    candidates = _value(isolation, "candidates", ()) or ()
    mapped = {}
    for isolated in candidates:
        candidate = _value(isolated, "candidate")
        if candidate is None:
            continue
        family = _enum(_value(candidate, "family"))
        mapped[family] = {
            "family": family,
            "mode": _enum(_value(isolated, "mode"), "SHADOW_ONLY"),
            "qualification": _enum(_value(candidate, "qualification"), "UNKNOWN"),
            "direction": _enum(_value(candidate, "direction"), "NONE"),
            "score": _value(candidate, "score"),
            "coverage": _value(candidate, "coverage"),
            "qualified": bool(_value(candidate, "qualified", False)),
        }
    rows = []
    for family in StrategyFamily:
        if family.value in mapped:
            rows.append(mapped[family.value])
        else:
            rows.append({
                "family": family.value,
                "mode": StrategyMode.ACTIVE_EXECUTION.value if family.value == active else StrategyMode.SHADOW_ONLY.value,
                "qualification": "NOT_PRESENT",
                "direction": "NONE",
                "score": None,
                "coverage": None,
                "qualified": False,
            })
    return rows

def build_snapshot(data: DashboardData, candles_by_tf: Mapping[str, tuple], *, runtime_result=None, generated_at_utc=None):
    generated = generated_at_utc or datetime.now(timezone.utc)
    if generated.tzinfo is None or generated.utcoffset() is None:
        raise ValueError("generated_at_utc must be timezone-aware")
    structure, indicators = _intelligence_payload(runtime_result)
    isolation = _value(_value(runtime_result, "cycle"), "isolation")
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
        "decision": _decision_payload(runtime_result, data),
        "timing": _timing_payload(runtime_result),
        "plan": _plan_payload(runtime_result),
        "risk": _risk_payload(runtime_result),
        "execution": {"text": data.execution_text, "activity": data.activity_text},
        "management": _management_payload(runtime_result),
        "learning": {"text": data.learning_text},
        "news": {"text": data.news_text},
        "shadows": list(data.shadow_setups),
        "shadow_count": len(data.shadow_setups),
        "strategy_board": _strategy_board(runtime_result, data),
        "isolation_active_family": _enum(_value(isolation, "active_family"), data.active_family),
    }
    encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False)
    if contains_probable_secret(encoded):
        raise ValueError("unsafe presentation snapshot")
    return payload

def publish_snapshot(path: Path, payload: dict[str, Any]) -> None:
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
