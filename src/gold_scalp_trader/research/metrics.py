from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ResearchMetrics:
    trades:int; net_r:float; wins:int; losses:int; missed:int=0; blocked:int=0
    @property
    def win_rate(self)->float|None:return None if self.trades==0 else self.wins/self.trades
    @property
    def average_r(self)->float|None:return None if self.trades==0 else self.net_r/self.trades
