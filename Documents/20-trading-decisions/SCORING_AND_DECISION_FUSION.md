# GoldScalpTrader — Scoring and Decision Fusion

**Status:** FROZEN V1 FUSION ARCHITECTURE — WEIGHTS/THRESHOLDS CALIBRATION PENDING
**Version:** 1.0-six-family-floor-manager
**Authority:** Independent BUY/SELL thesis fusion, Red-Team conflict, analytical coverage, correlation, attribution and Floor-Manager output.

## 1. Purpose

Fusion turns six FamilyReports into competing BUY and SELL theses while preserving why each side leads, what opposes it and how much evidence is available.

It never converts soft score into monetary Risk or broker permission.

> BUY and SELL are separate teams. Opposition remains visible conflict.

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

Fusion consumes the frozen V1 family set:

- Trend Pullback Continuation;
- Breakout Expansion;
- Breakout Retest Continuation;
- Liquidity Sweep Reversal;
- Failed Breakout Reversal;
- Compression Expansion.

Exact weights are calibration, not architecture.

## 4. Independent thesis construction

Each directional thesis consumes the same completed family set independently and preserves leading/supporting families, case strengths, evidence lineage, coverage, structural room, session/regime, freshness/cost warnings and timing preference.

Unanimity is not required. One coherent family can lead when others are neutral, subject to downstream timing/geometry/Risk/safety.

## 5. Correlation control

Fusion must distinguish independent support from correlated labels describing one causal episode.

A sweep + reclaim + MSS + failed-break evidence from the same event cannot become four independent votes merely because four labels exist.

Correlation/event lineage may cap/reweight synergy while preserving family attribution.

## 6. Optional confluence

Trendline/Fib/POC/FVG/OB may provide bounded support only when compatible with an existing family narrative.

Missing optional context leaves base case unchanged. Opposed/unclear optional context is visible conflict, not automatic hard BLOCK.

## 7. Red Team

Representative objections:

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

These remain analytical reasons. They cannot impersonate Risk, News/Session, Controller or Execution blockers.

## 8. Coverage / UNKNOWN

Coverage describes expected analytical evidence availability. Optional missing evidence may be omitted/reweighted where family contract permits.

Required financial/broker/safety truth is not a weighted market feature.

UNKNOWN states exactly what is unavailable and whether analysis can remain observational/WAIT or cannot complete.

## 9. Floor Manager versus Entry Timing

Floor Manager:

> Is this market idea worth tracking as a persistent Opportunity?

Entry Timing:

> Is this completed-M5 moment fresh/efficient enough to act?

A strong Opportunity cannot force ENTER when event is stale, move is chased, spread/cost burden is poor or target room has collapsed.

M1 is diagnostic/research only and cannot create independent V1 ENTER authority.

## 10. Analytical action vocabulary

```text
ENTER_BUY
ENTER_SELL
WAIT
MISSED
INVALID
```

`BLOCKED` is supplied by downstream hard authorities. Runtime preserves analytical result alongside later blocker so research can distinguish poor strategy from safe rejection.

## 11. Cost awareness

Fusion may use descriptive cost/room context to recognize analytically inefficient setups early.

TradePlan owns explicit gross + cost-adjusted geometry. Execution owns final fresh Bid/Ask/spread/drift acceptance. Fusion never shifts stop/target or decides monetary affordability.

## 12. Scheduling

Family reports may be computed serially or with bounded workers. Physical concurrency is optional/profiling-driven; canonical ordering and one-worker semantic parity are mandatory.

## 13. Persistence / research

Journal Opportunity/Episode, family cases, correlation grouping, Red-Team objections, coverage, timing, current cost/freshness context, policy/config/data identity and later hard blocker.

Blocked/counterfactual outcomes are not actual P/L.

## 14. Dashboard

Show BUY Thesis, SELL Thesis, Directional Edge, Leading Family, correlation/debate, Opportunity/Episode, Timing, Coverage, Analytical Action and separate Hard Permission/blocker.

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

Tests prove independent BUY/SELL construction, strong opposition visibility, bounded correlation, optional evidence handling, family attribution, Opportunity handoff, no broker authority and serial/parallel parity.

Weights, synergy cap, conflict penalties, coverage/Opportunity thresholds and cost/freshness penalty magnitudes remain calibration pending.