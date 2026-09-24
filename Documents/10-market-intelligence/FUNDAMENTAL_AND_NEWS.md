# GoldScalpTrader — Fundamental and News Intelligence

**Status:** DRAFT PRE-CHALLENGE INTELLIGENCE CONTRACT
**Version:** 0.1-scalp-news
**Authority:** Gold/USD macro context, scheduled-event facts, provider health, event windows, post-event stabilization and news-safety input semantics.

## 1. Purpose

News/fundamental information enters the system through distinct meanings:

1. factual scheduled-event data;
2. optional soft macro interpretation;
3. known event-blackout safety.

The first two are intelligence. Hard entry blocking for known event windows belongs to the permission state machine. Provider code never places an order and missing data never becomes fake `NEWS_CLEAR`.

## 2. Authority split

| Information | Owner | May influence | Must never do |
|---|---|---|---|
| USD/rates/yields/Fed/inflation/risk context | intelligence | explanation/bounded support | override contrary price structure alone |
| Scheduled event fact | intelligence/news | tier/window/research | place trade |
| Provider freshness/scope | provider + normalizer | NEWS_UNKNOWN/degraded truth | silently mean “no news” |
| Broker session/reopen | session/permissions | hard market state | be inferred from missing event data |
| Known event blackout | risk/permissions | hard new-entry block | bypass event mapping/versioning |
| Final execution permission | central gate | allow/block action | bypass identity/risk/controller/execution checks |

## 3. Independent session and news truth

Session and News must remain separate sub-authorities.

Examples:

```text
Market CLOSED + News UNKNOWN
→ new entry blocked because market is CLOSED

Market OPEN + News UNKNOWN
→ analytical floor may continue
→ final treatment of new entry follows the approved news-unknown policy

Market OPEN + News BLACKOUT
→ analysis may continue
→ new broker entry blocked for the known window
```

The baseline inherits the reference principle that provider degradation stays visible and does not erase independently known market-session truth.

## 4. Provider topology

The project should support a normalized provider boundary rather than embedding provider-specific semantics into strategies.

Possible sources include:

- operator-supplied scoped local JSON/calendar data;
- a zero-cost/best-effort public calendar adapter if approved;
- later optional source adapters that do not introduce required paid dependencies.

No provider credential is stored in the repository.

## 5. Input normalization

A scheduled event fact should preserve:

```text
provider_event_id
title
currency
scheduled_at_utc
impact/tier
provider identity/health
fetched_at_utc
as_of_utc
freshness TTL
mapping version
```

Timestamps are timezone-aware UTC and event IDs are stable enough for deduplication.

Malformed, stale or unsupported provider data remains explicit UNKNOWN/DEGRADED truth.

## 6. Event tiers

The initial architecture retains three conceptual classes:

```text
TIER_1  critical Gold/USD shock risk
TIER_2  high-impact USD risk
TIER_3  contextual event
```

Examples may include Fed decisions/speeches, CPI, NFP, PCE, GDP, PPI, ISM, retail sales and labour releases.

Exact mapping is versioned and challengeable. Free-text matching must not quietly create undocumented hard rules.

## 7. Blackout windows are not frozen yet

The Swing reference used defined Tier-1/Tier-2 before/after windows. GoldScalpTrader will preserve the mechanism but **not blindly freeze the same durations**.

Scalping is more sensitive to spread, slippage and immediate post-release dislocation, so blackout/warmup duration requires dedicated replay plus connected DEMO evidence.

The policy contract must eventually define:

```text
pre_event_blackout
post_event_blackout
post_news_warmup
required clean completed bars and/or stable spread condition
```

Until frozen, these are open calibration/policy items.

## 8. Post-news stabilization

A scheduled event ending does not prove that execution conditions normalized.

The final design may require some combination of:

- elapsed post-event time;
- at least one clean completed M5 bar;
- spread returning below an approved threshold;
- quote freshness;
- absence of dislocated volatility;
- fresh non-chased structural opportunity.

No single criterion is assumed final before challenge.

## 9. Optional macro context

Optional macro inputs may later include DXY/USD direction, yields/rate expectations, Fed policy, inflation/labour/growth and reliable risk/geopolitical context.

These remain soft evidence with source/fetch time/TTL/confidence and counter-evidence. They cannot create broker authority or reverse clear price structure by themselves.

The initial project must not depend on a commercial macro API.

## 10. Unscheduled shocks

Calendar truth is incomplete by nature. Unscheduled moves still have to be handled through independent market/execution safety:

- abrupt spread expansion;
- quote gaps;
- extreme velocity/dislocation;
- stale feed;
- executable drift;
- broker rejection/requote behaviour.

News intelligence must not pretend to provide complete breaking-news awareness.

## 11. Existing positions

A known news blackout primarily blocks new entries. It does not automatically force-close every existing managed trade.

Trade Manager and hard market/session safety own protective management/exit policy. PRE_CLOSE or other hard safety may independently require flattening.

News UNKNOWN must never block necessary risk-reducing management solely because an optional provider is degraded.

## 12. Restart/replay

Restart refreshes current provider facts and cannot reuse expired `NEWS_CLEAR` beyond its TTL.

Historical replay may only use event/provider facts knowable at the simulated timestamp. Later calendar revisions cannot leak backward.

Any research claim involving news must state provider coverage and UNKNOWN periods.

## 13. Dashboard/research visibility

Operator view should expose separately:

```text
Market State      OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
News State        CLEAR / BLACKOUT / UNKNOWN / POST_NEWS_WARMUP
Provider          identity + health + freshness
Next Event        title + tier + countdown
Reason            stable explicit reason
Entry Permission  ALLOW / BLOCK / UNKNOWN from owning authority
```

Research stores event IDs/windows, mapping version, provider health, as-of/fetch timestamps and whether the event affected hard permission or only soft context.

## 14. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/news.py
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 15. Planned proof

Tests must cover event normalization/deduplication, TTL/freshness, tier mapping, overlapping windows, independent session/news truth, provider failure without fake CLEAR, known blackout hard block, restart expiry and replay no-lookahead.

Actual provider reliability, broker holiday schedules and real-event execution conditions remain external/calibration evidence.

## 16. Explicit non-goals

This desk must not place orders, claim complete real-time breaking-news coverage, make macro opinion a hard directional rule, convert provider failure to CLEAR, fabricate broker OPEN/CLOSED or force-close merely because an event is scheduled.

## 17. Pre-challenge questions

- exact Tier-1/Tier-2 event mappings;
- pre/post blackout durations for scalping;
- spread/volatility stabilization requirements;
- how News UNKNOWN affects new entries in V1;
- whether any public provider is reliable enough for default use;
- historical news dataset strategy for replay;
- whether optional macro context earns measurable out-of-sample value.
