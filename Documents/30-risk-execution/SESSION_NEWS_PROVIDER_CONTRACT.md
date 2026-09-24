# GoldScalpTrader — Session/News Provider Contract

**Status:** DRAFT PRE-CHALLENGE PROVIDER CONTRACT
**Version:** 0.1-scalp-session-news-provider
**Authority:** Session/news acquisition boundaries, normalization, provider health/freshness and permission inputs.

## 1. Purpose

Session and scheduled-news data must enter through governed provider boundaries rather than strategy code.

Provider data does not directly authorize an order.

Core invariants:

- independently known market/session truth remains separate from external News availability;
- missing/stale/unavailable News is never converted into `NEWS_CLEAR`;
- a known blackout remains hard according to the final state-machine policy;
- provider credentials never enter repository/runtime backup artifacts;
- final broker write still requires every other hard authority.

## 2. Provider topology

Draft provider resolution supports:

```text
explicit injected provider for tests/integration
→ configured local scoped session/news snapshot file
→ narrow built-in Exness/XAU normal-session provider
   + best-effort zero-cost public calendar when approved
```

The built-in/public path is a fallback, not institutional-grade event coverage.

A paid provider is not required for V1.

## 3. Ownership

| Responsibility | Planned owner |
|---|---|
| provider resolution | app/main.py / config |
| normal Exness XAU schedule acquisition | app/session_news.py |
| optional external acquisition/credentials | outside core runtime |
| local snapshot schema/scope validation | app/session_news.py |
| event normalization/tier mapping | intelligence/news.py |
| hard market/pre-close/reopen permission | risk/permissions.py |
| News UNKNOWN/blackout composition | risk/permissions.py |
| final permission | execution Gate |

Providers cannot call the broker writer.

## 4. Scope validation

Every accepted scoped snapshot must match the intended runtime scope, including at least:

```text
account identity
server
resolved Gold symbol
```

A snapshot for another account/server/symbol is invalid and becomes UNKNOWN, not reusable convenience data.

## 5. Provider health

Draft vocabulary:

```text
VERIFIED
DEGRADED
STALE
UNAVAILABLE
UNKNOWN
```

Provider health and event truth are related but not interchangeable.

A public-calendar fallback may be `DEGRADED` while normal broker-session facts remain independently usable.

## 6. Event freshness

Normalized provider data should preserve:

- provider identity;
- provider event ID;
- event title/currency;
- scheduled UTC time;
- impact/tier;
- fetched-at UTC;
- scope;
- provider health;
- TTL/freshness;
- mapping/schema version.

Future-dated fetch timestamps or malformed timezones are rejected.

An empty events list is accepted as “no relevant events” only when a fresh valid provider positively supplied that result. Missing data must not masquerade as an empty calendar.

## 7. Optional local file override

A local provider file may be used for exact schedule/event facts, especially altered/holiday hours.

Draft schema shape:

```text
schema_version
provider
provider_health
fetched_at_utc
scope { account, server, symbol }
session {
  tradeable
  schedule_verified
  next_close_utc / kind
  reopened_at_utc / kind
  clean_completed_m5_since_reopen
  execution_normalized
  unresolved_gap_or_reconciliation
  weekend_gap_assessed
  holiday_context
}
events [ ... ]
```

The file cannot override canonical event-tier or risk/execution policy silently.

## 8. Atomic external publication

If an external producer writes the local snapshot, it must:

1. acquire/validate data outside the trading process;
2. build a complete schema-versioned scoped object;
3. write a temporary UTF-8 file in the same directory;
4. flush/close it;
5. atomically replace the configured live snapshot;
6. leave the previous valid file untouched on acquisition failure;
7. never rewrite stale fetch time merely to look fresh;
8. keep credentials outside the file and repository.

## 9. Built-in Exness/XAU session fallback

The reference architecture contains a narrow Exness Gold normal-session fallback with DST-aware daily/weekend breaks and reopen warmup.

GoldScalpTrader preserves the **architecture**, not hard-coded schedule values as eternal truth.

Before freeze, official/current broker schedule evidence must validate:

- supported Exness server/symbol scope;
- daily break;
- Friday/weekend close;
- Sunday reopen;
- DST handling;
- special holiday uncertainty;
- pre-close and warmup policy inputs.

If the broker/symbol is unsupported or schedule truth is ambiguous, session authority becomes UNKNOWN.

## 10. Public calendar fallback

If a zero-cost public calendar is approved, it should use bounded defensive network behaviour:

- HTTPS only;
- bounded timeout;
- bounded response size;
- strict JSON/schema validation;
- UTC normalization;
- current-week coverage validation;
- stable internal event IDs;
- bounded cache;
- at most a small controlled retry strategy for known cache-staleness cases;
- failure → News UNKNOWN, never fabricated CLEAR.

No aggressive polling/retry loop is allowed.

## 11. Session versus News failure semantics

The state machine owns final policy, but the provider must make facts distinguishable:

```text
known Market CLOSED + News unavailable
→ Market CLOSED preserved
→ News UNKNOWN

known Market OPEN + News unavailable
→ Market OPEN preserved
→ News UNKNOWN
→ final entry treatment decided by SESSION_AND_RISK_STATE_MACHINE.md

known News blackout
→ BLACKOUT fact preserved
```

Provider failure must never erase independently verified broker-session facts.

## 12. Holiday/special hours

A positively known holiday/special context that may change XAU trading hours prevents blind use of normal schedule assumptions unless exact altered hours are separately known.

Missing public calendar does not itself prove a holiday.

## 13. Restart/recovery

Provider observations are current context, not durable broker truth.

On restart:

- session/news data is re-read/re-fetched;
- old cache cannot become new CLEAR merely because it existed before shutdown;
- broker positions are reconciled separately through MT5 recovery truth;
- old provider scope/freshness is validated again.

## 14. Research/replay

Research records:

- provider identity/health;
- event IDs and mapping version;
- known blackouts;
- UNKNOWN intervals;
- differences between live and replay coverage;
- schedule assumptions/version.

Historical replay may use only event truth that would have been knowable at the simulated time.

## 15. Failure matrix

| Condition | Provider result |
|---|---|
| current valid session + calendar | scoped facts available |
| known blackout | blackout fact |
| public calendar stale/unavailable | News UNKNOWN |
| session schedule ambiguous | Session UNKNOWN |
| file missing/invalid/scope mismatch | configured provider invalid/UNKNOWN |
| future fetch time | reject |
| unsupported broker/symbol | session provider UNKNOWN |
| known altered holiday, no hours | session UNKNOWN |

## 16. Dashboard

Show separately:

```text
provider identity
provider health
fetch age/TTL
Market State
News State
next known event / countdown
holiday/special schedule caution
exact provider/session reason
```

Provider `DEGRADED` must not be rendered as `VERIFIED`.

## 17. Planned implementation ownership

```text
src/gold_scalp_trader/app/session_news.py
src/gold_scalp_trader/intelligence/news.py
src/gold_scalp_trader/risk/permissions.py
```

## 18. Planned deterministic proof

Tests must cover:

- provider resolution order;
- file scope/schema/TTL validation;
- atomic snapshot semantics;
- stale/unavailable News remains UNKNOWN;
- independently known session truth survives calendar failure;
- known blackout preservation;
- current-week validation;
- bounded retry behaviour;
- holiday/special schedule uncertainty;
- restart does not reuse stale CLEAR;
- no credentials in snapshot files.

Connected broker/provider evidence separately validates real schedule/calendar behaviour.

## 19. Pre-challenge questions

- whether built-in public calendar should be enabled by default;
- final `OPEN + News UNKNOWN` entry policy;
- exact provider TTL/cache interval;
- official schedule source and maintenance process;
- holiday override workflow;
- event-tier mapping;
- whether any paid provider is ever worth supporting as optional only.
