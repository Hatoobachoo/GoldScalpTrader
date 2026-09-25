# GoldScalpTrader — Open Questions and Closure Plan

**Status:** ACTIVE RECONSTRUCTION QUESTION REGISTER — APPROVED ARCHITECTURE SEPARATED FROM CALIBRATION
**Version:** 2.0-post-operator-approval
**Authority:** Remaining calibration, implementation choices, external proof and deferred architecture. Approved decisions are not reopened here.

## 1. Classification

```text
CLOSED / APPROVED
PRESERVED DEFAULT
IMPLEMENTATION CHOICE
CALIBRATION
EXTERNAL PROOF
DEFERRED
APPROVAL_REQUIRED
```

## 2. CLOSED / APPROVED architecture

The following are no longer open questions:

### OQ-C01 — News hard trading authority

**CLOSED:** News/Fundamentals are soft context/research only. News event/API/UNKNOWN does not directly block new trading, trigger News cooldown or require post-News warmup.

### OQ-C02 — M1 role

**CLOSED:** M5 owns primary setup/thesis; M1 may refine entry only after a valid M5 Opportunity. M1 cannot create a standalone production trade.

### OQ-C03 — Strategy Isolation Mode

**CLOSED:** Exactly one family is `ACTIVE_EXECUTION`; remaining five are `SHADOW_ONLY` for live efficiency attribution/research.

### OQ-C04 — Physical analytical concurrency

**CLOSED:** logical independence mandatory; physical concurrency profiling-driven. Financial/broker authority strictly serial.

### OQ-C05 — Spread architecture

**CLOSED:** fixed + aware hybrid: absolute emergency ceiling + spread/SL + spread/target + recent baseline + total cost/reward.

### OQ-C06 — Risk profile percentages/bands

**CLOSED:** preserve existing SMALL/MEDIUM/NORMAL bands/percentages. Do not change during this reconstruction.

### OQ-C07 — 120 trades/day

**CLOSED:** approved as research throughput benchmark, never mandatory quota.

### OQ-C08 — AI/invention/ML

**CLOSED:** active backend research/testing capabilities. Candidate/shadow parameters may evolve under research governance. Final production/live promotion requires explicit operator approval.

### OQ-C09 — Distributed same-account architecture

**CLOSED:** same-account active-active writer and distributed DB/fencing are deferred. Sequential handoff remains supported target.

### OQ-C10 — Repository visibility

**CLOSED CURRENT DECISION:** do not change visibility now. Current public state remains until operator explicitly changes it later.

### OQ-C11 — Documentation structure/depth

**CLOSED:** reconstruct latest 66-doc baseline to reference-equivalent-or-better institutional depth; diagrams/tables/state machines required where meaningful; final folders target `01`–`08`.

## 3. PRESERVED DEFAULTS — research may study, production unchanged

### PRD-001 — Monetary Risk profile table

| Profile | Normal | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

No change approved.

### PRD-002 — Aggressive mode

Disabled by default; 8% max single-trade SL-risk ceiling (not target), 16% aggregate and daily ceilings.

### PRD-003 — Cooldown / re-entry

Preserve:

- one genuinely fresh same-episode re-entry;
- three consecutive closed bot losses → at least 30m cooldown plus release conditions.

Research may compare alternatives; production default stays until a later approved change.

### PRD-004 — PRE_CLOSE / reopen

Preserve baseline while current Exness facts are verified:

```text
Daily:   T-20 no entry / T-10 flatten
Weekend: T-60 no entry / T-30 flatten
Daily reopen:   1 clean completed M5
Weekend reopen: 2 clean completed M5 + gap assessment
```

### PRD-005 — Runtime Git

No trading-runtime Git operation.

## 4. CALIBRATION — approved dimensions, values still open

These dimensions are approved. The open question is **their evidence-backed value/shape**, not whether they exist.

### CAL-001 — M1 entry-refinement patterns

Determine which micro-patterns add after-cost value after a valid M5 Opportunity:

- reclaim;
- rejection;
- pullback completion;
- micro continuation;
- micro failed break;
- other candidate patterns from governed research.

Need chronological replay + shadow/DEMO evidence.

### CAL-002 — M1 trigger freshness

Maximum age of M1 evidence before revalidation/WAIT/MISSED.

### CAL-003 — M5 event age

Family/event-specific age/number-of-bars validity.

### CAL-004 — Chase distance

Maximum movement from structural trigger/approved entry before current entry becomes inefficient.

### CAL-005 — Approved Entry → Executable Price drift

Allowed drift may vary with family, stop geometry, target room, spread and volatility.

### CAL-006 — Absolute emergency spread ceiling

Circuit-breaker threshold for obviously abnormal/broken conditions. Must not be tuned so low that normal valid scalps are unnecessarily rejected.

### CAL-007 — Spread / SL ratio

Approved dimension. Calibrate acceptable ranges by family/volatility and actual outcome evidence.

### CAL-008 — Spread / target ratio

Approved dimension. Calibrate acceptable ranges by remaining target room and family.

### CAL-009 — Cost / reward ratio

Approved dimension. Must include the agreed transaction-cost components without double counting.

### CAL-010 — Slippage allowance

Estimate realistic expected/upper-bound fill deterioration from controlled DEMO fills, segmented where useful by:

- session;
- volatility;
- spread regime;
- direction/order type;
- broker execution mode.

### CAL-011 — Broker deviation

Determine bounded request deviation compatible with current Exness execution mode. Too tight may reject valid entries; too loose may damage edge.

### CAL-012 — Decision→send latency

Measure stage latency and define when stale processing forces fresh quote/geometry/Risk revalidation. Threshold should not automatically kill a still-valid opportunity.

### CAL-013 — Minimum gross R

Scalp-specific minimum structural target quality. Swing 1.20R is not automatically the hard answer.

### CAL-014 — Minimum net/cost-adjusted quality

Define the after-cost opportunity threshold using real spread/slippage/target behavior.

### CAL-015 — Family qualification thresholds

Each strategy retains its own causal definition. Tune thresholds using out-of-sample evidence without turning every family into the same filter soup.

### CAL-016 — Fusion/Red-Team weights

Because one family is live-active at a time, weights primarily govern evidence aggregation inside the active family/Red Team and research comparisons—not cross-family live vote-counting.

Need transparent bounded weights; no opaque “score=probability” claim.

### CAL-017 — Family/event correlation caps

Prevent one causal event from appearing as multiple independent confirmations. Tune de-duplication strength without suppressing genuinely distinct evidence.

### CAL-018 — EMA/RSI/Fib/FVG/OB/Trendline/POC contribution

Some may be highly important to certain families. Determine required/supportive/neutral/opposing roles by family and ablation. Missing optional evidence is not a universal block.

### CAL-019 — Session performance

Measure each family separately in Asia/London/New York/overlap for opportunity count, cost, expectancy, entry/capture efficiency and false-block/missed rates.

### CAL-020 — Time-efficiency EXIT

Determine how long each family/regime normally needs to make meaningful progress and when lack of progress becomes EXIT evidence.

### CAL-021 — Protection/trailing timing

Determine when protection/trailing improves after-cost expectancy versus creating premature exits.

### CAL-022 — Runner conditions

Runner is optional. Research fresh continuation, remaining structural objective, protection state, volatility/cost and divisible volume.

### CAL-023 — Partial-close expectancy

Basic partial-close capability remains where broker-valid. Research whether/when it improves outcomes. Sophisticated optimization is deferred as release dependency.

### CAL-024 — PRE_CLOSE exact timing

Verify/calibrate against current Exness normal/holiday/DST schedule while preserving safe default until evidence.

### CAL-025 — Reopen/gap thresholds

Determine normalized spread/quote/gap/clean-M5 conditions that safely resume entry.

### CAL-026 — 120/day throughput benchmark

Measure whether the architecture can approach this level under suitable conditions **without degrading after-cost expectancy or safety**.

Report where throughput is lost:

- opportunity scarcity;
- strategy qualification;
- timing;
- cost;
- Risk/cooldown;
- position occupancy;
- broker/session;
- latency/system faults.

## 5. IMPLEMENTATION choices

### IMP-001 — Python/package version

Choose a currently supported Python + MetaTrader5 package combination during implementation proof.

### IMP-002 — SQLite durability details

Choose WAL/synchronous/checkpoint/checksum/migration details consistent with recovery contract.

### IMP-003 — Analytical scheduler

Implement deterministic serial baseline first; profile; add bounded concurrency only where beneficial.

### IMP-004 — Strategy isolation storage/API

Define typed active-family policy storage, versioning and switch workflow with restart-safe attribution.

### IMP-005 — Executable Quality owner/module shape

Decide whether it is a dedicated `decisions/executable_quality.py` or an equivalent explicitly bounded module. It must remain separate from structural TradePlan and monetary Risk even if implementation packages differ.

### IMP-006 — Dashboard libraries

Choose terminal/rendering implementation while preserving read-only semantics and rich fallback behavior.

### IMP-007 — Local checkpoint/backup format

Choose SQLite snapshot/export, manifest/hash/catalog implementation under the backup architecture.

### IMP-008 — Documentation verifier

Implement local validator for:

- 66-doc inventory;
- final `01`–`08` folders;
- required metadata;
- broken relative links;
- stale legacy folder names;
- owner/mirror consistency markers where practical;
- Mermaid code-block syntax presence/quality checks where feasible.

## 6. EXTERNAL proof

### EXT-001 — Exness SymbolSpec

Verify digits, point, tick size/value, min/max/step, stops/freeze, filling mode and margin behavior for intended symbol/account.

### EXT-002 — Broker schedule

Verify actual current weekday/weekend/DST/holiday behavior.

### EXT-003 — Spread/slippage/deviation

Collect real DEMO distributions across sessions/regimes and around high-volatility conditions.

### EXT-004 — Latency

Measure snapshot→decision→send→ack→reconcile timings on actual Windows/MT5 environment.

### EXT-005 — Controlled lifecycle

Prove OPEN/MODIFY/SL/TP/CLOSE/manual-known-close/restart/reconciliation without duplicates.

### EXT-006 — Recovery

Prove checkpoint/package→new DB/path→fresh MT5 reconciliation→controller→READY on a fresh/replacement machine.

### EXT-007 — Learning attribution

Prove exact active-family trade lineage, shadow evidence separation and exactly-once verified-close learning.

## 7. DEFERRED — deliberately not current dependencies

### DEF-001 — Same-account active-active multi-machine writer

Deferred by operator approval.

### DEF-002 — Distributed DB/fencing/consensus infrastructure

Deferred by operator approval. Sequential handoff/local state is current architecture.

### DEF-003 — Sophisticated partial-close optimizer

Deferred as a release dependency; basic valid partial management remains preserved.

### DEF-004 — Mandatory paid News/macro API

Not required.

### DEF-005 — GitHub Actions/cloud compute

Not required.

## 8. APPROVAL_REQUIRED future changes

Explicit operator approval is mandatory before:

- live/production promotion of a new strategy/candidate/ML policy;
- switching production policy where governance says approval is required;
- enabling future REAL trading;
- changing preserved monetary Risk profile bands/percentages;
- changing repository visibility;
- adding same-account active-active execution;
- adding distributed DB/fencing architecture;
- introducing paid/cloud mandatory dependencies.

## 9. Closure discipline

An open item closes only when the owning document, implementation/test/evidence plan and decision ledger agree.

No calibration result silently changes production. Evidence produces a proposal; governed approval changes production.
