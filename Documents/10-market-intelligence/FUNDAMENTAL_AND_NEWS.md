# GoldScalpTrader — Fundamental and News Intelligence

**Status:** FROZEN V1 NEWS INTELLIGENCE ARCHITECTURE — EVENT MAPPING/WINDOW CALIBRATION PENDING
**Version:** 1.0-cache-resilient-news
**Authority:** Gold/USD macro context, scheduled-event facts, provider health/freshness, last-known-good calendar semantics, blackout inputs and post-event stabilization.

## 1. Purpose

News/fundamental information enters through three distinct meanings:

1. factual scheduled-event truth;
2. optional soft macro interpretation;
3. known event-blackout safety input.

Provider code never places an order. Missing data never becomes fake `NEWS_CLEAR`.

## 2. Authority split

| Information | Owner | May influence | Must never do |
|---|---|---|---|
| USD/rates/yields/Fed/inflation/risk context | intelligence | explanation/bounded support | override price structure alone |
| Scheduled event fact | intelligence/news | tier/window/research | place trade |
| Provider freshness/scope/cache validity | provider + normalizer | CLEAR/BLACKOUT/UNKNOWN truth | silently mean “no news” |
| Broker session/reopen | session/permissions | hard market state | be inferred from missing event data |
| Known event blackout | risk/permissions | hard new-entry block | bypass event mapping/versioning |
| Final execution permission | central Gate | allow/block action | bypass identity/risk/controller/execution checks |

## 3. Frozen V1 News safety rule

Session and News remain separate sub-authorities.

```text
Market CLOSED + News unavailable
→ new entry blocked by Market state

Market OPEN + fresh provider/calendar truth
→ classify CLEAR / BLACKOUT / POST_NEWS_WARMUP

Market OPEN + provider/API fetch failure
+ last-known-good scoped calendar still valid inside approved TTL/coverage window
→ continue using that exact cached event truth
→ provider health may be DEGRADED
→ do NOT manufacture NEWS_UNKNOWN merely because the latest refresh failed

Market OPEN + provider/API fetch failure
+ no valid last-known-good cache, or cache expired/stale/scope-invalid/current-week-invalid
→ NEWS_SAFETY_UNKNOWN
→ V1 new-entry BLOCK / LIMITED
```

A cache may preserve already-verified event truth; it may never refresh its own timestamp or pretend stale data is current.

## 4. Provider topology

The runtime uses a normalized provider boundary rather than embedding provider-specific semantics inside strategies.

Candidate zero-cost inputs include:

- approved local scoped JSON/calendar snapshot;
- bounded best-effort public economic-calendar adapter;
- last-known-good normalized cache from a previously successful current-coverage fetch;
- later optional adapters that do not become mandatory paid dependencies.

Provider credentials never enter the repository or normal backup artifacts.

## 5. Event normalization

A scheduled event fact preserves at least:

```text
provider_event_id
title
currency
scheduled_at_utc
impact/tier
provider identity/health
fetched_at_utc
as_of_utc
freshness TTL / valid-until semantics
coverage window
mapping/schema version
source = LIVE_FETCH | LOCAL_FILE | LAST_KNOWN_GOOD_CACHE
```

Timestamps are timezone-aware UTC. Stable IDs support deduplication.

Malformed, future-dated, stale, unsupported or wrong-scope data is not accepted as current event truth.

## 6. Last-known-good cache contract

The cache exists to avoid making a temporary API/network failure a needless trading kill-switch while preserving conservative stale-data safety.

A cached calendar is usable only when all applicable checks pass:

- it came from a previously accepted provider response/file;
- schema/mapping version is accepted;
- intended runtime scope matches;
- fetch/as-of time is causal and not future-dated;
- current calendar coverage is still valid for the decision time;
- configured TTL/valid-until boundary has not expired;
- payload integrity is intact;
- no later positively known invalidation/holiday/schedule fact supersedes it.

A failed refresh does **not** rewrite `fetched_at_utc`, `as_of_utc`, coverage or event times.

When validity expires, the cache becomes stale context only and V1 News state becomes UNKNOWN unless another accepted source provides current truth.

## 7. Event tiers

The architecture retains conceptual tiers such as:

```text
TIER_1  critical Gold/USD shock risk
TIER_2  high-impact USD risk
TIER_3  contextual event
```

Exact title/category mapping remains versioned and calibration/governance controlled. Free-text matching cannot silently create a new hard rule.

## 8. Blackout and post-news windows

The Swing reference mechanism is preserved, but exact durations are not copied as scalp truth.

Scalping is more sensitive to spread/slippage/immediate dislocation. Final policy calibrates:

```text
pre_event_blackout
post_event_blackout
post_news_warmup
clean completed-M5 requirement
spread/quote/volatility normalization
```

A scheduled event ending does not itself prove execution normalized.

## 9. Optional macro context

DXY/USD direction, yields/rate expectations, Fed policy, inflation/labour/growth and reliable risk/geopolitical context remain optional soft evidence with source/time/TTL/confidence/counter-evidence.

They cannot create broker authority or reverse clear price structure alone.

V1 does not require a paid macro API.

## 10. Unscheduled shocks

Calendar truth is inherently incomplete. Independent market/execution safety still handles:

- abrupt spread expansion;
- quote gaps;
- extreme velocity/dislocation;
- stale feed;
- excessive executable drift;
- broker rejection/requote behaviour.

News intelligence never claims complete breaking-news awareness.

## 11. Existing positions

Known blackout or News UNKNOWN primarily affects **new entries/re-entries**.

Existing verified bot trade protection, governed MODIFY and necessary risk-reducing CLOSE remain action-sensitive. News-provider failure alone must not trap unwanted exposure.

## 12. Restart/replay

Restart revalidates any cached provider data against current time, scope, schema and coverage. An old cache does not become fresh because the process restarted.

Replay may use only event/provider/cache truth knowable at the simulated timestamp. Later calendar revisions must not leak backward.

## 13. Dashboard / diagnostics

Show separately where useful:

```text
Market State
News State
Provider identity + health
Source LIVE / FILE / LKG CACHE
Last successful refresh
Cache age / valid-until
Next accepted event + tier + countdown
Refresh error if present
Entry Permission from owning authority
```

`DEGRADED + VALID CACHE` is different from `NEWS_UNKNOWN`.

## 14. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/news.py
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 15. Planned proof

Tests must cover normalization/deduplication, TTL/coverage, accepted last-known-good reuse after refresh failure, no timestamp laundering, cache expiry → UNKNOWN, scope/schema mismatch rejection, known blackout preservation, restart revalidation and replay no-lookahead.

Provider reliability and real-event execution remain external/calibration evidence.

## 16. Explicit non-goals

This layer must not place orders, claim complete real-time news coverage, convert provider failure to CLEAR, extend cache validity by rewriting timestamps, use wrong-scope cache, fabricate broker OPEN/CLOSED or force-close merely because an event is scheduled.

## 17. Calibration pending

Exact Tier mappings, provider/cache TTL, proactive refresh cadence, pre/post blackout duration, post-news normalization and default zero-cost provider selection remain evidence/configuration questions.