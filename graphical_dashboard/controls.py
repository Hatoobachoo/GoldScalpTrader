"""Functional presentation-only chart controls; no trading authority."""
from dataclasses import dataclass,field
@dataclass
class ChartControlState:
    timeframe:str="M5";indicators_visible:bool=True;drawings_enabled:bool=False;settings_open:bool=False;overlays:set[str]=field(default_factory=lambda:{"EMA20","EMA50"});horizontal_drawings:list[float]=field(default_factory=list);candle_limit:int=80
    def set_timeframe(self,value:str)->None:
        if value not in {"M1","M5","M15","H1","H4"}:raise ValueError("unsupported chart timeframe")
        self.timeframe=value
    def toggle_indicators(self)->None:self.indicators_visible=not self.indicators_visible
    def toggle_drawings(self)->None:self.drawings_enabled=not self.drawings_enabled
    def toggle_settings(self)->None:self.settings_open=not self.settings_open
    def toggle_overlay(self,name:str)->None:self.overlays.remove(name) if name in self.overlays else self.overlays.add(name)
    def add_horizontal_drawing(self,price:float)->None:self.horizontal_drawings.append(float(price))
    def clear_drawings(self)->None:self.horizontal_drawings.clear()
    def set_candle_limit(self,value:int)->None:
        if value<20 or value>300:raise ValueError("candle_limit must be between 20 and 300")
        self.candle_limit=value
