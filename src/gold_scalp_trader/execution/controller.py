from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone
from gold_scalp_trader.persistence.store import StateStore
NS="controller"
@dataclass(frozen=True,slots=True)
class ControllerLease:
    scope:str; holder:str; epoch:int; expires_at:datetime
    def valid(self,as_of:datetime)->bool:return as_of<self.expires_at
def acquire(store:StateStore,scope:str,holder:str,as_of:datetime|None=None,ttl_seconds:int=30)->ControllerLease:
    now=as_of or datetime.now(tz=timezone.utc); rec=store.get(NS,scope); epoch=1
    if rec is not None:
        old=rec.payload; expires=datetime.fromisoformat(old["expires_at"])
        if expires>now and old["holder"]!=holder:raise RuntimeError("controller lease already held")
        epoch=int(old["epoch"])+(0 if old["holder"]==holder and expires>now else 1)
    lease=ControllerLease(scope,holder,epoch,now+timedelta(seconds=ttl_seconds)); store.put(NS,scope,{"scope":scope,"holder":holder,"epoch":epoch,"expires_at":lease.expires_at.isoformat()}); return lease
def verify(store:StateStore,lease:ControllerLease,as_of:datetime|None=None)->bool:
    now=as_of or datetime.now(tz=timezone.utc); rec=store.get(NS,lease.scope); return rec is not None and rec.payload["holder"]==lease.holder and int(rec.payload["epoch"])==lease.epoch and datetime.fromisoformat(rec.payload["expires_at"])>now
