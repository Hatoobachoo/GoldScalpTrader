"""Functional chart-view controls. These mutate presentation state only."""
from __future__ import annotations
from dataclasses import dataclass,field
@dataclass
class ChartControlState:
    timeframe:str="M5"; indicators_visible:bool=True; drawings_enabled:bool=False; settings_open:bool=False; overlays:set[str]=field(default_factory=lambda:{"EMA20","EMA50"})
    def set_timeframe(self,value:str)->None:
        if value not in {"M1","M5","M15","H1","H4"}:raise ValueError("unsupported chart timeframe")
        self.timeframe=value
    def toggle_indicators(self)->None:self.indicators_visible=not self.indicators_visible
    def toggle_drawings(self)->None:self.drawings_enabled=not self.drawings_enabled
    def toggle_settings(self)->None:self.settings_open=not self.settings_open
