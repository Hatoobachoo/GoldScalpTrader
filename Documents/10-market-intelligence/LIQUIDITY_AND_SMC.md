# GoldScalpTrader — Liquidity and SMC Evidence

**Status:** FROZEN V1 INTELLIGENCE ARCHITECTURE — SCALP EVENT/PATH CALIBRATION PENDING
**Version:** 1.0-causal-scalp-liquidity
**Authority:** Liquidity pools, probes, sweeps, reclaim/acceptance, FVG, qualified Order Blocks, premium/discount context, session liquidity and short-horizon path quality.

## 1. Purpose

This desk converts observable price behaviour around known levels into auditable liquidity evidence for short-duration Gold trading.

SMC terminology is geometry/chronology shorthand, not automatic trade authority.

> A liquidity label matters only when its level existed first and later price behaviour is causally observable.

The desk never places orders, sizes money or defines final stop.

## 2. Causal dependency

```text
confirmed/protected structure
→ pre-existing pool/level
→ later interaction
→ probe / sweep-reclaim / accepted break
→ optional FVG / qualified Order Block / path context
→ LiquidityReport
```

A pool cannot be swept before it existed. FVG is known only after third candle closes. Order Block is qualified only after the structural consequence that makes its origin meaningful.

## 3. Inputs

- completed chronological candles;
- same-timeframe StructureReport;
- same-timeframe QuantReport/shared ATR;
- current price and broker tick size;
- explicitly accepted session-range facts;
- versioned liquidity configuration.

The desk does not recalculate swings/ATR or consume mismatched timeframe reports.

## 4. Published model

May expose:

- `LiquidityPool` with side, bounds, provenance, creation time and significance;
- `LiquidityEvent`: PROBE, SWEEP/RECLAIM or ACCEPTED_BREAK;
- `FairValueGap` with causal creation/mitigation state;
- qualified `OrderBlock` tied to meaningful structural event;
- nearest buy/sell-side pools;
- path up/down state;
- bounded BUY/SELL evidence;
- coverage/freshness inputs;
- related event-lineage/correlation identity.

Path vocabulary:

```text
OPEN
MIXED
CROWDED
UNKNOWN
```

## 5. Pool construction

Primary sources are confirmed/protected swings. Explicit-provenance sources may also include current/previous session highs/lows, prior-day high/low where governed, recent range boundaries, accepted breakout/retest levels and causally qualified displacement origins.

Nearby compatible highs/lows may be clustered with tick/ATR-aware tolerance. Similar levels become one pool rather than fake independent votes.

## 6. Pool lifecycle

```text
UNTOUCHED
APPROACHED
PROBED
SWEPT
RECLAIMED
ACCEPTED_BEYOND
CONSUMED
STALE
```

An interaction bar must close after the pool was causally created. Same-bar retroactive interaction is prohibited.

Consumed/accepted-beyond liquidity is not reused as live executable geometry unless a later causal reclaim/new event makes it relevant again.

For scalping, age matters. A pool can remain historically valid while becoming stale for new entry; creation/interaction time must remain available to Entry Timing.

## 7. Sweep versus accepted break

```text
pre-existing pool
+ penetration
+ completed close/reclaim back through pool
→ sweep/reclaim evidence

pre-existing pool
+ completed close with acceptance beyond
→ continuation/break evidence
```

A wick alone is not automatically a sweep. BOS/MSS remains owned by Candle Structure.

## 8. Fair Value Gap

Deterministic three-candle FVG geometry may be retained, with creation no earlier than third-candle close.

States may include FRESH, PARTIAL, MITIGATED and STALE.

FVG remains optional context. Absence cannot reject an otherwise valid scalp by itself. M1 FVG is diagnostic/research only under current timeframe authority.

## 9. Qualified Order Block

Not every opposite candle is an Order Block.

Qualified OB preserves direction, timeframe, bounds, origin time, `qualified_at`, source break/event and state. Geometry identity and qualification time remain separate.

## 10. Scalp liquidity path

Short target horizons make path congestion first-class. Publish nearest relevant pools and normalized path density so downstream can assess meaningful room, already-completed objectives, chase risk and whether a nearby pool is objective/obstacle/thesis level.

No pool is a guaranteed target. TradePlan owns objectives and R geometry.

## 11. Session liquidity

Asia range, London expansion, New York continuation/reversal and overlap may create important scalp liquidity context. Session highs/lows become pool sources only through explicit timestamped provenance. Session label itself does not grant direction.

## 12. Correlation / double counting

Sweep, rejection, MSS, FVG and OB may describe one episode. Related lineage is preserved so Fusion bounds correlated evidence.

## 13. Frozen timeframe roles

| Timeframe | Liquidity role |
|---|---|
| H4/H1 | major/external pools/context |
| M15 | opportunity pools, session path and target context |
| M5 | primary scalp sweep/reclaim/break and entry path |
| M1 | diagnostic/research micro-liquidity only |

M1 production authority is not an open V1 question.

## 14. Restart/replay

Pools/FVG/OB/events rebuild from the same causal prefix. Geometry time and knowledge time remain separate. No interaction/state may use future candles.

## 15. Failure behaviour

| Condition | Result |
|---|---|
| no confirmed sources | no fabricated pool |
| no ATR | reduced coverage/no normalized path claim |
| no FVG/OB | optional evidence absent, not veto |
| corrupt chronology | rejected upstream |
| correlated labels | bounded lineage, not score inflation |

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/liquidity.py
src/gold_scalp_trader/intelligence/snapshot.py
src/gold_scalp_trader/strategies/confluence.py
```

## 17. Planned proof

Tests prove pool-before-sweep chronology, clustering/provenance, pool consumption, sweep versus accepted break, FVG creation/mitigation, OB qualification, event timestamps, path classification, session lineage, M1 non-authority, no double count and replay no-lookahead.

## 18. Scalp calibration pending

Pool clustering tolerance, session/prior-day source weighting, sweep/reclaim quality, event expiry, FVG minimum size, OB qualification/mitigation, premium/discount range definition and path-density thresholds remain evidence questions.