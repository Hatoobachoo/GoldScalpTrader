# GoldScalpTrader — Session, News and Risk State Machine

**Status:** FROZEN V1 PERMISSION ARCHITECTURE — TIMING CALIBRATION / EXTERNAL SCHEDULE PROOF PENDING
**Version:** 1.0-news-unknown-conservative
**Authority:** Market schedule states, News-safety states, monetary-risk/system states, action-sensitive permission composition and transitions.

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

Accepted current event truth and no configured hard blackout/warmup.

### NEWS_BLACKOUT

Known high-impact configured event window; hard new-entry/re-entry block.

### NEWS_SAFETY_UNKNOWN

Provider/event truth is missing, stale, malformed or unavailable. Audit 1 freezes conservative V1 treatment:

```text
Session OPEN + News UNKNOWN
→ new-entry BLOCK / LIMITED
```

UNKNOWN is never relabelled CLEAR.

Existing verified bot position management, protection and mandatory risk-reducing CLOSE continue under action-specific authorities; News UNKNOWN alone must not trap risk.

### POST_NEWS_WARMUP

After known event/dislocation, new entries can remain blocked until calibrated clean-bar/spread/market normalization conditions return.

## 4. Risk states

```text
NORMAL
LOSS_LOCKED
COOLDOWN
RISK_UNKNOWN
```

NORMAL cannot override another hard authority. LOSS_LOCKED/COOLDOWN/RISK_UNKNOWN block new entry while safe management continues according to action-specific rules.

## 5. System / lifecycle states

```text
HEALTHY
BLOCKED
UNKNOWN
RECONCILING
```

Hard unresolved examples include account/server/symbol mismatch, stale/corrupt required market data, unresolved Intent, StateStore integrity failure, unknown financial truth, ownership ambiguity, external Gold exposure or stale controller authority.

`RECONCILING` is not flat exposure.

## 6. New-entry composition

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

## 7. V1 News matrix

| Market | News | New entry |
|---|---|---|
| OPEN | CLEAR | may proceed to remaining authorities |
| OPEN | BLACKOUT | BLOCK |
| OPEN | UNKNOWN | BLOCK / LIMITED |
| OPEN | POST_NEWS_WARMUP | BLOCK until release conditions |
| PRE_CLOSE/CLOSED/WARMUP | any | BLOCK |
| SESSION_UNKNOWN | any | UNKNOWN / fail closed |

## 8. Action-sensitive management

Conditions that block OPEN must not mechanically trap unwanted exposure.

Examples:

- wide spread may block discretionary OPEN;
- mandatory CLOSE still needs identity/controller/fresh quote/broker permission/Intent/reconciliation but elevated spread may be diagnostic rather than veto;
- News UNKNOWN/BLACKOUT blocks new entry but does not automatically block protection/close;
- loss lock blocks new exposure, not safe management;
- MODIFY can have stricter cost/drift checks than mandatory CLOSE.

## 9. PRE_CLOSE / reopen mechanism

Preserve the two-stage architecture:

```text
no-new-entry cutoff
→ later mandatory flatten cutoff while market still tradeable
```

Exact daily/weekend minutes are **not** copied from Swing and require broker schedule plus scalp hold-duration evidence.

Reopen retains a warmup mechanism requiring verified OPEN, fresh data, normalized execution conditions, no unresolved recovery issue and calibrated clean completed-M5 evidence. Exact counts remain calibration/external proof.

## 10. Holiday / special schedule uncertainty

If current altered broker schedule cannot be verified, session remains UNKNOWN. Missing public News alone is not proof of holiday/closure.

## 11. Controller / machine boundary

One active PRIMARY writer per account/symbol scope. Same-scope simultaneous active writers are unsupported. Sequential handoff requires old stop → checkpoint/package → restore → fresh broker reconciliation → controller acquisition.

## 12. Persistence / restart

Persist risk-day/lock/cooldown/episode state, unresolved Intents, ManagedTrade, controller lineage and relevant permission transitions through their owners.

Restart refreshes current session/news observations and cannot convert unavailable News to CLEAR or forget cooldown/episode lock.

## 13. Dashboard

Display independently:

```text
Market State
News State
Risk State
System/Recovery State
Controller State
Entry Permission
Management Permission / mandatory flatten
primary/secondary blocker
```

An upstream TradePlan/Risk stop is not automatically a central Gate failure.

## 14. Planned implementation ownership

```text
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/execution/checks.py
src/gold_scalp_trader/execution/gate.py
src/gold_scalp_trader/execution/service.py
```

## 15. Planned proof

Tests cover market-state transitions, CLEAR/BLACKOUT/UNKNOWN News matrix, STANDARD risk composition, action-sensitive CLOSE, holiday/schedule UNKNOWN, restart persistence, controller/reconciliation blocks and truthful blocker-vs-Gate presentation.

Connected proof separately verifies actual Exness schedule/reopen/close behaviour.

## 16. Calibration pending

News blackout/post-event windows, PRE_CLOSE minutes, reopen clean-bar counts, holiday schedule source, spread rules for MODIFY/CLOSE and cooldown release requirements remain evidence questions.