# GoldScalpTrader — Audit 7: Individual Component Review

**Status:** FINAL COMPONENT-AUDIT PROTOCOL — NOT RUN AGAINST IMPLEMENTATION
**Version:** 2.0-every-component-authority-review
**Authority:** Component-by-component audit of purpose, input/output, authority, chronology, failure, persistence, tests and operator/research effects.

## 1. Purpose

Audit 7 walks every implemented component individually so a correct whole-system diagram cannot hide a broken local boundary.

For each component ask:

```text
Why does it exist?
What facts enter?
What typed output leaves?
What authority does it own?
What authority is forbidden?
What chronology/freshness applies?
What does UNKNOWN mean?
What state persists?
What can fail/restart?
Which tests prove it?
What does operator see?
What does research learn?
```

## 2. Market-data review

Verify:

- one normalized analytical MT5 reader;
- no raw write calls;
- symbol/account/spec/quote normalization;
- completed-bar rules;
- bounded M1;
- exposure/history unknown semantics;
- current/recovery reads clearly separated from causal historical snapshot.

## 3. Candle Structure review

Verify:

- pivot vs confirmation time;
- candidate/confirmed/protected lifecycle;
- BOS/MSS/failed-break causality;
- completed bars only;
- no future confirmation leakage;
- M5 authority vs subordinate M1 microstructure.

## 4. Technical / Liquidity / Confluence review

Verify:

- zone/pool/FVG/OB lifecycle;
- consumed/invalid geometry excluded;
- trendline/Fib anchors causal;
- POC source labelled broker-local;
- event/source lineage retained;
- optional evidence not universalized.

## 5. Indicator / Quant review

Verify:

- EMA/RSI/ATR chronological calculation;
- warmup missingness;
- shared/reused series;
- no “RSI >70 = SELL” universal shortcut;
- family-specific importance;
- M1 quant remains subordinate timing context.

## 6. Session / News review

Session Context:

- soft Asia/London/NY labels;
- DST-safe chronology;
- no inference of broker OPEN.

News:

- soft context/research;
- provider health truthful;
- no hard News block/cooldown/warmup;
- no cache timestamp laundering.

Broker Session:

- independent hard OPEN/PRE_CLOSE/CLOSED/UNKNOWN authority.

## 7. Setup Detector review

This component must be market-first.

Verify:

- all six family definitions evaluated as applicable;
- can return NONE;
- can return one/multiple candidates;
- active-family identity does not change raw setup classification;
- setup candidates retain family/event evidence;
- no Risk/write authority.

## 8. Strategy Isolation review

Verify:

- exactly one active policy;
- five shadow families;
- shadow cannot live-originate;
- switch versioned/approval-governed;
- restart restores identity;
- historical attribution immutable.

## 9. Active-family decision / Red Team review

Verify:

- independent BUY/SELL;
- required vs optional evidence;
- correlation caps/lineage;
- shadow conflict contextual only;
- no score→Risk linkage;
- explicit reasons/coverage.

## 10. Opportunity / Timing review

Verify:

- M5 setup before Opportunity;
- persistent identity through WAIT;
- M1 subordinate refinement;
- READY/WAIT/MISSED/INVALID;
- fresh-event-only re-arm;
- restart revalidation;
- timing does not call broker.

## 11. TradePlan review

Verify:

- family-aware invalidation;
- correct event-specific fallback;
- structural buffer/tick normalization;
- Immediate/Primary/Expansion/Runner targets;
- original R immutable;
- no stop rewrite for min lot;
- no automatic Swing 1.20R hard floor.

## 12. Executable Quality review

Verify current calculations/units:

- emergency spread;
- spread/SL;
- spread/target;
- spread baseline;
- cost/reward;
- slippage allowance;
- deviation;
- latency;
- drift/chase;
- fresh revalidation.

No monetary sizing or broker write authority.

## 13. Risk review

Verify exact preserved profile values and boundaries, dynamic lot/min-lot, margin, cash flow, daily lock/reset, aggressive mode, cooldown/re-entry and capacity.

Risk must never modify strategy/structural stop or use confidence score to increase monetary policy.

## 14. Gate / Intent / writer / reconciliation review

Inspect separately:

### Gate

- central composition only;
- actual BLOCK vs NOT_EVALUATED truth.

### Intent

- durable identity/state;
- one send allowance.

### Checks

- current broker facts/order_check;
- zero send on failure.

### Writer

- sole raw write boundary.

### Reconciler

- current broker truth;
- ambiguous ack resolution;
- no blind retry.

## 15. Controller review

Verify current holder/epoch/lease before writes, stale epoch denial and local single-primary semantics.

Distributed active-active is not accidentally introduced.

## 16. ManagedTrade review

Verify:

- original strategy/policy/plan identity;
- current position truth;
- HOLD/PROTECT/TRAIL/RUNNER/EXIT;
- no stop widening;
- time-efficiency;
- partial management correctness;
- PRE_CLOSE;
- verified close archive.

## 17. Persistence / checkpoint review

Verify:

- strict types/schema;
- idempotency/conflict detection;
- all authority-bearing local state included;
- checkpoint consistency/hash;
- restore into new path;
- fresh broker reconciliation;
- no credentials;
- no runtime Git.

## 18. Learning / discovery / invention / ML review

Verify:

- actual/shadow/missed/blocked/fault separation;
- exactly-once actual learning;
- causal replay;
- candidate identity/fingerprint;
- durable rejection memory;
- bounded declarative invention;
- ML data/feature/model identity;
- automatic stage progression evidence-bound;
- production promotion stops for operator approval;
- zero broker authority.

## 19. Operator / dashboard review

Verify:

- read-only DTOs;
- one-screen/no-scroll primary graphical layout;
- functional chart controls;
- Detected Setup vs Active Test Family separation;
- shadow setup visible;
- exact blocker vs Gate;
- unknown never zero;
- no hidden policy mutation through UI.

## 20. App/runtime review

Verify startup/recovery/cycle/loop composition uses owning modules rather than reimplementing policy.

No runtime Git activity.

## 21. Component result format

For each component:

```text
PASS
PARTIAL
MISSING
BROKEN
UNTESTED
EXTERNAL_PROOF_PENDING
```

Record exact evidence and finding IDs.

## 22. Current status

This individual-component protocol is final but **NOT RUN** against implementation. It becomes a required post-build/pre-release audit.
