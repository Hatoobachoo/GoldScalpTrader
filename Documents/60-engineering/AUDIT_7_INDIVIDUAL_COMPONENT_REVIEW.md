# GoldScalpTrader — Audit 7: Individual Component Review

**Status:** FROZEN AUDIT PROTOCOL — NOT RUN
**Version:** 1.0-preservation-first-component-by-component
**Authority:** Individual review of every material production/research/operator component rather than assuming one subsystem explains overall behaviour.

## 1. Scope

Review every meaningful component independently:

```text
MarketSnapshot
→ Indicators
→ Candle Structure / BOS / MSS
→ Technical levels / location / room
→ Liquidity / FVG / Order Blocks
→ Session / News context
→ six independent strategy families
→ BUY/SELL fusion + Red Team
→ Opportunity lifecycle
→ Entry Timing / event freshness
→ TradePlan invalidation / targets / cost context
→ executable-price geometry
→ SMALL/MEDIUM/NORMAL Risk + optional explicit aggressive overlay
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

Research/discovery/promotion gets parallel traversal.

## 2. Per-component worksheet

Record:

```text
Name
Canonical contract
Preserved / scalp-specific / operator-directed classification where inherited
Purpose
Inputs
Outputs/state
Authority owned
Authority forbidden
Freshness/chronology semantics
Failure/UNKNOWN semantics
Persistence/restart semantics
Implementation files
Focused tests
Integration tests
Operator visibility
Research evidence
External/scalp-calibration proof
Verdict
Defect/action
```

## 3. Required review principles

- Do not assume Gate problem when candidate never reached Gate.
- Do not assume no trades means strategy too strict.
- Do not assume many trades means good Opportunity Recall.
- Do not conflate broker affordability with strategy quality.
- Do not conflate UI labels with owning authority.
- Do not count correlated evidence repeatedly.
- Do not accept stale events/levels merely because original thesis was strong.
- Do not let test fixtures bypass production safety.
- Do not remove/change a Swing feature/default unless a direct scalp reason, explicit operator instruction or proven reference defect authorizes it.

### Threshold rule

The old blanket statement “do not copy Swing thresholds without scalp evidence” is **not** current governance.

Correct rule:

```text
threshold/default directly sensitive to scalp horizon/cost/freshness
→ may require scalp calibration

non-scalp reference feature/default without justified delta
→ preserve reference baseline
```

Examples preserved unless governed later: Risk profiles/bands, reset default, one-fresh-reentry baseline, three-loss cooldown, 1800s provider TTL, PRE_CLOSE/reopen defaults, bounded analytical concurrency and future REAL governance path.

## 4. Scalp-specific component questions

Check target room after transaction costs, event/trigger age, signal-to-submit drift, frozen M5/M1 roles, min-lot actual risk, time-in-trade efficiency, family invalidation, News/dislocation exposure and latency observability.

These questions do not reopen unrelated preserved policy.

## 5. Classification

```text
PASS
PASS WITH SCALP CALIBRATION PENDING
DEFECT
PRESERVATION VIOLATION
DESIGN CHANGE REQUIRED
EXTERNAL PROOF PENDING
NOT IMPLEMENTED
NOT RUN
```

Neighboring component PASS cannot grant this component PASS.

## 6. Final traversal output

Identify correct components, implementation defects, doc/code/test mismatches, genuine scalp calibration issues, preservation violations, presentation-only issues, external evidence gaps, ownership duplication, dead complexity and backup/recovery gaps.

Every corrective action links to affected docs/tests.

## 7. Current state

```text
AUDIT RESULT: NOT RUN
Reason: implementation from the final frozen manual has not yet occurred.
```

Protocol is frozen; result remains NOT RUN.