"""Hash-verified full StateStore checkpoint export/restore."""
from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
from .store import StateStore
def export_checkpoint(store:StateStore,path:str|Path,namespaces:tuple[str,...]|None=None)->Path:
    selected=set(namespaces or store.namespaces());records=[{"namespace":r.namespace,"key":r.key,"payload":r.payload,"checksum":r.checksum} for r in store.list_records() if r.namespace in selected];events=[{"namespace":e.namespace,"event_key":e.event_key,"payload":e.payload,"checksum":e.checksum} for e in store.list_events() if e.namespace in selected];body={"schema":1,"created_at":datetime.now(tz=timezone.utc).isoformat(),"records":records,"events":events};canonical=json.dumps(body,sort_keys=True,separators=(",",":"),allow_nan=False);wrapper={"sha256":hashlib.sha256(canonical.encode()).hexdigest(),"body":body};out=Path(path);out.parent.mkdir(parents=True,exist_ok=True);temp=out.with_suffix(out.suffix+".tmp");temp.write_text(json.dumps(wrapper,indent=2,sort_keys=True),encoding="utf-8");temp.replace(out);return out
def restore_checkpoint(path:str|Path,store:StateStore)->None:
    wrapper=json.loads(Path(path).read_text(encoding="utf-8"));body=wrapper["body"];canonical=json.dumps(body,sort_keys=True,separators=(",",":"),allow_nan=False)
    if hashlib.sha256(canonical.encode()).hexdigest()!=wrapper["sha256"]:raise ValueError("checkpoint hash mismatch")
    if body.get("schema")!=1:raise ValueError("unsupported checkpoint schema")
    for item in body.get("records",[]):store.put(item["namespace"],item["key"],item["payload"])
    for item in body.get("events",[]):store.append_event(item["namespace"],item["event_key"],item["payload"])
