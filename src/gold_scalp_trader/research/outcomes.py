"""Typed actual/shadow research outcomes and conservative counterfactual evaluation.

Counterfactual evaluation is research-only. It requires explicit hypothetical
entry/stop/target geometry and a chronological completed-candle path. It never
pretends shadow P/L is broker P/L and refuses to guess intrabar ordering when a
single candle touches both stop and target.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from math import isfinite
from typing import Iterable

from gold_scalp_trader.domain.enums import Direction, StrategyMode
from gold_scalp_trader.domain.market import Candle
from gold_scalp_trader.persistence.store import StateStore

SHADOW_OUTCOME_NS = "shadow_counterfactual_outcomes"


@dataclass(frozen=True, slots=True)
class ResearchOutcome:
    episode_id: str
    family: str
    mode: StrategyMode
    qualified: bool
    executed: bool
    net_r: float | None = None
    mfe_r: float | None = None
    mae_r: float | None = None
    entry_efficiency: float | None = None
    capture_efficiency: float | None = None
    exit_efficiency: float | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        if not self.episode_id.strip() or not self.family.strip():
            raise ValueError("episode_id and family are required")
        if self.executed and self.mode is not StrategyMode.ACTIVE_EXECUTION:
            raise ValueError("shadow/research outcome cannot be marked as broker executed")
        if self.executed and not self.qualified:
            raise ValueError("broker-executed research outcome must have qualified")
        for name in ("net_r", "mfe_r", "mae_r"):
            value = getattr(self, name)
            if value is not None and not isfinite(float(value)):
                raise ValueError(f"{name} must be finite when present")
        for name in ("entry_efficiency", "capture_efficiency", "exit_efficiency"):
            value = getattr(self, name)
            if value is not None and (not isfinite(float(value)) or not 0.0 <= float(value) <= 1.0):
                raise ValueError(f"{name} must be within 0..1 when present")


class CounterfactualStatus(str, Enum):
    TARGET = "TARGET"
    STOP = "STOP"
    UNRESOLVED = "UNRESOLVED"
    AMBIGUOUS_INTRABAR_ORDER = "AMBIGUOUS_INTRABAR_ORDER"


@dataclass(frozen=True, slots=True)
class CounterfactualPlan:
    episode_id: str
    family: str
    direction: Direction
    entry: float
    initial_sl: float
    primary_target: float
    entry_time_iso: str
    cost_r: float = 0.0
    assumption: str = "HYPOTHETICAL_ENTRY_AT_RECORDED_REFERENCE"

    def __post_init__(self) -> None:
        if not self.episode_id.strip() or not self.family.strip() or not self.entry_time_iso.strip():
            raise ValueError("counterfactual identity and entry time are required")
        try:
            entry_time = datetime.fromisoformat(self.entry_time_iso.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("counterfactual entry time must be ISO-8601") from exc
        if entry_time.tzinfo is None or entry_time.utcoffset() is None:
            raise ValueError("counterfactual entry time must be timezone-aware")
        if self.direction not in {Direction.BUY, Direction.SELL}:
            raise ValueError("counterfactual direction must be BUY or SELL")
        for name in ("entry", "initial_sl", "primary_target", "cost_r"):
            value = float(getattr(self, name))
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.entry <= 0 or self.initial_sl <= 0 or self.primary_target <= 0:
            raise ValueError("counterfactual prices must be positive")
        if self.cost_r < 0:
            raise ValueError("counterfactual cost_r cannot be negative")
        if self.direction is Direction.BUY and not (self.initial_sl < self.entry < self.primary_target):
            raise ValueError("BUY counterfactual geometry must be SL < entry < target")
        if self.direction is Direction.SELL and not (self.primary_target < self.entry < self.initial_sl):
            raise ValueError("SELL counterfactual geometry must be target < entry < SL")

    @property
    def original_r_price(self) -> float:
        return abs(self.entry - self.initial_sl)

    @property
    def entry_time(self) -> datetime:
        return datetime.fromisoformat(self.entry_time_iso.replace("Z", "+00:00"))


@dataclass(frozen=True, slots=True)
class CounterfactualEvaluation:
    status: CounterfactualStatus
    outcome: ResearchOutcome
    bars_observed: int
    exit_time_iso: str | None = None
    gross_r: float | None = None
    cost_r: float | None = None
    evidence_quality: str = "BAR_PATH_ONLY"


def _path_r(plan: CounterfactualPlan, price: float) -> float:
    move = price - plan.entry if plan.direction is Direction.BUY else plan.entry - price
    return move / plan.original_r_price


def evaluate_counterfactual_path(plan: CounterfactualPlan, candles: Iterable[Candle]) -> CounterfactualEvaluation:
    """Evaluate an explicit shadow plan without pre-entry leakage or intrabar guessing."""
    rows = tuple(candles)
    previous = None
    for candle in rows:
        if candle.open_time < plan.entry_time:
            raise ValueError("counterfactual path contains a pre-entry candle")
        if previous is not None and candle.open_time <= previous:
            raise ValueError("counterfactual candles must be strictly chronological")
        previous = candle.open_time

    favorable: list[float] = []
    adverse: list[float] = []
    for index, candle in enumerate(rows, start=1):
        if plan.direction is Direction.BUY:
            stop_hit = candle.low <= plan.initial_sl
            target_hit = candle.high >= plan.primary_target
            favorable.append(_path_r(plan, candle.high))
            adverse.append(_path_r(plan, candle.low))
        else:
            stop_hit = candle.high >= plan.initial_sl
            target_hit = candle.low <= plan.primary_target
            favorable.append(_path_r(plan, candle.low))
            adverse.append(_path_r(plan, candle.high))

        mfe = max(favorable) if favorable else None
        mae = min(adverse) if adverse else None
        exit_time = candle.close_time.isoformat()
        if stop_hit and target_hit:
            outcome = ResearchOutcome(
                plan.episode_id, plan.family, StrategyMode.SHADOW_ONLY, True, False,
                net_r=None, mfe_r=mfe, mae_r=mae,
                reason="COUNTERFACTUAL_INTRABAR_ORDER_UNKNOWN",
            )
            return CounterfactualEvaluation(
                CounterfactualStatus.AMBIGUOUS_INTRABAR_ORDER, outcome, index,
                exit_time, None, plan.cost_r, "AMBIGUOUS_OHLC_ORDER",
            )
        if stop_hit or target_hit:
            gross = _path_r(plan, plan.primary_target) if target_hit else -1.0
            net = gross - plan.cost_r
            outcome = ResearchOutcome(
                plan.episode_id, plan.family, StrategyMode.SHADOW_ONLY, True, False,
                net_r=net, mfe_r=mfe, mae_r=mae,
                reason="COUNTERFACTUAL_PRIMARY_TARGET" if target_hit else "COUNTERFACTUAL_INITIAL_STOP",
            )
            return CounterfactualEvaluation(
                CounterfactualStatus.TARGET if target_hit else CounterfactualStatus.STOP,
                outcome, index, exit_time, gross, plan.cost_r,
            )

    outcome = ResearchOutcome(
        plan.episode_id, plan.family, StrategyMode.SHADOW_ONLY, True, False,
        net_r=None,
        mfe_r=max(favorable) if favorable else None,
        mae_r=min(adverse) if adverse else None,
        reason="COUNTERFACTUAL_PATH_UNRESOLVED",
    )
    return CounterfactualEvaluation(
        CounterfactualStatus.UNRESOLVED, outcome, len(rows), None, None, plan.cost_r,
    )


def save_counterfactual(store: StateStore, plan: CounterfactualPlan, evaluation: CounterfactualEvaluation) -> str:
    """Persist a content-addressed shadow outcome with zero broker authority."""
    if evaluation.outcome.episode_id != plan.episode_id or evaluation.outcome.family != plan.family:
        raise ValueError("counterfactual evaluation identity does not match plan")
    payload = {
        "schema_version": 1,
        "plan": asdict(plan),
        "status": evaluation.status.value,
        "outcome": {**asdict(evaluation.outcome), "mode": evaluation.outcome.mode.value},
        "bars_observed": evaluation.bars_observed,
        "exit_time_iso": evaluation.exit_time_iso,
        "gross_r": evaluation.gross_r,
        "cost_r": evaluation.cost_r,
        "evidence_quality": evaluation.evidence_quality,
        "broker_executed": False,
        "broker_authority": "NONE",
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    event_key = f"CFO-{sha256(raw.encode('utf-8')).hexdigest()}"
    store.append_event(SHADOW_OUTCOME_NS, event_key, payload)
    return event_key
