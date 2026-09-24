# GoldScalpTrader — Documentation Audit

**Status:** ACTIVE FREEZE-PREPARATION AUDIT — CORE + MARKET/TRADING/EXECUTION NORMALIZATION COMPLETE; REMAINING MANUAL SCAN PENDING
**Version:** 0.4-market-trading-normalized
**Authority:** Structural and expert-level review of the canonical `Documents/` manual before implementation freeze.

## 1. Audit purpose

This audit checks whether the manual is complete, reconstructable without chat history and faithful to the operator's preservation requirement.

It does not claim implementation, DEMO/REAL certification or profitability.

## 2. Structural inventory — VERIFIED

```text
Top level                  7
00-foundation              5
10-market-intelligence     7
20-trading-decisions       7
30-risk-execution          6
40-research-learning       7
50-operator                3
60-engineering            14
90-governance              8
TOTAL                      64 Markdown documents
```

## 3. Governing preservation test

For every material difference from GoldSwingTraderAI ask:

```text
Is it directly required by scalping?
OR explicitly instructed by operator?
OR a separately proven reference defect?
```

If no, preserve reference feature/default. If uncertain, preserve now and list for final documentation discussion.

## 4. Preservation-first correction — VERIFIED AT CORE OWNERS

Restored/retained current authority includes:

- automatic SMALL/MEDIUM/NORMAL DayStartEquity Risk profiles and reference bands;
- explicit disabled-by-default aggressive small-account operational option;
- 8% maximum SL-risk ceiling as ceiling, not target;
- 16% aggregate-open-risk and daily-loss ceilings under aggressive mode;
- governed manual daily-loss reset capability, disabled by default;
- one fresh same-episode re-entry baseline;
- three-loss / at-least-30-minute cooldown baseline + release conditions;
- bounded physical analytical concurrency target + one-worker fallback/parity;
- Daily PRE_CLOSE T-20/T-10;
- Weekend PRE_CLOSE T-60/T-30;
- daily reopen 1 clean M5;
- weekend reopen 2 clean M5 + gap assessment;
- 1800-second News provider TTL baseline;
- future governed REAL capability;
- optional broker-valid partial management where divisible.

## 5. Genuine scalp-specific deltas retained

- H1/M15/M5 hierarchy with H4 optional;
- stronger event freshness/anti-chase;
- gross + cost-adjusted room;
- no automatic inherited 1.20R hard scalp floor;
- stronger spread/drift/latency observability;
- true News UNKNOWN new-entry block;
- valid LKG News-cache resilience without timestamp laundering;
- exceptional Runner;
- time/efficiency EXIT reasoning;
- scalp-specific cost/latency/duration/capture research.

## 6. Explicit operator-directed differences retained

- no trading-runtime Git commit/push/pull;
- source backup via coherent remote bulk → `git pull --ff-only` → optional clean ZIP;
- aggressive small-account option preserved but disabled by default.

## 7. Current normalization pass — COMPLETED SCOPE

This pass verified/corrected:

### Foundation
- `PROJECT_VISION.md` no longer states STANDARD-only Risk or removed REAL capability.

### Market Intelligence
- `CANDLE_STRUCTURE.md`
- `TECHNICAL_STRUCTURE_AND_LEVELS.md`
- `LIQUIDITY_AND_SMC.md`
- `INDICATORS_AND_VOLATILITY.md`
- `SESSION_CONTEXT.md`
- `MARKET_DATA_AND_HISTORY.md`
- `FUNDAMENTAL_AND_NEWS.md`

Results:

- stale `DRAFT PRE-CHALLENGE` metadata removed from accepted market contracts;
- frozen H1/M15/M5/H4/M1 roles reflected consistently;
- M1 production role no longer described as unresolved V1 question;
- 1800-second provider TTL preserved explicitly;
- genuine scalp threshold questions remain calibration rather than architecture ambiguity.

### Trading Decisions
- `STRATEGY_FLOOR.md` and `SCORING_AND_DECISION_FUSION.md` now preserve bounded analytical concurrency instead of describing it as removable/optional feature;
- `ENTRY_TIMING.md` reflects preserved one-fresh-same-episode-reentry count while keeping event/chase thresholds as scalp calibration;
- `BREAKOUT_RETEST_GEOMETRY.md` and `REVERSAL_EVENT_GEOMETRY.md` moved from pre-challenge metadata to frozen family-geometry extensions and reflect M1 non-authority.

### Execution
- `EXECUTION_AND_BROKER_SAFETY.md` now consumes profiled Risk/optional aggressive overlay instead of STANDARD-only Risk;
- future REAL is preserved as a gated capability rather than described as removed/deferred shorthand;
- optional broker-valid partial reconciliation remains supported where applicable.

## 8. Semantic review checklist

Still check across the remaining untouched manual:

- no stale `DRAFT PRE-CHALLENGE` metadata;
- no `STANDARD-only` Risk leakage;
- no false 0.50% scaffold-as-policy wording;
- no `physical concurrency optional/removable` leakage;
- no `REAL removed/outside feature` wording;
- no reopening of preserved cooldown/re-entry/reset defaults without scalp reason;
- no reopening of 1800s TTL / PRE_CLOSE / reopen defaults without direct reason;
- no wording that removes partial-management capability;
- no runtime Git publication path;
- dashboard blocker vs Gate truth;
- research/learning authority stays downstream;
- source/test maps match current contracts.

## 9. Reconstructability target

A new developer/AI must be able to answer from `Documents/` alone:

- what is preserved from Swing;
- what changed specifically for scalping;
- what changed by operator instruction;
- exact Risk profiles/aggressive semantics;
- cooldown/reset/session/reopen/provider defaults;
- timeframe/freshness/cost rules;
- bounded analytical concurrency vs serial broker authority;
- DEMO progression and future REAL gate;
- runtime/source backup methods;
- which values remain genuine scalp calibration or external proof.

## 10. Evidence truth

```text
architecture/preservation decisions     available
implementation proof                    not yet available
scalp replay/calibration evidence       pending
current Exness/provider external proof  pending
controlled DEMO lifecycle proof         pending
future REAL release proof               not started
profitability claim                     none
```

## 11. Current audit result

```text
STRUCTURAL INVENTORY                    PASS
PRESERVATION-FIRST CORE                 PASS
MARKET INTELLIGENCE NORMALIZATION       PASS for current pass
TRADING DECISION NORMALIZATION          PASS for current pass
EXECUTION OWNER NORMALIZATION           PASS for current pass
UNJUSTIFIED FEATURE REMOVALS            CORRECTED at reviewed owners
GENUINE SCALP DELTA LEDGER              CURRENT
RESEARCH/LEARNING FULL SCAN              PENDING
REMAINING OPERATOR/ENGINEERING SCAN      PENDING
64-DOC FINAL METADATA NORMALIZATION      IN PROGRESS
FINAL RECONSTRUCTABILITY SIGN-OFF        NOT YET FINAL
DOCUMENTATION FREEZE                     NOT YET COMPLETE
```

Implementation must not begin until the remaining 64-document semantic/metadata/cross-link scan is clean and the operator completes final discussion of genuine scalp-specific deltas.