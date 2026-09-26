# GoldScalpTrader — Audit 2: Document → Code → Test Compliance

**Status:** OFFLINE BASELINE PASS / CONNECTED-EVIDENCE VISIBILITY EXTENSION REVALIDATION REQUIRED  
**Version:** 2.3-implementation-trace  
**Authority:** Traceability from canonical contract to actual source owner to deterministic/integration evidence, with connected DEMO facts explicitly separated.

## 1. Evidence rule

```text
canonical contract
→ source owner
→ deterministic/integration proof
→ connected proof where broker reality is required
→ operator truth
```

A lower evidence layer cannot substitute for a higher one. Offline tests do not prove Exness broker behavior.

## 2. Last validated baseline

The operator-provided Windows run at commit `417ea2c` reported:

```text
compileall     PASS
documents      PASS
contract-sync  PASS
secrets        PASS
pytest         PASS
OFFLINE STATUS: PASS
```

Subsequent connected-evidence visibility changes must be re-run through the same verifier before inheriting that PASS.

## 3. High-risk trace status

| Requirement | Implementation owner | Offline status |
|---|---|---|
| normalized MT5 reads | `market_data/mt5_reader.py` | COMPLIANT; connected facts external |
| market-first setup | setup detector/isolation | COMPLIANT |
| independent BUY/SELL + Red Team | decision fusion/cycle | COMPLIANT |
| persistent M5 Opportunity | `app/opportunity_lifecycle.py` | COMPLIANT |
| M1 subordinate timing | decisions/timing + runtime | COMPLIANT |
| timing lineage into learning | runtime core + ManagedTrade + learning | COMPLIANT |
| preserved Risk profiles/ceilings | config/risk | COMPLIANT |
| daily lock/cooldown persistence | risk state/runtime | COMPLIANT |
| Session OPEN/PRE_CLOSE/CLOSED/UNKNOWN | session provider/authority/runtime | COMPLIANT offline; schedule external |
| News soft only | News/session boundary | COMPLIANT |
| Gate/persist-before-send/one-shot | execution + runtime core | COMPLIANT offline |
| sole raw writer | `execution/mt5_writer.py` | COMPLIANT |
| ambiguous ACK reconciliation | execution/reconcile | COMPLIANT offline; real drill external |
| ManagedTrade/verified close | management/runtime core | COMPLIANT offline |
| exactly-once actual learning | live learning | COMPLIANT offline |
| management/shadow evidence | `research/runtime_evidence.py` | COMPLIANT offline |
| autonomous candidate governance | invention/promotion/candidate registry | COMPLIANT offline |
| graphical dashboard read-only | operator/graphical runner/UI | COMPLIANT offline |
| local recovery/checkpoint | persistence/recovery | COMPLIANT offline; connected handoff external |
| REAL disabled | config/startup/runtime layers | HARD DISABLED |

## 4. Connected evidence visibility extension

The connected evidence stack now includes:

```text
diagnostics/connected_runtime_evidence.py
scripts/certify_connected_demo.py
scripts/monitor_connected_demo.py
scripts/report_demo_learning_evidence.py

tests/test_connected_runtime_evidence.py
tests/test_connected_reporting_wiring.py
```

The certifier observes and reports:

- hard Session state/source/schedule verification/tradeability/reason;
- Timing Intelligence evidence count;
- Timing samples associated with a broker-write cycle;
- management evidence count;
- shadow-family evidence count;
- qualified shadow count;
- existing Intent/ManagedTrade/close/actual-learning evidence.

The monitor prints Session separately from quote age and prints runtime-research counts. A stale quote is therefore not used as a market-hours proxy.

These local durable counts are observability evidence only. They do not automatically PASS `m1_refinement_timing`, `shadow_learning_report`, broker schedule, latency or spread/slippage/deviation drills.

## 5. Execution and safety boundary

Irreversible flow remains:

```text
Gate
→ durable Intent
→ fresh prechecks/order_check
→ SUBMITTING persisted
→ sole MT5Writer send
→ ack classification
→ reconciliation
```

Connected certification/monitor/report tooling remains read-only and cannot enable REAL.

## 6. Learning / autonomous governance

```text
verified full close
→ durable learning queue
→ immutable source validation
→ StrategyMemory save
→ consume queue only after durable save
```

Timing/management/shadow evidence feeds governed research. Candidate stage progression remains separate from live deployment; research/candidate evidence cannot self-activate runtime policy or mutate Risk/Gate.

## 7. Connected proof still required

The following remain external until actually observed on the intended Windows + Exness DEMO scope:

- real SymbolSpec/filling/stops/freeze/margin/order-check behavior;
- current broker schedule/PRE_CLOSE/DST/holiday/maintenance;
- controlled OPEN/MODIFY/PROTECT/TRAIL/CLOSE;
- broker-side TP/SL visibility;
- manual known-trade close attribution;
- ambiguous acknowledgement/no duplicate;
- restart during active lifecycle;
- spread/slippage/deviation and latency distributions;
- 3-loss/cooldown persistence under actual closed deals;
- connected M1 timing and active/shadow learning evidence;
- fresh-machine restore and sequential handoff;
- intended Windows graphical review.

## 8. Verdict discipline

Until the post-change verifier is rerun:

```text
LAST VALIDATED OFFLINE BASELINE             PASS
CURRENT CONNECTED-EVIDENCE EXTENSION        REVALIDATION REQUIRED
CONNECTED EXNESS FACTS                      PENDING
FULL CONNECTED DEMO CERTIFICATION            PENDING
FUTURE REAL RELEASE                         HARD DISABLED
```

No profitability claim is made.
