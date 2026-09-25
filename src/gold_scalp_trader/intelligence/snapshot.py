"""One immutable intelligence snapshot built from one MarketSnapshot."""
from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping
from gold_scalp_trader.domain.enums import Timeframe
from gold_scalp_trader.domain.market import MarketSnapshot
from .candle_structure import StructureReport,analyze as analyze_structure
from .confluence import ConfluenceReport,analyze as analyze_confluence
from .indicators import IndicatorSeries,QuantReport,calculate as calculate_quant
from .liquidity import LiquidityReport,analyze as analyze_liquidity
from .news import NewsContext
from .session import SessionReport,classify as classify_session
from .technical import TechnicalReport,analyze as analyze_technical
@dataclass(frozen=True,slots=True)
class TimeframeIntelligence:indicators:IndicatorSeries; quant:QuantReport; structure:StructureReport; technical:TechnicalReport; liquidity:LiquidityReport; confluence:ConfluenceReport
@dataclass(frozen=True,slots=True)
class IntelligenceSnapshot:
    market:MarketSnapshot; by_timeframe:Mapping[Timeframe,TimeframeIntelligence]; session:SessionReport; news:NewsContext|None
    def __post_init__(self)->None:object.__setattr__(self,"by_timeframe",MappingProxyType(dict(self.by_timeframe)))
def build(market:MarketSnapshot,news:NewsContext|None=None)->IntelligenceSnapshot:
    reports={}; price=(market.quote.bid+market.quote.ask)/2.0
    for tf,candles in market.candles.items():
        if not candles:continue
        series,quant=calculate_quant(candles); structure=analyze_structure(candles); technical=analyze_technical(structure,quant,price); liquidity=analyze_liquidity(candles,structure,quant); confluence=analyze_confluence(candles,structure); reports[tf]=TimeframeIntelligence(series,quant,structure,technical,liquidity,confluence)
    return IntelligenceSnapshot(market,reports,classify_session(market.captured_at),news)
