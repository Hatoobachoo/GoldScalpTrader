from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
from .store import StateStore
def export_checkpoint(store:StateStore,path:str|Path,namespaces:tuple[str,...])->Path:
    out=Path(path); records=[]
    for ns in namespaces:
        for r in store.list_records(ns):records.append({"namespace":ns,"key":r.key,"payload":r.payload,"checksum":r.checksum})
    body={"schema":1,"created_at":datetime.now(tz=timezone.utc).isoformat(),"records":records}; canonical=json.dumps(body,sort_keys=True,separators=(",",":"),allow_nan=False); wrapper={"sha256":hashlib.sha256(canonical.encode()).hexdigest(),"body":body}
    out.parent.mkdir(parents=True,exist_ok=True); temp=out.with_suffix(out.suffix+".tmp"); temp.write_text(json.dumps(wrapper,indent=2,sort_keys=True),encoding="utf-8"); temp.replace(out); return out
def restore_checkpoint(path:str|Path,store:StateStore)->None:
    wrapper=json.loads(Path(path).read_text(encoding="utf-8")); body=wrapper["body"]; canonical=json.dumps(body,sort_keys=True,separators=(",",":"),allow_nan=False)
    if hashlib.sha256(canonical.encode()).hexdigest()!=wrapper["sha256"]:raise ValueError("checkpoint hash mismatch")
    for item in body["records"]:store.put(item["namespace"],item["key"],item["payload"])
