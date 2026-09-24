# GoldScalpTrader — Session, News and Risk State Machine

**Status:** FROZEN V1 PERMISSION ARCHITECTURE — TIMING/TTL CALIBRATION AND EXTERNAL SCHEDULE PROOF PENDING
**Version:** 1.1-cache-aware-news-safety
**Authority:** Market schedule states, News-safety states, cache-aware provider semantics, monetary-risk/system states, action-sensitive permission composition and transitions.

## 1. Purpose

This contract defines how independent hard authorities become safe new-entry permission and how existing-position management behaves while entry is blocked.

Market/session truth and News truth remain separate.

## 2. Market states

```text
OPEN
PRE_CLOSE
CLOSED
REOPEN_WARMUP
SESSION_UNKNOWN
```

Only verified OPEN can permit consideration of a new entry. Exact pre-close/reopen timing remains calibration/external proof.

`SESSION_UNKNOWN` fails closed for new entry; no schedule is invented.

## 3. News states

```text
NEWS_CLEAR
NEWS_BLACKOUT
NEWS_SAFETY_UNKNOWN
POST_NEWS_WARMUP
```

### NEWS_CLEAR

Accepted event truth is current and no configured blackout/warmup is active.

Current accepted truth may come from a fresh live/file provider or from a **last-known-good cache that still passes its original scope/schema/coverage/TTL rules**.

A provider refresh error may make provider health DEGRADED without changing News truth to UNKNOWN while that accepted cache remains valid.

### NEWS_BLACKOUT

Known high-impact configured event window; hard new-entry/re-entry block. A valid cached event can preserve a known blackout across a temporary provider refresh outage.

### NEWS_SAFETY_UNKNOWN

News becomes UNKNOWN when current event safety cannot be proved, for example:

- provider/API unavailable and no valid accepted cache exists;
- cache TTL/coverage expired;
- cache is malformed/corrupt;
- schema/mapping version is unsupported;
- scope is wrong;
- timestamps are invalid/future-dated;
- provider truth is otherwise untrustworthy.

Audit 1 + cache-resilience refinement freezes V1 treatment:

```text
Session OPEN + NEWS_SAFETY_UNKNOWN
→ new-entry BLOCK / LIMITED
```

UNKNOWN is never relabelled CLEAR.

Existing verified bot position management, protection and mandatory risk-reducing CLOSE continue under action-specific authorities; News UNKNOWN alone must not trap risk.

### POST_NEWS_WARMUP

After known event/dislocation, new entries can remain blocked until calibrated clean-bar/spread/market normalization conditions return.

## 4. Provider failure versus News UNKNOWN

These are deliberately not identical:

```text
latest provider/API refresh failed
+ last-known-good calendar still valid
→ provider DEGRADED
→ use accepted cached News truth
→ no unnecessary new-entry block merely because refresh failed

latest provider/API refresh failed
+ no valid current cache
→ NEWS_SAFETY_UNKNOWN
→ V1 new-entry BLOCK / LIMITED
```

A failed refresh never extends cache TTL or rewrites old timestamps.

## 5. Risk states

```text
NORMAL
LOSS_LOCKED
COOLDOWN
RISK_UNKNOWN
```

NORMAL cannot override another hard authority. LOSS_LOCKED/COOLDOWN/RISK_UNKNOWN block new entry while safe management continues according to action-specific rules.

## 6. System / lifecycle states

```text
HEALTHY
BLOCKED
UNKNOWN
RECONCILING
```

Hard unresolved examples include account/server/symbol mismatch, stale/corrupt required market data, unresolved Intent, StateStore integrity failure, unknown financial truth, ownership ambiguity, external Gold exposure or stale controller authority.

`RECONCILING` is not flat exposure.

## 7. New-entry composition

```text
MarketPermission
+ NewsPermission
+ STANDARD RiskPermission
+ Data / quote freshness
+ Account/server/symbol identity
+ Position ownership/capacity
+ Recovery/reconciliation
+ Controller holder/epoch
+ fresh spread/drift/volume/margin/stops
= central ExecutionPermission
```

The Gate consumes owner results; it does not duplicate their logic.

## 8. V1 News matrix

| Market | News/current provider truth | New entry |
|---|---|---|
| OPEN | CLEAR from fresh source | may proceed to remaining authorities |
| OPEN | CLEAR from still-valid LKG cache | may proceed; provider may show DEGRADED |
| OPEN | BLACKOUT from fresh source or valid cache | BLOCK |
| OPEN | UNKNOWN because no valid current truth | BLOCK / LIMITED |
| OPEN | POST_NEWS_WARMUP | BLOCK until release conditions |
| PRE_CLOSE/CLOSED/WARMUP | any | BLOCK |
| SESSION_UNKNOWN | any | UNKNOWN / fail closed |

## 9. Action-sensitive management

Conditions that block OPEN must not mechanically trap unwanted exposure.

Examples:

- wide spread may block discretionary OPEN;
- mandatory CLOSE still needs identity/controller/fresh quote/broker permission/Intent/reconciliation but elevated spread may be diagnostic rather than veto;
- News UNKNOWN/BLACKOUT blocks new entry but does not automatically block protection/close;
- loss lock blocks new exposure, not safe management;
- MODIFY can have stricter cost/drift checks than mandatory CLOSE.

## 10. PRE_CLOSE / reopen mechanism

Preserve the two-stage architecture:

```text
no-new-entry cutoff
→ later mandatory flatten cutoff while market still tradeable
```

Exact daily/weekend minutes are not copied from Swing and require broker schedule plus scalp hold-duration evidence.

Reopen retains a warmup mechanism requiring verified OPEN, fresh data, normalized execution conditions, no unresolved recovery issue and calibrated clean completed-M5 evidence. Exact counts remain calibration/external proof.

## 11. Holiday / special schedule uncertainty

If current altered broker schedule cannot be verified, session remains UNKNOWN. Missing public News alone is not proof of holiday/closure.

## 12. Controller / machine boundary

One active PRIMARY writer per account/symbol scope. Same-scope simultaneous active writers are unsupported. Sequential handoff requires old stop → checkpoint/package → restore → fresh broker reconciliation → controller acquisition.

## 13. Persistence / restart

Persist risk-day/lock/cooldown/episode state, unresolved Intents, ManagedTrade, controller lineage and relevant permission transitions through their owners.

Restart revalidates current session/news provider/cache state from original timestamps/coverage and cannot make stale cache fresh.

## 14. Dashboard

Display independently:

```text
Market State
News State
Provider Health / Source
Last successful News refresh / cache age where useful
Risk State
System/Recovery State
Controller State
Entry Permission
Management Permission / mandatory flatten
primary/secondary blocker
```

An upstream TradePlan/Risk stop is not automatically a central Gate failure.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/execution/checks.py
src/gold_scalp_trader/execution/gate.py
src/gold_scalp_trader/execution/service.py
```

## 16. Planned proof

Tests cover market-state transitions, fresh-source/cache CLEAR, valid-cache survival after provider failure, cache expiry → UNKNOWN, BLACKOUT preservation, STANDARD risk composition, action-sensitive CLOSE, restart revalidation, controller/reconciliation blocks and truthful blocker-vs-Gate presentation.

Connected proof separately verifies actual Exness schedule/reopen/close and provider behaviour.

## 17. Calibration pending

News provider/cache TTL and refresh cadence, blackout/post-event windows, PRE_CLOSE minutes, reopen clean-bar counts, holiday schedule source, spread rules for MODIFY/CLOSE and cooldown release requirements remain evidence questions.