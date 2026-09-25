from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PathOutcome:
    mfe_r:float|None; mae_r:float|None; realized_r:float|None
