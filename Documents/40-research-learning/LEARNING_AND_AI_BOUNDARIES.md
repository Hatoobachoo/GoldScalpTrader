# GoldScalpTrader — Learning and AI Boundaries

**Status:** FROZEN V1 LEARNING GOVERNANCE — RESEARCH THRESHOLDS / IMPLEMENTATION EVIDENCE PENDING
**Version:** 1.0-preservation-first-scalp-learning
**Authority:** StrategyMemory, entry/exit learning, bounded adaptive influence, AI limits, evidence isolation, persistence/local backup and per-scope ownership.

## 1. Purpose

Learning may observe verified experience, remember it, explain it and propose bounded changes. It must not turn the live scalper into a self-mutating broker client.

> Learning may observe, remember, research and propose. Production changes only through governed promotion.

Hard monetary Risk, account/runtime identity, market/news safety, controller fencing, reconciliation, broker execution safety, preservation-first constraints and UNKNOWN fail-closed semantics cannot be learned away.

## 2. One-way influence

```text
verified actual/counterfactual evidence
→ versioned StrategyMemory
→ bounded recommendation
→ declarative challenger
→ chronological validation / holdout / stress / shadow / DEMO canary
→ explicit governed approval
→ versioned production policy
```

No learning record/candidate/AI explanation may call MT5Writer or grant broker authority.

## 3. Preservation-first learning boundary

Learning may propose a change to an inherited Swing feature/default, but it does not automatically convert that proposal into a Scalp difference.

A production change to a preserved reference feature/default still requires:

```text
direct scalp-specific justification or explicit operator decision
→ affected-graph documentation change
→ validation/promotion evidence
→ explicit approval
```

Hard safety cannot be made an ordinary search parameter.

## 4. Allowed influence levels

| Level | Output | Direct broker authority |
|---|---|---:|
| L0 observation | metrics/explanation/journal | none |
| L1 recommendation | hypothesis/candidate idea | none |
| L2 validated bounded adjustment | ranking/timing input | none until promotion |
| L3 Shadow | hypothetical result | none |
| L4 DEMO Canary | governed candidate | ordinary gates only |
| L5 approved policy | explicit versioned config | no safety bypass |

Future REAL remains a separately governed runtime capability; research/promotion does not itself authorize REAL.

## 5. Evidence identities remain separate

Never silently combine:

```text
actual reconciled broker outcome
counterfactual MISSED / BLOCKED outcome
system/broker fault episode
REPLAY
VALIDATION
FINAL_HOLDOUT
SHADOW
DEMO_CANARY
MAIN_DEMO
```

Counterfactual R is never broker P/L. System/broker failure is not evidence that strategy logic needs changing. Unknown manual exposure is never bot learning evidence.

## 6. StrategyMemory durability

Primary durable namespace:

```text
strategy_learning_memory
```

A scoped record contains LearningConfig/policy identity, chronological raw observations, deterministic summaries, stable source IDs, account/symbol scope where applicable, environment identity and code/data/policy lineage.

```text
same source + same evidence → idempotent no-op
same source + changed evidence → explicit integrity conflict
```

Summaries are recomputed/verified from raw observations. Policy/config changes never rewrite historical evidence.

## 7. Small samples and confidence

Small sample does not become strong evidence because win rate looks high. Minimum evidence, shrinkage/confidence and context grouping remain research-policy questions.

Scalping may produce more trades, but correlated trades from one session/regime/episode are not automatically independent observations.

## 8. Bounded adaptive influence

A validated memory effect may eventually produce a small, versioned analytical ranking/timing adjustment, for example:

```text
base opportunity score
+ bounded validated family/session adjustment
```

It must not create silent hard rules such as “one weak London sample → never trade London again.”

Adaptive influence requires explicit bounds, minimum samples, policy identity and OFF/DEGRADED state.

## 9. Scalp entry learning

May study:

- approved entry reference versus actual fill;
- adverse slippage / spread at signal-check-send-fill;
- early/optimal/late/chased classification;
- distance/time since causal event;
- pullback/retest depth;
- breakout acceptance timing;
- MFE/MAE after entry;
- preserved one-fresh-reentry outcomes;
- MISSED opportunity cost;
- family/session/regime performance;
- optional confluence marginal value;
- decision/check/send/ack latency diagnostics.

Learning may propose an Entry Policy Challenger but cannot directly rewrite live thresholds or the preserved one-reentry baseline.

## 10. Scalp exit/management learning

May study MFE versus realized R, MAE, Capture Efficiency, premature-exit cost, trade duration/M5 bars, time-efficiency exits, structural protect/trail quality, Primary/Expansion/Runner outcomes, optional broker-valid partial-management outcomes, profit giveback and exit spread/slippage.

One outcome never justifies self-modification.

## 11. Frozen production identities consumed by learning

Current architecture assumes:

```text
H1   broad soft context
M15  opportunity/location/path
M5   primary setup/timing/management
H4   optional major context
M1   diagnostic/research only
```

Learning can study M1 diagnostics, but cannot silently promote M1 into production authority.

Monetary policy consumed by learning includes the preserved SMALL/MEDIUM/NORMAL DayStartEquity profile identity plus whether the explicit disabled-by-default aggressive overlay was enabled. Historical policy identity is immutable after the trade.

## 12. Actual DEMO learning identity

When governed DEMO execution exists, verified OPEN freezes at least family, approved entry reference, policy/profile/overlay identity, direction, original R, actual fill, ticket and TradePlan/Opportunity/Episode IDs.

Later policy edits may not relabel the trade. Missing legacy identity is not invented.

## 13. Close durability and exactly-once ingestion

```text
verified close
→ persist closed_trade_learning_queue
→ persist managed_trade_closure_receipt
→ clear active ManagedTrade safely
→ reconstruct broker/path outcome
→ save exactly one MAIN_DEMO observation
→ remove queue only after durable StrategyMemory success
```

Unresolved `SUBMITTING`/`ACCEPTED_UNKNOWN` Intent reconciles first.

## 14. Causal path metrics

For completed-bar path estimates:

```text
bar_open >= verified entry time
AND
bar_close <= verified exit time
```

Boundary bars containing pre-entry/post-exit action are excluded unless future tick-accurate evidence proves exact slicing. Exact broker exit remains independent truth.

## 15. Learning metrics

Where evidence supports it store realized R, entry efficiency, MFE_R, MAE_R, capture efficiency, duration/M5 bars, signal-to-fill drift, spread/slippage/latency diagnostics, session/regime/family/policy identity and close origin BOT/EXTERNAL/MIXED.

Missing measurements remain missing, never zero.

## 16. AI supervisor boundary

AI may explain stored facts, summarize audits/research, identify labelled clusters, propose declarative candidates and draft documentation/research recommendations.

AI may not call broker writer, alter hard Risk directly, turn UNKNOWN into PASS, execute arbitrary generated production Python, self-promote candidates, hide failed evidence, adopt unknown manual trades or perform Git operations from trading runtime.

AI output remains untrusted research input until schema/provenance/chronology/governance checks pass.

## 17. Discovery handoff

```text
actual/counterfactual evidence
→ ResearchEpisodeRecord / StrategyMemory
→ recurring independent cluster
→ declarative Candidate
→ validation / holdout / stress / shadow / canary
→ explicit approval
→ versioned production policy
```

Safety/system faults remain separately attributed.

## 18. Local persistence / backup / scope ownership

Learning lives in canonical StateStore and complete local checkpoints/recovery packages. Key namespaces include memory, learning queue, closure receipt, episode journal, candidate registry, discovery status and promotion registry.

There is no automatic GitHub publication on shutdown. Same account/symbol scope has one production learning writer. Same-scope machine movement is sequential handoff only.

## 19. Dashboard

Show Strategy Memory, Entry/Exit Learning, Discovery Health, Champion/Challenger, Adaptive Impact and Broker Authority `NONE` for research/shadow. Research recommendation must never render as active policy before promotion.

## 20. Planned implementation ownership

```text
src/gold_scalp_trader/research/learning.py
src/gold_scalp_trader/research/live_learning.py
src/gold_scalp_trader/research/episode_journal.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
src/gold_scalp_trader/research/promotion.py
src/gold_scalp_trader/management/*
src/gold_scalp_trader/persistence/*
```

## 21. Planned proof / research calibration

Tests prove idempotent/conflicting-source handling, summary recomputation, evidence-environment isolation, frozen entry/profile identity, close queue/receipt, causal path boundaries, exactly-once ingestion, no self-promotion, no broker authority and backup preservation.

Open research values include memory windows, minimum samples, confidence/shrinkage, maximum adaptive effect, clustering, latency/cost metrics and context-specific confluence value. These do not reopen hard Risk/session/execution invariants by default.