from __future__ import annotations
from dataclasses import asdict,is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from .store import StateStore
def _jsonable(value:Any)->Any:
    if isinstance(value,Enum):return value.value
    if isinstance(value,datetime):return value.isoformat()
    if is_dataclass(value):return {k:_jsonable(v) for k,v in asdict(value).items()}
    if isinstance(value,dict):return {str(k):_jsonable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [_jsonable(v) for v in value]
    return value
def save_runtime_object(store:StateStore,namespace:str,key:str,value:Any)->None:
    payload=_jsonable(value); store.put(namespace,key,payload if isinstance(payload,dict) else {"value":payload})
