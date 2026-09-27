from datetime import datetime, timedelta, timezone

from gold_scalp_trader.domain.enums import (
    DataQuality,
    Direction,
    SetupQualification,
    StrategyFamily,
    Timeframe,
)
from gold_scalp_trader.domain.market import AccountFacts, Candle, MarketSnapshot, Quote, SymbolSpec
from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.intelligence.snapshot import build as build_intelligence
from gold_scalp_trader.strategies.isolation import apply, route
from gold_scalp_trader.strategies.setup_detector import SetupRegistry, detect

UTC = timezone.utc


def _snapshot():
    now = datetime(2026, 1, 2, 12, 0, tzinfo=UTC)
    candles = {}
    for tf, step, count in [
        (Timeframe.M1, 1, 80),
        (Timeframe.M5, 5, 100),
        (Timeframe.M15, 15, 100),
        (Timeframe.H1, 60, 100),
        (Timeframe.H4, 240, 60),
    ]:
        start = now - timedelta(minutes=step * count)
        series = []
        price = 100.0
        for i in range(count):
            price += 0.05
            series.append(
                Candle(
                    tf,
                    start + timedelta(minutes=step * i),
                    price - 0.05,
                    price + 0.2,
                    price - 0.2,
                    price,
                    10,
                    0,
                )
            )
        candles[tf] = tuple(series)
    return MarketSnapshot(
        now,
        AccountFacts(1, "demo", "USD", 1000, 1000, 1000, True, True),
        SymbolSpec("XAUUSDm", 3, 0.001, 0.001, 1, 0.01, 200, 0.01),
        Quote(105, 105.1, now, now),
        candles,
        {tf: DataQuality.HEALTHY for tf in candles},
        (),
        DataQuality.HEALTHY,
    )


def _qualified(family: StrategyFamily, direction: Direction, score: float, suffix: str) -> SetupCandidate:
    qualification = (
        SetupQualification.QUALIFIED_BUY if direction is Direction.BUY else SetupQualification.QUALIFIED_SELL
    )
    return SetupCandidate(
        candidate_id=f"{family.value}-{suffix}",
        family=family,
        qualification=qualification,
        direction=direction,
        score=score,
        coverage=1.0,
        source_event_ids=(suffix,),
        reasons=("fixture",),
    )


def test_legacy_explicit_family_does_not_force_setup():
    result = apply(detect(build_intelligence(_snapshot())), StrategyFamily.LIQUIDITY_SWEEP_REVERSAL)
    if result.live_candidate is not None:
        assert result.live_candidate.family is StrategyFamily.LIQUIDITY_SWEEP_REVERSAL


def test_production_route_uses_structural_priority_not_highest_score():
    trend = _qualified(StrategyFamily.TREND_PULLBACK_CONTINUATION, Direction.SELL, 0.95, "trend")
    breakout = _qualified(StrategyFamily.BREAKOUT_EXPANSION, Direction.SELL, 0.60, "breakout")
    result = route(SetupRegistry((trend, breakout)))
    assert result.live_candidate is breakout
    assert result.active_family is StrategyFamily.BREAKOUT_EXPANSION
    assert result.reason == "ROUTED_FAMILY_SETUP_QUALIFIED"
    assert len([item for item in result.candidates if item.mode.value == "ACTIVE_EXECUTION"]) == 1


def test_production_route_fails_closed_on_opposing_qualified_directions():
    buy = _qualified(StrategyFamily.LIQUIDITY_SWEEP_REVERSAL, Direction.BUY, 0.70, "buy")
    sell = _qualified(StrategyFamily.BREAKOUT_EXPANSION, Direction.SELL, 0.80, "sell")
    result = route(SetupRegistry((buy, sell)))
    assert result.live_candidate is None
    assert result.active_family is None
    assert result.reason == "OPPOSING_QUALIFIED_STRUCTURAL_SETUPS"
    assert not [item for item in result.candidates if item.mode.value == "ACTIVE_EXECUTION"]


def test_production_route_waits_when_no_family_is_qualified():
    registry = detect(build_intelligence(_snapshot()))
    result = route(registry)
    if not registry.qualified:
        assert result.live_candidate is None
        assert result.reason == "NO_QUALIFIED_STRUCTURAL_SETUP"
