from __future__ import annotations
import hashlib,json
def fingerprint(payload:dict)->str:return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
