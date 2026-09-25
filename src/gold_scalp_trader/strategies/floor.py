"""Market-first six-family setup detection with independent BUY/SELL cases.

The active-family policy is deliberately absent from this module.  Each family
must prove its own causal setup from the immutable intelligence snapshot; the
Strategy Isolation controller decides live eligibility only after detection.

The numerical weights below are the existing uncalibrated baseline policy. They
are versioned research parameters, not probabilities and not monetary-Risk
inputs.  Family-defining evidence is separated from optional support so a pile
of indicators cannot manufacture a missing setup.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha1

from gold_scalp_trader.domain.enums import (
    Direction,
    EvidenceRole,
    SetupQualification,
    StrategyFamily,
    StructureState,
    Timeframe,
)
from gold_scalp_trader.domain.models import DirectionalCase, Evidence, SetupCandidate
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot, TimeframeIntelligence


@dataclass(frozen=True, slots=True)
class StrategyPolicy:
    """Versioned, intentionally calibratable analytical baseline."""

    version: str = "BASELINE_UNCALIBRATED_V2"
    qualification_score: float = 0.60
    possible_score: float = 0.40
    max_extension_atr: float = 1.50
    compression_atr_ratio: float = 0.85
    expansion_atr_ratio: float = 1.10

    def __post_init__(self) -> None:
        if not 0.0 < self.possible_score <= self.qualification_score <= 1.0:
            raise ValueError("strategy score thresholds must satisfy 0 < possible <= qualification <= 1")
        if self.max_extension_atr <= 0 or self.compression_atr_ratio <= 0 or self.expansion_atr_ratio <= 0:
            raise ValueError("strategy normalized thresholds must be positive")


def detect_all(
    snapshot: IntelligenceSnapshot,
    policy: StrategyPolicy | None = None,
) -> tuple[SetupCandidate, ...]:
    """Evaluate all six families in deterministic canonical order."""

    p = policy or StrategyPolicy()
    return tuple(
        detector(snapshot, p)
        for detector in (
            _trend_pullback,
            _breakout_expansion,
            _breakout_retest,
            _liquidity_sweep,
            _failed_breakout,
            _compression_expansion,
        )
    )


def _tf(snapshot: IntelligenceSnapshot, timeframe: Timeframe) -> TimeframeIntelligence | None:
    return snapshot.by_timeframe.get(timeframe)


def _e(
    snapshot: IntelligenceSnapshot,
    code: str,
    role: EvidenceRole,
    value: float | str | bool | None,
    source_id: str,
    explanation: str,
    *,
    observed_at: datetime | None = None,
) -> Evidence:
    return Evidence(
        code=code,
        role=role,
        value=value,
        source_id=source_id,
        observed_at=observed_at or snapshot.market.captured_at,
        explanation=explanation,
    )


def _case(
    direction: Direction,
    *,
    score: float,
    observed: int,
    expected: int,
    required_complete: bool,
    reasons: list[str],
    evidence: list[Evidence],
) -> DirectionalCase:
    return DirectionalCase(
        direction=direction,
        score=max(0.0, min(1.0, score)),
        coverage=0.0 if expected <= 0 else max(0.0, min(1.0, observed / expected)),
        required_complete=required_complete,
        reasons=tuple(reasons),
        evidence=tuple(evidence),
    )


def _candidate(
    snapshot: IntelligenceSnapshot,
    family: StrategyFamily,
    buy: DirectionalCase,
    sell: DirectionalCase,
    policy: StrategyPolicy,
    *,
    source_ids: tuple[str, ...] = (),
    m5_event_time: datetime | None = None,
    buy_location: str | None = None,
    sell_location: str | None = None,
    buy_room: float | None = None,
    sell_room: float | None = None,
    timing_profile: str | None = None,
    correlation_ids: tuple[str, ...] = (),
) -> SetupCandidate:
    """Combine two independent family cases without making them inverses."""

    if buy.score > sell.score:
        leading = buy
    elif sell.score > buy.score:
        leading = sell
    else:
        leading = None

    if max(buy.coverage, sell.coverage) == 0.0:
        qualification = SetupQualification.UNKNOWN
        direction = Direction.NONE
        score = 0.0
        reasons = ("required family inputs unavailable",)
        required_complete: bool | None = None
        selected_evidence = tuple(buy.evidence + sell.evidence)
    elif leading is None:
        qualification = SetupQualification.POSSIBLE if buy.score >= policy.possible_score else SetupQualification.NOT_PRESENT
        direction = Direction.NONE
        score = buy.score
        reasons = tuple(dict.fromkeys((*buy.reasons, *sell.reasons)))
        required_complete = buy.required_complete and sell.required_complete
        selected_evidence = tuple(buy.evidence + sell.evidence)
    else:
        direction = leading.direction if leading.score >= policy.possible_score else Direction.NONE
        score = leading.score
        required_complete = leading.required_complete
        reasons = leading.reasons
        selected_evidence = leading.evidence
        if leading.required_complete and leading.score >= policy.qualification_score:
            qualification = (
                SetupQualification.QUALIFIED_BUY
                if leading.direction is Direction.BUY
                else SetupQualification.QUALIFIED_SELL
            )
        elif leading.score >= policy.possible_score:
            qualification = SetupQualification.POSSIBLE
        else:
            qualification = SetupQualification.NOT_PRESENT

    raw = (
        f"{family.value}|{direction.value}|{snapshot.market.captured_at.isoformat()}|"
        f"{'|'.join(source_ids)}|{policy.version}"
    )
    candidate_id = f"SET-{sha1(raw.encode()).hexdigest()[:16]}"
    location = buy_location if direction is Direction.BUY else sell_location if direction is Direction.SELL else None
    room = buy_room if direction is Direction.BUY else sell_room if direction is Direction.SELL else None
    return SetupCandidate(
        candidate_id=candidate_id,
        family=family,
        qualification=qualification,
        direction=direction,
        score=score,
        coverage=max(buy.coverage, sell.coverage),
        source_event_ids=source_ids,
        reasons=reasons,
        evidence=selected_evidence,
        buy_case=buy,
        sell_case=sell,
        required_evidence_complete=required_complete,
        m5_event_time=m5_event_time,
        location_quality=location,
        target_room=room,
        preferred_m1_profile=timing_profile,
        correlation_ids=correlation_ids or source_ids,
    )


def _trend_pullback_case(
    snapshot: IntelligenceSnapshot,
    policy: StrategyPolicy,
    direction: Direction,
) -> DirectionalCase:
    h1, m15, m5 = _tf(snapshot, Timeframe.H1), _tf(snapshot, Timeframe.M15), _tf(snapshot, Timeframe.M5)
    candles = snapshot.market.series(Timeframe.M5)
    reasons: list[str] = []
    evidence: list[Evidence] = []
    expected, observed, score = 7, 0, 0.0
    if not (h1 and m15 and m5) or len(candles) < 2:
        return _case(direction, score=0.0, observed=0, expected=expected, required_complete=False,
                     reasons=["H1/M15/M5 pullback evidence unavailable"], evidence=[])

    prev, latest = candles[-2], candles[-1]
    wanted_structure = StructureState.BULLISH if direction is Direction.BUY else StructureState.BEARISH
    wanted_flow = direction.value
    structure_ok = h1.structure.state is wanted_structure
    observed += 1
    evidence.append(_e(snapshot, "H1_STRUCTURE", EvidenceRole.REQUIRED_FOR_FAMILY, structure_ok,
                       f"H1:{h1.structure.state.value}", "established broad structure supports continuation"))
    if structure_ok:
        score += 0.20
        reasons.append(f"H1 {wanted_structure.value.lower()} structure")

    flow_ok = m5.quant.ema_flow == wanted_flow
    observed += 1
    evidence.append(_e(snapshot, "M5_EMA_FLOW", EvidenceRole.REQUIRED_FOR_FAMILY, flow_ok,
                       "M5:EMA20_50", "M5 EMA flow agrees with continuation direction"))
    if flow_ok:
        score += 0.15
        reasons.append(f"M5 EMA flow {wanted_flow}")

    if direction is Direction.BUY:
        pullback_ok = prev.close < prev.open and latest.close > latest.open and latest.close > prev.close
    else:
        pullback_ok = prev.close > prev.open and latest.close < latest.open and latest.close < prev.close
    observed += 1
    evidence.append(_e(snapshot, "M5_PULLBACK_RESUMPTION", EvidenceRole.REQUIRED_FOR_FAMILY, pullback_ok,
                       f"M5:{latest.close_time.isoformat()}", "completed counter candle followed by directional resumption",
                       observed_at=latest.close_time))
    if pullback_ok:
        score += 0.25
        reasons.append("completed M5 pullback/resumption behavior")

    location = m15.technical.buy_location if direction is Direction.BUY else m15.technical.sell_location
    location_known = location != "UNKNOWN"
    if location_known:
        observed += 1
    location_ok = location in {"GOOD", "NEUTRAL"}
    evidence.append(_e(snapshot, "M15_LOCATION", EvidenceRole.STRONG_SUPPORT, location if location_known else None,
                       "M15:LOCATION", "higher-timeframe location supports or opposes the family"))
    if location_ok:
        score += 0.15
        reasons.append("M15 location is not hostile")
    elif location == "POOR":
        evidence.append(_e(snapshot, "M15_LOCATION_OPPOSITION", EvidenceRole.OPPOSITION, location,
                           "M15:LOCATION", "location is poor for this continuation direction"))
        reasons.append("M15 location opposes continuation")

    extension = m5.quant.extension_atr
    if extension is not None:
        observed += 1
    extension_ok = extension is not None and extension <= policy.max_extension_atr
    evidence.append(_e(snapshot, "M5_EXTENSION_ATR", EvidenceRole.STRONG_SUPPORT, extension,
                       "M5:ATR_EXTENSION", "entry should not already be severely extended"))
    if extension_ok:
        score += 0.10
        reasons.append("M5 continuation is not severely chased")
    elif extension is not None:
        evidence.append(_e(snapshot, "M5_EXTENSION_OPPOSITION", EvidenceRole.OPPOSITION, extension,
                           "M5:ATR_EXTENSION", "late extension weakens entry quality"))

    rsi = m5.quant.rsi14
    if rsi is not None:
        observed += 1
    rsi_ok = rsi is not None and ((40 <= rsi <= 70) if direction is Direction.BUY else (30 <= rsi <= 60))
    evidence.append(_e(snapshot, "M5_RSI", EvidenceRole.OPTIONAL_SUPPORT, rsi, "M5:RSI14",
                       "momentum reset/continuation context; never a universal veto"))
    if rsi_ok:
        score += 0.075
        reasons.append("RSI supports reset/continuation")

    room = m15.technical.buy_room if direction is Direction.BUY else m15.technical.sell_room
    if room is not None:
        observed += 1
    room_ok = room is not None and room > 0
    evidence.append(_e(snapshot, "M15_TARGET_ROOM", EvidenceRole.STRONG_SUPPORT, room,
                       "M15:TARGET_ROOM", "credible continuation room exists before opposing structure"))
    if room_ok:
        score += 0.075
        reasons.append("structural continuation room exists")

    required = structure_ok and flow_ok and pullback_ok
    if not required:
        reasons.append("family-defining trend/pullback/resumption evidence incomplete")
    return _case(direction, score=score, observed=observed, expected=expected,
                 required_complete=required, reasons=reasons, evidence=evidence)


def _trend_pullback(snapshot: IntelligenceSnapshot, policy: StrategyPolicy) -> SetupCandidate:
    buy = _trend_pullback_case(snapshot, policy, Direction.BUY)
    sell = _trend_pullback_case(snapshot, policy, Direction.SELL)
    m15 = _tf(snapshot, Timeframe.M15)
    m5 = _tf(snapshot, Timeframe.M5)
    return _candidate(
        snapshot,
        StrategyFamily.TREND_PULLBACK_CONTINUATION,
        buy,
        sell,
        policy,
        m5_event_time=m5.structure.event_time if m5 else None,
        buy_location=m15.technical.buy_location if m15 else None,
        sell_location=m15.technical.sell_location if m15 else None,
        buy_room=m15.technical.buy_room if m15 else None,
        sell_room=m15.technical.sell_room if m15 else None,
        timing_profile="PULLBACK_COMPLETION_OR_MICRO_RECLAIM",
    )


def _accepted_break(
    snapshot: IntelligenceSnapshot,
    direction: Direction,
) -> tuple[bool, str | None, datetime | None]:
    m5 = _tf(snapshot, Timeframe.M5)
    candles = snapshot.market.series(Timeframe.M5)
    if m5 is None or len(candles) < 2:
        return False, None, None
    prev, latest = candles[-2], candles[-1]
    if direction is Direction.BUY and m5.structure.last_swing_high is not None:
        swing = m5.structure.last_swing_high
        ok = swing.confirmed_at < prev.close_time and prev.close > swing.price and latest.close > swing.price
        return ok, f"M5:SWING_HIGH:{swing.pivot_time.isoformat()}", latest.close_time if ok else None
    if direction is Direction.SELL and m5.structure.last_swing_low is not None:
        swing = m5.structure.last_swing_low
        ok = swing.confirmed_at < prev.close_time and prev.close < swing.price and latest.close < swing.price
        return ok, f"M5:SWING_LOW:{swing.pivot_time.isoformat()}", latest.close_time if ok else None
    return False, None, None


def _breakout_expansion_case(snapshot: IntelligenceSnapshot, policy: StrategyPolicy, direction: Direction) -> DirectionalCase:
    m5, m15 = _tf(snapshot, Timeframe.M5), _tf(snapshot, Timeframe.M15)
    reasons: list[str] = []
    evidence: list[Evidence] = []
    expected, observed, score = 5, 0, 0.0
    if not (m5 and m15):
        return _case(direction, score=0.0, observed=0, expected=expected, required_complete=False,
                     reasons=["M5/M15 breakout evidence unavailable"], evidence=[])

    accepted, source, event_time = _accepted_break(snapshot, direction)
    observed += 1
    evidence.append(_e(snapshot, "M5_ACCEPTED_BREAK", EvidenceRole.REQUIRED_FOR_FAMILY, accepted,
                       source or "M5:BREAK", "two completed closes accept beyond causal confirmed structure",
                       observed_at=event_time))
    if accepted:
        score += 0.45
        reasons.append("completed M5 structural break has acceptance")

    vol = m5.quant.volatility_state
    if vol != "UNKNOWN":
        observed += 1
    vol_ok = vol in {"BUILDING", "EXPANDING", "EXTREME"}
    evidence.append(_e(snapshot, "M5_VOLATILITY", EvidenceRole.STRONG_SUPPORT, vol,
                       "M5:VOLATILITY", "expansion family prefers building/expanding participation"))
    if vol_ok:
        score += 0.20
        reasons.append("volatility supports expansion")

    room = m15.technical.buy_room if direction is Direction.BUY else m15.technical.sell_room
    if room is not None:
        observed += 1
    room_ok = room is not None and room > 0
    evidence.append(_e(snapshot, "M15_TARGET_ROOM", EvidenceRole.STRONG_SUPPORT, room,
                       "M15:TARGET_ROOM", "structural path remains open in breakout direction"))
    if room_ok:
        score += 0.20
        reasons.append("higher-timeframe path/room exists")

    extension = m5.quant.extension_atr
    if extension is not None:
        observed += 1
    extension_ok = extension is not None and extension <= policy.max_extension_atr
    evidence.append(_e(snapshot, "M5_EXTENSION_ATR", EvidenceRole.STRONG_SUPPORT, extension,
                       "M5:ATR_EXTENSION", "anti-chase context"))
    if extension_ok:
        score += 0.10
        reasons.append("breakout is not severely extended")

    latest = snapshot.market.series(Timeframe.M5)[-1]
    directional_body = latest.close > latest.open if direction is Direction.BUY else latest.close < latest.open
    observed += 1
    evidence.append(_e(snapshot, "M5_DIRECTIONAL_EXPANSION", EvidenceRole.OPTIONAL_SUPPORT, directional_body,
                       f"M5:{latest.close_time.isoformat()}", "latest completed candle continues in accepted-break direction",
                       observed_at=latest.close_time))
    if directional_body:
        score += 0.05

    if not accepted:
        reasons.append("family-defining accepted breakout is absent")
    return _case(direction, score=score, observed=observed, expected=expected,
                 required_complete=accepted, reasons=reasons, evidence=evidence)


def _breakout_expansion(snapshot: IntelligenceSnapshot, policy: StrategyPolicy) -> SetupCandidate:
    buy = _breakout_expansion_case(snapshot, policy, Direction.BUY)
    sell = _breakout_expansion_case(snapshot, policy, Direction.SELL)
    m15 = _tf(snapshot, Timeframe.M15)
    _, buy_source, buy_time = _accepted_break(snapshot, Direction.BUY)
    _, sell_source, sell_time = _accepted_break(snapshot, Direction.SELL)
    sources = tuple(x for x in (buy_source, sell_source) if x)
    return _candidate(
        snapshot,
        StrategyFamily.BREAKOUT_EXPANSION,
        buy,
        sell,
        policy,
        source_ids=sources,
        m5_event_time=buy_time or sell_time,
        buy_location=m15.technical.buy_location if m15 else None,
        sell_location=m15.technical.sell_location if m15 else None,
        buy_room=m15.technical.buy_room if m15 else None,
        sell_room=m15.technical.sell_room if m15 else None,
        timing_profile="FRESH_ACCEPTED_BREAK_NO_CHASE",
        correlation_ids=sources,
    )


def _breakout_retest_case(snapshot: IntelligenceSnapshot, policy: StrategyPolicy, direction: Direction) -> DirectionalCase:
    m5, m15 = _tf(snapshot, Timeframe.M5), _tf(snapshot, Timeframe.M15)
    candles = snapshot.market.series(Timeframe.M5)
    reasons: list[str] = []
    evidence: list[Evidence] = []
    expected, observed, score = 5, 0, 0.0
    if not (m5 and m15) or len(candles) < 2:
        return _case(direction, score=0.0, observed=0, expected=expected, required_complete=False,
                     reasons=["M5/M15 retest evidence unavailable"], evidence=[])
    breakout, retest = candles[-2], candles[-1]
    level = m15.structure.last_swing_high if direction is Direction.BUY else m15.structure.last_swing_low
    sequence_ok = False
    source_id = "M15:RETEST_LEVEL"
    if level is not None and level.confirmed_at < breakout.close_time:
        source_id = f"M15:SWING:{level.pivot_time.isoformat()}"
        if direction is Direction.BUY:
            sequence_ok = breakout.close > level.price and retest.low <= level.price <= retest.close
        else:
            sequence_ok = breakout.close < level.price and retest.high >= level.price >= retest.close
    observed += 1
    evidence.append(_e(snapshot, "BREAKOUT_RETEST_SEQUENCE", EvidenceRole.REQUIRED_FOR_FAMILY, sequence_ok,
                       source_id, "completed breakout followed by completed retest holding the broken structure",
                       observed_at=retest.close_time))
    if sequence_ok:
        score += 0.55
        reasons.append("causal breakout + completed retest hold")

    resumption = retest.close > retest.open if direction is Direction.BUY else retest.close < retest.open
    observed += 1
    evidence.append(_e(snapshot, "M5_RETEST_RESPONSE", EvidenceRole.STRONG_SUPPORT, resumption,
                       f"M5:{retest.close_time.isoformat()}", "retest candle responds in continuation direction",
                       observed_at=retest.close_time))
    if resumption:
        score += 0.10
        reasons.append("M5 retest response supports continuation")

    room = m15.technical.buy_room if direction is Direction.BUY else m15.technical.sell_room
    if room is not None:
        observed += 1
    if room is not None and room > 0:
        score += 0.20
        reasons.append("continuation room exists")
    evidence.append(_e(snapshot, "M15_TARGET_ROOM", EvidenceRole.STRONG_SUPPORT, room,
                       "M15:TARGET_ROOM", "remaining structural room after retest"))

    extension = m5.quant.extension_atr
    if extension is not None:
        observed += 1
    if extension is not None and extension <= policy.max_extension_atr:
        score += 0.10
        reasons.append("retest entry is not severely extended")
    evidence.append(_e(snapshot, "M5_EXTENSION_ATR", EvidenceRole.STRONG_SUPPORT, extension,
                       "M5:ATR_EXTENSION", "anti-chase context after retest"))

    location = m15.technical.buy_location if direction is Direction.BUY else m15.technical.sell_location
    if location != "UNKNOWN":
        observed += 1
    if location == "GOOD":
        score += 0.05
    evidence.append(_e(snapshot, "M15_LOCATION", EvidenceRole.OPTIONAL_SUPPORT, location,
                       "M15:LOCATION", "higher-timeframe location is optional supporting context"))

    if not sequence_ok:
        reasons.append("family-defining breakout+retest sequence absent")
    return _case(direction, score=score, observed=observed, expected=expected,
                 required_complete=sequence_ok, reasons=reasons, evidence=evidence)


def _breakout_retest(snapshot: IntelligenceSnapshot, policy: StrategyPolicy) -> SetupCandidate:
    buy = _breakout_retest_case(snapshot, policy, Direction.BUY)
    sell = _breakout_retest_case(snapshot, policy, Direction.SELL)
    m15 = _tf(snapshot, Timeframe.M15)
    candles = snapshot.market.series(Timeframe.M5)
    event_time = candles[-1].close_time if len(candles) >= 2 else None
    source_ids = tuple(
        ev.source_id
        for case in (buy, sell)
        for ev in case.evidence
        if ev.code == "BREAKOUT_RETEST_SEQUENCE" and bool(ev.value)
    )
    return _candidate(
        snapshot,
        StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
        buy,
        sell,
        policy,
        source_ids=source_ids,
        m5_event_time=event_time if source_ids else None,
        buy_location=m15.technical.buy_location if m15 else None,
        sell_location=m15.technical.sell_location if m15 else None,
        buy_room=m15.technical.buy_room if m15 else None,
        sell_room=m15.technical.sell_room if m15 else None,
        timing_profile="RETEST_HOLD_THEN_MICRO_CONTINUATION",
        correlation_ids=source_ids,
    )


def _liquidity_sweep_case(snapshot: IntelligenceSnapshot, policy: StrategyPolicy, direction: Direction) -> DirectionalCase:
    m5, m15 = _tf(snapshot, Timeframe.M5), _tf(snapshot, Timeframe.M15)
    reasons: list[str] = []
    evidence: list[Evidence] = []
    expected, observed, score = 5, 0, 0.0
    if m5 is None:
        return _case(direction, score=0.0, observed=0, expected=expected, required_complete=False,
                     reasons=["M5 liquidity evidence unavailable"], evidence=[])

    report = m5.liquidity
    pool = report.sell_side if direction is Direction.BUY else report.buy_side
    expected_event = "SELL_SIDE_SWEEP_RECLAIM" if direction is Direction.BUY else "BUY_SIDE_SWEEP_RECLAIM"
    causal_pool = pool is not None and report.event_time is not None and pool.created_at < report.event_time
    sweep_ok = report.latest_event == expected_event and report.event_direction is direction and causal_pool
    observed += 1
    evidence.append(_e(snapshot, "M5_CAUSAL_SWEEP_RECLAIM", EvidenceRole.REQUIRED_FOR_FAMILY, sweep_ok,
                       pool.pool_id if pool else "M5:LIQUIDITY_POOL", "pre-existing liquidity is penetrated and reclaimed on a completed M5 event",
                       observed_at=report.event_time))
    if sweep_ok:
        score += 0.60
        reasons.append(expected_event)

    structure_response = (
        m5.structure.state in {StructureState.BULLISH, StructureState.TRANSITION}
        if direction is Direction.BUY
        else m5.structure.state in {StructureState.BEARISH, StructureState.TRANSITION}
    )
    observed += 1
    evidence.append(_e(snapshot, "M5_REVERSAL_STRUCTURE", EvidenceRole.STRONG_SUPPORT, structure_response,
                       f"M5:STRUCTURE:{m5.structure.state.value}", "local structure is compatible with reversal response"))
    if structure_response:
        score += 0.10
        reasons.append("M5 structure supports reversal response")

    location = None
    room = None
    if m15 is not None:
        location = m15.technical.buy_location if direction is Direction.BUY else m15.technical.sell_location
        room = m15.technical.buy_room if direction is Direction.BUY else m15.technical.sell_room
    if location is not None and location != "UNKNOWN":
        observed += 1
    location_ok = location not in {None, "UNKNOWN", "POOR"}
    evidence.append(_e(snapshot, "M15_LOCATION", EvidenceRole.STRONG_SUPPORT, location,
                       "M15:LOCATION", "higher-timeframe location should not be hostile to the reversal"))
    if location_ok:
        score += 0.10
        reasons.append("M15 location is not hostile")

    if room is not None:
        observed += 1
    evidence.append(_e(snapshot, "M15_OPPOSING_PATH", EvidenceRole.STRONG_SUPPORT, room,
                       "M15:TARGET_ROOM", "opposing-side structural path provides reversal room"))
    if room is not None and room > 0:
        score += 0.10
        reasons.append("reversal target path exists")

    extension = m5.quant.extension_atr
    if extension is not None:
        observed += 1
    evidence.append(_e(snapshot, "M5_EXTENSION_ATR", EvidenceRole.OPTIONAL_SUPPORT, extension,
                       "M5:ATR_EXTENSION", "extension is timing context, not a family-defining veto"))
    if extension is not None and extension <= policy.max_extension_atr:
        score += 0.10

    if not sweep_ok:
        reasons.append("family-defining causal sweep/reclaim absent")
    return _case(direction, score=score, observed=observed, expected=expected,
                 required_complete=sweep_ok, reasons=reasons, evidence=evidence)


def _liquidity_sweep(snapshot: IntelligenceSnapshot, policy: StrategyPolicy) -> SetupCandidate:
    buy = _liquidity_sweep_case(snapshot, policy, Direction.BUY)
    sell = _liquidity_sweep_case(snapshot, policy, Direction.SELL)
    m5, m15 = _tf(snapshot, Timeframe.M5), _tf(snapshot, Timeframe.M15)
    source_ids = tuple(
        ev.source_id
        for case in (buy, sell)
        for ev in case.evidence
        if ev.code == "M5_CAUSAL_SWEEP_RECLAIM" and bool(ev.value)
    )
    return _candidate(
        snapshot,
        StrategyFamily.LIQUIDITY_SWEEP_REVERSAL,
        buy,
        sell,
        policy,
        source_ids=source_ids,
        m5_event_time=m5.liquidity.event_time if m5 else None,
        buy_location=m15.technical.buy_location if m15 else None,
        sell_location=m15.technical.sell_location if m15 else None,
        buy_room=m15.technical.buy_room if m15 else None,
        sell_room=m15.technical.sell_room if m15 else None,
        timing_profile="SWEEP_RECLAIM_THEN_MICRO_REVERSAL",
        correlation_ids=source_ids,
    )


def _failed_break_case(snapshot: IntelligenceSnapshot, direction: Direction) -> DirectionalCase:
    m5, m15 = _tf(snapshot, Timeframe.M5), _tf(snapshot, Timeframe.M15)
    candles = snapshot.market.series(Timeframe.M5)
    reasons: list[str] = []
    evidence: list[Evidence] = []
    expected, observed, score = 5, 0, 0.0
    if m5 is None or len(candles) < 2:
        return _case(direction, score=0.0, observed=0, expected=expected, required_complete=False,
                     reasons=["M5 failed-break evidence unavailable"], evidence=[])

    attempt, response = candles[-2], candles[-1]
    level = m5.structure.last_swing_low if direction is Direction.BUY else m5.structure.last_swing_high
    failed = False
    source_id = "M5:FAILED_BREAK_LEVEL"
    if level is not None and level.confirmed_at < attempt.close_time:
        source_id = f"M5:SWING:{level.pivot_time.isoformat()}"
        if direction is Direction.BUY:
            failed = attempt.close < level.price and response.close > level.price
        else:
            failed = attempt.close > level.price and response.close < level.price
    observed += 1
    evidence.append(_e(snapshot, "M5_FAILED_ACCEPTANCE", EvidenceRole.REQUIRED_FOR_FAMILY, failed,
                       source_id, "completed acceptance beyond structure is followed by completed return through it",
                       observed_at=response.close_time))
    if failed:
        score += 0.60
        reasons.append("accepted breakout attempt failed back through structure")

    response_body = response.close > response.open if direction is Direction.BUY else response.close < response.open
    observed += 1
    evidence.append(_e(snapshot, "M5_OPPOSING_RESPONSE", EvidenceRole.STRONG_SUPPORT, response_body,
                       f"M5:{response.close_time.isoformat()}", "response candle moves in reversal direction",
                       observed_at=response.close_time))
    if response_body:
        score += 0.10
        reasons.append("M5 reversal response is directional")

    transition = (
        m5.structure.state in {StructureState.BULLISH, StructureState.TRANSITION}
        if direction is Direction.BUY
        else m5.structure.state in {StructureState.BEARISH, StructureState.TRANSITION}
    )
    observed += 1
    evidence.append(_e(snapshot, "M5_STRUCTURE_RESPONSE", EvidenceRole.STRONG_SUPPORT, transition,
                       f"M5:STRUCTURE:{m5.structure.state.value}", "structure is compatible with the reversal direction"))
    if transition:
        score += 0.10

    location = None
    room = None
    if m15 is not None:
        location = m15.technical.buy_location if direction is Direction.BUY else m15.technical.sell_location
        room = m15.technical.buy_room if direction is Direction.BUY else m15.technical.sell_room
    if location is not None and location != "UNKNOWN":
        observed += 1
    evidence.append(_e(snapshot, "M15_LOCATION", EvidenceRole.OPTIONAL_SUPPORT, location,
                       "M15:LOCATION", "higher location is supporting context, not a universal requirement"))
    if location == "GOOD":
        score += 0.10

    if room is not None:
        observed += 1
    evidence.append(_e(snapshot, "M15_TARGET_ROOM", EvidenceRole.STRONG_SUPPORT, room,
                       "M15:TARGET_ROOM", "reversal requires usable opposing path"))
    if room is not None and room > 0:
        score += 0.10
        reasons.append("reversal target room exists")

    if not failed:
        reasons.append("family-defining accepted-break failure absent")
    return _case(direction, score=score, observed=observed, expected=expected,
                 required_complete=failed, reasons=reasons, evidence=evidence)


def _failed_breakout(snapshot: IntelligenceSnapshot, policy: StrategyPolicy) -> SetupCandidate:
    buy = _failed_break_case(snapshot, Direction.BUY)
    sell = _failed_break_case(snapshot, Direction.SELL)
    m15 = _tf(snapshot, Timeframe.M15)
    candles = snapshot.market.series(Timeframe.M5)
    source_ids = tuple(
        ev.source_id
        for case in (buy, sell)
        for ev in case.evidence
        if ev.code == "M5_FAILED_ACCEPTANCE" and bool(ev.value)
    )
    return _candidate(
        snapshot,
        StrategyFamily.FAILED_BREAKOUT_REVERSAL,
        buy,
        sell,
        policy,
        source_ids=source_ids,
        m5_event_time=candles[-1].close_time if source_ids and candles else None,
        buy_location=m15.technical.buy_location if m15 else None,
        sell_location=m15.technical.sell_location if m15 else None,
        buy_room=m15.technical.buy_room if m15 else None,
        sell_room=m15.technical.sell_room if m15 else None,
        timing_profile="FAILED_ACCEPTANCE_THEN_MICRO_REVERSAL",
        correlation_ids=source_ids,
    )


def _compression_case(snapshot: IntelligenceSnapshot, policy: StrategyPolicy, direction: Direction) -> DirectionalCase:
    m5, m15 = _tf(snapshot, Timeframe.M5), _tf(snapshot, Timeframe.M15)
    candles = snapshot.market.series(Timeframe.M5)
    reasons: list[str] = []
    evidence: list[Evidence] = []
    expected, observed, score = 5, 0, 0.0
    if m5 is None or len(candles) < 8 or m5.quant.atr14 is None or m5.quant.atr14 <= 0:
        return _case(direction, score=0.0, observed=0, expected=expected, required_complete=False,
                     reasons=["M5 compression/ATR history unavailable"], evidence=[])

    atr = m5.quant.atr14
    pre_release = candles[-8:-1]
    average_range = sum(c.range for c in pre_release) / len(pre_release)
    latest = candles[-1]
    compressed = average_range < atr * policy.compression_atr_ratio
    directional_release = (
        latest.close > latest.open if direction is Direction.BUY else latest.close < latest.open
    ) and latest.range > atr * policy.expansion_atr_ratio
    observed += 2
    evidence.append(_e(snapshot, "M5_COMPRESSION", EvidenceRole.REQUIRED_FOR_FAMILY,
                       average_range / atr, "M5:COMPRESSION_WINDOW",
                       "pre-release completed candles form ATR-normalized compression"))
    evidence.append(_e(snapshot, "M5_DIRECTIONAL_RELEASE", EvidenceRole.REQUIRED_FOR_FAMILY,
                       directional_release, f"M5:{latest.close_time.isoformat()}",
                       "fresh completed expansion candle supplies direction",
                       observed_at=latest.close_time))
    if compressed:
        score += 0.25
        reasons.append("causal M5 compression exists")
    if directional_release:
        score += 0.40
        reasons.append("fresh directional M5 expansion release")

    room = None
    if m15 is not None:
        room = m15.technical.buy_room if direction is Direction.BUY else m15.technical.sell_room
    if room is not None:
        observed += 1
    evidence.append(_e(snapshot, "M15_TARGET_ROOM", EvidenceRole.STRONG_SUPPORT, room,
                       "M15:TARGET_ROOM", "release should have usable continuation path"))
    if room is not None and room > 0:
        score += 0.15
        reasons.append("expansion path/room exists")

    extension = m5.quant.extension_atr
    if extension is not None:
        observed += 1
    evidence.append(_e(snapshot, "M5_EXTENSION_ATR", EvidenceRole.STRONG_SUPPORT, extension,
                       "M5:ATR_EXTENSION", "anti-chase context after release"))
    if extension is not None and extension <= policy.max_extension_atr:
        score += 0.10

    vol = m5.quant.volatility_state
    if vol != "UNKNOWN":
        observed += 1
    evidence.append(_e(snapshot, "M5_VOLATILITY", EvidenceRole.OPTIONAL_SUPPORT, vol,
                       "M5:VOLATILITY", "volatility build/expansion supports release"))
    if vol in {"BUILDING", "EXPANDING", "EXTREME"}:
        score += 0.10

    required = compressed and directional_release
    if not required:
        reasons.append("family-defining compression+directional-release sequence absent")
    return _case(direction, score=score, observed=observed, expected=expected,
                 required_complete=required, reasons=reasons, evidence=evidence)


def _compression_expansion(snapshot: IntelligenceSnapshot, policy: StrategyPolicy) -> SetupCandidate:
    buy = _compression_case(snapshot, policy, Direction.BUY)
    sell = _compression_case(snapshot, policy, Direction.SELL)
    m15 = _tf(snapshot, Timeframe.M15)
    candles = snapshot.market.series(Timeframe.M5)
    source_ids = tuple(
        ev.source_id
        for case in (buy, sell)
        for ev in case.evidence
        if ev.code == "M5_DIRECTIONAL_RELEASE" and bool(ev.value)
    )
    return _candidate(
        snapshot,
        StrategyFamily.COMPRESSION_EXPANSION,
        buy,
        sell,
        policy,
        source_ids=source_ids,
        m5_event_time=candles[-1].close_time if source_ids and candles else None,
        buy_location=m15.technical.buy_location if m15 else None,
        sell_location=m15.technical.sell_location if m15 else None,
        buy_room=m15.technical.buy_room if m15 else None,
        sell_room=m15.technical.sell_room if m15 else None,
        timing_profile="FRESH_RELEASE_NO_CHASE",
        correlation_ids=source_ids,
    )
