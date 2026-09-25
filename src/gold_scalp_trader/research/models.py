"""ML research metadata; model output has no broker authority."""
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ModelIdentity:
    model_id:str; feature_schema_version:str; data_version:str; code_revision:str; purpose:str
