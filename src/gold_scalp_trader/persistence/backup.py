from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True,slots=True)
class BackupStatus:created_at:datetime; path:str; verified:bool; sha256:str|None=None
