# GoldScalpTrader — Final Release Audit

**Status:** FINAL AUDIT PROTOCOL — NOT RUN AGAINST IMPLEMENTED RELEASE
**Version:** 2.0-institutional-scalp
**Authority:** Final evidence-based release sign-off protocol for an exact revision/capability stage.

## 1. Purpose

This audit answers:

> **Does this exact revision satisfy the documented contracts and evidence requirements for the capability it claims?**

It is not a profitability certification and not a generic “looks good” review.

## 2. Audit identity

A completed release audit records:

```text
repository
commit SHA
date/time
auditor/operator
capability stage: DOCS / DRY_RUN / DEMO / RECOVERY_CERTIFIED / REAL_CANDIDATE
Python version
MetaTrader5 version
MT5 terminal/account/server/symbol scope
OS/machine identity where relevant
config/policy versions
dataset/evidence package IDs
```

No audit may be reused for a materially different revision without explicit revalidation.

## 3. Evidence hierarchy

```text
canonical Documents
→ source ownership
→ deterministic tests
→ integration tests
→ replay/calibration evidence
→ connected MT5 facts
→ controlled DEMO lifecycle
→ recovery/handoff drills
→ release/operator approvals
```

A lower layer cannot substitute for a missing higher layer where the release requires it.

## 4. Documentation trace

Audit all canonical areas:

- Foundation;
- Market Intelligence;
- Trading Decisions;
- Risk/Execution;
- Research/Learning;
- Operator;
- Engineering;
- Governance;
- top-level policies/manuals.

For each material contract identify:

```text
canonical owner
source owner
test/evidence owner
release status
exception if any
```

## 5. Architecture invariants to prove

- one normalized analytical MT5 read boundary;
- immutable snapshot semantics;
- causal completed-candle chronology;
- market-first setup detection;
- active family cannot force chart classification;
- exactly one live `ACTIVE_EXECUTION` family during Strategy Isolation;
- five `SHADOW_ONLY` families cannot write/live-originate;
- M5 setup authority;
- M1 subordinate refinement only;
- TradePlan before monetary Risk;
- Executable Quality separate from structural geometry;
- preserved SMALL/MEDIUM/NORMAL Risk policy;
- News soft-context-only behavior;
- hard broker/session authority separate;
- central Gate;
- persist-before-send Intent;
- sole raw writer;
- no blind retry;
- verified ManagedTrade lifecycle;
- learning/research no broker authority;
- candidate promotion stops at `APPROVAL_REQUIRED`;
- no runtime Git publication.

## 6. Setup/strategy audit

Use deliberately conflicting fixtures/scenarios:

### Scenario A — active family setup exists

```text
active = Breakout Retest
market = valid Breakout Retest
→ may progress to active BUY/SELL debate
```

### Scenario B — different setup exists

```text
active = Breakout Retest
market = valid Liquidity Sweep only
→ Setup Detector says Liquidity Sweep
→ live WAIT
→ Sweep shadow record
→ no fabricated Breakout Retest
```

### Scenario C — no setup exists

```text
→ Detected Setup NONE
→ live WAIT
```

### Scenario D — multiple candidates

Preserve all causal candidates; live eligibility still follows current isolation policy.

## 7. Timing / geometry audit

Prove:

- M1 cannot create a production Opportunity;
- stale M5 event/M1 trigger handled causally;
- chase/drift measured;
- re-arm requires fresh event;
- family-aware invalidation;
- event-specific stop only with exact causal proof;
- no stop tightening for min-lot affordability;
- no hard inherited Swing 1.20R dependency;
- original R immutable.

## 8. Executable-quality audit

Verify numerical units/calculations for:

```text
spread
emergency ceiling
spread/SL
spread/target
cost/reward
slippage allowance
broker deviation
drift
quote age
decision→send latency
```

Check no double counting and prove latency revalidation path.

## 9. Monetary Risk audit

Regression-check exact documented values and boundary cases around $300 and $1,000.

Verify:

- profile fixed through risk day;
- aggressive mode default false;
- 8% treated as ceiling not target;
- 16% aggregate/daily semantics;
- manual reset default false;
- same-episode re-entry count;
- 3-loss/30m cooldown;
- cash-flow/account safety accounting;
- min-lot actual risk;
- no score/confidence-based risk inflation.

## 10. News/session audit

News:

- event exists → no direct hard block;
- provider unavailable → no direct hard block;
- no News cooldown/warmup;
- provider health remains truthful.

Session:

- current broker OPEN/CLOSED/PRE_CLOSE/UNKNOWN semantics;
- pre-close/reopen baseline behavior;
- current Exness schedule evidence for connected release.

## 11. Execution audit

Inject/prove:

- upstream stop → Gate NOT_EVALUATED;
- hard authority fail → Gate BLOCKED;
- precheck fail → zero sends;
- SUBMITTING persisted before send;
- one Intent one send;
- broker rejection;
- timeout/ambiguous acknowledgement;
- no blind retry;
- broker reconciliation;
- stale controller fencing;
- manual/foreign exposure isolation.

## 12. Management audit

Review:

- HOLD ordinary pullback;
- earned PROTECT;
- structural TRAIL;
- no widening;
- time-efficiency EXIT;
- Runner only with fresh objective/evidence;
- partial management only when valid;
- PRE_CLOSE flatten;
- exact close recovery;
- verified close before learning.

## 13. Persistence/recovery audit

Crash-window review:

```text
before Intent
APPROVED Intent
SUBMITTING before/after broker send
ambiguous ack
verified OPEN before ManagedTrade persistence
MODIFY/CLOSE windows
verified close before queue
queue before receipt
receipt before lifecycle clear
learning save before queue consumption
```

Every crash window must recover without duplicate irreversible action or invented broker state.

## 14. Research/ML audit

Verify:

- actual/shadow/missed/blocked/fault evidence separation;
- no-lookahead replay;
- one-shot holdout;
- immutable candidate fingerprint after lock;
- failed evidence retained;
- autonomous invention uses bounded declarative primitives;
- advanced ML has data/feature/model identity;
- candidate stage transitions evidence-bound;
- no research raw writer import;
- `APPROVAL_REQUIRED` cannot be bypassed.

## 15. Dashboard audit

Against the approved operator contract verify:

- single-screen desktop composition;
- no scrollbar at target geometry;
- chart renders current intended data;
- M1/M5/M15/H1/H4 buttons function;
- Indicators/Drawings/Settings function within UI authority;
- Detected Setup separate from Active Test Family;
- shadow status clear;
- signal/reason exact;
- blocker vs Gate exact;
- TradePlan/Risk/execution/activity/learning/system/closes visible;
- no dashboard mutation of trading authority.

## 16. Performance audit

Use recorded stage timings and profiles.

Questions:

- are shared calculations reused?
- is strategy critical path fast enough for the documented timing semantics?
- does M1 refinement introduce unacceptable latency?
- does physical parallelism improve measured critical path if enabled?
- are serial/parallel outputs semantically identical?
- does graphical UI materially block runtime analysis?

No arbitrary performance PASS without measurement.

## 17. Security / Git / backup audit

Verify:

- secrets absent from repo/logs/packages;
- runtime has no GitHub credential dependency;
- runtime shutdown has no Git operation;
- source/history backup is separate from runtime state;
- checkpoint integrity/hash verification;
- sequential same-scope handoff;
- no active-active distributed writer dependency;
- repository visibility fact reported truthfully without unauthorized change.

## 18. Final findings format

Every finding:

```text
ID
severity: CRITICAL / HIGH / MEDIUM / LOW / INFO
owner
contract violated / evidence missing
exact reproduction/evidence
impact
required remediation
status
```

No vague “needs improvement” findings.

## 19. Release verdict

Only:

```text
PASS FOR DECLARED CAPABILITY
PASS WITH EXPLICIT NON-BLOCKING LIMITATIONS
BLOCKED
NOT RUN
```

For future REAL release, explicit operator approval is a separate required artifact and cannot be inferred from audit PASS.

## 20. Current status

This protocol is documentation-complete but **NOT RUN against a final implemented GoldScalpTrader release**. Until implementation/DEMO evidence exists, no execution or profitability claim is made.
