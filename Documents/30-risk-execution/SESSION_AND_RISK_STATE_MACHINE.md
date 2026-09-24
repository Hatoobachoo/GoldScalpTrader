# GoldScalpTrader — Session, News and Risk State Machine

**Status:** FROZEN V1 PERMISSION ARCHITECTURE — PRESERVED SESSION/RISK DEFAULTS + SCALP NEWS POLICY
**Version:** 1.2-preserved-session-risk-cache-aware
**Authority:** Market schedule states, News-safety states, cache-aware provider semantics, profiled monetary-risk/system states, action-sensitive permission composition and transitions.

## 1. Purpose

This contract defines how independent hard authorities become safe new-entry permission and how existing-position management behaves while entry is blocked.

Market/session truth, News truth and monetary Risk remain separate owners.

## 2. Market states

```text
OPEN
PRE_CLOSE
CLOSED
REOPEN_WARMUP
SESSION_UNKNOWN
```

Only verified OPEN can permit new-entry consideration. `SESSION_UNKNOWN` fails closed.

Preserved policy baselines:

```text
Daily close cycle:
  T-20 minutes → no new entry
  T-10 minutes → mandatory flatten

Weekend close cycle:
  T-60 minutes → no new entry
  T-30 minutes → mandatory flatten

Daily reopen:
  verified OPEN
  + 1 clean completed M5
  + execution/recovery normal

Weekend reopen:
  verified OPEN
  + 2 clean completed M5
  + weekend gap assessment
  + execution/recovery normal
```

These defaults are preserved because removing them was not scalp-required. Actual current broker schedule/DST/holiday facts still require external proof.

## 3. News states

```text
NEWS_CLEAR
NEWS_BLACKOUT
NEWS_SAFETY_UNKNOWN
POST_NEWS_WARMUP
```

### NEWS_CLEAR
Accepted event truth is current and no configured blackout/warmup applies. Source can be fresh provider/file or still-valid accepted last-known-good cache.

### NEWS_BLACKOUT
Known configured high-impact event window; hard new-entry/re-entry block.

### NEWS_SAFETY_UNKNOWN
Current News safety cannot be proved because no accepted current source/cache exists.

Scalp-specific policy:

```text
Session OPEN + NEWS_SAFETY_UNKNOWN
→ new-entry BLOCK / LIMITED
```

Existing verified bot-position management/protection/mandatory risk-reducing CLOSE remains action-sensitive.

### POST_NEWS_WARMUP
Known event/dislocation can hold new entries until the configured stabilization conditions are satisfied.

## 4. Provider failure versus News UNKNOWN

```text
latest provider/API refresh failed
+ LKG calendar still valid under original scope/schema/coverage/TTL/integrity
→ provider DEGRADED
→ use accepted cached News truth
→ do not block merely because refresh failed

refresh failed
+ no valid current cache
→ NEWS_SAFETY_UNKNOWN
→ new-entry BLOCK / LIMITED
```

Failed refresh never rewrites old timestamps or extends TTL.

Preserved provider TTL baseline:

```text
1800 seconds
```

A later change needs a direct provider/scalp reason.

## 5. Risk states and profiles

```text
NORMAL
LOSS_LOCKED
COOLDOWN
RISK_UNKNOWN
```

Risk profile is resolved from positive DayStartEquity at UTC risk-day boundary and fixed for the day:

```text
SMALL   < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

Profile target/elevated/hard/daily values are owned by `RISK_CONTRACT.md`.

Explicit `AGGRESSIVE_SMALL_ACCOUNT` overlay is preserved but disabled by default. When explicitly enabled and eligible:

```text
8% max monetary SL risk per trade — not target
16% max aggregate open risk
16% daily loss ceiling
```

`LOSS_LOCKED`, `COOLDOWN` and `RISK_UNKNOWN` block new exposure while safe management continues.

## 6. Preserved cooldown / reset semantics

Baseline:

- one ordinary losing trade does not create global cooldown;
- one genuinely fresh same-episode re-entry may be allowed;
- if that re-entry loses, the episode locks;
- three consecutive closed bot losses trigger at least 30 minutes global cooldown;
- release also requires fresh/healthy conditions defined in the Risk contract.

Governed manual daily-loss reset capability remains present but disabled by default.

## 7. System / lifecycle states

```text
HEALTHY
BLOCKED
UNKNOWN
RECONCILING
```

Hard unresolved examples include account/server/symbol mismatch, stale/corrupt required market data, unresolved Intent, StateStore integrity failure, unknown financial truth, ownership ambiguity, external Gold exposure or stale controller authority.

`RECONCILING` is not flat exposure.

## 8. New-entry composition

```text
MarketPermission
+ NewsPermission
+ profiled RiskPermission / optional explicit overlay
+ Data / quote freshness
+ Account/server/symbol identity
+ Position ownership/capacity
+ Recovery/reconciliation
+ Controller holder/epoch
+ fresh spread/drift/volume/margin/stops
= central ExecutionPermission
```

The Gate consumes owner results; it does not duplicate their logic.

## 9. Entry matrix

| Market | News | New entry |
|---|---|---|
| OPEN | CLEAR from fresh source | may proceed to remaining authorities |
| OPEN | CLEAR from valid LKG cache | may proceed; provider may be DEGRADED |
| OPEN | BLACKOUT | BLOCK |
| OPEN | UNKNOWN | BLOCK / LIMITED |
| OPEN | POST_NEWS_WARMUP | BLOCK until release conditions |
| PRE_CLOSE/CLOSED/REOPEN_WARMUP | any | BLOCK |
| SESSION_UNKNOWN | any | UNKNOWN / fail closed |

Risk/profile/overlay and every other hard authority must also pass.

## 10. Action-sensitive management

Conditions that block OPEN must not mechanically trap unwanted exposure.

Examples:

- wide spread may block discretionary OPEN;
- mandatory CLOSE still needs identity/controller/fresh quote/broker permission/Intent/reconciliation but elevated spread may be diagnostic rather than veto;
- News UNKNOWN/BLACKOUT blocks new entry but does not automatically block protection/close;
- loss lock blocks new exposure, not safe management;
- MODIFY can have stricter friction checks than mandatory CLOSE.

## 11. Controller / machine boundary

One active PRIMARY writer per account/symbol scope. Same-scope simultaneous active writers are unsupported without a future deliberate shared-fencing design.

## 12. Persistence / restart

Persist risk-day profile/overlay identity, lock/reset/cooldown/episode state, unresolved Intents, ManagedTrade, controller lineage and relevant permission transitions.

Restart revalidates session/news/cache from original timestamps/coverage and never makes stale cache fresh.

## 13. Dashboard

Display independently:

```text
Market State
News State
Provider Health / Source / cache age
Risk Profile SMALL / MEDIUM / NORMAL
Aggressive mode ENABLED / DISABLED
actual proposed risk / active ceilings
Risk State / cooldown / reset
System/Recovery State
Controller State
Entry Permission
Management Permission / mandatory flatten
primary/secondary blocker
```

An upstream TradePlan/Risk stop is not automatically a central Gate failure.

## 14. Planned ownership

```text
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/risk/engine.py
src/gold_scalp_trader/risk/state.py
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/execution/checks.py
src/gold_scalp_trader/execution/gate.py
```

## 15. Planned proof

Tests cover:

- profile resolution and fixed-risk-day identity;
- normal/aggressive loss-lock composition;
- preserved cooldown/re-entry/reset defaults;
- market PRE_CLOSE/reopen transitions;
- fresh-source/cache CLEAR;
- valid-cache survival after provider failure;
- cache expiry → UNKNOWN;
- BLACKOUT preservation;
- action-sensitive CLOSE;
- restart persistence;
- controller/reconciliation blocks;
- truthful blocker-vs-Gate presentation.

Connected proof separately verifies actual current Exness schedule/reopen/close/provider behaviour.