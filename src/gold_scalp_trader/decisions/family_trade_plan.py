"""Family-aware structural invalidation selection.

This module chooses only causal thesis-failure geometry already present in the
immutable snapshot.  It never invents an ATR-distance stop merely to make Risk
or R look better.
"""
from __future__ import annotations

from dataclasses import dataclass

from gold_scalp_trader.domain.enums import Direction, StrategyFamily, Timeframe
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot

from .opportunity import Opportunity


@dataclass(frozen=True, slots=True)
class Invalidation:
    price: float
    source: str


def preferred_invalidation_source(family: StrategyFamily) -> tuple[str, ...]:
    if family is StrategyFamily.BREAKOUT_RETEST_CONTINUATION:
        return ("M5_RETEST_FAILURE", "M15_STRUCTURE", "H1_STRUCTURE")
    if family is StrategyFamily.LIQUIDITY_SWEEP_REVERSAL:
        return ("M5_SWEEP_EXTREME", "M5_STRUCTURE", "M15_STRUCTURE", "H1_STRUCTURE")
    if family is StrategyFamily.FAILED_BREAKOUT_REVERSAL:
        return ("M5_FAILED_BREAK_EXTREME", "M5_STRUCTURE", "M15_STRUCTURE", "H1_STRUCTURE")
    return ("M5_STRUCTURE", "M15_STRUCTURE", "H1_STRUCTURE")


def _correct_side(direction: Direction, price: float, entry: float) -> bool:
    return price < entry if direction is Direction.BUY else price > entry


def _family_event_invalidation(
    opportunity: Opportunity,
    snapshot: IntelligenceSnapshot,
    entry: float,
) -> Invalidation | None:
    candles = snapshot.market.series(Timeframe.M5)
    m5 = snapshot.by_timeframe.get(Timeframe.M5)
    if m5 is None or not candles:
        return None

    if opportunity.family is StrategyFamily.BREAKOUT_RETEST_CONTINUATION:
        # Setup detection defines the latest completed M5 bar as the retest
        # response.  Its opposite extreme is the first thesis-failure boundary.
        retest = candles[-1]
        price = retest.low if opportunity.direction is Direction.BUY else retest.high
        if _correct_side(opportunity.direction, price, entry):
            return Invalidation(price, "M5_RETEST_FAILURE")

    if opportunity.family is StrategyFamily.LIQUIDITY_SWEEP_REVERSAL:
        event = m5.liquidity
        if event.event_direction is opportunity.direction and event.event_time == candles[-1].close_time:
            price = candles[-1].low if opportunity.direction is Direction.BUY else candles[-1].high
            if _correct_side(opportunity.direction, price, entry):
                return Invalidation(price, "M5_SWEEP_EXTREME")

    if opportunity.family is StrategyFamily.FAILED_BREAKOUT_REVERSAL and len(candles) >= 2:
        # The prior completed candle is the accepted-break attempt and therefore
        # the event extreme that disproves the failed-break reversal if retaken.
        attempt = candles[-2]
        price = attempt.low if opportunity.direction is Direction.BUY else attempt.high
        if _correct_side(opportunity.direction, price, entry):
            return Invalidation(price, "M5_FAILED_BREAK_EXTREME")
    return None


def _structural_invalidation(
    opportunity: Opportunity,
    snapshot: IntelligenceSnapshot,
    entry: float,
) -> Invalidation | None:
    for timeframe in (Timeframe.M5, Timeframe.M15, Timeframe.H1):
        report = snapshot.by_timeframe.get(timeframe)
        if report is None:
            continue
        swing = (
            report.structure.last_swing_low
            if opportunity.direction is Direction.BUY
            else report.structure.last_swing_high
        )
        if swing is None or swing.confirmed_at > snapshot.market.captured_at:
            continue
        if _correct_side(opportunity.direction, swing.price, entry):
            return Invalidation(swing.price, f"{timeframe.value}_STRUCTURE")
    return None


def select_invalidation(
    opportunity: Opportunity,
    snapshot: IntelligenceSnapshot,
    entry: float,
) -> Invalidation | None:
    """Return nearest family-correct causal invalidation or no plan geometry."""

    family_event = _family_event_invalidation(opportunity, snapshot, entry)
    if family_event is not None:
        return family_event
    return _structural_invalidation(opportunity, snapshot, entry)
