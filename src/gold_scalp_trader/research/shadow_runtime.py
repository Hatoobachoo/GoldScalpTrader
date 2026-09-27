"""Automatic causal lifecycle for qualified SHADOW_ONLY strategy episodes.

This module is research-only. It freezes contemporaneous hypothetical geometry
for each qualified shadow family, then resolves that plan only from future
completed M1 candles. It never imports Risk, Gate, Intent or the MT5 writer and
never presents counterfactual P/L as broker-executed P/L.
"""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from math import isfinite

from gold_scalp_trader.decisions.opportunity import Opportunity
from gold_scalp_trader.decisions.timing import evaluate as timing_evaluate
from gold_scalp_trader.decisions.trade_plan import build as build_trade_plan
from gold_scalp_trader.domain.enums import OpportunityState, StrategyMode, Timeframe, TimingOutcome
from gold_scalp_trader.persistence.store import StateIntegrityError, StateStore

from .outcomes import (
    CounterfactualPlan,
    CounterfactualStatus,
    evaluate_counterfactual_path,
    save_counterfactual,
)

PLAN_NS = "shadow_counterfactual_plans"
TERMINAL_NS = "shadow_counterfactual_terminal"
SCHEMA_VERSION = 1


def _episode_key(candidate) -> str:
    identity = {
        "family": candidate.family.value,
        "direction": candidate.direction.value,
        "source_event_ids": list(candidate.source_event_ids),
        "policy_version": candidate.policy_version,
        "m5_event_time": None if candidate.m5_event_time is None else candidate.m5_event_time.isoformat(),
    }
    raw = json.dumps(identity, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return f"SHADOW-{sha256(raw.encode('utf-8')).hexdigest()[:32]}"


def _plan_payload(plan: CounterfactualPlan) -> dict:
    payload = asdict(plan)
    payload["direction"] = plan.direction.value
    return {
        "schema_version": SCHEMA_VERSION,
        "plan": payload,
        "runtime_authority": "NONE",
        "broker_authority": "NONE",
    }


def _load_plan(store: StateStore, episode_id: str) -> CounterfactualPlan | None:
    row = store.get(PLAN_NS, episode_id)
    if row is None:
        return None
    payload = row.payload
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise StateIntegrityError("unsupported shadow-plan schema")
    if payload.get("runtime_authority") != "NONE" or payload.get("broker_authority") != "NONE":
        raise StateIntegrityError("shadow plan gained forbidden authority")
    raw = payload.get("plan")
    if not isinstance(raw, dict):
        raise StateIntegrityError("shadow plan payload missing")
    from gold_scalp_trader.domain.enums import Direction

    try:
        return CounterfactualPlan(
            episode_id=str(raw["episode_id"]),
            family=str(raw["family"]),
            direction=Direction(str(raw["direction"])),
            entry=float(raw["entry"]),
            initial_sl=float(raw["initial_sl"]),
            primary_target=float(raw["primary_target"]),
            entry_time_iso=str(raw["entry_time_iso"]),
            cost_r=float(raw.get("cost_r", 0.0)),
            assumption=str(raw.get("assumption", "HYPOTHETICAL_ENTRY_AT_RECORDED_REFERENCE")),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise StateIntegrityError("shadow plan is corrupt/incomplete") from exc


def _freeze_new_shadow_plans(store: StateStore, result) -> int:
    cycle = result.cycle
    snapshot = cycle.intelligence
    market = snapshot.market
    created = 0
    for isolated in cycle.isolation.candidates:
        candidate = isolated.candidate
        if isolated.mode is not StrategyMode.SHADOW_ONLY or not candidate.qualified:
            continue
        episode_id = _episode_key(candidate)
        if store.get(PLAN_NS, episode_id) is not None or store.get(TERMINAL_NS, episode_id) is not None:
            continue

        opportunity = Opportunity(
            opportunity_id=f"OPP-{episode_id}",
            episode_id=episode_id,
            family=candidate.family,
            direction=candidate.direction,
            created_at=market.captured_at,
            updated_at=market.captured_at,
            state=OpportunityState.ARMED,
            source_event_ids=candidate.source_event_ids,
            score=candidate.score,
            reasons=candidate.reasons,
            policy_version=candidate.policy_version,
            m5_event_time=candidate.m5_event_time,
            preferred_m1_profile=candidate.preferred_m1_profile,
            coverage=candidate.coverage,
        )
        timing = timing_evaluate(opportunity, snapshot)
        if timing.outcome not in {TimingOutcome.READY_BUY, TimingOutcome.READY_SELL}:
            continue
        trade_plan = build_trade_plan(opportunity, timing, snapshot)
        if trade_plan is None:
            continue

        original_r = abs(trade_plan.entry_reference - trade_plan.initial_sl)
        if original_r <= 0 or not isfinite(original_r):
            continue
        cost_r = market.quote.spread / original_r
        plan = CounterfactualPlan(
            episode_id=episode_id,
            family=candidate.family.value,
            direction=candidate.direction,
            entry=trade_plan.entry_reference,
            initial_sl=trade_plan.initial_sl,
            primary_target=trade_plan.primary_target,
            entry_time_iso=market.captured_at.isoformat(),
            cost_r=cost_r,
            assumption=(
                "RESEARCH_ONLY_CONTEMPORANEOUS_ENTRY;COST=QUOTED_SPREAD_R;"
                "NO_SLIPPAGE_OR_COMMISSION_ASSUMED"
            ),
        )
        store.put(PLAN_NS, episode_id, _plan_payload(plan), allow_replace=False)
        created += 1
    return created


def _resolve_open_shadow_plans(store: StateStore, result) -> int:
    market = result.cycle.intelligence.market
    m1 = market.series(Timeframe.M1)
    resolved = 0
    for row in store.list_records(PLAN_NS):
        plan = _load_plan(store, row.key)
        if plan is None:
            continue
        future = tuple(candle for candle in m1 if candle.open_time >= plan.entry_time)
        evaluation = evaluate_counterfactual_path(plan, future)
        if evaluation.status is CounterfactualStatus.UNRESOLVED:
            continue
        with store.transaction():
            event_key = save_counterfactual(store, plan, evaluation)
            store.put(
                TERMINAL_NS,
                plan.episode_id,
                {
                    "schema_version": SCHEMA_VERSION,
                    "episode_id": plan.episode_id,
                    "family": plan.family,
                    "status": evaluation.status.value,
                    "outcome_event_id": event_key,
                    "runtime_authority": "NONE",
                    "broker_authority": "NONE",
                },
                allow_replace=False,
            )
            store.delete(PLAN_NS, plan.episode_id)
        resolved += 1
    return resolved


def record_shadow_runtime(store: StateStore, result) -> tuple[int, int]:
    """Advance the entire research-only shadow lifecycle for one runtime sample.

    Existing plans resolve before new plans freeze so a just-created plan cannot
    consume a candle that was already complete before its entry timestamp.
    Returns ``(created, resolved)`` for diagnostics only.
    """
    resolved = _resolve_open_shadow_plans(store, result)
    created = _freeze_new_shadow_plans(store, result)
    return created, resolved


__all__ = ["PLAN_NS", "TERMINAL_NS", "record_shadow_runtime"]
