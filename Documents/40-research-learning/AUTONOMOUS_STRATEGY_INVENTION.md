# GoldScalpTrader — Autonomous Strategy Invention

**Status:** FROZEN V1 RESEARCH GOVERNANCE — DECLARATIVE PROPOSAL ONLY
**Version:** 1.0-preservation-first-declarative-invention
**Authority:** Safe automatic creation of declarative scalp hypotheses from audited research evidence.

## 1. Purpose / hard boundary

Autonomous invention turns recurring evidence into bounded declarative candidates.

It does not write executable production code, change live Strategy Floor, set monetary Risk, bypass hard safety or acquire broker authority.

> Autonomy may invent hypotheses. It may not invent permission.

Every candidate stops at governed validation/promotion.

## 2. Pipeline

```text
outcome-labelled research episodes
→ durable episode journal
→ approved primitive mapping
→ recurring independent cluster
→ declarative hypothesis
→ chronology/similarity/complexity/preservation checks
→ CandidateRegistry or explicit suppression
→ governed validation/promotion
```

Eligible evidence must end in candidate or explicit suppression reason; otherwise invention health is DEGRADED.

## 3. Approved primitive registry

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

`EVENT_FRESHNESS`, `SPREAD_COST_CONTEXT` and `HOLD_TIME_EFFICIENCY` are accepted scalp-specific primitives; their numerical thresholds remain researchable.

M1 information may be used only as diagnostic/research input under current V1; invention cannot promote it into production authority without separate governed design change.

Unknown strings, arbitrary Python, MT5 operations and hard-safety concepts are rejected.

## 4. Candidate format

Each candidate records ID/version/type (`VARIANT`, `NEW_FAMILY`, `ENTRY_POLICY`, `EXIT_POLICY`), parent family, trigger/hypothesis, required/optional primitives, preferred regime/session/timing, invalidation/target, freshness/cost assumptions, evidence Episode IDs, semantic fingerprint/similarity and state/rejection reason.

Recipes are data only. They contain no `eval`, `exec`, generated production Python, Risk ceilings, broker requests or permission overrides.

## 5. Evidence triggers

Potential triggers include meaningful missed scalp moves, false/poor entries, late/chased entries, transaction-cost clusters, weak-capture/premature exits, high-capture examples, time-efficiency clusters, regime/session deterioration and analytically attributable blocked episodes.

System/broker safety faults remain separate. Duplicate observations from one Episode ID cannot inflate evidence.

## 6. Variant versus new family

Small parameter/timing/primitive change is `VARIANT` or policy challenger. `NEW_FAMILY` requires materially distinct recurring behavior not already expressed by the six production families.

Adding one RSI/FVG/Fib/POC condition does not create a new family.

## 7. Preservation-first invention rule

Invention may propose changing a preserved Swing feature/default, but candidate cannot progress toward production until the difference is explicitly classified as a genuine scalp-specific change, operator-directed change or proven reference defect correction.

Therefore invention cannot silently optimize away or treat as free parameters:

- SMALL/MEDIUM/NORMAL Risk architecture/bands;
- disabled-by-default aggressive overlay semantics;
- disabled-by-default manual reset;
- one fresh same-episode re-entry baseline;
- three-loss cooldown baseline;
- PRE_CLOSE/reopen defaults;
- provider TTL baseline;
- bounded analytical concurrency capability;
- future governed REAL release path;
- one-shot/reconciliation/controller safety.

## 8. Complexity control

Required/optional primitive counts are bounded. Filter-soup candidates are presumed overfit until ablation, Opportunity Recall, frequency, cost-adjusted expectancy and out-of-sample evidence justify complexity.

Scalp cost/freshness primitives should reduce unrealistic entries, not merely eliminate trades.

## 9. Duplicate / rejection memory

Candidate fingerprints/similarity suppress repeated proposals. Rejected candidates/suppression reasons survive restart/local backup. Similar rejected idea may return only with materially new evidence or explicit versioned policy change.

## 10. Hard exclusions

Invention cannot modify/optimize away runtime/broker identity, completed-candle/no-lookahead, hard Risk/session/execution authority, UNKNOWN fail-safe, one-shot Intent, reconciliation, controller fencing, unknown exposure, original-R immutability, secret handling, backup integrity or central Gate ownership.

## 11. Promotion / runtime boundary

Invention creates `PROPOSED` research candidates only.

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

Production runtime reads only approved versioned policy. Future REAL capability remains separately gated; invention/promotion does not authorize it.

## 12. Persistence / dashboard

Restore invention journal, registry, fingerprints, rejection memory and liveness from canonical StateStore/checkpoint.

Display Discovery Health, eligible clusters, Candidate Count, latest candidate ID/type/stage, suppression reason and Broker Authority `NONE`.

## 13. Planned implementation ownership

```text
src/gold_scalp_trader/research/episode_journal.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
src/gold_scalp_trader/research/promotion.py
```

## 14. Planned proof

Tests cover candidate creation/classification, primitive validation, preservation classification, complexity bounds, journal feed, duplicate/rejection memory, restart persistence, stage locks and self-promotion denial.

## 15. Research calibration

Sample thresholds, similarity distance, cluster definitions, scheduling/CPU budget, recipe complexity, session/freshness/cost primitive value and optional-confluence evidence threshold remain research questions.