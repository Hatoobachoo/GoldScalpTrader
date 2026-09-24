# GoldScalpTrader — Autonomous Strategy Invention

**Status:** DRAFT PRE-CHALLENGE RESEARCH CONTRACT — PROPOSAL ONLY
**Version:** 0.1-scalp-declarative-invention
**Authority:** Safe automatic creation of declarative scalp hypotheses from audited research evidence.

## 1. Purpose and hard boundary

Autonomous invention turns recurring evidence into bounded declarative candidates.

It does not write executable production code, change the live Strategy Floor, set monetary risk, bypass hard safety or acquire broker authority.

> Autonomy may invent hypotheses. It may not invent permission.

Every candidate stops at governed validation and promotion.

## 2. Pipeline

```text
outcome-labelled research episodes
→ durable episode journal
→ approved primitive mapping
→ recurring independent cluster
→ declarative hypothesis
→ chronology/similarity/complexity checks
→ CandidateRegistry or explicit suppression
→ governed validation/promotion
```

If eligible evidence cannot produce either a candidate or an explicit suppression reason, invention health is DEGRADED.

## 3. Approved primitive registry

Candidate recipes may use only audited declarative primitives, initially including:

```text
STRUCTURE_TREND
STRUCTURE_BREAK
MSS_SHIFT
CANDLE_REJECTION
DISPLACEMENT
COMPRESSION
TECHNICAL_LOCATION
TRENDLINE
FIBONACCI
VOLUME_PROFILE_POC
LIQUIDITY_SWEEP
FVG
ORDER_BLOCK
EMA_FLOW
RSI_MOMENTUM
ATR_VOLATILITY
SESSION_CONTEXT
TARGET_PATH
ENTRY_TIMING
EVENT_FRESHNESS
SPREAD_COST_CONTEXT
HOLD_TIME_EFFICIENCY
```

The last three are scalp-specific candidate primitives and remain subject to challenge.

Unknown strings, arbitrary Python, MT5 operations and hard-safety concepts are rejected.

## 4. Candidate format

Each candidate records:

- candidate ID/version;
- type: `VARIANT`, `NEW_FAMILY`, `ENTRY_POLICY`, `EXIT_POLICY`;
- parent family if applicable;
- discovery trigger and falsifiable hypothesis;
- required and optional approved primitives;
- preferred regime/session/timing profile;
- invalidation and target model;
- freshness/transaction-cost assumptions if relevant;
- evidence episode IDs/chronology;
- semantic fingerprint/similarity;
- state and rejection/suppression reason.

Recipes are data only. They contain no `eval`, `exec`, generated Python, risk ceilings, broker requests or permission overrides.

## 5. Evidence triggers

Potential recurring triggers include:

- meaningful missed scalp moves;
- false/poor entries;
- late/chased entries;
- excessive transaction-cost clusters;
- weak-capture/premature-exit sequences;
- high-capture examples;
- time-stop clusters;
- regime/session deterioration;
- repeated blocked episodes only when attribution proves the cause is analytical rather than broker/system safety.

Independent Episode IDs are required. Duplicate observations of one episode cannot inflate sample strength.

## 6. Variant versus new family

A small parameter/timing/primitive change is a `VARIANT` or policy challenger.

A `NEW_FAMILY` requires materially distinct recurring market behaviour not already expressed by the production families.

Adding one RSI/FVG/Fib/POC condition does not create a new family.

## 7. Complexity control

Required/optional primitive counts are bounded.

Candidates that combine every available feature are presumed overfit until ablation, Opportunity Recall, trade frequency and out-of-sample evidence prove otherwise.

Scalping-specific cost/freshness primitives should reduce unrealistic entries, not become an opaque checklist whose only effect is eliminating trades.

## 8. Duplicate/rejection memory

Candidate fingerprints and similarity suppress repeated proposals.

Rejected candidates and suppression reasons survive restart/local backup. A similar rejected idea may return only with materially new evidence or explicit versioned policy change.

## 9. Hard exclusions

Invention may not modify or optimize away:

- runtime/broker identity;
- closed-candle/no-lookahead semantics;
- monetary risk ceilings/daily loss lock;
- one-shot Intent;
- reconciliation;
- controller fencing;
- unknown exposure fail-safe;
- original-R immutability;
- secret handling;
- local backup integrity;
- central Gate ownership.

## 10. Promotion boundary

Invention creates `PROPOSED` research candidates only.

Typical governed path:

```text
PROPOSED
→ RESEARCHING / VALIDATING
→ LOCKED
→ one-shot FINAL HOLDOUT
→ STRESS
→ SHADOW
→ DEMO_CANARY
→ PROMOTION_READY
→ explicit approval
```

Locked semantic changes create a new candidate/version.

## 11. Runtime boundary

Invention is offline/research work. Production runtime reads only approved versioned policy.

It does not invent or deploy a strategy inside an active broker cycle.

## 12. Persistence/dashboard

Restore invention journal, registry, fingerprints, rejection memory and liveness state from canonical local StateStore/checkpoint.

Display:

```text
Discovery Health     IDLE / HEALTHY / DEGRADED
Eligible Clusters    count
Candidate Count      count
Latest Candidate     ID / type / stage
Suppressed           explicit reason
Broker Authority     NONE
```

## 13. Planned implementation ownership

```text
src/gold_scalp_trader/research/episode_journal.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
src/gold_scalp_trader/research/promotion.py
```

## 14. Planned proof

Tests cover candidate creation/classification, approved primitive validation, complexity limits, automatic journal feed, duplicate/rejection memory, restart persistence, stage locks and self-promotion denial.

Market quality still requires chronological replay, walk-forward, holdout, stress and forward DEMO evidence.

## 15. Open calibration

Sample thresholds, similarity distance, cluster definitions, scheduling/CPU budget, allowed recipe complexity, session/freshness/cost primitive value and evidence threshold for retaining optional confluence remain research questions.
