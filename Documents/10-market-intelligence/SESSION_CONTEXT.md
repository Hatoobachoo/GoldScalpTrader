# GoldScalpTrader — Session Context

**Status:** DRAFT PRE-CHALLENGE INTELLIGENCE CONTRACT
**Version:** 0.1-scalp-session-context
**Authority:** Asia, London, New York and overlap context, chronological session ranges, transitions, participation context and soft session evidence.

## 1. Purpose and boundary

Session Context answers:

> Which participation window surrounds the current completed candles, what range has that session built, and how does the current scalp sit relative to that range?

This is soft market intelligence. It does not own broker OPEN/CLOSED/PRE_CLOSE state, reopen warmup, daily-loss lock or news blackout. Those are hard authorities in risk/execution.

## 2. Session-context flow

```text
UTC time + completed candles
→ DST-safe zone conversion
→ ASIA / LONDON / NEW_YORK / OVERLAP / OFF_HOURS
→ current + previous session range
→ transition/range context
→ SessionReport
→ Technical / Liquidity / Strategy / Timing
```

Broker schedule facts flow separately into the hard permission state machine.

## 3. Baseline session names

```text
ASIA
LONDON
NEW_YORK
LONDON_NY_OVERLAP
OFF_HOURS
```

Exact descriptive session hours remain configurable and DST-aware. They are not universal entry windows or hard vetoes.

## 4. Published facts

SessionReport should expose:

- current session label;
- current high/low/range from known completed candles only;
- previous session label and range where available;
- overlap flag;
- session transition context;
- optional holiday/participation caution;
- coverage;
- as-of timestamp and config/timezone version.

## 5. Why sessions matter more for a Gold scalper

Short-duration Gold behaviour can change materially around participation transitions.

Session context may explain:

- Asia compression/range formation;
- London sweep/expansion;
- London breakout failure/retest;
- New York continuation or reversal;
- London–New York overlap acceleration;
- target room relative to current/previous session extremes;
- spread/volatility transition risk around opens/closes.

These are analytical relationships, not guaranteed patterns.

## 6. Session range lifecycle

For each completed candle used by session analysis:

1. classify its time using DST-safe rules;
2. group only candles already known by the as-of time;
3. update the current session high/low/range;
4. expose the most recent previous session group;
5. preserve historical ranges without future revision at earlier replay timestamps.

A later candle may extend the live current-session range. It may not leak backward into an earlier replay decision.

## 7. Session extremes as liquidity/technical sources

Current/previous session highs/lows may be consumed by Technical/Liquidity only with explicit provenance and creation time.

A session extreme is not automatically support/resistance or a trade target. It is an observable range fact that another desk may interpret.

## 8. Soft session context versus hard broker schedule

The dashboard and domain model must keep these separate:

```text
Soft session: LONDON_NY_OVERLAP
Hard market state: OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
```

An analytical London label cannot prove that XAUUSDm is executable at this broker. A holiday caution does not itself mean the market is closed.

## 9. Scalping session specialization

The Strategy Floor may later use bounded session-specific evidence or family performance, but only after versioned replay/holdout proof.

The live system must not silently say “no Asia trades” or “only London trades” simply because historical averages look better without a governed policy decision.

## 10. Timeframe baseline

| Timeframe | Draft contribution |
|---|---|
| H1 | broad range/regime context |
| M15 | opportunity location versus session range/extremes |
| M5 | primary trigger/sweep/retest timing around session development |
| M1 | optional diagnostic transition context |

The normal SessionReport can be constructed from completed M5 chronology while other timeframe reports remain separate.

## 11. Holiday and transition context

Holiday context is descriptive unless hard broker schedule truth separately confirms altered hours.

Session transitions may be associated with wider spread or abrupt volatility. Actual hard spread/drift/market-open checks remain downstream.

## 12. Restart/replay

The report must rebuild deterministically from the same completed candles, as-of time, timezone database and SessionConfig.

Historical replay uses the same classification logic as production and stores the session/config version at each decision point.

## 13. Failure behaviour

| Condition | Result |
|---|---|
| naive/non-UTC timestamp | reject |
| no candles | no range, zero coverage |
| incomplete current session | valid partial range with coverage |
| holiday flag | descriptive caution only |
| broker schedule unavailable | hard permission UNKNOWN elsewhere; soft label can still exist |

## 14. Dashboard visibility

The operator view should show separately:

```text
Soft Session      ASIA / LONDON / NEW_YORK / OVERLAP
Current Range     high-low
Previous Range    high-low
Transition        normal / opening / overlap / off-hours
Holiday Context   none / caution / unknown
Hard Market       OPEN / PRE_CLOSE / CLOSED / WARMUP / UNKNOWN
```

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/session.py
src/gold_scalp_trader/intelligence/snapshot.py
src/gold_scalp_trader/risk/permissions.py   # hard market state only
```

## 16. Planned proof

Tests must cover DST-aware labels, overlap, current/previous range chronology, no-lookahead session ranges, holiday separation, session-extreme provenance and soft-versus-hard state separation.

Actual broker schedule and special holiday acceptance remain connected/external evidence.

## 17. Pre-challenge calibration

Open items: exact session boundaries, transition windows, session-specific strategy weights, whether Asia setups are retained equally, overlap specialization, prior-session range lookback and whether session conditioning improves out-of-sample expectancy after costs.
