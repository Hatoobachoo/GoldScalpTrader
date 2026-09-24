# GoldScalpTrader — Audit 2 Documents → Code → Tests/Evidence Compliance

**Status:** DRAFT AUDIT PROTOCOL — NOT RUN
**Version:** 0.1-doc-code-test-compliance
**Authority:** Compliance between canonical `Documents/`, actual source, deterministic tests and explicit external/calibration evidence boundaries.

## 1. Audit question

> Does current canonical `Documents/` meaning match the code that actually runs, and is each behaviour covered by deterministic proof or explicitly classified as external/calibration evidence?

## 2. PASS is narrow

A Documents→Code→Tests PASS means only the synchronized revision satisfies its deterministic software contracts.

It does not prove:

- MT5 connectivity;
- real broker schedule/permissions;
- real fills/slippage/latency;
- strategy edge/profitability;
- fresh-machine continuity.

## 3. Traceability matrix

For each canonical topic/feature record:

```text
Document owner
Behaviour/invariant
Implementation owner
Runtime entry path
Focused tests
Negative/UNKNOWN tests
Persistence/recovery impact
Operator presentation
Research/evidence impact
External/calibration requirement
Verdict
```

## 4. Critical compliance paths

Audit at minimum:

- one MT5 read boundary;
- immutable MarketSnapshot;
- causal completed-candle intelligence;
- final timeframe roles;
- bounded parallelism/serial parity;
- strategy families/Fusion/Opportunity/Timing;
- family-aware TradePlan;
- final R/cost-room policy;
- monetary Risk/min-lot;
- session/news state policy;
- Gate/Intent/sole writer/reconciliation;
- controller/fencing;
- management/close recovery;
- StateStore/checkpoint/local backup;
- actual learning/research/promotion boundaries;
- dashboard blocker/Gate truth;
- secret handling;
- explicit absence of runtime Git auto-push.

## 5. Contradiction handling

If Documents, code and tests disagree, do not select the most convenient version.

Classify:

```text
DOCUMENT DEFECT
CODE DEFECT
TEST DEFECT
IMPLEMENTATION GAP
EVIDENCE GAP
CALIBRATION GAP
EXTERNAL PROOF GAP
```

Repair through an affected-graph change packet.

## 6. Source/test inventory check

Compare actual tree against `MODULE_STRUCTURE.md` and `FILE_AND_TEST_CATALOG.md`.

No source/test may silently own behaviour absent from canonical docs; no canonical owner may claim implemented proof from a nonexistent file/test.

## 7. Evidence classification

Every claim is marked as one or more:

```text
DETERMINISTIC SOFTWARE PROOF
REPLAY/RESEARCH EVIDENCE
CONNECTED READ-ONLY PROOF
CONNECTED DEMO PROOF
LOCAL RECOVERY PROOF
CALIBRATION PENDING
EXTERNAL PROOF PENDING
```

## 8. Current state

```text
AUDIT RESULT: NOT RUN
Reason: implementation has not yet been rebuilt from the challenged/frozen canonical manual.
```
