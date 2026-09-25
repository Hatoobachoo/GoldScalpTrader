"""Structural TradePlan geometry with no monetary-sizing authority.

The plan is built only from causal market structure that already exists in the
immutable snapshot.  Missing invalidation or target geometry means no executable
plan; ATR is used only as an outward noise buffer, never as a synthetic stop or
target fallback.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor

from gold_scalp_trader.domain.enums import Direction, StrategyFamily, Timeframe, TimingOutcome
from gold_scalp_trader.domain.ids import new_id
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot

from .family_trade_plan import select_invalidation
from .opportunity import Opportunity
from .timing import TimingDecision


@dataclass(frozen=True, slots=True)
class TradePlanPolicy:
    version: str = "TRADE_PLAN_BASELINE_UNCALIBRATED_V2"
    stop_buffer_atr: float = 0.10
    minimum_gross_r: float | None = None

    def __post_init__(self) -> None:
        if self.stop_buffer_atr < 0:
            raise ValueError("stop_buffer_atr cannot be negative")
        if self.minimum_gross_r is not None and self.minimum_gross_r <= 0:
            raise ValueError("minimum_gross_r must be positive when configured")


@dataclass(frozen=True, slots=True)
class TradePlan:
    trade_plan_id: str
    opportunity_id: str
    direction: Direction
    entry_reference: float
    initial_sl: float
    primary_target: float
    expansion_target: float | None
    invalidation_source: str
    gross_r: float
    state: str
    reasons: tuple[str, ...]
    immediate_obstacle: float | None = None
    runner_objective: float | None = None
    family: StrategyFamily | None = None
    policy_version: str | None = None
    stop_buffer: float | None = None
    target_source_ids: tuple[str, ...] = ()


def _normalize_outward(price: float, tick_size: float, direction: Direction) -> float:
    if tick_size <= 0:
        raise ValueError("tick_size must be positive")
    steps = price / tick_size
    normalized = floor(steps) * tick_size if direction is Direction.BUY else ceil(steps) * tick_size
    return round(normalized, 12)


def _objective_candidates(
    opportunity: Opportunity,
    snapshot: IntelligenceSnapshot,
    entry: float,
) -> list[tuple[float, str]]:
    candidates: list[tuple[float, str]] = []
    for timeframe in (Timeframe.M5, Timeframe.M15, Timeframe.H1, Timeframe.H4):
        report = snapshot.by_timeframe.get(timeframe)
        if report is None:
            continue
        if opportunity.direction is Direction.BUY:
            zone = report.technical.resistance
            pool = report.liquidity.buy_side
            if zone is not None and zone.lower > entry:
                candidates.append((zone.lower, f"{timeframe.value}:RESISTANCE:{zone.source}"))
            if pool is not None and pool.lower > entry:
                candidates.append((pool.lower, f"{timeframe.value}:BUY_SIDE_LIQUIDITY:{pool.pool_id}"))
            swing = report.structure.last_swing_high
            if swing is not None and swing.price > entry and swing.confirmed_at <= snapshot.market.captured_at:
                candidates.append((swing.price, f"{timeframe.value}:SWING_HIGH:{swing.pivot_time.isoformat()}"))
        else:
            zone = report.technical.support
            pool = report.liquidity.sell_side
            if zone is not None and zone.upper < entry:
                candidates.append((zone.upper, f"{timeframe.value}:SUPPORT:{zone.source}"))
            if pool is not None and pool.upper < entry:
                candidates.append((pool.upper, f"{timeframe.value}:SELL_SIDE_LIQUIDITY:{pool.pool_id}"))
            swing = report.structure.last_swing_low
            if swing is not None and swing.price < entry and swing.confirmed_at <= snapshot.market.captured_at:
                candidates.append((swing.price, f"{timeframe.value}:SWING_LOW:{swing.pivot_time.isoformat()}"))

    # One causal level can appear through zone/swing/liquidity labels.  De-dupe
    # by price for geometry while retaining a deterministic first provenance.
    by_price: dict[float, str] = {}
    for price, source in candidates:
        by_price.setdefault(round(price, 12), source)
    ordered = [(price, by_price[price]) for price in by_price]
    ordered.sort(key=lambda item: abs(item[0] - entry))
    return ordered


def build(
    opportunity: Opportunity,
    timing: TimingDecision,
    snapshot: IntelligenceSnapshot,
    policy: TradePlanPolicy | None = None,
) -> TradePlan | None:
    p = policy or TradePlanPolicy()
    if timing.outcome not in {TimingOutcome.READY_BUY, TimingOutcome.READY_SELL}:
        return None

    m5 = snapshot.by_timeframe.get(Timeframe.M5)
    if m5 is None or m5.quant.atr14 is None or m5.quant.atr14 <= 0:
        return None
    if snapshot.market.symbol_spec.tick_size <= 0:
        return None

    entry = snapshot.market.quote.ask if opportunity.direction is Direction.BUY else snapshot.market.quote.bid
    invalidation = select_invalidation(opportunity, snapshot, entry)
    if invalidation is None:
        return None

    buffer = max(m5.quant.atr14 * p.stop_buffer_atr, snapshot.market.symbol_spec.tick_size)
    raw_sl = invalidation.price - buffer if opportunity.direction is Direction.BUY else invalidation.price + buffer
    sl = _normalize_outward(raw_sl, snapshot.market.symbol_spec.tick_size, opportunity.direction)
    if opportunity.direction is Direction.BUY and sl >= entry:
        return None
    if opportunity.direction is Direction.SELL and sl <= entry:
        return None

    objectives = _objective_candidates(opportunity, snapshot, entry)
    if not objectives:
        return None
    primary, primary_source = objectives[0]
    expansion = objectives[1][0] if len(objectives) > 1 else None
    runner = objectives[2][0] if len(objectives) > 2 else None

    risk_distance = abs(entry - sl)
    reward_distance = abs(primary - entry)
    if risk_distance <= 0 or reward_distance <= 0:
        return None
    gross_r = reward_distance / risk_distance
    state = "READY"
    reasons = [
        f"family-correct invalidation: {invalidation.source}",
        f"primary structural objective: {primary_source}",
        "ATR used only as outward structural noise buffer",
    ]
    if p.minimum_gross_r is not None and gross_r < p.minimum_gross_r:
        state = "DEGRADED"
        reasons.append(
            f"gross R {gross_r:.3f} below configured calibration floor {p.minimum_gross_r:.3f}"
        )

    return TradePlan(
        trade_plan_id=str(new_id("PLAN")),
        opportunity_id=opportunity.opportunity_id,
        direction=opportunity.direction,
        entry_reference=entry,
        initial_sl=sl,
        primary_target=primary,
        expansion_target=expansion,
        invalidation_source=invalidation.source,
        gross_r=gross_r,
        state=state,
        reasons=tuple(reasons),
        immediate_obstacle=primary,
        runner_objective=runner,
        family=opportunity.family,
        policy_version=p.version,
        stop_buffer=buffer,
        target_source_ids=tuple(source for _, source in objectives[:3]),
    )
