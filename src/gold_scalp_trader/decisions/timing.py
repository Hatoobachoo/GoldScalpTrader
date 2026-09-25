"""Subordinate M1 entry refinement after a valid persistent M5 Opportunity.

Timing is deliberately recoverable: a weak micro entry returns WAIT while the
M5 thesis survives.  MISSED/INVALID are reserved for explicit configured
freshness/chase limits or fresh opposing structural evidence.  Timing never
creates monetary/broker permission.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from gold_scalp_trader.domain.enums import (
    Direction,
    OpportunityState,
    StrategyFamily,
    Timeframe,
    TimingOutcome,
)
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot

from .opportunity import Opportunity


@dataclass(frozen=True, slots=True)
class TimingPolicy:
    version: str = "TIMING_BASELINE_UNCALIBRATED_V2"
    max_micro_extension_atr: float = 1.50
    max_m5_event_age_seconds: float | None = None
    max_m1_trigger_age_seconds: float | None = None
    max_chase_atr: float | None = None

    def __post_init__(self) -> None:
        if self.max_micro_extension_atr <= 0:
            raise ValueError("max_micro_extension_atr must be positive")
        for name, value in (
            ("max_m5_event_age_seconds", self.max_m5_event_age_seconds),
            ("max_m1_trigger_age_seconds", self.max_m1_trigger_age_seconds),
            ("max_chase_atr", self.max_chase_atr),
        ):
            if value is not None and value <= 0:
                raise ValueError(f"{name} must be positive when configured")


@dataclass(frozen=True, slots=True)
class TimingDecision:
    outcome: TimingOutcome
    reason: str
    trigger_time: datetime | None
    micro_extension_atr: float | None
    m5_event_age_seconds: float | None = None
    m5_event_age_bars: int | None = None
    trigger_age_seconds: float | None = None
    chase_atr: float | None = None
    profile: str | None = None
    policy_version: str = "TIMING_BASELINE_UNCALIBRATED_V2"


def _event_reference_close(opportunity: Opportunity, snapshot: IntelligenceSnapshot) -> float | None:
    if opportunity.m5_event_time is None:
        return None
    for candle in reversed(snapshot.market.series(Timeframe.M5)):
        if candle.close_time == opportunity.m5_event_time:
            return candle.close
    return None


def _event_age(opportunity: Opportunity, snapshot: IntelligenceSnapshot) -> tuple[float | None, int | None]:
    if opportunity.m5_event_time is None:
        return None, None
    seconds = max(0.0, (snapshot.market.captured_at - opportunity.m5_event_time).total_seconds())
    bars = sum(
        1
        for candle in snapshot.market.series(Timeframe.M5)
        if candle.close_time > opportunity.m5_event_time
    )
    return seconds, bars


def _fresh_opposing_m5_break(opportunity: Opportunity, snapshot: IntelligenceSnapshot) -> bool:
    m5 = snapshot.by_timeframe.get(Timeframe.M5)
    if m5 is None or m5.structure.event_time is None:
        return False
    reference_time = opportunity.m5_event_time or opportunity.created_at
    if m5.structure.event_time <= reference_time:
        return False
    return (
        opportunity.direction is Direction.BUY and m5.structure.break_direction is Direction.SELL
    ) or (
        opportunity.direction is Direction.SELL and m5.structure.break_direction is Direction.BUY
    )


def _directional_progress(direction: Direction, latest, previous) -> bool:
    if direction is Direction.BUY:
        return latest.close > latest.open and latest.close > previous.close
    return latest.close < latest.open and latest.close < previous.close


def _continuation_refinement(opportunity: Opportunity, snapshot: IntelligenceSnapshot, latest, previous) -> bool:
    m1 = snapshot.by_timeframe[Timeframe.M1]
    progress = _directional_progress(opportunity.direction, latest, previous)
    if not progress:
        return False
    flow_ok = m1.quant.ema_flow in {opportunity.direction.value, "UNKNOWN", "NONE"}
    if opportunity.direction is Direction.BUY:
        counter_then_resume = previous.close <= previous.open
    else:
        counter_then_resume = previous.close >= previous.open
    # Keep opportunity recall high: either a micro pullback/resumption or a
    # non-opposing micro flow is enough.  Exact profile thresholds remain
    # calibration variables.
    return flow_ok or counter_then_resume


def _reversal_refinement(opportunity: Opportunity, snapshot: IntelligenceSnapshot, latest, previous) -> bool:
    m1 = snapshot.by_timeframe[Timeframe.M1]
    progress = _directional_progress(opportunity.direction, latest, previous)
    if not progress:
        return False
    prior_opposite = (
        previous.close <= previous.open
        if opportunity.direction is Direction.BUY
        else previous.close >= previous.open
    )
    liquidity_turn = m1.liquidity.event_direction is opportunity.direction
    structure_turn = m1.structure.break_direction is opportunity.direction
    return prior_opposite or liquidity_turn or structure_turn


def _profile_ready(opportunity: Opportunity, snapshot: IntelligenceSnapshot, latest, previous) -> bool:
    reversal_families = {
        StrategyFamily.LIQUIDITY_SWEEP_REVERSAL,
        StrategyFamily.FAILED_BREAKOUT_REVERSAL,
    }
    if opportunity.family in reversal_families:
        return _reversal_refinement(opportunity, snapshot, latest, previous)
    return _continuation_refinement(opportunity, snapshot, latest, previous)


def evaluate(
    opportunity: Opportunity | None,
    snapshot: IntelligenceSnapshot,
    policy: TimingPolicy | None = None,
) -> TimingDecision:
    p = policy or TimingPolicy()
    if opportunity is None or opportunity.state not in {
        OpportunityState.ARMED,
        OpportunityState.WAITING,
        OpportunityState.READY,
    }:
        return TimingDecision(
            TimingOutcome.INVALID,
            "no valid M5 Opportunity",
            None,
            None,
            policy_version=p.version,
        )

    m1 = snapshot.by_timeframe.get(Timeframe.M1)
    candles = snapshot.market.series(Timeframe.M1)
    event_age_seconds, event_age_bars = _event_age(opportunity, snapshot)
    profile = opportunity.preferred_m1_profile or "GENERIC_SUBORDINATE_REFINEMENT"

    if _fresh_opposing_m5_break(opportunity, snapshot):
        return TimingDecision(
            TimingOutcome.INVALID,
            "fresh opposing M5 structural event invalidates the armed thesis",
            None,
            None,
            event_age_seconds,
            event_age_bars,
            profile=profile,
            policy_version=p.version,
        )

    if p.max_m5_event_age_seconds is not None and event_age_seconds is not None:
        if event_age_seconds > p.max_m5_event_age_seconds:
            return TimingDecision(
                TimingOutcome.MISSED,
                "M5 setup event exceeded configured freshness budget",
                None,
                None,
                event_age_seconds,
                event_age_bars,
                profile=profile,
                policy_version=p.version,
            )

    if m1 is None or len(candles) < 2:
        return TimingDecision(
            TimingOutcome.WAIT,
            "M1 refinement unavailable; M5 Opportunity remains recoverable",
            None,
            None,
            event_age_seconds,
            event_age_bars,
            profile=profile,
            policy_version=p.version,
        )

    latest, previous = candles[-1], candles[-2]
    extension = m1.quant.extension_atr
    trigger_age = max(0.0, (snapshot.market.captured_at - latest.close_time).total_seconds())
    event_reference = _event_reference_close(opportunity, snapshot)
    atr = m1.quant.atr14
    executable_mid = (snapshot.market.quote.bid + snapshot.market.quote.ask) / 2.0
    chase = None
    if event_reference is not None and atr is not None and atr > 0:
        directional_move = (
            executable_mid - event_reference
            if opportunity.direction is Direction.BUY
            else event_reference - executable_mid
        )
        chase = max(0.0, directional_move / atr)

    if extension is not None and extension > p.max_micro_extension_atr:
        return TimingDecision(
            TimingOutcome.MISSED,
            "M1 severely extended/chased",
            latest.close_time,
            extension,
            event_age_seconds,
            event_age_bars,
            trigger_age,
            chase,
            profile,
            p.version,
        )
    if p.max_m1_trigger_age_seconds is not None and trigger_age > p.max_m1_trigger_age_seconds:
        return TimingDecision(
            TimingOutcome.WAIT,
            "latest M1 trigger is stale; waiting for a fresh refinement",
            latest.close_time,
            extension,
            event_age_seconds,
            event_age_bars,
            trigger_age,
            chase,
            profile,
            p.version,
        )
    if p.max_chase_atr is not None and chase is not None and chase > p.max_chase_atr:
        return TimingDecision(
            TimingOutcome.MISSED,
            "M5 opportunity escaped configured chase budget",
            latest.close_time,
            extension,
            event_age_seconds,
            event_age_bars,
            trigger_age,
            chase,
            profile,
            p.version,
        )

    ready = _profile_ready(opportunity, snapshot, latest, previous)
    if opportunity.direction is Direction.BUY:
        outcome = TimingOutcome.READY_BUY if ready else TimingOutcome.WAIT
    else:
        outcome = TimingOutcome.READY_SELL if ready else TimingOutcome.WAIT
    reason = (
        f"{profile}: fresh M1 refinement supports the surviving M5 thesis"
        if ready
        else f"{profile}: waiting for efficient M1 refinement"
    )
    return TimingDecision(
        outcome,
        reason,
        latest.close_time,
        extension,
        event_age_seconds,
        event_age_bars,
        trigger_age,
        chase,
        profile,
        p.version,
    )
