# GoldScalpTrader — Session, News and Risk State Machine

**Status:** DRAFT PRE-CHALLENGE PERMISSION CONTRACT
**Version:** 0.1-scalp-session-risk-state
**Authority:** Market schedule states, news-safety states, risk/system states, permission composition and action-sensitive transitions.

## 1. Purpose

This document defines how independent hard authorities become safe new-entry permission and how existing-position management behaves while entry is blocked.

Market/session truth and News truth remain separate:

- broker/session truth is hard;
- positively known high-impact blackout truth is hard;
- external News-provider availability is adaptive context;
- News UNKNOWN is never fabricated as CLEAR;
- the treatment of `OPEN + News UNKNOWN` remains a deliberate policy item for the scalp challenge, because short-duration execution is unusually event-sensitive.

## 2. State topology

```text
Market Permission
+ News Permission
+ Monetary Risk State
+ Data / account / exposure / recovery / controller state
→ centralized permission composition
→ ALLOW / BLOCK / UNKNOWN for the requested action
```

The result for a **new entry** is not automatically the result for managing an already-open verified bot position.

## 3. Market schedule states

Draft states:

```text
OPEN
PRE_CLOSE
CLOSED
REOPEN_WARMUP
SESSION_UNKNOWN
```

Only verified OPEN can permit consideration of a new entry.

### OPEN

Means accepted broker/session facts support tradeability. It does not bypass risk, data, identity, controller, news or fresh execution checks.

### PRE_CLOSE

Verified symbol schedule says a closure is approaching.

The mechanism from the reference system is retained:

- stop new entries before a defined cutoff;
- flatten bot-managed exposure before known closure where policy requires it;
- route flatten through normal governed CLOSE Intent/writer/reconciliation;
- never assume closed merely because schedule reached T-0.

Exact daily/weekend scalp cutoff minutes remain challengeable and must use current broker evidence.

### CLOSED

No new entries. Analysis/dashboard/background research may remain alive.

Any unexpected open position or unresolved Intent remains a reconciliation obligation, not invented flat truth.

### REOPEN_WARMUP

The first returned quote does not immediately grant entry authority.

Warmup may require:

- verified schedule OPEN;
- fresh Bid/Ask and required bars;
- normalized spread/execution conditions;
- no unresolved gap/reconciliation issue;
- one or more clean completed M5 bars;
- additional weekend gap assessment.

Exact clean-bar counts remain challengeable.

### SESSION_UNKNOWN

If required current schedule truth cannot be established, new entries fail closed. No open/close time is invented.

## 4. News-safety states

```text
NEWS_CLEAR
NEWS_BLACKOUT
NEWS_SAFETY_UNKNOWN
POST_NEWS_WARMUP
```

### NEWS_CLEAR

Accepted event truth is current and no configured hard blackout/warmup is active.

### NEWS_BLACKOUT

A positively known high-impact window is active. It blocks new entries/re-entry/add-ons. Scheduled news alone does not automatically force-close an existing position.

### NEWS_SAFETY_UNKNOWN

Provider truth is missing/stale/malformed/unavailable. It remains visibly UNKNOWN.

The reference system allowed `Session PASS + News UNKNOWN → combined PASS`. GoldScalpTrader will **not freeze that automatically** before the fresh-zero challenge because a scalper's holding/entry horizon is more exposed to immediate event shocks.

Candidate policies to challenge include:

```text
A) preserve reference adaptive-PASS behaviour;
B) block only new entries when News is UNKNOWN while management continues;
C) session/regime-specific degraded policy.
```

Whatever is chosen must remain explicit and tested; UNKNOWN may never be renamed CLEAR.

### POST_NEWS_WARMUP

A known event/dislocation can keep new entries blocked until normalized conditions and fresh completed-bar evidence return. Exact duration/conditions remain calibration.

## 5. Risk states

```text
NORMAL
LOSS_LOCKED
COOLDOWN
RISK_UNKNOWN
```

`NORMAL` only means no risk-state lock is active. It cannot override another hard authority.

`LOSS_LOCKED` blocks new exposure while allowing safe management.

`COOLDOWN` blocks new entries until its documented release conditions pass.

`RISK_UNKNOWN` fails closed for new entries.

## 6. System/lifecycle states

```text
HEALTHY
BLOCKED
UNKNOWN
RECONCILING
```

Examples of hard unresolved truth:

- account/server/symbol mismatch;
- stale/corrupt required market data;
- unknown schedule;
- unresolved Intent;
- StateStore integrity failure;
- unknown financial truth;
- position ownership ambiguity;
- external Gold exposure;
- lost/stale controller authority.

`RECONCILING` is not empty exposure.

## 7. Controller state

Initial V1 permits one active PRIMARY writer per account/symbol scope.

Only the current verified controller holder/fencing epoch may proceed to an irreversible write.

Same-scope simultaneous active writers are unsupported. Sequential handoff requires stop → checkpoint → transfer/restore → broker reconciliation → new controller acquisition.

## 8. Permission composition

Conceptual new-entry composition:

```text
MarketPermission
+ NewsPermission
+ RiskPermission
+ DataQuality / quote freshness
+ Account/server/symbol identity
+ Position ownership / capacity
+ Recovery/reconciliation
+ Controller holder/epoch
+ fresh spread/drift/volume/margin/stops
= centralized ExecutionPermission
```

The central Gate consumes these results; it does not reimplement them independently.

## 9. Action-sensitive entry versus management

Some conditions that block OPEN must not trap risk inside an existing position.

Examples:

- elevated spread may block discretionary OPEN;
- a mandatory CLOSE still requires fresh quote/broker/controller/lifecycle authority, but should not be vetoed merely because spread is elevated if closing reduces unwanted exposure and broker accepts it;
- MODIFY may retain stricter spread/drift controls;
- News blackout normally blocks new entry, not necessary protection/close;
- loss lock blocks new exposure, not safe management.

Exact action-specific rules belong jointly to this contract and `EXECUTION_AND_BROKER_SAFETY.md`.

## 10. PRE_CLOSE policy seed

The reference design used:

```text
daily close:   T-20m no new entry, T-10m mandatory flatten
weekend close: T-60m no new entry, T-30m mandatory flatten
```

GoldScalpTrader preserves the **two-stage mechanism**, not these exact numbers as frozen policy. The challenge should account for scalp duration, broker schedule and real execution conditions.

## 11. Reopen policy seed

The reference required one clean completed M5 after daily reopen and two after weekend reopen plus gap assessment.

This is retained as a candidate baseline because M5 is the primary scalp timeframe, but exact counts remain external/calibration items.

Clean bars never override abnormal spread, stale data, unresolved reconciliation, identity or risk failures.

## 12. Holiday/special schedule uncertainty

A positively known holiday that may alter Gold hours means normal assumptions may be insufficient. Exact altered broker schedule is required or session remains UNKNOWN.

A missing public news calendar alone is not proof of a holiday or special closure.

## 13. Persistence/restart

Persist through owners:

- risk-day/lock/cooldown/episode state;
- unresolved Intents;
- ManagedTrade context;
- controller epoch/ownership lineage where durable;
- relevant permission-transition evidence.

Current session/news observations are refreshed on restart.

Restart must not:

- create a fresh risk baseline while lifecycle is unresolved;
- turn unavailable News into CLEAR;
- forget cooldown/episode lock;
- assume external exposure is gone;
- call writer before controller/reconciliation authority is ready.

## 14. Dashboard

Display independently:

```text
Market State
News State
Risk State
System / Recovery State
Controller State
Entry Permission
Management Permission / mandatory flatten state
primary blocker
secondary blocker
```

An upstream TradePlan/Risk stop must not be mislabelled as a Central Gate failure.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/execution/checks.py
src/gold_scalp_trader/execution/gate.py
src/gold_scalp_trader/execution/service.py
```

## 16. Planned deterministic proof

Tests must cover:

- OPEN/PRE_CLOSE/CLOSED/WARMUP/UNKNOWN transitions;
- known blackout versus News UNKNOWN;
- whichever `OPEN + News UNKNOWN` scalp policy is eventually frozen;
- loss lock/cooldown composition;
- action-sensitive CLOSE semantics;
- holiday/special schedule unknown;
- restart persistence;
- controller/reconciliation blocks;
- truthful upstream-vs-Gate presentation.

Connected broker proof separately verifies real Exness schedule and close/reopen behaviour.

## 17. Non-goals

This state machine does not choose strategy direction, calculate lots, fabricate News CLEAR, ignore known blackout, force-close solely due scheduled news, bypass controller/reconciliation, perform raw MT5 writes or claim profitability.

## 18. Pre-challenge questions

- final `News UNKNOWN` new-entry policy for scalping;
- exact news blackout/warmup windows;
- PRE_CLOSE cutoffs;
- reopen clean-bar counts;
- holiday schedule source;
- action-sensitive spread rules for CLOSE/MODIFY;
- cooldown release requirements.
