"""Causal optional confluence calculations; never a universal permission gate."""
from __future__ import annotations
from dataclasses import dataclass
from gold_scalp_trader.domain.market import Candle
from .candle_structure import StructureReport
@dataclass(frozen=True,slots=True)
class PriceLevel:name:str; price:float; source_ids:tuple[str,...]
@dataclass(frozen=True,slots=True)
class FairValueGap:direction:str; lower:float; upper:float; created_at:object; state:str
@dataclass(frozen=True,slots=True)
class OrderBlock:direction:str; lower:float; upper:float; origin_time:object; qualified_at:object; state:str
@dataclass(frozen=True,slots=True)
class ConfluenceReport:
    trendline:str="UNKNOWN"; trendline_price:float|None=None; fibonacci:tuple[PriceLevel,...]=(); poc:float|None=None; poc_source:str="UNKNOWN"; fvg:tuple[FairValueGap,...]=(); order_blocks:tuple[OrderBlock,...]=(); coverage:float=0.0

def _fibonacci(structure:StructureReport)->tuple[PriceLevel,...]:
    hi,lo=structure.last_swing_high,structure.last_swing_low
    if hi is None or lo is None or hi.price==lo.price:return ()
    lower,upper=sorted((lo.price,hi.price)); span=upper-lower; ids=(hi.pivot_time.isoformat(),lo.pivot_time.isoformat())
    return tuple(PriceLevel(f"FIB_{r:.3f}",upper-span*r,ids) for r in (.382,.5,.618,.786))
def _poc(candles:tuple[Candle,...],bins:int=24)->tuple[float|None,str]:
    if not candles:return None,"UNKNOWN"
    lo=min(c.low for c in candles); hi=max(c.high for c in candles)
    if hi<=lo:return candles[-1].close,"TICK_VOLUME"
    step=(hi-lo)/bins; bucket=[0.0]*bins
    for c in candles:
        price=(c.high+c.low+c.close)/3.0; idx=min(bins-1,max(0,int((price-lo)/step))); bucket[idx]+=max(0,c.real_volume if c.real_volume>0 else c.tick_volume)
    best=max(range(bins),key=bucket.__getitem__); return lo+(best+.5)*step,"REAL_VOLUME" if any(c.real_volume>0 for c in candles) else "TICK_VOLUME"
def _fvgs(candles:tuple[Candle,...],lookback:int=40)->tuple[FairValueGap,...]:
    result=[]; recent=candles[-lookback:]
    for i in range(2,len(recent)):
        c1,_,c3=recent[i-2],recent[i-1],recent[i]
        if c3.low>c1.high:lower,upper,direction=c1.high,c3.low,"BULLISH"
        elif c3.high<c1.low:lower,upper,direction=c3.high,c1.low,"BEARISH"
        else:continue
        later=recent[i+1:]; mitigated=any(c.low<=upper and c.high>=lower for c in later); result.append(FairValueGap(direction,lower,upper,c3.close_time,"MITIGATED" if mitigated else "FRESH"))
    return tuple(result[-8:])
def _order_blocks(candles:tuple[Candle,...],structure:StructureReport)->tuple[OrderBlock,...]:
    if structure.break_event.value=="NONE" or structure.event_time is None or len(candles)<2:return ()
    event_idx=next((i for i,c in enumerate(candles) if c.close_time==structure.event_time),None)
    if event_idx is None or event_idx<1:return ()
    direction=structure.break_direction.value; opposite="SELL" if direction=="BUY" else "BUY"
    for source in reversed(candles[max(0,event_idx-5):event_idx]):
        cd="BUY" if source.close>source.open else "SELL" if source.close<source.open else "NEUTRAL"
        if cd==opposite:return (OrderBlock(direction,source.low,source.high,source.open_time,structure.event_time,"FRESH"),)
    return ()
def analyze(candles:tuple[Candle,...],structure:StructureReport)->ConfluenceReport:
    if not candles:return ConfluenceReport()
    trend="AVAILABLE_CONTEXT" if structure.last_swing_high is not None or structure.last_swing_low is not None else "UNKNOWN"; fib=_fibonacci(structure); poc,source=_poc(candles[-120:]); fvg=_fvgs(candles); obs=_order_blocks(candles,structure); available=sum((trend!="UNKNOWN",bool(fib),poc is not None,bool(fvg),bool(obs)))
    return ConfluenceReport(trend,None,fib,poc,source,fvg,obs,available/5.0)
