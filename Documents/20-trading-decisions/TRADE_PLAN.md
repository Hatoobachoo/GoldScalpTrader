# GoldScalpTrader — Structural Trade Plan

**Status:** DRAFT PRE-CHALLENGE TRADE-PLAN CONTRACT
**Version:** 0.1-scalp-geometry
**Authority:** Approved entry reference, family-aware structural invalidation, initial SL, objective hierarchy, original R, transaction-cost-aware target/path quality and structural RR.

## 1. Purpose and boundary

Trade Plan converts a valid Opportunity plus analytical ENTER timing into explicit market geometry before monetary sizing or broker submission.

> Strategy decides whether the idea is worth pursuing. Trade Plan defines how it would be entered, invalidated and targeted. Risk decides whether the account can afford it.

Trade Plan does not size lots, move a structural stop merely to fit a small account, call MT5 or grant final execution permission.

## 2. Construction pipeline

```text
READY analytical Opportunity
→ Approved Entry Reference
→ family-aware structural invalidation
→ volatility/noise + broker-tick outward buffer
→ immediate / primary / expansion objectives
→ stop quality
→ path/target quality
→ gross and cost-aware structural R context
→ READY / DEGRADED / INVALID TradePlan
→ independent monetary Risk
```

## 3. Price identities

These identities must remain separate:

| Identity | Meaning | Owner |
|---|---|---|
| Signal Price | price where evidence formed | decisions/timing |
| Approved Entry Reference | reference used to build geometry | Trade Plan |
| Executable Quote | fresh Bid/Ask immediately before submit | execution |
| Actual Fill | broker-confirmed filled price | reconciliation |

A scalp is especially sensitive to the difference between Signal Price and Actual Fill.

## 4. Trade Plan output

A plan should preserve:

- Opportunity/Episode/family identity;
- direction;
- signal and approved entry reference;
- invalidation source/price;
- buffer and initial SL;
- Stop Quality;
- immediate obstacle;
- Primary structural target;
- optional Expansion target;
- optional Runner objective only where the family/session supports it;
- original structural R distance;
- gross R multiples;
- spread/cost-aware room diagnostics;
- plan/path/target quality;
- state and exact reason.

Draft states:

```text
READY
DEGRADED
INVALID
```

## 5. Family-aware structural invalidation

Core question:

> What price behaviour proves this exact thesis wrong?

Candidate sources include:

- protected swing;
- confirmed swing;
- retest-failure boundary;
- sweep extreme;
- failed-break extreme;
- meaningful technical zone;
- family-specific fresh M5 structural event.

A source must be causal, provable from the same immutable market/intelligence context and on the correct side of entry.

## 6. Draft invalidation hierarchy

The starting hierarchy preserves the reference principle but is adapted for a scalper:

| Family | Draft preferred invalidation |
|---|---|
| Trend Pullback Continuation | M5 local pullback failure → M15 structure → H1 fallback |
| Breakout Expansion | M5/M15 acceptance-failure geometry → broader fallback |
| Breakout Retest Continuation | M5 retest-failure boundary → M15 → H1 |
| Liquidity Sweep Reversal | exact proven M5 sweep extreme → M5 structure → M15 → H1 |
| Failed Breakout Reversal | exact proven M5 failed-break extreme → M5 structure → M15 → H1 |
| Compression Expansion | M5 range-release failure / M15 range boundary → broader fallback |

This table is a DRAFT starting point. The fresh-zero challenge must test whether each hierarchy matches short-duration Gold behaviour.

## 7. Initial SL and Stop Quality

Initial SL is structural invalidation plus a volatility/noise-aware buffer normalized outward to broker-valid tick geometry.

ATR supports the buffer; ATR does not replace market invalidation.

If broker minimum distance or executable geometry materially distorts the thesis, the plan becomes INVALID rather than silently changing market logic.

Draft stop-quality vocabulary:

```text
ROBUST
ACCEPTABLE
FRAGILE
INVALID
```

FRAGILE normally means WAIT/DEGRADED while the Opportunity may survive for better geometry.

## 8. Scalping objective hierarchy

Unlike a swing system, a scalp should not assume a large runner is the default objective.

Draft hierarchy:

```text
Immediate Obstacle
→ Primary Scalp Target
→ Expansion Target when fresh structure/session momentum supports it
→ Runner only as exceptional continuation, not default requirement
```

Multiple objectives are analytical/management references; they do not imply multiple broker orders or required partial closes.

## 9. Structural R versus transaction cost

Gross R alone is insufficient for a scalp.

The plan should retain enough diagnostics to compare:

```text
gross reward distance
current spread
expected/observed execution friction assumptions
net room after current spread context
room-to-cost ratio
```

Final fill/slippage cannot be known before submission. The plan must not fabricate it. Execution separately checks fresh executable drift/spread.

The challenge must decide the minimum acceptable structural R and any cost-adjusted requirement. The Swing system's 1.20R floor is **not automatically inherited as frozen scalp policy**.

## 10. Target selection

Targets come from causally known structure/liquidity/session geometry, not fixed arbitrary Gold-dollar/pip targets.

Potential sources:

- nearest meaningful opposing structural zone;
- pre-existing liquidity pool;
- session/prior-range extreme;
- breakout measured continuation only if evidence-based;
- family-specific objective.

A nearby obstacle may make the current entry poor even when a farther theoretical target exists.

## 11. Deterioration before submit

A Trade Plan can become DEGRADED between analytical ENTER and actual broker submission if:

- price drifts materially;
- spread expands;
- target room collapses;
- fresh structure changes invalidation;
- broker constraints make the geometry invalid;
- event freshness expires.

Risk may block unaffordable geometry but may not rewrite the stop.

## 12. Original R

After a verified fill plus original structural stop, original risk distance defines historical 1R for management/research.

Original R remains immutable even when the Trade Manager later protects/trails.

## 13. Persistence/recovery

A persisted Trade Plan belongs to exactly one Opportunity/Episode identity.

Recovery validates identity plus fresh broker/market truth before any new write. A restored plan is not automatic execution permission.

## 14. Dashboard

When a plan exists, show:

```text
Entry Reference
Current executable Bid/Ask separately
SL
Primary target + gross R
Expansion target + R if present
Invalidation source
Stop Quality
Path/Target Quality
spread/cost context
Plan state/reason
```

Never show zero values when no valid geometry exists.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/trade_plan.py
src/gold_scalp_trader/decisions/family_trade_plan.py
```

## 16. Planned proof

Tests must cover BUY/SELL geometry, family-aware invalidation, event-specific extremes, buffer/tick normalization, broker constraints, target ordering, transaction-cost diagnostics, original-R immutability, stale/drift degradation and risk independence.

## 17. Explicit non-goals

Trade Plan must not:

- size lots;
- use account balance to distort structural invalidation;
- invent tighter event extremes;
- call MT5;
- let a high score rescue poor geometry;
- use fixed TP/SL distances as market truth;
- promise fills/slippage that are not yet known.

## 18. Pre-challenge calibration

Open items: minimum structural R, cost-adjusted room requirement, buffers, fragile-stop thresholds, target quality, family invalidation hierarchy, session-target sources, runner policy, target merge tolerance and plan expiry/freshness.
