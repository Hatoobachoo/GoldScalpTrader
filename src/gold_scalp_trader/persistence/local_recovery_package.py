from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RecoveryPackage:checkpoint_path:str; source_revision:str|None; secret_scan_passed:bool
