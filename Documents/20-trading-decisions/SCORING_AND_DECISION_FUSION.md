# GoldScalpTrader — Scoring and Decision Fusion

**Status:** DRAFT PRE-CHALLENGE TOPIC CONTRACT
**Version:** 0.1-scalp-floor-manager
**Authority:** Independent BUY/SELL thesis fusion, Debate/Red-Team conflict, analytical coverage, correlation, attribution and Floor-Manager output.

## 1. Purpose

Fusion turns separate FamilyReports into two competing directional theses while preserving why each side leads, what opposes it and how much evidence is available.

It never converts a soft score into monetary risk or broker permission.

> BUY and SELL are separate teams. Opposition is visible conflict, not hidden inside one confidence number.

## 2. Pipeline

```text
six FamilyReports
→ bounded optional confluence
→ BUY Team
→ SELL Team
→ Debate / Red Team
→ Floor Manager / DecisionBoard
→ persistent Opportunity
→ Entry Timing
→ analytical DecisionSnapshot
```

Hard risk/session/account/controller/execution authorities remain separate and downstream.

## 3. Independent thesis construction

Each directional thesis consumes the same family reports independently.

The reference weighted-top-family model is retained as a design candidate, but exact percentages are not frozen for the scalper.

The thesis must preserve:

- leading family and supporting families;
- family case strengths;
- evidence names/lineage;
- coverage;
- structural target/room context;
- session/regime context;
- transaction-cost/freshness warnings;
- preferred timing profile.

Unanimity is not required. One strong coherent family may lead when other families are neutral.

## 4. Correlation control

Correlation control is mandatory because scalp evidence is dense and many labels can describe one five-minute episode.

Fusion must distinguish:

```text
independent support
correlated support
ordinary disagreement
material opposing thesis
```

A sweep + rejection + MSS + failed-break label from one event cannot be treated as four independent votes.

## 5. Optional confluence

Optional Trendline/Fib/POC/FVG/OB support may provide a bounded uplift only where the owning strategy narrative already exists.

Missing optional context leaves the base case unchanged. Opposed optional context remains visible to the Red Team but does not automatically become hard BLOCK.

## 6. Debate / Red Team

The Red Team challenges the leading thesis without requiring perfection.

Draft objection classes include:

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

These are analytical objections. They cannot impersonate Risk, Session/News, Controller or Execution blockers.

## 7. Coverage and UNKNOWN

Coverage describes availability of expected analytical evidence.

Optional missing evidence may be omitted/reweighted where the family contract allows. Required financial/broker/safety truth is not a weighted market feature.

UNKNOWN must state what is unknown and whether the analytical result can remain observational, WAIT, or cannot be completed.

## 8. Floor Manager versus Entry Timing

Floor Manager asks:

> Is this market idea worth tracking as a qualified scalp Opportunity?

Entry Timing asks:

> Is this specific M5 moment efficient and fresh enough to act?

A strong Opportunity cannot force ENTER when current price is extended, event lineage is stale, spread is poor, or the clean room has disappeared.

## 9. Analytical actions

The analytical decision vocabulary is:

```text
ENTER_BUY
ENTER_SELL
WAIT
MISSED
INVALID
```

`BLOCKED` belongs to downstream hard authorities, not to analytical scoring.

The runtime/dashboard must preserve the original analytical result even when later risk/safety blocks execution so research can distinguish a weak strategy from a safely blocked good idea.

## 10. Scalp score interpretation

Human-readable bands may describe:

```text
NO_EDGE
WATCH
ARMABLE
STRONG
EXCEPTIONAL
```

Exact thresholds remain research/calibration.

No analytical score may:

- increase monetary risk;
- rescue structurally poor Trade Plan geometry;
- lower the spread/slippage safety standard;
- bypass news/session/account/controller rules;
- change original R;
- call MT5.

## 11. Transaction-cost awareness

Fusion may consume descriptive cost context from current market facts/Technical reports, such as spread relative to ATR or target room.

This is used to identify poor analytical efficiency early. Final executable spread/drift/slippage acceptance remains owned downstream.

## 12. Persistence and research

Decision/family evidence should be journaled with:

- Opportunity/Episode identity;
- family/BUY/SELL cases;
- Red-Team objections;
- coverage;
- timing result;
- current cost/freshness context;
- policy/config/code/data identity;
- later hard blocker if any.

Blocked/counterfactual outcomes are not executed P/L.

## 13. Dashboard

Show separately:

```text
BUY Thesis
SELL Thesis
Directional Edge
Leading Family
Debate / Red Team
Opportunity / Episode
Entry Timing
Coverage
Analytical Action
Hard Permission / blocker
```

No optional confluence should be presented as a mandatory checkbox unless the final family contract explicitly says so.

## 14. Planned implementation ownership

```text
src/gold_scalp_trader/strategies/floor.py
src/gold_scalp_trader/strategies/parallel.py
src/gold_scalp_trader/strategies/confluence.py
src/gold_scalp_trader/decisions/fusion.py
src/gold_scalp_trader/decisions/snapshot.py
src/gold_scalp_trader/decisions/opportunity.py
src/gold_scalp_trader/decisions/timing.py
```

## 15. Planned proof

Tests must prove independent BUY/SELL construction, visible strong opposition, bounded correlation/synergy, optional-evidence handling, stable family attribution, Opportunity handoff, no broker authority and serial/parallel family parity.

## 16. Pre-challenge calibration

Open questions: thesis weights, synergy cap, conflict penalty, coverage threshold, Opportunity threshold, cost/freshness penalty semantics, Red-Team thresholds, and combinations that best balance opportunity recall, transaction-cost-adjusted expectancy, drawdown and healthy trade frequency.
