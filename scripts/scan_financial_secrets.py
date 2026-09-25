from __future__ import annotations
from pathlib import Path
import sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else ".")
sys.path.insert(0,str(ROOT/"src"))
from gold_scalp_trader.security.financial_secrets import contains_probable_secret
SKIP={".git","__pycache__",".pytest_cache",".venv","venv"}
found=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or any(x in p.parts for x in SKIP) or p.name=="scan_financial_secrets.py":continue
    try:text=p.read_text(encoding="utf-8")
    except Exception:continue
    if contains_probable_secret(text):found.append(str(p))
if found:print("Potential secrets detected in:"); print("\n".join(found)); raise SystemExit(1)
print("Secret scan PASS")
