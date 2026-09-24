# GoldScalpTrader — Session/News Provider Contract

**Status:** FROZEN V1 PROVIDER ARCHITECTURE — SOURCE/TTL CALIBRATION AND EXTERNAL PROOF PENDING
**Version:** 1.0-last-known-good-cache
**Authority:** Session/news acquisition, normalization, provider health/freshness, bounded last-known-good cache and permission inputs.

## 1. Purpose

Session and scheduled-news data enter through governed provider boundaries rather than strategy code.

Providers do not directly authorize broker actions.

Core invariants:

- independently known broker/session truth remains separate from external News availability;
- known blackout remains hard according to the state machine;
- missing/stale News is never renamed CLEAR;
- a temporary API/network refresh failure does not erase still-valid previously verified event truth;
- credentials never enter repository/runtime-backup artifacts;
- final broker action still requires every other hard authority.

## 2. Provider resolution

V1 architecture supports:

```text
explicit injected provider for tests/integration
→ configured local scoped session/news snapshot file
→ approved zero-cost/best-effort calendar adapter
→ last-known-good normalized cache when live refresh fails and cache is still valid
```

Normal Exness/XAU session truth remains a separate broker-schedule concern.

A paid provider is not required for V1.

## 3. Ownership

| Responsibility | Planned owner |
|---|---|
| provider resolution | app/main.py / config |
| session/news acquisition | app/session_news.py |
| local snapshot validation | app/session_news.py |
| last-known-good cache validation | app/session_news.py |
| event normalization/tier mapping | intelligence/news.py |
| hard market/pre-close/reopen permission | risk/permissions.py |
| News CLEAR/BLACKOUT/UNKNOWN composition | risk/permissions.py |
| final permission | execution Gate |

Providers cannot call the broker writer.

## 4. Scope validation

Every accepted provider snapshot/cache must match the intended runtime scope where scope applies, including account/server/resolved Gold symbol or the explicitly defined provider-global event scope.

Wrong-scope data is rejected. It is never reused for convenience.

## 5. Provider health versus usable event truth

Provider health vocabulary may include:

```text
VERIFIED
DEGRADED
STALE
UNAVAILABLE
UNKNOWN
```

Provider health and current event truth are not identical.

Example:

```text
latest HTTP refresh failed
+ previous accepted calendar remains inside valid TTL/coverage
→ Provider health = DEGRADED
→ Event truth = usable from LAST_KNOWN_GOOD_CACHE

latest HTTP refresh failed
+ cache expired/stale/invalid
→ Provider health = UNAVAILABLE/DEGRADED
→ Event truth = NEWS_SAFETY_UNKNOWN
```

## 6. Normalized event/cache fields

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

An empty event list means “no relevant events” only when a fresh accepted provider positively supplied that result for the current coverage window.

## 7. Last-known-good cache rules

A successful accepted calendar may be cached locally for bounded reuse.

The cache is usable after a refresh/API failure only if:

1. original provider result was valid;
2. schema/mapping version remains accepted;
3. scope remains correct;
4. current decision time lies inside accepted coverage;
5. TTL/valid-until has not expired;
6. payload integrity is intact;
7. no later positively known invalidating fact supersedes it.

On refresh failure:

```text
keep prior valid cache unchanged
record refresh failure separately
never rewrite fetched_at/as_of/valid_until
never extend TTL because the API failed
```

When cache validity expires, it becomes stale diagnostic/research context only and cannot support NEWS_CLEAR.

## 8. Atomic local snapshot/cache publication

Any external/local producer should:

1. acquire/validate data;
2. build a complete schema-versioned object;
3. write a same-directory temporary UTF-8 file;
4. flush/close it;
5. atomically replace the live accepted file/cache only after validation;
6. leave the last accepted file untouched on acquisition failure;
7. never rewrite old timestamps merely to look fresh;
8. keep credentials outside the file/repository.

## 9. Bounded network behaviour

An approved zero-cost public calendar adapter uses defensive network behaviour:

- HTTPS;
- bounded timeout;
- bounded response size;
- strict schema validation;
- UTC normalization;
- current-coverage validation;
- stable event IDs;
- bounded cache;
- at most a small documented retry for specific stale-edge cases;
- no aggressive polling/retry loop.

Repeated failure does not trigger high-frequency retries.

## 10. Session versus News failure semantics

```text
known Market CLOSED + calendar refresh failure
→ Market CLOSED preserved
→ cached News may remain usable or become UNKNOWN independently
→ new entry remains BLOCKED by market state

known Market OPEN + calendar refresh failure + valid cache
→ Market OPEN preserved
→ use cached accepted CLEAR/BLACKOUT/post-event truth
→ provider health DEGRADED may be visible

known Market OPEN + calendar refresh failure + invalid/expired cache
→ Market OPEN preserved
→ NEWS_SAFETY_UNKNOWN
→ V1 new-entry BLOCK / LIMITED

known blackout in valid cache/current provider truth
→ BLACKOUT preserved
```

Provider failure never erases independent session truth.

## 11. Holiday / special hours

A positively known holiday/special context that may alter XAU hours prevents blind normal-schedule assumptions unless exact altered broker hours are known.

A missing calendar alone does not prove a holiday.

## 12. Restart/recovery

On restart:

- provider/session data is re-read/re-fetched where configured;
- existing last-known-good cache is revalidated from original timestamps/coverage;
- stale cache cannot become current CLEAR merely because it exists;
- broker exposure is reconciled separately.

## 13. Research/replay

Record provider identity/health, source type, cache age/coverage, known blackout, UNKNOWN intervals and live/replay coverage differences.

Historical replay may use only event/cache truth causally available at the simulated time.

## 14. Failure matrix

| Condition | News/provider result |
|---|---|
| current valid live/file calendar | current accepted event truth |
| refresh fails + valid LKG cache | use cache; provider degraded |
| refresh fails + expired/invalid cache | NEWS UNKNOWN |
| known blackout in accepted current/cache truth | BLACKOUT |
| file missing/invalid/scope mismatch with no valid fallback | UNKNOWN |
| future fetch time | reject |
| session schedule ambiguous | Session UNKNOWN independently |
| known altered holiday, no exact hours | Session UNKNOWN independently |

## 15. Dashboard

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

`DEGRADED` must not render as `VERIFIED`; valid cached truth must not render as UNKNOWN merely because the most recent refresh failed.

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/intelligence/news.py
src/gold_scalp_trader/risk/permissions.py
```

## 17. Planned proof

Tests must cover provider resolution, schema/scope/TTL, atomic publication, live-success cache creation, refresh failure with still-valid cache, cache expiry → UNKNOWN, no timestamp laundering, known blackout preservation, restart revalidation, bounded retry and secret exclusion.

Connected evidence separately validates real provider reliability and broker schedule behaviour.

## 18. Calibration / implementation choices pending

Exact provider selection, cache persistence format/path, cache TTL/refresh cadence, holiday workflow, event-tier mapping and any optional commercial adapter remain configuration/calibration choices. The architectural fallback semantics above are frozen.