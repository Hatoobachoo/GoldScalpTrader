# GoldScalpTrader — Session/News Provider Contract

**Status:** FROZEN V1 PROVIDER ARCHITECTURE — PRESERVED 1800s BASELINE / EXTERNAL PROVIDER PROOF PENDING
**Version:** 1.1-lkg-cache-preserved-ttl
**Authority:** Session/news acquisition, normalization, provider health/freshness, bounded last-known-good cache and permission inputs.

## 1. Purpose

Session and scheduled-news data enter through governed provider boundaries rather than strategy code.

Providers do not directly authorize broker actions.

Core invariants:

- independently known broker/session truth remains separate from external News availability;
- known blackout remains hard according to the state machine;
- missing/stale News is never renamed CLEAR;
- temporary API/network refresh failure does not erase still-valid previously verified event truth;
- cache validity is never extended merely because refresh failed;
- provider credentials never enter repository/runtime-backup artifacts;
- final broker action still requires every other hard authority.

## 2. Provider resolution

```text
explicit injected provider for tests/integration
→ configured local scoped session/news snapshot file
→ approved zero-cost/best-effort public calendar adapter
→ accepted last-known-good normalized cache when live refresh fails and cache remains valid
```

Normal Exness/XAU session truth remains a separate broker-schedule concern.

A paid provider is not required.

## 3. Ownership

| Responsibility | Planned owner |
|---|---|
| provider resolution | app/main.py / config |
| session/news acquisition | app/session_news.py |
| local snapshot validation | app/session_news.py |
| LKG cache persistence/validation | app/session_news.py |
| event normalization/tier mapping | intelligence/news.py |
| hard market/pre-close/reopen permission | risk/permissions.py |
| News CLEAR/BLACKOUT/UNKNOWN composition | risk/permissions.py |
| final permission | execution Gate |

Providers cannot call the broker writer.

## 4. Scope validation

Every accepted provider snapshot/cache must match its intended account/server/resolved Gold symbol scope where scope applies, or the explicitly defined provider-global event scope.

Wrong-scope data is rejected.

## 5. Provider health versus usable event truth

Provider health vocabulary:

```text
VERIFIED
DEGRADED
STALE
UNAVAILABLE
UNKNOWN
```

Provider health and News truth are not identical.

```text
latest HTTP refresh failed
+ accepted cache remains valid
→ Provider Health = DEGRADED
→ News truth = accepted cached CLEAR/BLACKOUT/warmup state

latest refresh failed
+ cache expired/invalid/missing
→ provider unavailable/degraded
→ NEWS_SAFETY_UNKNOWN
```

## 6. Preserved TTL baseline

GoldSwingTraderAI's reference provider TTL baseline is preserved:

```text
SESSION_NEWS_TTL_SECONDS = 1800
```

This is an initial policy/configuration baseline, not a claim that every provider must update exactly every 30 minutes forever.

A later change requires a direct provider/scalp operational reason and governed documentation update.

## 7. Normalized event/cache fields

Preserve where applicable:

```text
provider identity
provider event ID
title/currency/scheduled UTC time
impact/tier
fetched_at_utc
as_of_utc
coverage_start / coverage_end
TTL / valid_until
scope
provider health
schema/mapping version
source LIVE_FETCH | LOCAL_FILE | LAST_KNOWN_GOOD_CACHE
payload/checksum identity where useful
```

Future fetch times or malformed timezones are rejected.

An empty event list means “no relevant events” only when a valid accepted provider positively supplied that result for the current coverage window.

## 8. LKG cache rules

A successful accepted calendar may be cached locally.

It is usable after refresh failure only if:

1. original provider result was valid;
2. schema/mapping version remains accepted;
3. scope remains correct;
4. current time lies inside accepted coverage;
5. original 1800-second/default configured TTL or valid-until has not expired;
6. payload integrity is intact;
7. no later positively known invalidating fact supersedes it.

On failure:

```text
keep prior accepted cache unchanged
record refresh failure separately
never rewrite fetched_at/as_of/valid_until
never extend TTL because the API failed
```

Expired cache becomes stale diagnostic/research context only.

## 9. Atomic publication

Any external/local producer should:

1. acquire/validate data;
2. build complete schema-versioned object;
3. write same-directory temporary UTF-8 file;
4. flush/close;
5. atomically replace accepted file/cache only after validation;
6. leave last accepted file untouched on acquisition failure;
7. never rewrite old timestamps to look fresh;
8. keep credentials outside file/repository.

## 10. Bounded network behaviour

Approved public adapter uses:

- HTTPS;
- bounded timeout;
- bounded response size;
- strict schema validation;
- UTC normalization;
- current-coverage validation;
- stable event IDs;
- bounded cache;
- at most small documented retry for specific stale-edge cases;
- no aggressive polling/retry loop.

## 11. Session versus News failure semantics

```text
known Market CLOSED + calendar failure
→ Market CLOSED preserved
→ cached News may independently remain usable or become UNKNOWN
→ entry blocked by market state

known Market OPEN + refresh failure + valid cache
→ Market OPEN preserved
→ accepted cached News truth used
→ Provider Health may be DEGRADED

known Market OPEN + refresh failure + invalid/expired/no cache
→ Market OPEN preserved
→ NEWS_SAFETY_UNKNOWN
→ scalp new-entry BLOCK / LIMITED

known blackout in accepted fresh/cache truth
→ BLACKOUT preserved
```

Provider failure never erases independent session truth.

## 12. Preserved normal session safety baseline

The provider/permission layer preserves these reference policy inputs unless current broker truth or a later specifically justified change supersedes them:

```text
Daily PRE_CLOSE     T-20 no new entry / T-10 mandatory flatten
Weekend PRE_CLOSE   T-60 no new entry / T-30 mandatory flatten
Daily reopen        1 clean completed M5
Weekend reopen      2 clean completed M5 + gap assessment
```

Normal Exness Gold schedule hours/DST/special holidays are external broker facts and must be verified during connected proof.

If exact altered holiday hours are unknown, session authority becomes UNKNOWN rather than inventing hours.

## 13. Restart/recovery

On restart:

- provider/session data is re-read/re-fetched where configured;
- existing LKG cache is revalidated from original timestamps/coverage;
- stale cache cannot become current merely because it exists;
- broker exposure is reconciled separately.

## 14. Research/replay

Record provider identity/health, source type, cache age/coverage, known blackout, UNKNOWN intervals and live/replay coverage differences.

Historical replay may use only event/cache truth causally available at the simulated time.

## 15. Failure matrix

| Condition | Result |
|---|---|
| current valid live/file calendar | accepted current event truth |
| refresh fails + valid LKG cache | use cache; provider DEGRADED |
| refresh fails + expired/invalid cache | NEWS UNKNOWN |
| known blackout in accepted truth | BLACKOUT |
| file invalid/scope mismatch + no fallback | UNKNOWN |
| future fetch time | reject |
| session schedule ambiguous | Session UNKNOWN independently |
| known altered holiday, no exact hours | Session UNKNOWN independently |

## 16. Dashboard

Show separately where practical:

```text
provider identity
provider health
source LIVE / FILE / CACHE
last successful refresh
cache age / valid-until
last refresh error
Market State
News State
next accepted event/countdown
```

Valid cached truth must not render UNKNOWN merely because newest refresh failed.

## 17. Planned implementation ownership

```text
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/intelligence/news.py
src/gold_scalp_trader/risk/permissions.py
```

## 18. Planned proof

Tests cover provider resolution, 1800-second baseline/config override semantics, schema/scope/TTL, atomic publication, live-success cache creation, refresh failure with valid cache, cache expiry → UNKNOWN, no timestamp laundering, known blackout preservation, restart revalidation, bounded retry and secret exclusion.

Connected evidence separately validates real provider reliability and current broker schedule behaviour.