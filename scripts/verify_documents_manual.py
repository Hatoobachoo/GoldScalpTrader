from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else ".")/"Documents"
counts={"01-foundation":5,"02-market-intelligence":7,"03-trading-decisions":7,"04-risk-execution":6,"05-research-learning":7,"06-operator":3,"07-engineering":14,"08-governance":8}
errors=[]
for folder,count in counts.items():
    actual=len(list((root/folder).glob("*.md")))
    if actual!=count:errors.append(f"{folder}: expected {count}, got {actual}")
for old in ("00-foundation","10-market-intelligence","20-trading-decisions","30-risk-execution","40-research-learning","50-operator","60-engineering","90-governance"):
    if (root/old).exists():errors.append(f"legacy folder still exists: {old}")
total=len(list(root.rglob("*.md")))
if total!=66:errors.append(f"expected 66 Markdown docs, got {total}")
if errors:print("\n".join(errors)); raise SystemExit(1)
print("Documentation manual PASS: 66 files / 01-08 topology")
