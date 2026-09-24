# GoldScalpTrader — Fundamental and News Intelligence

**Status:** FROZEN V1 NEWS INTELLIGENCE ARCHITECTURE — EVENT-MAPPING / SCALP WINDOW CALIBRATION PENDING
**Version:** 1.1-preserved-ttl-cache-resilient-news
**Authority:** Gold/USD macro context, scheduled-event facts, provider health/freshness, last-known-good calendar semantics, blackout inputs and post-event stabilization.

## 1. Purpose

News/fundamental information enters through three meanings:

1. factual scheduled-event truth;
2. optional soft macro interpretation;
3. known event-blackout safety input.

Provider/intelligence code never places orders. Missing data never becomes fake `NEWS_CLEAR`.

## 2. Authority split

| Information | Owner | May influence | Must never do |
|---|---|---|---|
| USD/rates/yields/Fed/inflation/risk context | intelligence | explanation/bounded support | override price structure alone |
| scheduled event fact | intelligence/news | tier/window/research | place trade |
| provider freshness/scope/cache validity | provider + normalizer | CLEAR/BLACKOUT/UNKNOWN truth | silently mean “no news” |
| broker session/reopen | session/permissions | hard market state | be inferred from missing event data |
| known event blackout | risk/permissions | hard new-entry block | bypass event mapping/versioning |
| final execution permission | central Gate | allow/block action | bypass identity/Risk/controller/execution |

## 3. News safety rule

```text
Market CLOSED + News unavailable
→ entry blocked by Market state

Market OPEN + fresh accepted provider truth
→ classify CLEAR / BLACKOUT / POST_NEWS_WARMUP

Market OPEN + refresh failure
+ accepted LKG calendar remains valid inside original scope/schema/coverage/TTL
→ use exact cached event truth
→ Provider Health may be DEGRADED

Market OPEN + refresh failure
+ no valid current cache
→ NEWS_SAFETY_UNKNOWN
→ new scalp entry BLOCK / LIMITED
```

A cache may preserve already-verified truth; it may never refresh its own timestamp or validity.

## 4. Preserved provider TTL baseline

GoldSwingTraderAI's baseline remains the starting policy:

```text
SESSION_NEWS_TTL_SECONDS = 1800
```

This 1800-second TTL is **not reopened merely because this is a scalper**. A later change requires a direct provider/scalp operational reason and governed affected-graph update.

Proactive refresh cadence and provider-specific acquisition behavior may be implementation choices, but failed acquisition never extends the original TTL.

## 5. Provider topology

Candidate zero-cost inputs:

- approved local scoped JSON/calendar snapshot;
- bounded best-effort public economic-calendar adapter;
- accepted LKG normalized cache;
- later optional adapters that do not become mandatory paid dependencies.

Provider credentials never enter repository or normal backup artifacts.

## 6. Event normalization

Preserve at least:

```text
provider_event_id
title
currency
scheduled_at_utc
impact/tier
provider identity/health
fetched_at_utc
as_of_utc
TTL / valid_until
coverage window
mapping/schema version
source LIVE_FETCH | LOCAL_FILE | LAST_KNOWN_GOOD_CACHE
```

Malformed, future-dated, stale, unsupported or wrong-scope data is not current event truth.

## 7. LKG cache contract

Cached calendar is usable after refresh failure only when:

- original result was accepted;
- schema/mapping version remains accepted;
- scope remains correct;
- decision time remains inside accepted coverage;
- original configured TTL/valid-until (baseline 1800s unless governed override) has not expired;
- integrity is intact;
- no later known invalidating fact supersedes it.

On failure:

```text
keep accepted cache unchanged
record acquisition failure separately
never rewrite fetched_at/as_of/valid_until
never extend TTL because provider failed
```

Expired cache becomes stale diagnostic/research context only.

## 8. Event tiers

Conceptual tiers remain:

```text
TIER_1  critical Gold/USD shock risk
TIER_2  high-impact USD risk
TIER_3  contextual event
```

Exact title/category mapping remains versioned. Free-text matching cannot silently create new hard policy.

## 9. Blackout / post-news windows

The reference blackout/warmup **mechanism** is preserved. Exact durations may be a genuine scalp-specific calibration because short target horizons are more sensitive to immediate spread/slippage/dislocation.

Final scalp evidence may calibrate:

```text
pre_event_blackout
post_event_blackout
post_news_warmup
clean completed-M5 requirement
spread/quote/volatility normalization
```

A scheduled event ending does not prove execution normalized.

## 10. Optional macro context

DXY/USD direction, yields/rate expectations, Fed policy, inflation/labour/growth and reliable risk/geopolitical context remain optional soft evidence with source/time/TTL/confidence/counter-evidence.

They cannot create broker authority or reverse clear price structure alone. No paid macro API is mandatory.

## 11. Unscheduled shocks

Independent market/execution safety still handles abrupt spread expansion, quote gaps, extreme velocity/dislocation, stale feed, excessive executable drift and broker rejection/requote behavior.

News intelligence never claims complete breaking-news awareness.

## 12. Existing positions

Known blackout or News UNKNOWN primarily blocks **new entry/re-entry**. Existing verified bot-trade protection, governed MODIFY and necessary risk-reducing CLOSE remain action-sensitive.

## 13. Restart/replay

Restart revalidates cached data against original time/scope/schema/coverage/TTL. Replay uses only event/provider/cache truth knowable at simulated timestamp; later revisions never leak backward.

## 14. Dashboard / diagnostics

Show Market State, News State, provider identity/health, LIVE/FILE/LKG source, last success, cache age/valid-until, next event/tier/countdown, refresh error and downstream Entry Permission.

`DEGRADED + VALID CACHE` is not `NEWS_UNKNOWN`.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/news.py
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 16. Planned proof

Tests cover normalization/deduplication, preserved 1800s baseline, scope/schema/coverage, LKG reuse, no timestamp laundering, cache expiry → UNKNOWN, known blackout preservation, restart revalidation and replay no-lookahead.

## 17. Pending scalp/external evidence

Exact Tier mappings, pre/post-event blackout durations, post-news stabilization, default zero-cost provider and provider reliability remain evidence/configuration questions. The 1800-second baseline itself remains preserved until a specifically justified change packet supersedes it.