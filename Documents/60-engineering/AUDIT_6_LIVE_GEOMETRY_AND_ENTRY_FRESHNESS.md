# GoldScalpTrader — Audit 6: Live Geometry and Entry Freshness

**Status:** DRAFT CORRECTIVE AUDIT PROTOCOL — NOT RUN
**Version:** 0.1-scalp-live-geometry-freshness
**Authority:** Review/correction of live technical-zone, liquidity, structural-level, strategy-context and executable-entry freshness defects.

## 1. Scope

Run after connected observation reveals no-trade/false-ready/late-entry behaviour that may be caused by stale geometry rather than the final Gate.

This audit never lowers monetary risk or structural quality merely to increase entries.

## 2. Technical-zone review

For every zone near current price verify:

- causal source swing/event;
- confirmation time;
- lifecycle state ACTIVE/WEAKENING/BROKEN/RETEST/RECLAIMED/CONSUMED/STALE;
- whether a confirmed break incorrectly leaves old same-side support/resistance live;
- whether a polarity-changing retest candidate is represented correctly;
- whether target room ignores a consumed/broken obstacle.

## 3. Liquidity review

Verify:

- pool existed before interaction;
- sweep/probe/accepted-break chronology;
- pool lifecycle after consumption;
- FVG third-candle knowledge time;
- OB qualification time;
- session/prior-range source provenance;
- path is not crowded by already-consumed/fake pools.

## 4. Strategy-context review

A FamilyReport/Opportunity must not carry stale supporting event identity indefinitely.

Check:

- source family remains valid;
- event timestamps survive through Fusion/Opportunity/TradePlan;
- same thesis does not get fresh ID on each poll;
- MISSED/terminal identity does not re-arm without new event;
- correlated labels do not inflate freshness/score.

## 5. Entry-freshness review

For each analytical ENTER/WAIT/MISSED record:

```text
latest event age
distance travelled since event
M5 extension/momentum
approved entry drift
spread/cost context
remaining target room
processing time
time since plan creation/rebuild
```

Determine whether the correct outcome should have been ENTER, WAIT, MISSED or INVALID under frozen policy.

## 6. M1/tick boundary

If final architecture keeps M1 diagnostic-only, confirm no hidden M1 authority slipped into strategy/TradePlan.

If fresh-zero audit promotes M1, confirm ownership/knowledge time/test/replay semantics are explicit rather than accidental.

Quote/tick data may determine executable condition but cannot retroactively rewrite structural history.

## 7. Corrective evidence

A correction needs:

- exact observed incident/replay evidence;
- documented owner mismatch/defect;
- focused regression test;
- replay no-lookahead test;
- affected Documents sync;
- no reduction in Risk/Gate safety.

## 8. Current state

```text
AUDIT RESULT: NOT RUN
No connected live-geometry/freshness correction has been performed yet.
```
