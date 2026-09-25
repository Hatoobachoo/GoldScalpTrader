"""Six market-first strategy-family detectors.

Active-family policy is deliberately absent so no strategy can be forced onto a
chart merely because it is currently eligible for live execution.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha1
from gold_scalp_trader.domain.enums import Direction,SetupQualification,StrategyFamily,StructureState,Timeframe
from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot,TimeframeIntelligence

@dataclass(frozen=True, slots=True)
class StrategyPolicy:
    version: str="BASELINE_UNCALIBRATED_V1"
    qualification_score: float=.60
    possible_score: float=.40
    max_extension_atr: float=1.50

def detect_all(snapshot: IntelligenceSnapshot,policy: StrategyPolicy|None=None)->tuple[SetupCandidate,...]:
    p=policy or StrategyPolicy()
    return tuple(fn(snapshot,p) for fn in (_trend_pullback,_breakout_expansion,_breakout_retest,_liquidity_sweep,_failed_breakout,_compression_expansion))

def _tf(s: IntelligenceSnapshot,tf: Timeframe)->TimeframeIntelligence|None: return s.by_timeframe.get(tf)

def _candidate(family,direction,score,reasons,source_ids,observed_at,p):
    score=max(0.0,min(1.0,score))
    if direction is Direction.NONE: q=SetupQualification.NOT_PRESENT if score<p.possible_score else SetupQualification.POSSIBLE
    elif score>=p.qualification_score: q=SetupQualification.QUALIFIED_BUY if direction is Direction.BUY else SetupQualification.QUALIFIED_SELL
    elif score>=p.possible_score: q=SetupQualification.POSSIBLE
    else: q=SetupQualification.NOT_PRESENT
    raw=f"{family.value}|{direction.value}|{observed_at.isoformat()}|{'|'.join(source_ids)}|{p.version}"; cid=f"SET-{sha1(raw.encode()).hexdigest()[:16]}"
    return SetupCandidate(cid,family,q,direction,score,min(1.0,max(0.0,score+.20)),tuple(source_ids),tuple(reasons),())

def _trend_pullback(s,p):
    h1,m15,m5=_tf(s,Timeframe.H1),_tf(s,Timeframe.M15),_tf(s,Timeframe.M5); reasons=[]; ids=[]; score=0.0; d=Direction.NONE
    if not(h1 and m15 and m5): return _candidate(StrategyFamily.TREND_PULLBACK_CONTINUATION,d,0,["required timeframe intelligence unavailable"],ids,s.market.captured_at,p)
    if h1.structure.state is StructureState.BULLISH and m5.quant.ema_flow=="BUY": d=Direction.BUY; score+=.30; reasons.append("H1 bullish + M5 EMA flow BUY")
    elif h1.structure.state is StructureState.BEARISH and m5.quant.ema_flow=="SELL": d=Direction.SELL; score+=.30; reasons.append("H1 bearish + M5 EMA flow SELL")
    else: reasons.append("directional structure/EMA flow not aligned")
    if d is Direction.BUY and m15.technical.buy_location in {"GOOD","NEUTRAL"}: score+=.20; reasons.append("M15 location acceptable")
    elif d is Direction.SELL and m15.technical.sell_location in {"GOOD","NEUTRAL"}: score+=.20; reasons.append("M15 location acceptable")
    if m5.quant.extension_atr is not None and m5.quant.extension_atr<=p.max_extension_atr: score+=.20; reasons.append("M5 not severely chased")
    rsi=m5.quant.rsi14
    if rsi is not None and d is Direction.BUY and 40<=rsi<=70: score+=.15; reasons.append("RSI supports bullish reset/continuation")
    elif rsi is not None and d is Direction.SELL and 30<=rsi<=60: score+=.15; reasons.append("RSI supports bearish reset/continuation")
    if d is Direction.BUY and (m15.technical.buy_room or 0)>0: score+=.15; reasons.append("upside structural room exists")
    elif d is Direction.SELL and (m15.technical.sell_room or 0)>0: score+=.15; reasons.append("downside structural room exists")
    return _candidate(StrategyFamily.TREND_PULLBACK_CONTINUATION,d,score,reasons,ids,s.market.captured_at,p)

def _breakout_expansion(s,p):
    m5,m15=_tf(s,Timeframe.M5),_tf(s,Timeframe.M15); reasons=[]; ids=[]; score=0.0; d=Direction.NONE
    if not(m5 and m15): return _candidate(StrategyFamily.BREAKOUT_EXPANSION,d,0,["M5/M15 unavailable"],ids,s.market.captured_at,p)
    if m5.structure.break_direction in {Direction.BUY,Direction.SELL}: d=m5.structure.break_direction; score+=.45; reasons.append(f"M5 {m5.structure.break_event.value} {d.value}"); ids.append(f"M5-BREAK-{m5.structure.event_time.isoformat()}" if m5.structure.event_time else "M5-BREAK")
    if m5.quant.volatility_state in {"BUILDING","EXPANDING","EXTREME"}: score+=.20; reasons.append("volatility supports expansion")
    if d is Direction.BUY and (m15.technical.buy_room or 0)>0: score+=.20; reasons.append("upside path exists")
    elif d is Direction.SELL and (m15.technical.sell_room or 0)>0: score+=.20; reasons.append("downside path exists")
    if m5.quant.extension_atr is not None and m5.quant.extension_atr<=p.max_extension_atr: score+=.15; reasons.append("break is not severely extended")
    return _candidate(StrategyFamily.BREAKOUT_EXPANSION,d,score,reasons,ids,s.market.captured_at,p)

def _breakout_retest(s,p):
    m5,m15=_tf(s,Timeframe.M5),_tf(s,Timeframe.M15); reasons=[]; ids=[]; score=0.0; d=Direction.NONE; candles=s.market.series(Timeframe.M5)
    if not(m5 and m15): return _candidate(StrategyFamily.BREAKOUT_RETEST_CONTINUATION,d,0,["M5/M15 unavailable"],ids,s.market.captured_at,p)
    if len(candles)>=3 and m15.structure.last_swing_high and candles[-2].close>m15.structure.last_swing_high.price and candles[-1].low<=m15.structure.last_swing_high.price<=candles[-1].close: d=Direction.BUY; score=.55; reasons += ["M15 resistance broken","M5 retest held above broken level"]; ids.append(f"RET-{candles[-1].close_time.isoformat()}")
    elif len(candles)>=3 and m15.structure.last_swing_low and candles[-2].close<m15.structure.last_swing_low.price and candles[-1].high>=m15.structure.last_swing_low.price>=candles[-1].close: d=Direction.SELL; score=.55; reasons += ["M15 support broken","M5 retest held below broken level"]; ids.append(f"RET-{candles[-1].close_time.isoformat()}")
    if d is not Direction.NONE and m5.quant.extension_atr is not None and m5.quant.extension_atr<=p.max_extension_atr: score+=.20; reasons.append("retest entry is not severely extended")
    if d is Direction.BUY and (m15.technical.buy_room or 0)>0: score+=.25; reasons.append("continuation room exists")
    elif d is Direction.SELL and (m15.technical.sell_room or 0)>0: score+=.25; reasons.append("continuation room exists")
    return _candidate(StrategyFamily.BREAKOUT_RETEST_CONTINUATION,d,score,reasons,ids,s.market.captured_at,p)

def _liquidity_sweep(s,p):
    m5,m15=_tf(s,Timeframe.M5),_tf(s,Timeframe.M15); reasons=[]; ids=[]; score=0.0; d=Direction.NONE
    if not m5: return _candidate(StrategyFamily.LIQUIDITY_SWEEP_REVERSAL,d,0,["M5 unavailable"],ids,s.market.captured_at,p)
    if m5.liquidity.latest_event!="NONE": d=m5.liquidity.event_direction; score=.60; reasons.append(m5.liquidity.latest_event); ids.append(f"SWEEP-{m5.liquidity.event_time.isoformat()}" if m5.liquidity.event_time else "SWEEP")
    if m15 and d is Direction.BUY and m15.technical.buy_location!="POOR": score+=.20; reasons.append("higher location not hostile")
    if m15 and d is Direction.SELL and m15.technical.sell_location!="POOR": score+=.20; reasons.append("higher location not hostile")
    if m5.quant.extension_state!="SEVERELY_EXTENDED": score+=.10
    return _candidate(StrategyFamily.LIQUIDITY_SWEEP_REVERSAL,d,score,reasons,ids,s.market.captured_at,p)

def _failed_breakout(s,p):
    m5=_tf(s,Timeframe.M5); reasons=[]; ids=[]; score=0.0; d=Direction.NONE; candles=s.market.series(Timeframe.M5)
    if not m5 or len(candles)<2: return _candidate(StrategyFamily.FAILED_BREAKOUT_REVERSAL,d,0,["M5 history unavailable"],ids,s.market.captured_at,p)
    prev,latest=candles[-2],candles[-1]; hi=m5.structure.last_swing_high; lo=m5.structure.last_swing_low
    if hi and prev.high>hi.price and latest.close<hi.price: d=Direction.SELL; score=.65; reasons.append("upside break attempt failed back below structure"); ids.append(f"FAIL-{latest.close_time.isoformat()}")
    elif lo and prev.low<lo.price and latest.close>lo.price: d=Direction.BUY; score=.65; reasons.append("downside break attempt failed back above structure"); ids.append(f"FAIL-{latest.close_time.isoformat()}")
    if d is not Direction.NONE and m5.quant.volatility_state in {"NORMAL","BUILDING","EXPANDING"}: score+=.15
    return _candidate(StrategyFamily.FAILED_BREAKOUT_REVERSAL,d,score,reasons,ids,s.market.captured_at,p)

def _compression_expansion(s,p):
    m5=_tf(s,Timeframe.M5); reasons=[]; ids=[]; score=0.0; d=Direction.NONE; candles=s.market.series(Timeframe.M5)
    if not m5 or len(candles)<8 or m5.quant.atr14 is None: return _candidate(StrategyFamily.COMPRESSION_EXPANSION,d,0,["insufficient M5 compression history"],ids,s.market.captured_at,p)
    recent=candles[-8:-1]; atr=m5.quant.atr14; avg=sum(c.range for c in recent)/len(recent); latest=candles[-1]
    if avg<atr*.85 and latest.range>atr*1.10:
        d=Direction.BUY if latest.close>latest.open else Direction.SELL if latest.close<latest.open else Direction.NONE
        if d is not Direction.NONE: score=.65; reasons += ["recent range compression","fresh M5 expansion release"]; ids.append(f"COMP-{latest.close_time.isoformat()}")
    if d is not Direction.NONE and m5.quant.extension_atr is not None and m5.quant.extension_atr<=p.max_extension_atr: score+=.15
    return _candidate(StrategyFamily.COMPRESSION_EXPANSION,d,score,reasons,ids,s.market.captured_at,p)
