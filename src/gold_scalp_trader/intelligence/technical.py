"""Causal technical zones and target-room context."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.enums import Direction
from .candle_structure import StructureReport
from .indicators import QuantReport

@dataclass(frozen=True, slots=True)
class Zone:
    lower: float; upper: float; side: str; source: str

@dataclass(frozen=True, slots=True)
class TechnicalReport:
    support: Zone | None; resistance: Zone | None; buy_room: float | None; sell_room: float | None; buy_location: str; sell_location: str; coverage: float

def analyze(structure: StructureReport, quant: QuantReport, price: float) -> TechnicalReport:
    atr=quant.atr14; half=None if atr is None else max(atr*.12,1e-9); support=resistance=None
    if structure.last_swing_low is not None and half is not None:
        p=structure.last_swing_low.price; support=Zone(p-half,p+half,"SUPPORT","CONFIRMED_SWING_LOW")
    if structure.last_swing_high is not None and half is not None:
        p=structure.last_swing_high.price; resistance=Zone(p-half,p+half,"RESISTANCE","CONFIRMED_SWING_HIGH")
    buy_room=None if resistance is None else max(0.0,resistance.lower-price); sell_room=None if support is None else max(0.0,price-support.upper)
    return TechnicalReport(support,resistance,buy_room,sell_room,_location(price,support,resistance,Direction.BUY),_location(price,support,resistance,Direction.SELL),sum(v is not None for v in (support,resistance,atr))/3.0)

def _location(price: float, support: Zone | None, resistance: Zone | None, direction: Direction) -> str:
    if support is None or resistance is None: return "UNKNOWN"
    total=resistance.upper-support.lower
    if total<=0: return "UNKNOWN"
    pos=(price-support.lower)/total
    if direction is Direction.BUY:
        return "GOOD" if pos<=.35 else "POOR" if pos>=.80 else "NEUTRAL"
    return "GOOD" if pos>=.65 else "POOR" if pos<=.20 else "NEUTRAL"
