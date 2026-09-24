# GoldScalpTrader — Strategy Floor

**Status:** DRAFT PRE-CHALLENGE STRATEGY CONTRACT
**Version:** 0.1-scalp-six-family-floor
**Authority:** Independent production strategy-family hypotheses, shared evidence, bounded concurrency, optional confluence, attribution and runtime handoff.

## 1. Purpose and boundary

The Strategy Floor defines independent, auditable scalp hypotheses. It does not own monetary risk, hard session/news permission, broker identity, controller ownership or order execution.

> Parallel hypotheses, bounded evidence, no sequential filter soup, no unanimity requirement.

Every family receives the same verified IntelligenceSnapshot. Family outputs remain attributable until BUY/SELL fusion.

The objective is selective but healthy scalp opportunity coverage—not raw trade count and not a perfect checklist that almost never triggers.

## 2. Initial six-family map

The reference six-family architecture is retained as the **starting decomposition** because the narratives remain meaningful at scalp horizons. Their exact definitions are adapted toward M5 opportunity/entry behaviour and remain challengeable.

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

All six are evaluated independently. The fresh-zero audit may KEEP, MERGE, SPLIT, REPLACE or REMOVE a family only with explicit reasoning.

## 3. Shared timeframe baseline

Draft role mapping:

```text
H1  → broad regime / important structural context
M15 → opportunity location, path, session/liquidity context
M5  → primary scalp setup + trigger structure
M1  → diagnostic/micro-timing context only in baseline
quote/spread → executable condition, not strategy history
```

H4 may remain optional major context and can never be required for every scalp.

## 4. Family reports

Each `FamilyReport` should preserve:

- family identity;
- independent BUY and SELL cases;
- bounded score/strength and coverage;
- supporting/conflicting evidence labels;
- source timestamps/lineage;
- nearest plausible structural objective;
- path/room context;
- preferred timing profile;
- scalp freshness context;
- session/regime attribution.

A FamilyReport is soft analytical evidence, not a broker vote.

## 5. Trend Pullback Continuation

Question:

> Is an established short-horizon move resuming after a controlled pullback into useful location?

Draft evidence:

- H1/M15 directional context;
- M15/M5 location and target room;
- M5 pullback depth and resumption structure;
- EMA flow, ATR-normalized extension and momentum;
- liquidity path / nearby obstacle context;
- session context.

Optional FVG/OB/Fib/trendline/POC support is not mandatory.

Scalp-specific concern: reject/WAIT when the resumption is already extended or the remaining move after costs is too small.

## 6. Breakout Expansion

Question:

> Is a meaningful level being accepted and releasing a fresh expansion that still has executable room?

Draft evidence:

- meaningful M15/M5 level/break;
- completed-bar acceptance, not wick-only probe;
- M5 displacement/expansion and volatility build;
- liquidity path/target room;
- non-chased entry geometry;
- current session context.

A retest is not mandatory. Entry Timing owns late-chase protection.

## 7. Breakout Retest Continuation

Question:

> Did a meaningful break hold on a fresh retest, with M5 structure showing continuation?

Draft evidence:

- prior causal break;
- M15/M5 retest area;
- M5 hold/reclaim/rejection and continuation;
- path/target room;
- event age/freshness.

The executable retest structure may require M5-first invalidation; `BREAKOUT_RETEST_GEOMETRY.md` owns that extension.

## 8. Liquidity Sweep Reversal

Question:

> Was a pre-existing pool taken and rejected strongly enough to support a short-horizon reversal scalp?

Draft evidence:

- pre-existing M15/M5/session pool;
- completed sweep/reclaim;
- M5 rejection/structure shift;
- acceptable opposing path room;
- non-hostile broader context;
- event freshness.

A wick alone is insufficient.

## 9. Failed Breakout Reversal

Question:

> Did attempted acceptance beyond a meaningful level fail and produce a credible opposing response?

Draft evidence:

- causal failed break;
- M5 opposing response/MSS/reclaim;
- M15 location/path;
- target room;
- event freshness and non-chased entry.

This remains distinct from a sweep narrative even when the same market episode contains correlated evidence.

## 10. Compression Expansion

Question:

> Did a real compressed range release with fresh directional evidence and sufficient remaining room?

Draft evidence:

- M15/M5 compression;
- causal range boundary;
- M5 release/acceptance;
- volatility/momentum expansion;
- path/target room;
- session context.

No direction is guessed before release evidence.

## 11. Optional confluence

Initial philosophy:

```text
supportive Trendline/Fib/POC/FVG/OB → bounded positive support
missing optional context             → no automatic base penalty
opposed/unclear optional context     → visible conflict/context
POC alone                            → no direction
```

Optional tools cannot become hidden universal gates.

## 12. Correlation and family overlap

Several families can describe the same episode. Fusion must preserve attribution and bound correlated support.

Examples:

- a sweep can also create failed-break evidence;
- breakout/retest and pullback narratives can overlap;
- compression release can simultaneously look like breakout expansion.

The system must not interpret three correlated labels as three independent confirmations.

## 13. Runtime and bounded concurrency

Family calculations are pure analytical jobs.

The semantic contract is:

```text
one immutable IntelligenceSnapshot
→ six pure FamilyReports
→ deterministic canonical ordering
→ optional bounded confluence
→ BUY/SELL fusion
```

A one-worker serial run and bounded-parallel run must produce the same reports.

Family workers cannot persist broker lifecycle state, size lots or call MT5.

## 14. Frequency and quality philosophy

Research must jointly measure:

- Opportunity Recall;
- meaningful missed moves;
- analytical ENTER frequency;
- capacity-admitted trade frequency;
- Net R / expectancy / Profit Factor;
- drawdown and loss streak;
- MAE/MFE;
- entry/exit/capture efficiency;
- hold duration;
- spread/slippage/transaction cost;
- family/session/regime attribution.

A stricter rule is not automatically better merely because historical win rate rises.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/strategies/floor.py
src/gold_scalp_trader/strategies/parallel.py
src/gold_scalp_trader/strategies/confluence.py
src/gold_scalp_trader/decisions/fusion.py
src/gold_scalp_trader/decisions/opportunity.py
src/gold_scalp_trader/decisions/timing.py
```

## 16. Planned proof

Tests must prove:

- all families consume the same snapshot;
- BUY and SELL are independent;
- family attribution survives fusion;
- one strong coherent family can lead without unanimity;
- optional evidence absence does not silently become veto;
- correlated support is bounded;
- parallel and serial evaluation are semantically identical;
- no family has broker/risk authority.

## 17. Pre-challenge questions

- whether six families remain the optimal decomposition for scalping;
- exact family evidence/weights;
- whether M1 contributes explicit timing evidence;
- family-specific event freshness;
- session specialization;
- family overlap/correlation rules;
- opportunity thresholds balancing quality and frequency;
- latency/resource cost of bounded concurrency.
