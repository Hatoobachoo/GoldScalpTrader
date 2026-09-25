"""Read-only DEMO learning/evidence report from the local StateStore.

This script never connects to MT5 and never performs a broker action. It reports
what durable DEMO evidence actually exists so Phase 15 claims remain honest.
"""
from __future__ import annotations

from collections import Counter
import os
from pathlib import Path

from gold_scalp_trader.execution.intent_store import NS as INTENT_NS, unresolved
from gold_scalp_trader.management.store import NS as MANAGED_TRADE_NS
from gold_scalp_trader.persistence.store import StateStore, StateStoreError
from gold_scalp_trader.research.episode_journal import NS as EPISODE_NS
from gold_scalp_trader.research.learning import NS as LEARNING_NS


def _fmt(value: object) -> str:
    return "—" if value is None else str(value)


def main() -> int:
    db_path = Path(os.getenv("STATE_DB_PATH", "runtime/gold_scalp_demo.sqlite3"))
    print("GoldScalpTrader — DEMO durable evidence report")
    print(f"State DB: {db_path}")
    if not db_path.is_file():
        print("STATUS: NO DURABLE DEMO DATABASE FOUND")
        print("Run the governed DEMO runtime first; no evidence is invented.")
        return 2

    try:
        store = StateStore(db_path)
    except StateStoreError as exc:
        print(f"STATUS: STATESTORE ERROR: {exc}")
        return 1

    try:
        integrity = store.integrity_check()
        intents = store.list_records(INTENT_NS)
        learning = store.list_records(LEARNING_NS)
        episodes = store.list_events(EPISODE_NS)
        managed = store.list_records(MANAGED_TRADE_NS)
        unresolved_intents = unresolved(store)

        intent_states = Counter(str(r.payload.get("state", "UNKNOWN")) for r in intents)
        intent_actions = Counter(str(r.payload.get("action", "UNKNOWN")) for r in intents)
        episode_classes = Counter(str(e.payload.get("evidence_class", "UNKNOWN")) for e in episodes)
        families = Counter(str(r.payload.get("family", "UNKNOWN")) for r in learning)

        realized = [float(r.payload["realized_r"]) for r in learning if r.payload.get("realized_r") is not None]
        entry_eff = [float(r.payload["entry_efficiency"]) for r in learning if r.payload.get("entry_efficiency") is not None]
        capture_eff = [float(r.payload["capture_efficiency"]) for r in learning if r.payload.get("capture_efficiency") is not None]

        print(f"StateStore integrity: {'PASS' if integrity else 'FAIL'}")
        print(f"Namespaces: {', '.join(store.namespaces()) or 'none'}")
        print(f"Execution Intents: {len(intents)}")
        print(f"  by action: {dict(intent_actions)}")
        print(f"  by state:  {dict(intent_states)}")
        print(f"  unresolved SUBMITTING/ACCEPTED_UNKNOWN: {len(unresolved_intents)}")
        print(f"Current ManagedTrade records: {len(managed)}")
        print(f"StrategyMemory actual observations: {len(learning)}")
        print(f"  by family: {dict(families)}")
        print(f"Research episodes: {len(episodes)}")
        print(f"  by evidence class: {dict(episode_classes)}")

        if realized:
            print(f"Observed realized R: count={len(realized)} avg={sum(realized)/len(realized):.4f} net={sum(realized):.4f}")
        else:
            print("Observed realized R: —")
        if entry_eff:
            print(f"Entry Efficiency avg: {sum(entry_eff)/len(entry_eff):.4f}")
        else:
            print("Entry Efficiency avg: —")
        if capture_eff:
            print(f"Capture Efficiency avg: {sum(capture_eff)/len(capture_eff):.4f}")
        else:
            print("Capture Efficiency avg: —")

        has_open = any(str(r.payload.get("action")) == "OPEN" and str(r.payload.get("state")) == "ACCEPTED_VERIFIED" for r in intents)
        has_modify = any(str(r.payload.get("action")) == "MODIFY" and str(r.payload.get("state")) == "ACCEPTED_VERIFIED" for r in intents)
        has_close = any(str(r.payload.get("action")) == "CLOSE" and str(r.payload.get("state")) == "ACCEPTED_VERIFIED" for r in intents)
        print("\nPHASE 15 EVIDENCE SNAPSHOT")
        print(f"  verified OPEN evidence:   {'YES' if has_open else 'NO'}")
        print(f"  verified MODIFY evidence: {'YES' if has_modify else 'NO'}")
        print(f"  verified CLOSE evidence:  {'YES' if has_close else 'NO'}")
        print(f"  actual learning evidence: {'YES' if learning else 'NO'}")
        print(f"  unresolved intent safety: {'CLEAR' if not unresolved_intents else 'RECONCILIATION REQUIRED'}")

        if not integrity:
            print("STATUS: FAIL — StateStore integrity check failed")
            return 1
        print("STATUS: REPORT COMPLETE")
        print("NOTE: absence of an item means NOT YET PROVEN, not FAIL by itself.")
        print("NOTE: broker schedule, slippage, latency, manual-close and fresh-machine drills still require connected evidence.")
        return 0
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(main())
