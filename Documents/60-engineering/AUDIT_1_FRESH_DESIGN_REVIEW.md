# GoldScalpTrader — Audit 1 Fresh Architecture and Design Review

**Status:** DRAFT AUDIT PROTOCOL — NOT RUN
**Version:** 0.1-fresh-zero-scalp-review
**Authority:** Fresh-from-zero architecture/design challenge, module-by-module and feature-by-feature, independent of implementation inertia.

## 1. Review question

Ask deliberately:

> If GoldScalpTrader were designed today from zero chat history, with the same user requirements and retail Exness/MT5 constraints, what architecture would we build, what would we keep, simplify, change, remove or add?

Existing GoldSwingTraderAI or provisional GoldScalpTrader code is not correct merely because it exists.

## 2. Classification vocabulary

```text
KEEP AS-IS
SMALL IMPROVEMENT
SHOULD CHANGE
MAJOR ARCHITECTURAL CHANGE
REMOVE / SIMPLIFY
ADD
NEEDS REAL-MARKET CALIBRATION
NEEDS EXTERNAL DEMO PROOF
```

Each verdict records reason, affected contracts/source/tests and evidence boundary.

## 3. Mandatory challenge areas

Review individually:

- product mission/non-goals;
- H4/H1/M15/M5/M1/quote roles;
- one-read immutable snapshot;
- staged parallelism versus serial authority;
- candle/structure knowledge time;
- Technical/Liquidity/Quant/Session/News desks;
- six-family starting floor — keep/merge/split/replace/remove;
- BUY/SELL fusion + Red Team;
- Opportunity lifecycle/event freshness/re-arm;
- TradePlan family geometry;
- minimum structural R and transaction-cost room;
- risk profiles/min-lot/daily limits/cooldown;
- News UNKNOWN policy;
- session/pre-close/reopen policy;
- one-shot execution/reconciliation/controller;
- scalp Trade Manager/time efficiency;
- persistence/local backup/recovery;
- learning/research/discovery/promotion;
- terminal/browser UX;
- dependency/module/test design;
- zero-cost/GitHub-safety architecture.

## 4. Special zero-design questions for a scalper

Challenge whether:

- M1 should remain diagnostic or gain explicit timing authority;
- completed-M5 entry timing is fast enough;
- tick/quote sampling is sufficient without tick-history authority;
- six families are truly independent on scalp horizons;
- transaction costs deserve earlier analytical rejection or only final execution checks;
- target/stop geometry remains viable at 0.01 lot on ~$100 account;
- time exits prevent accidental swing conversion;
- event-freshness rules are family specific;
- London/NY specialization improves edge without overfitting;
- latency measurement changes architecture or only observability;
- local backup design is simpler/safer than reference Git publication.

## 5. Preserve versus copy bias

A reference feature can be retained only because its ownership/safety/evidence logic still makes sense for scalping—not because “Swing had it.”

Likewise, a feature is not removed simply to make code shorter if it protects lifecycle, safety, recovery or evidence quality.

## 6. Required output

For every material component produce a table:

```text
Component
Current draft design
Fresh-zero alternative
Verdict
Reason
Risk if unchanged
Affected Documents
Implementation consequence
Test/evidence consequence
Calibration/external proof
```

Then update the full affected graph before freeze.

## 7. Review sequence

```text
complete canonical Documents draft
→ freeze nothing yet
→ review market/strategy/risk/execution/recovery/research/operator independently
→ challenge cross-layer contradictions
→ classify every major component
→ update Design Decisions/Open Questions
→ synchronize all affected docs
→ repeat contradiction/reconstructability review
→ only then mark architecture contracts FROZEN for implementation
```

## 8. Current state

```text
AUDIT RESULT: NOT RUN
Reason: canonical document tree is still being completed.
```

This file becomes the primary record of the requested “if designed from zero, what would be upgraded and what would not?” challenge before implementation begins.
