# GoldScalpTrader — Strategy Floor

**Status:** IMPLEMENTED PRODUCTION CONTRACT — STRUCTURAL ROUTING / SIX-FAMILY RESEARCH BOARD  
**Version:** 3.0-structural-production-routing  
**Authority:** Six strategy-family definitions, market-first setup detection, production family routing, shadow attribution, family evidence semantics and analytical scheduling.

## 1. Core rule

> **The market decides what setup exists. Production routes one qualified structural family; a manual family setting and a generic score cannot manufacture or select a live trade.**

Canonical order:

```text
one causal IntelligenceSnapshot
→ evaluate all six family definitions independently
→ preserve all SetupCandidate records
→ consider QUALIFIED structural candidates only
→ if qualified directions conflict: FAIL CLOSED / WAIT
→ otherwise route exactly one family by structural semantic priority
→ routed family may enter BUY/SELL + Red Team
→ remaining families stay SHADOW_ONLY research
→ M5 Opportunity
→ subordinate M1 Timing
→ TradePlan
→ Executable Quality
→ Risk
→ hard authorities / Gate
→ Intent / writer / reconciliation
```

Scores explain candidate quality. **Scores never choose the production family.**

## 2. Six preserved families

```text
TREND_PULLBACK_CONTINUATION
BREAKOUT_EXPANSION
BREAKOUT_RETEST_CONTINUATION
LIQUIDITY_SWEEP_REVERSAL
FAILED_BREAKOUT_REVERSAL
COMPRESSION_EXPANSION
```

Every family owns its own causal definition and may return:

```text
QUALIFIED_BUY
QUALIFIED_SELL
POSSIBLE / INCOMPLETE
NOT_PRESENT
UNKNOWN
```

No family becomes qualified because of configuration, dashboard state, score ranking or another family.

## 3. Production routing

Current deterministic structural priority is:

```text
1  FAILED_BREAKOUT_REVERSAL
2  LIQUIDITY_SWEEP_REVERSAL
3  BREAKOUT_RETEST_CONTINUATION
4  COMPRESSION_EXPANSION
5  BREAKOUT_EXPANSION
6  TREND_PULLBACK_CONTINUATION
```

This is **semantic priority, not profitability ranking**. More specific reversal/retest/release event semantics outrank generic continuation when the candidates agree on direction.

If independently qualified candidates disagree on direction:

```text
BUY-qualified family + SELL-qualified family
→ OPPOSING_QUALIFIED_STRUCTURAL_SETUPS
→ no ACTIVE_EXECUTION family
→ no live Opportunity
→ WAIT
```

If no family qualifies:

```text
NO_QUALIFIED_STRUCTURAL_SETUP
→ all six remain SHADOW_ONLY
→ WAIT
```

When one direction survives routing:

```text
exactly one routed family = ACTIVE_EXECUTION
remaining five          = SHADOW_ONLY
```

`ACTIVE_STRATEGY_FAMILY` is retained only as an optional legacy/research focus field for compatibility. The canonical production cycle does **not** consult it.

## 4. Setup Detector contract

Every `SetupCandidate` preserves, where available:

```text
candidate_id
family
direction
qualification
required evidence status
supporting/opposing evidence
coverage
M5 source event IDs / knowledge time
location/path/room
preferred M1 refinement profile
correlation/source lineage
reasons
```

Setup detection must not:

- use a configured family to fabricate qualification;
- use family score to choose broker authority;
- size money;
- call Risk/Gate/MT5;
- convert a shadow observation into an Intent;
- use future bars.

## 5. Routed family vs shadow families

### Routed ACTIVE_EXECUTION family

May continue only if:

1. its own setup is genuinely `QUALIFIED_BUY` or `QUALIFIED_SELL`;
2. structural routing has resolved it without opposite-direction ambiguity;
3. BUY/SELL + Red Team accepts the thesis;
4. a causal M5 Opportunity exists;
5. subordinate M1 Timing later reaches a valid outcome;
6. TradePlan, executable quality, Risk and all hard authorities pass.

### SHADOW_ONLY families

May:

- detect setups;
- preserve BUY/SELL cases;
- freeze research-only hypothetical geometry;
- resolve causal future outcomes;
- feed timing/management/discovery research.

May not:

- create a live Opportunity;
- create Intent;
- call the MT5 writer;
- consume live position capacity;
- override the routed family;
- change Risk, Session or Gate.

## 6. Canonical examples

### Example A — qualified breakout beats possible trend

```text
Trend Pullback       POSSIBLE SELL
Breakout Expansion  QUALIFIED SELL
→ route BREAKOUT_EXPANSION
→ Trend Pullback stays SHADOW_ONLY
```

This is the screenshot case that static-family isolation previously mishandled.

### Example B — multiple same-direction qualified structures

```text
Breakout Expansion          QUALIFIED SELL
Breakout Retest Continuation QUALIFIED SELL
→ route BREAKOUT_RETEST_CONTINUATION by structural priority
→ score difference does not choose the route
```

### Example C — opposite qualified directions

```text
Liquidity Sweep Reversal QUALIFIED BUY
Breakout Expansion       QUALIFIED SELL
→ WAIT
→ no production family selected
```

### Example D — no setup

```text
all families POSSIBLE / NOT_PRESENT / UNKNOWN
→ WAIT
```

## 7. Trend Pullback Continuation

Question:

> Is an established move resuming after an efficient pullback rather than already being chased?

Useful evidence includes H1/M15 directional structure, M5 pullback/resumption, location/room, EMA flow, momentum reset, ATR/volatility and optional confluence. A missing pullback/resumption means the family is not qualified.

## 8. Breakout Expansion

Question:

> Is a meaningful structural break being accepted with enough displacement, freshness and path to expand rather than fail?

A perfect retest is not required. Break freshness, completed acceptance, volatility/momentum and target room matter.

## 9. Breakout Retest Continuation

Question:

> Did a meaningful breakout hold on retest with credible continuation and efficient invalidation geometry?

A real breakout+retest sequence is required. M1 may refine timing only after the M5 Opportunity exists.

## 10. Liquidity Sweep Reversal

Question:

> Did price take a pre-existing meaningful liquidity pool and reject/reclaim it sufficiently for reversal?

A wick alone is insufficient. Pool existence, penetration, reclaim/rejection, transition and path matter.

## 11. Failed Breakout Reversal

Question:

> Did attempted structural acceptance fail and produce a credible opposing response?

It remains a distinct semantic family even where some evidence overlaps a liquidity sweep.

## 12. Compression Expansion

Question:

> Did meaningful compression release with actual direction, fresh expansion and enough room?

Direction is never guessed before release evidence exists.

## 13. Evidence roles

```text
REQUIRED_FOR_FAMILY
STRONG_SUPPORT
OPTIONAL_SUPPORT
OPPOSITION
NOT_RELEVANT
UNKNOWN
```

A factor that is required for one family does not become globally required for every trade.

## 14. Production / research separation

```text
Production:
market-first setup detection
→ structural router
→ exactly one relevant family

Research:
all six candidates
→ family scores/coverage
→ shadow timing/plans/outcomes
→ governed learning/discovery
```

Hard authorities are never learnable and the research board never gains broker authority.

## 15. Final invariant

> **GoldScalpTrader routes the setup the market actually proves. It does not force a manually selected family onto the chart, it does not use the highest score as broker authority, and it fails closed when structural candidates conflict.**
