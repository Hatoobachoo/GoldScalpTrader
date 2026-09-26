# Connected DEMO Evidence and Learning Visibility — As-Built Guide

**Status:** IMPLEMENTED READ-ONLY CERTIFICATION TOOLING / CONNECTED BROKER PROOF STILL EXTERNAL  
**Authority:** Describes how connected DEMO evidence observes Session, execution lifecycle, Timing Intelligence, management evidence, shadow evidence and actual learning without gaining trading authority.

## 1. Safety boundary

The connected evidence tools are observers only.

```text
MT5/account/symbol reads
+ local durable StateStore reads
+ scoped operator drill artifacts
→ certification report
```

They never call the raw MT5 writer, never create an ExecutionIntent, never alter Risk/Gate/Session authority, and never enable REAL.

## 2. Main files

```text
scripts/certify_connected_demo.py
scripts/monitor_connected_demo.py
scripts/report_demo_learning_evidence.py
src/gold_scalp_trader/diagnostics/connected_demo.py
src/gold_scalp_trader/diagnostics/connected_runtime_evidence.py
src/gold_scalp_trader/app/session_authority.py
src/gold_scalp_trader/research/timing_learning.py
src/gold_scalp_trader/research/runtime_evidence.py
```

## 3. Hard Session visibility

`certify_connected_demo.py` reads the same scoped hard Session authority used by the governed DEMO runtime through `app/session_authority.py`.

The report preserves:

- `OPEN / PRE_CLOSE / CLOSED / UNKNOWN`;
- source;
- `schedule_verified`;
- broker tradeability fact;
- reason;
- validity window;
- next close and close kind;
- unresolved gap/reconciliation state;
- hard new-entry permission.

The monitor prints Session separately from quote freshness, so a stale quote is never presented as proof that the market is closed.

## 4. Runtime learning evidence visibility

`diagnostics/connected_runtime_evidence.py` summarizes three durable research-only streams:

```text
timing_decision_evidence
management_decision_evidence
shadow_strategy_evidence
```

The connected report includes:

- total Timing Intelligence samples;
- timing samples associated with an observed broker-write cycle;
- management-decision samples;
- shadow-family samples;
- qualified shadow samples.

The standalone DEMO learning report shows the same counts together with actual StrategyMemory observations and execution lifecycle evidence.

## 5. No false connected PASS

Durable local samples improve observability but do **not** automatically certify canonical Phase-15 drills.

In particular:

```text
m1_refinement_timing
shadow_learning_report
broker_schedule_preclose_dst_holiday
latency_distribution
spread_slippage_deviation_distribution
```

remain pending until the required connected/artifact-backed evidence is actually produced.

## 6. Certification hierarchy

```text
connected DEMO identity
→ SymbolSpec / quote / Session observation
→ durable OPEN/MODIFY/CLOSE evidence
→ actual verified-close learning
→ Timing / management / shadow evidence visibility
→ explicit connected/manual drill evidence
→ full Phase-15 certification
```

Offline tests and local StateStore records cannot replace real Exness behavior where broker proof is required.

## 7. Tests

```text
tests/test_connected_demo_evidence.py
tests/test_connected_runtime_evidence.py
tests/test_connected_reporting_wiring.py
```

The tests verify read-only aggregation, scope safety, Session normalization, runtime research counts, and that the certifier/monitor/reporter remain wired to the new evidence streams.

## 8. REAL boundary

REAL remains hard-disabled. Nothing in connected evidence tooling is an enablement path for REAL or for automatic candidate promotion.
