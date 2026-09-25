from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DatasetIdentity:source:str; symbol:str; version:str; sha256:str
