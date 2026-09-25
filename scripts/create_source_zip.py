from __future__ import annotations
from pathlib import Path
import sys,zipfile
root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve(); out=Path(sys.argv[2] if len(sys.argv)>2 else root.parent/(root.name+"_source.zip")).resolve()
SKIP_DIRS={".git",".venv","venv","__pycache__",".pytest_cache"}; SKIP_NAMES={".env"}; SKIP_SUFFIXES={".db",".sqlite",".sqlite3",".wal",".shm"}
with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob("*"):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(root).parts) or p.name in SKIP_NAMES or p.suffix.lower() in SKIP_SUFFIXES:continue
        z.write(p,p.relative_to(root))
print(out)
