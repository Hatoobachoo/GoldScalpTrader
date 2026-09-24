# GoldScalpTrader — Audit 7: Individual Component Review

**Status:** DRAFT AUDIT PROTOCOL — NOT RUN
**Version:** 0.1-scalp-component-by-component
**Authority:** Individual review of every material production/research/operator component rather than assuming one central subsystem explains overall behaviour.

## 1. Scope

Review every meaningful component in the production path independently:

```text
MarketSnapshot
→ Indicators
→ Candle Structure / BOS / MSS
→ Technical levels / location / room
→ Liquidity / FVG / Order Blocks
→ Session / News context
→ independent strategy families
→ BUY/SELL fusion + Red Team
→ Opportunity lifecycle
→ Entry Timing / event freshness
→ TradePlan invalidation / targets / cost context
→ executable-price geometry
→ monetary Risk / min lot / margin
→ session/news/system permissions
→ central Gate
→ ExecutionIntent
→ fresh broker prechecks
→ sole writer
→ reconciliation
→ ManagedTrade / Trade Manager
→ verified close recovery
→ learning queue/receipt/StrategyMemory
→ local backup/recovery
→ operator presentation
```

Research/discovery/promotion gets a parallel component traversal.

## 2. Per-component worksheet

For each component record:

```text
Name
Canonical contract
Purpose
Inputs
Outputs/state
Authority it owns
Authority explicitly forbidden
Freshness/chronology semantics
Failure/UNKNOWN semantics
Persistence/restart semantics
Implementation files
Focused tests
Integration tests
Operator visibility
Research evidence
External/calibration proof
Verdict
Defect/action
```

## 3. Required review principles

- Do not assume a central Gate problem when candidate never reached Gate.
- Do not assume “no trades” means strategy is too strict.
- Do not assume “many trades” means good Opportunity Recall.
- Do not conflate broker affordability with strategy quality.
- Do not conflate UI labels with owning authority.
- Do not count correlated evidence multiple times.
- Do not accept stale events/levels merely because original thesis was strong.
- Do not copy Swing thresholds without scalp evidence.
- Do not let a test fixture bypass the production safety path.

## 4. Scalp-specific component questions

Check explicitly:

- target room after spread/slippage assumptions;
- event/trigger age;
- signal-to-submit drift;
- M5/M1 role adherence;
- min-lot actual risk;
- time-in-trade/efficiency management;
- family-specific invalidation;
- News/dislocation exposure;
- latency observability;
- local backup/recovery independence from GitHub.

## 5. Classification

Per component:

```text
PASS
PASS WITH CALIBRATION PENDING
DEFECT
DESIGN CHANGE REQUIRED
EXTERNAL PROOF PENDING
NOT IMPLEMENTED
NOT RUN
```

A neighboring component's PASS cannot grant this component PASS.

## 6. Final traversal output

The final audit should identify:

- components genuinely correct;
- implementation defects;
- document/code/test mismatches;
- over/under restrictive calibration;
- presentation-only issues;
- external evidence gaps;
- unresolved ownership duplication;
- dead/unnecessary complexity;
- local backup/recovery gaps.

Every corrective action is linked to affected docs/tests.

## 7. Current state

```text
AUDIT RESULT: NOT RUN
Reason: implementation from the challenged/frozen manual has not yet occurred.
```
