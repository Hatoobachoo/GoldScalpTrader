"""Soft trading-session context; broker market state is owned elsewhere."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

@dataclass(frozen=True, slots=True)
class SessionReport:
    label: str; london_open: bool; new_york_open: bool; overlap: bool

def classify(as_of_utc: datetime) -> SessionReport:
    if as_of_utc.tzinfo is None: raise ValueError("as_of_utc must be timezone-aware")
    london=as_of_utc.astimezone(ZoneInfo("Europe/London")); new_york=as_of_utc.astimezone(ZoneInfo("America/New_York"))
    lo=8<=london.hour<17; ny=8<=new_york.hour<17
    label="LONDON_NY_OVERLAP" if lo and ny else "LONDON" if lo else "NEW_YORK" if ny else "ASIA_OR_OFF_HOURS"
    return SessionReport(label,lo,ny,lo and ny)
