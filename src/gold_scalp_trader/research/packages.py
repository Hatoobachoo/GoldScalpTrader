from __future__ import annotations
import json
from pathlib import Path
from .evidence import fingerprint
def write_package(path:str|Path,payload:dict)->Path:
    out=Path(path); wrapper={"fingerprint":fingerprint(payload),"payload":payload}; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(wrapper,indent=2,sort_keys=True),encoding="utf-8"); return out
