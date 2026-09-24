# GoldScalpTrader — Session Context

**Status:** FROZEN V1 INTELLIGENCE ARCHITECTURE — SESSION-CONDITIONING CALIBRATION / BROKER-SCHEDULE PROOF PENDING
**Version:** 1.0-scalp-session-context
**Authority:** Asia, London, New York and overlap context, chronological session ranges, transitions, participation context and soft session evidence.

## 1. Purpose and boundary

Session Context answers:

> Which participation window surrounds the current completed candles, what range has that session built, and how does the current scalp sit relative to that range?

This is soft intelligence. It does not own broker OPEN/CLOSED/PRE_CLOSE state, reopen warmup, daily-loss lock or News blackout. Those are hard authorities downstream.

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

Broker schedule facts flow separately to hard permission state machine.

## 3. Session names

```text
ASIA
LONDON
NEW_YORK
LONDON_NY_OVERLAP
OFF_HOURS
```

Descriptive session hours remain configurable/DST-aware. They are not universal entry windows or hard vetoes.

## 4. Published facts

SessionReport exposes where available:

- current session label;
- current high/low/range from known completed candles;
- previous session/range;
- overlap flag;
- transition context;
- optional holiday/participation caution;
- coverage;
- as-of timestamp and config/timezone version.

## 5. Why sessions matter to a Gold scalper

Short-duration Gold behaviour can change around participation transitions. Context may explain Asia compression/range formation, London sweep/expansion, breakout failure/retest, New York continuation/reversal, overlap acceleration, room relative to session extremes and spread/volatility transitions.

These are analytical relationships, not guaranteed patterns.

## 6. Session range lifecycle

For each completed candle:

1. classify time with DST-safe rules;
2. group only candles knowable by as-of time;
3. update current-session range;
4. expose most recent previous-session group;
5. preserve historical range truth without later-bar leakage.

A later candle may extend the live current range; it may not leak backward into earlier replay decisions.

## 7. Session extremes as technical/liquidity sources

Current/previous session highs/lows may be consumed only with explicit provenance and creation time. A session extreme is observable range fact, not automatic support/resistance/target.

## 8. Soft session versus hard broker schedule

```text
Soft Session:      LONDON_NY_OVERLAP
Hard Market State: OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
```

An analytical London label cannot prove XAUUSDm is executable. Holiday caution does not itself mean market closed.

Hard state uses the preserved baseline session policy from `SESSION_AND_RISK_STATE_MACHINE.md` while current broker schedule/DST/holiday truth still requires connected proof.

## 9. Scalping session specialization

The Strategy Floor may later use bounded session-specific evidence/performance only after replay/holdout proof. Live policy cannot silently prohibit Asia or force London-only trading from descriptive averages.

## 10. Frozen timeframe contribution

| Timeframe | Contribution |
|---|---|
| H1 | broad range/regime context |
| M15 | opportunity location versus session range/extremes |
| M5 | primary trigger/sweep/retest timing around session development |
| H4 | optional major context where relevant |
| M1 | diagnostic/research transition context only |

M1 is not production timing authority under current V1.

## 11. Holiday and transition context

Holiday context is descriptive unless hard broker schedule truth confirms altered hours. Session transitions may associate with wider spread/volatility; actual hard spread/drift/market-open checks remain downstream.

## 12. Restart/replay

Report rebuilds deterministically from same completed candles, as-of time, timezone database and SessionConfig. Replay uses same classification logic and stores config version.

## 13. Failure behaviour

| Condition | Result |
|---|---|
| naive/non-UTC timestamp | reject |
| no candles | no range / zero coverage |
| incomplete current session | valid partial range + coverage |
| holiday flag | descriptive caution only |
| broker schedule unavailable | hard permission UNKNOWN elsewhere; soft label may still exist |

## 14. Dashboard visibility

Show Soft Session, current/previous range, transition, holiday context and separate hard Market State. Presentation never derives hard broker schedule from soft session label.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/session.py
src/gold_scalp_trader/intelligence/snapshot.py
src/gold_scalp_trader/risk/permissions.py   # hard market state only
```

## 16. Planned proof

Tests cover DST-aware labels, overlap, chronological current/previous ranges, no-lookahead, holiday separation, session-extreme provenance, frozen timeframe roles and soft-versus-hard state separation.

Actual broker schedule/special-holiday behavior remains connected external evidence.

## 17. Scalp calibration pending

Descriptive session boundaries/transition windows where configurable, session-specific strategy conditioning, overlap specialization and prior-session lookback remain evidence questions. Preserved hard PRE_CLOSE/reopen policy is not silently reopened by this soft intelligence document.