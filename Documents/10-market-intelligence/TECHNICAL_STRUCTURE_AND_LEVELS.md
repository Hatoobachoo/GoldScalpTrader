# GoldScalpTrader — Technical Structure and Levels

**Status:** DRAFT PRE-CHALLENGE LOCATION CONTRACT
**Version:** 0.1-scalp-location-and-room
**Authority:** Support/resistance zones, structural level lifecycle, scalp location quality, target room, causal trendlines, Fibonacci geometry and broker-local volume-profile context.

## 1. Purpose

The Technical desk answers:

> Where is current Gold price relative to confirmed geometry, and is there enough clean room for a short-duration trade after considering nearby structure?

It consumes confirmed structure and quantitative context. It does not redefine BOS/MSS, choose strategy direction, set the final broker stop or grant execution permission.

## 2. Output boundary

The desk publishes generic location facts and optional confluence:

| Output | Question | Hard permission? |
|---|---|---:|
| adaptive zones | where are confirmed support/resistance areas? | no |
| BUY/SELL location | is each side positioned near supportive/opposing geometry? | no |
| gross target room | distance to meaningful opposing structure | no |
| cost-aware room context | how much room remains relative to current spread/expected friction? | no |
| trendline | causal touch/break/reclaim context | no |
| Fibonacci | location inside a confirmed impulse | no |
| POC | broker-local volume concentration | no |
| conflict | competing zones/path compression | no |

Hard spread/slippage acceptance remains downstream.

## 3. Pipeline

```text
StructureReport + QuantReport
→ adaptive zones
→ independent BUY/SELL location
→ target/path room

confirmed swings → causal trendlines
confirmed impulse → Fibonacci
completed candles + labelled volume → broker-local POC

all outputs
→ TechnicalReport / ConfluenceReport
→ strategy families / fusion / Trade Plan / management
```

The desk never rereads MT5 and never recomputes shared ATR merely for convenience.

## 4. Adaptive zones

Zones are areas, not exact prices.

A source swing can become a volatility-aware band using broker tick size plus ATR-normalized width. Nearby compatible same-side zones may merge only with preserved provenance.

Draft lifecycle vocabulary:

```text
ACTIVE
WEAKENING
BROKEN
RETEST_CANDIDATE
RECLAIMED
CONSUMED
STALE
```

A zone must not remain active forever after causally confirmed price acceptance through it.

## 5. Scalping adaptation: local geometry matters more

A swing system can sometimes tolerate broad zones. A scalper cannot assume that a structurally valid level is executable when the invalidation distance or target room is too large relative to the intended move.

The Technical report therefore needs enough geometry to let later layers evaluate:

- nearest meaningful support/resistance;
- distance from current executable side of the market;
- gross path room;
- local conflict density;
- whether a breakout level is an obstacle or the thesis itself;
- whether a retest remains fresh;
- current spread relative to gross room as descriptive context.

This desk does not convert those facts into a monetary risk decision.

## 6. Independent BUY/SELL location

BUY and SELL location are evaluated independently.

A good BUY location does not make SELL impossible, and a poor BUY location does not erase a valid SELL thesis.

Draft categories:

```text
EXCELLENT
GOOD
NEUTRAL
POOR
DANGEROUS
UNKNOWN
```

`DANGEROUS` means current geometry is unusually constrained; exact thresholds remain calibration.

## 7. Target room and transaction-cost context

Target-room distance is factual context, not the final TP.

The report may publish both:

```text
gross_room_to_structure
current_spread
room_to_spread_ratio
```

or an equivalent normalized representation.

This is especially important for scalping because a setup with apparently good chart room may have poor executable economics after Bid/Ask friction.

The final structural target and original R belong to Trade Plan. Slippage/deviation and current pre-submit cost acceptance belong to Execution.

## 8. Causal trendlines

Trendlines may be built only from already-confirmed structural anchors.

Possible outputs:

```text
SUPPORT / RESISTANCE
ASCENDING / DESCENDING / FLAT
TOUCH / BREAK / RECLAIM / NONE
projected price
ATR-normalized distance
```

Trendlines are optional confluence and cannot replace confirmed structure.

## 9. Fibonacci geometry

Fibonacci anchors require a causal confirmed impulse pair. Future pivots and arbitrary visual highs/lows are prohibited.

Initial retracement/extension labels may mirror the reference system as researchable confluence, but no exact ratio becomes a universal scalp entry rule.

Fib context is optional; absence or disagreement cannot become a hidden veto.

## 10. Broker-local volume profile / POC

POC is computed from a bounded recent candle window and labelled by source:

```text
real_volume when meaningful
otherwise tick_volume
```

Tick volume is broker-local activity, not centralized exchange volume.

POC is direction-neutral and cannot independently create a BUY/SELL thesis.

For scalping, the challenge should test whether shorter rolling POC windows add useful local context or simply duplicate price structure.

## 11. Session and prior-range levels

Session highs/lows, prior session ranges and possibly prior-day extremes may be accepted as additional technical/liquidity sources only if their creation time and provenance are explicit.

They must not be silently mixed with confirmed swing zones as if every source had identical meaning.

## 12. Timeframe baseline

| Timeframe | Draft technical role |
|---|---|
| H4 | optional major external zones |
| H1 | broad regime/major support-resistance |
| M15 | main scalp opportunity location and target path |
| M5 | primary local setup/retest/entry geometry |
| M1 | optional diagnostic micro-level context |

M5 location cannot overwrite H1/M15 context; lower timeframe detail refines rather than rewrites higher-timeframe facts.

## 13. Confluence rule

Draft composition follows the reference philosophy:

```text
base strategy-family evidence
+ bounded positive optional confluence
= adjusted analytical evidence
```

Guarantees:

- missing confluence does not reduce a valid base thesis automatically;
- optional items cannot become universal gates;
- correlated confluence must be capped/bounded;
- POC alone remains neutral;
- hard safety remains outside weighted scoring.

## 14. Restart/replay

Zones, trendlines, Fib anchors and POC must rebuild from the same causal prefix after restart.

Replay stores source swing IDs, confirmation times, zone provenance, merge lineage, target-room facts, volume source and configuration fingerprint.

No later bar may upgrade an earlier replay point.

## 15. Failure behaviour

| Condition | Result |
|---|---|
| no confirmed swings | no fabricated zones |
| no ATR | normalized location UNKNOWN |
| no optional confluence | base analytical evidence remains intact |
| no real volume | explicitly labelled tick-volume fallback where allowed |
| opposing nearby zones | conflict exposed, not forced direction |
| corrupt chronology | rejected upstream |

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/technical.py
src/gold_scalp_trader/intelligence/confluence.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 17. Planned proof

Tests must cover zone construction/merging/provenance, independent BUY/SELL location, gross room, cost-aware descriptive ratios, causal trendline/Fib anchors, POC source labelling, timeframe separation, no-penalty missing confluence and replay no-lookahead.

## 18. Pre-challenge calibration

Open items include zone width/merge tolerance, local-vs-major zone ranking, retest lifecycle, room thresholds, cost-aware room normalization, session/prior-day sources, POC lookback/binning, trendline tolerance, Fib impulse quality and whether any optional confluence adds out-of-sample value.
