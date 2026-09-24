# GoldScalpTrader — Technical Structure and Levels

**Status:** FROZEN V1 LOCATION ARCHITECTURE — SCALP GEOMETRY CALIBRATION PENDING
**Version:** 1.0-scalp-location-and-room
**Authority:** Support/resistance zones, structural level lifecycle, scalp location quality, target room, causal trendlines, Fibonacci geometry and broker-local volume-profile context.

## 1. Purpose

The Technical desk answers:

> Where is current Gold price relative to confirmed geometry, and is there enough clean room for a short-duration trade after considering nearby structure?

It consumes confirmed structure and quantitative context. It does not redefine BOS/MSS, choose strategy direction, set final broker stop or grant execution permission.

## 2. Output boundary

| Output | Question | Hard permission? |
|---|---|---:|
| adaptive zones | where are confirmed support/resistance areas? | no |
| BUY/SELL location | is each side positioned near supportive/opposing geometry? | no |
| gross target room | distance to meaningful opposing structure | no |
| cost-aware room context | how much room remains relative to current spread/friction? | no |
| trendline | causal touch/break/reclaim context | no |
| Fibonacci | location inside confirmed impulse | no |
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
→ strategy families / fusion / TradePlan / management
```

The desk never rereads MT5 and never recomputes shared ATR merely for convenience.

## 4. Adaptive zones

Zones are areas, not exact prices. A source swing may become a tick/ATR-aware band; nearby compatible same-side zones may merge only with preserved provenance.

Lifecycle vocabulary:

```text
ACTIVE
WEAKENING
BROKEN
RETEST_CANDIDATE
RECLAIMED
CONSUMED
STALE
```

Consumed/broken structure must not continue polluting live executable geometry unless a later causal reclaim makes it relevant again.

## 5. Scalp-specific local geometry

A scalper cannot assume a valid broad level remains executable when invalidation distance or target room is too large relative to intended move.

Publish enough geometry for downstream evaluation of:

- nearest meaningful support/resistance;
- distance from current executable side;
- gross path room;
- local conflict density;
- whether breakout level is obstacle or thesis level;
- whether retest remains fresh;
- current spread relative to gross room as descriptive context.

This desk does not convert those facts into monetary Risk.

## 6. Independent BUY/SELL location

BUY and SELL location are evaluated independently.

Categories may include:

```text
EXCELLENT
GOOD
NEUTRAL
POOR
DANGEROUS
UNKNOWN
```

`DANGEROUS` means unusually constrained geometry; exact thresholds remain scalp calibration.

## 7. Target room / transaction-cost context

Target-room distance is factual context, not final TP.

Publish gross room plus spread/cost-relative facts such as:

```text
gross_room_to_structure
current_spread
room_to_spread_ratio
```

TradePlan owns structural target/original R and explicit cost-adjusted planning truth. Execution owns final fresh spread/slippage/drift acceptance.

## 8. Causal trendlines

Trendlines use only already-confirmed structural anchors and may expose support/resistance, slope, touch/break/reclaim, projected price and ATR-normalized distance.

Trendlines are optional confluence and cannot replace confirmed structure.

## 9. Fibonacci geometry

Fib anchors require a causal confirmed impulse pair. Future pivots and arbitrary visual highs/lows are prohibited.

Reference ratios may remain researchable confluence; no ratio becomes universal scalp entry gate without separate governed evidence.

## 10. Broker-local volume profile / POC

POC uses bounded completed history and explicitly labels volume source:

```text
real_volume when meaningful
otherwise tick_volume
```

Tick volume is broker-local activity, not centralized Gold exchange volume. POC is direction-neutral and cannot independently create BUY/SELL thesis.

## 11. Session / prior-range levels

Session highs/lows, prior-session ranges and prior-day extremes may be technical/liquidity sources only with explicit provenance and creation time. They are not silently equivalent to confirmed swing zones.

## 12. Frozen timeframe roles

| Timeframe | Technical role |
|---|---|
| H4 | optional major external zones |
| H1 | broad regime/major support-resistance |
| M15 | main scalp opportunity location and target path |
| M5 | primary local setup/retest/entry geometry |
| M1 | diagnostic/research micro-level context only |

M5 detail refines but does not rewrite H1/M15 facts. M1 has no hidden production authority.

## 13. Confluence rule

```text
base strategy-family evidence
+ bounded positive optional confluence
= adjusted analytical evidence
```

Missing optional evidence does not automatically penalize a valid base thesis; correlated confluence is bounded; POC alone is neutral; hard safety remains outside scoring.

## 14. Restart/replay

Zones, trendlines, Fib anchors and POC rebuild from same causal prefix. Replay stores source IDs, confirmation times, zone provenance/merge lineage, room facts, volume source and config fingerprint. No later bar upgrades an earlier replay point.

## 15. Failure behaviour

| Condition | Result |
|---|---|
| no confirmed swings | no fabricated zones |
| no ATR | normalized location UNKNOWN |
| no optional confluence | base analytical evidence remains intact |
| no real volume | labelled tick-volume fallback where allowed |
| opposing nearby zones | conflict exposed, not forced direction |
| corrupt chronology | rejected upstream |

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/technical.py
src/gold_scalp_trader/intelligence/confluence.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 17. Planned proof

Tests cover zone construction/merging/provenance, lifecycle/consumption, independent BUY/SELL location, gross room, cost-aware descriptive ratios, causal trendline/Fib anchors, POC source labelling, frozen timeframe separation, missing-confluence semantics and replay no-lookahead.

## 18. Scalp calibration pending

Zone width/merge tolerance, local-vs-major ranking, retest lifecycle/freshness, room thresholds, cost-aware normalization, session/prior-day sources, POC lookback/binning, trendline tolerance, Fib impulse quality and marginal confluence value remain evidence questions.