# GoldScalpTrader — Documentation Audit

**Status:** ACTIVE FREEZE-PREPARATION AUDIT — PRESERVATION-FIRST SEMANTIC CORRECTION IN PROGRESS
**Version:** 0.3-preservation-first-doc-review
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

If **no**, the reference feature/default must be preserved.

If uncertain, preserve now and list it for final documentation discussion.

## 4. Fresh-zero correction finding

The original Fresh-Zero Audit correctly identified many scalp-specific improvements but also simplified several **non-scalp** reference features. The operator explicitly rejected those removals.

Corrective result:

### Restored

- automatic SMALL/MEDIUM/NORMAL DayStartEquity Risk profiles;
- their reference target/elevated/hard/daily-loss values;
- explicit disabled-by-default aggressive small-account operational option;
- 8% maximum SL-risk ceiling as ceiling, not target;
- 16% aggregate open-risk and daily-loss ceilings under aggressive mode;
- governed manual daily-loss reset capability, disabled by default;
- one fresh same-episode re-entry baseline;
- three-loss / at-least-30-minute cooldown baseline + release conditions;
- bounded physical analytical concurrency target + one-worker fallback/parity;
- Daily PRE_CLOSE T-20/T-10;
- Weekend PRE_CLOSE T-60/T-30;
- daily reopen 1 clean M5;
- weekend reopen 2 clean M5 + gap assessment;
- 1800-second provider TTL baseline;
- future governed REAL capability;
- optional broker-valid partial-management capability where divisible.

### Retained as genuine scalp changes

- H1/M15/M5 hierarchy with H4 optional;
- stronger event freshness/anti-chase;
- gross + cost-adjusted room;
- no automatic inherited 1.20R hard scalp floor;
- stronger spread/drift/latency observability;
- true News UNKNOWN new-entry block;
- valid LKG News-cache resilience without timestamp laundering;
- exceptional Runner;
- time/efficiency EXIT reasoning;
- scalp-specific cost/latency/duration research.

## 5. Explicit operator-directed non-scalp differences

These are allowed because the operator explicitly requested them:

- no trading-runtime Git commit/push/pull;
- local source backup via coherent remote bulk → `git pull --ff-only` → optional clean ZIP;
- aggressive small-account option preserved but disabled by default.

## 6. Semantic review checklist

The audit now checks:

- preservation-first rule visible at system and governance level;
- consistent timeframe roles;
- six-family preservation;
- bounded analytical concurrency preserved;
- profile Risk architecture consistent everywhere;
- aggressive mode is disabled-by-default operational capability, not research-only;
- no `STANDARD-only` leakage;
- no false claim that 0.50% scaffold is production policy;
- cooldown/re-entry/reset defaults aligned;
- News cache/UNKNOWN policy aligned;
- 1800s provider baseline aligned;
- PRE_CLOSE/reopen defaults aligned;
- future REAL is gated, not removed or hidden;
- partial-management wording does not remove capability;
- runtime Git publication remains absent;
- dashboard blocker vs Gate truth remains correct;
- learning/research stays downstream;
- source/test maps match contracts.

## 7. Reconstructability test

A new developer/AI must be able to answer from `Documents/` alone:

- what is preserved from Swing;
- what changed specifically for scalping;
- what changed because the operator explicitly asked;
- exact risk profiles/bands;
- exact aggressive-mode semantics;
- cooldown/reset/session/reopen/provider defaults;
- timeframe/freshness/cost rules;
- bounded analytical concurrency vs serial broker authority;
- DEMO progression and future REAL gate;
- runtime/source backup methods;
- which values still genuinely require scalp calibration or external proof.

## 8. Metadata normalization finding

A separate issue remains: some untouched topic documents still carry stale `DRAFT PRE-CHALLENGE` headers even though their architecture was preserved/accepted.

That metadata normalization must be completed in a coherent documentation bulk before final freeze. It must not fabricate implementation/test PASS evidence.

## 9. Evidence truth

Current classification:

```text
architecture/preservation decisions     available
implementation proof                    not yet available
scalp replay/calibration evidence       pending
current Exness/provider external proof  pending
controlled DEMO lifecycle proof         pending
future REAL release proof               not started
profitability claim                     none
```

## 10. Current audit result

```text
STRUCTURAL INVENTORY                 PASS
PRESERVATION-FIRST RULE              PASS after current correction packet
UNJUSTIFIED FEATURE REMOVALS         CORRECTED in current packet
GENUINE SCALP DELTA LEDGER           UPDATED in current packet
NEWS CACHE SEMANTICS                 PASS / retained
FULL AFFECTED-GRAPH SYNC             CURRENT
64-DOC METADATA NORMALIZATION        STILL PENDING
FINAL RECONSTRUCTABILITY SIGN-OFF    NOT YET FINAL
DOCUMENTATION FREEZE                 NOT YET DECLARED COMPLETE
```

Implementation must not begin until affected-graph synchronization and metadata/cross-link normalization are clean, followed by the operator's final documentation discussion of the remaining genuine scalp-specific deltas.