# GoldScalpTrader — Liquidity and SMC Evidence

**Status:** DRAFT PRE-CHALLENGE INTELLIGENCE CONTRACT
**Version:** 0.1-scalp-liquidity
**Authority:** Liquidity pools, probes, sweeps, reclaim/acceptance, FVG, qualified Order Blocks, premium/discount context, session liquidity and short-horizon path quality.

## 1. Purpose

This desk converts observable price behaviour around known levels into auditable liquidity evidence for short-duration Gold trading.

SMC terminology is geometry and chronology shorthand. It is not automatic trade authority.

> A liquidity label matters only when its level existed first and subsequent price behaviour is causally observable.

The desk never places orders, sizes money or defines the final stop.

## 2. Causal dependency

Ordered facts must remain ordered:

```text
confirmed/protected structure
→ pre-existing pool/level
→ later interaction
→ probe / sweep-reclaim / accepted break
→ optional FVG / qualified Order Block / path context
→ LiquidityReport
```

A pool cannot be swept before it existed. An FVG is known only after the third candle closes. An Order Block is qualified only after the structural consequence that makes the origin meaningful.

## 3. Inputs

- completed chronological candles;
- same-timeframe StructureReport;
- same-timeframe QuantReport/shared ATR;
- current price and broker tick size;
- session range facts where explicitly accepted;
- versioned liquidity configuration.

The desk does not recalculate swings or ATR and cannot silently consume a mismatched timeframe report.

## 4. Published model

The report may expose:

- `LiquidityPool` with side, bounds, source provenance, creation time and significance;
- `LiquidityEvent`: PROBE, SWEEP/RECLAIM or ACCEPTED_BREAK;
- `FairValueGap` with causal creation time and mitigation state;
- `OrderBlock` only when tied to a meaningful structural event;
- nearest buy-side/sell-side pools;
- path up/down state;
- bounded BUY/SELL evidence;
- coverage and freshness inputs.

Draft path vocabulary:

```text
OPEN
MIXED
CROWDED
UNKNOWN
```

## 5. Pool construction

Primary sources are confirmed/protected swings. Scalp-specific candidate sources that require explicit provenance include:

- current/previous session highs and lows;
- prior-day high/low where later approved;
- recent range boundaries;
- accepted breakout/retest levels;
- displacement origins where causally qualified.

Nearby compatible highs/lows may be clustered with tick/ATR-aware tolerance. Several similar levels become one pool rather than several independent votes.

## 6. Pool lifecycle

Draft states:

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

A completed bar used as an interaction must close after the pool was causally created. Same-bar retroactive interaction is prohibited.

For scalping, age matters. A pool can remain historically valid while becoming too stale to justify a fresh M5 entry. The report must retain creation/interaction time so Entry Timing can apply policy.

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

A wick through a level is not automatically a sweep. BOS/MSS remains owned by Candle Structure.

## 8. Fair Value Gap

The baseline may retain deterministic three-candle FVG geometry with creation at the third candle close.

States may include:

```text
FRESH
PARTIAL
MITIGATED
STALE
```

FVG remains optional context. A valid scalp is not rejected solely because no FVG exists.

The challenge must test whether very small M1/M5 FVGs add signal or simply amplify noise.

## 9. Qualified Order Block

The system must not label every opposite candle an Order Block.

A qualified OB requires a traceable origin tied to a meaningful break/structural consequence and preserves:

```text
direction
timeframe
bounds
origin_time
qualified_at
source_break
state
```

Geometry identity and qualification time remain separate.

## 10. Scalp liquidity path

Short target horizons make path congestion critical.

The report should expose nearest relevant pools and ATR/tick-normalized path density so later layers can ask:

- is there meaningful room before opposing liquidity?
- is the move already at the likely pool?
- is the entry chasing a sweep/expansion that already completed?
- is a nearby pool an objective, an obstacle or the thesis level itself?

No pool is a guaranteed target. Trade Plan owns final objectives and R geometry.

## 11. Session liquidity

Asia range, London expansion, New York continuation/reversal and London–New York overlap can create important scalp liquidity.

Session highs/lows may become pool sources only through explicit timestamped provenance. Session labels themselves do not grant direction.

## 12. Correlation and double counting

A sweep, rejection, MSS, FVG and OB can all describe one episode. The report preserves related lineage so Strategy/Fusion can bound correlated evidence rather than summing labels as independent certainty.

## 13. Timeframe baseline

| Timeframe | Draft liquidity role |
|---|---|
| H4/H1 | major/external pools only |
| M15 | opportunity pools, session path and target context |
| M5 | primary scalp sweep/reclaim/break and entry path |
| M1 | diagnostic micro-liquidity until explicitly promoted |

Lower-timeframe events cannot rewrite higher-timeframe pool history.

## 14. Restart/replay

Pools/FVG/OB/events must rebuild from the same causal prefix. Replay stores geometry time and knowledge time separately.

No pool interaction may appear before the pool's causal creation; no FVG/OB state may use future candles.

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

Tests must prove pool-before-sweep chronology, clustering/provenance, sweep versus accepted break, FVG creation/mitigation, OB qualification, event timestamps, path classification, session-source lineage, no double count and replay no-lookahead.

## 18. Pre-challenge calibration

Open items: pool clustering tolerance, session/prior-day sources, sweep/reclaim quality, event expiry, FVG minimum size, OB qualification/mitigation, premium/discount range definition, M1 usefulness and path-density thresholds.
