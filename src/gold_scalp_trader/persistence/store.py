"""Strict transactional SQLite state store. Local state is context, never broker truth."""
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import sqlite3
from typing import Any,Iterator
UTC=timezone.utc; SCHEMA_VERSION=1
class StateStoreError(RuntimeError):pass
class StateIntegrityError(StateStoreError):pass
@dataclass(frozen=True,slots=True)
class StoredRecord:namespace:str; key:str; payload:dict[str,Any]; updated_at:str; checksum:str
class StateStore:
    def __init__(self,path:str|Path=":memory:")->None:
        self.path=str(path); self._conn=sqlite3.connect(self.path,timeout=5.0,isolation_level=None); self._conn.row_factory=sqlite3.Row; self._conn.execute("PRAGMA foreign_keys=ON")
        if self.path != ":memory:":self._conn.execute("PRAGMA journal_mode=WAL"); self._conn.execute("PRAGMA synchronous=FULL")
        self._migrate()
    def _migrate(self)->None:
        self._conn.executescript("CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);CREATE TABLE IF NOT EXISTS records(namespace TEXT NOT NULL,key TEXT NOT NULL,payload TEXT NOT NULL,checksum TEXT NOT NULL,updated_at TEXT NOT NULL,PRIMARY KEY(namespace,key));CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,namespace TEXT NOT NULL,event_key TEXT NOT NULL,payload TEXT NOT NULL,checksum TEXT NOT NULL,created_at TEXT NOT NULL,UNIQUE(namespace,event_key));")
        row=self._conn.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
        if row is None:self._conn.execute("INSERT INTO meta(key,value) VALUES('schema_version',?)",(str(SCHEMA_VERSION),))
        elif int(row[0])!=SCHEMA_VERSION:raise StateIntegrityError("unsupported state schema version")
    @contextmanager
    def transaction(self)->Iterator[sqlite3.Connection]:
        self._conn.execute("BEGIN IMMEDIATE")
        try:yield self._conn; self._conn.execute("COMMIT")
        except Exception:self._conn.execute("ROLLBACK"); raise
    @staticmethod
    def _encode(payload:dict[str,Any])->tuple[str,str]:
        raw=json.dumps(payload,sort_keys=True,separators=(",",":"),allow_nan=False); return raw,hashlib.sha256(raw.encode()).hexdigest()
    def put(self,namespace:str,key:str,payload:dict[str,Any],*,allow_replace:bool=True)->None:
        raw,checksum=self._encode(payload); now=datetime.now(tz=UTC).isoformat(); existing=self._conn.execute("SELECT checksum FROM records WHERE namespace=? AND key=?",(namespace,key)).fetchone()
        if existing is not None and existing[0]==checksum:return
        if existing is not None and not allow_replace:raise StateIntegrityError(f"conflicting record {namespace}/{key}")
        self._conn.execute("INSERT INTO records(namespace,key,payload,checksum,updated_at) VALUES(?,?,?,?,?) ON CONFLICT(namespace,key) DO UPDATE SET payload=excluded.payload,checksum=excluded.checksum,updated_at=excluded.updated_at",(namespace,key,raw,checksum,now))
    def get(self,namespace:str,key:str)->StoredRecord|None:
        row=self._conn.execute("SELECT * FROM records WHERE namespace=? AND key=?",(namespace,key)).fetchone()
        if row is None:return None
        raw=row["payload"]
        if hashlib.sha256(raw.encode()).hexdigest()!=row["checksum"]:raise StateIntegrityError(f"checksum mismatch {namespace}/{key}")
        payload=json.loads(raw)
        if not isinstance(payload,dict):raise StateIntegrityError("record payload must be object")
        return StoredRecord(namespace,key,payload,row["updated_at"],row["checksum"])
    def append_event(self,namespace:str,event_key:str,payload:dict[str,Any])->None:
        raw,checksum=self._encode(payload); now=datetime.now(tz=UTC).isoformat(); row=self._conn.execute("SELECT checksum FROM events WHERE namespace=? AND event_key=?",(namespace,event_key)).fetchone()
        if row is not None:
            if row[0]==checksum:return
            raise StateIntegrityError(f"conflicting event {namespace}/{event_key}")
        self._conn.execute("INSERT INTO events(namespace,event_key,payload,checksum,created_at) VALUES(?,?,?,?,?)",(namespace,event_key,raw,checksum,now))
    def list_records(self,namespace:str)->tuple[StoredRecord,...]:
        keys=[r[0] for r in self._conn.execute("SELECT key FROM records WHERE namespace=? ORDER BY key",(namespace,))]; return tuple(x for k in keys if (x:=self.get(namespace,k)) is not None)
    def delete(self,namespace:str,key:str)->None:self._conn.execute("DELETE FROM records WHERE namespace=? AND key=?",(namespace,key))
    def integrity_check(self)->bool:return self._conn.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    def close(self)->None:self._conn.close()
