# GoldScalpTrader — Scoring and Decision Fusion

**Status:** FROZEN V1 FUSION ARCHITECTURE — WEIGHTS/THRESHOLDS CALIBRATION PENDING
**Version:** 1.1-preserved-parallel-floor-manager
**Authority:** Independent BUY/SELL thesis fusion, Red-Team conflict, analytical coverage, correlation, attribution and Floor-Manager output.

## 1. Purpose

Fusion turns six FamilyReports into competing BUY and SELL theses while preserving why each side leads, what opposes it and how much evidence is available.

It never converts soft score into monetary Risk or broker permission.

## 2. Pipeline

```text
six FamilyReports
→ bounded optional confluence
→ BUY Team + SELL Team
→ correlation control
→ Debate / Red Team
→ Floor Manager / DecisionBoard
→ persistent Opportunity
→ completed-M5 Entry Timing
→ analytical DecisionSnapshot
```

Hard Risk/session/news/account/controller/execution authority remains downstream.

## 3. Six-family input

Fusion consumes the preserved production set: Trend Pullback Continuation, Breakout Expansion, Breakout Retest Continuation, Liquidity Sweep Reversal, Failed Breakout Reversal and Compression Expansion.

Exact analytical weights are calibration, not architecture.

## 4. Independent thesis construction

Each directional thesis consumes the same completed family set and preserves leading/supporting families, strengths, lineage, coverage, structural room, session/regime, freshness/cost warnings and timing preference.

Unanimity is not required. One coherent family may lead when others are neutral, subject to downstream timing/geometry/Risk/safety.

## 5. Correlation control

A sweep + reclaim + MSS + failed-break evidence from the same causal event cannot become four independent votes. Correlation/event lineage may cap/reweight synergy while preserving family attribution.

## 6. Optional confluence

Trendline/Fib/POC/FVG/OB may provide bounded support only when compatible with an existing family narrative. Missing optional context does not automatically penalize a valid base case. Opposed/unclear optional context remains visible conflict, not hard BLOCK.

## 7. Red Team

Representative objections include:

```text
STRONG_OPPOSING_THESIS
LOW_EVIDENCE_COVERAGE
LEADING_FAMILY_CONFLICTS
CORRELATED_SUPPORT
ENTRY_EXTENDED
EVENT_STALE_OR_AGING
TARGET_ROOM_WEAK
TRANSACTION_COST_HEAVY
FAILED_ACCEPTANCE
NO_DIRECTIONAL_EDGE
```

These are analytical reasons, not Risk/News/Session/Controller/Execution blockers.

## 8. Coverage / UNKNOWN

Optional missing evidence may be omitted/reweighted where family contract permits. Required financial/broker/safety truth is never a weighted market feature.

UNKNOWN states what is unavailable and whether analysis can remain observational/WAIT or cannot complete.

## 9. Floor Manager versus Entry Timing

Floor Manager asks whether an idea is worth tracking as persistent Opportunity. Entry Timing asks whether the completed-M5 moment is fresh/efficient enough to act.

Strong Opportunity cannot force ENTER when event is stale, move chased, cost burden poor or target room collapsed.

M1 remains diagnostic/research only.

## 10. Analytical action vocabulary

```text
ENTER_BUY
ENTER_SELL
WAIT
MISSED
INVALID
```

`BLOCKED` belongs to downstream hard authorities. Preserve analytical result alongside later blocker for truthful research.

## 11. Cost awareness

Fusion may use descriptive cost/room context. TradePlan owns explicit gross + cost-adjusted geometry; Execution owns final fresh Bid/Ask/spread/drift acceptance. Fusion never shifts stop/target or decides affordability.

## 12. Preserved scheduling semantics

Family reports are designed for bounded dependency-independent workers with immutable common input and deterministic canonical ordering.

A one-worker fallback is mandatory and semantically identical. Physical worker count may be tuned after profiling, but **bounded concurrency itself is a preserved reference capability**, not an optional feature to delete.

Workers have zero lifecycle/Risk/Gate/broker-write authority.

## 13. Persistence / research

Journal Opportunity/Episode, family cases, correlation grouping, Red-Team objections, coverage, timing, cost/freshness context, policy/config/data identity and later hard blocker. Blocked/counterfactual outcomes are not actual P/L.

## 14. Dashboard

Show BUY Thesis, SELL Thesis, Directional Edge, Leading Family, correlation/debate, Opportunity/Episode, Timing, Coverage, Analytical Action and separate hard Permission/blocker.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/strategies/floor.py
src/gold_scalp_trader/strategies/parallel.py
src/gold_scalp_trader/strategies/confluence.py
src/gold_scalp_trader/decisions/fusion.py
src/gold_scalp_trader/decisions/snapshot.py
src/gold_scalp_trader/decisions/opportunity.py
src/gold_scalp_trader/decisions/timing.py
```

## 16. Planned proof / calibration

Tests prove independent BUY/SELL construction, opposition visibility, correlation bounding, optional evidence handling, family attribution, Opportunity handoff, no broker authority and bounded-parallel ↔ one-worker parity.

Weights, synergy caps, conflict penalties, coverage/Opportunity thresholds and cost/freshness penalty magnitudes remain scalp calibration.