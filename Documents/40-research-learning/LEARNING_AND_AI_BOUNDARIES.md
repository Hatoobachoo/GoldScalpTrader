# GoldScalpTrader — Learning and AI Boundaries

**Status:** DRAFT PRE-CHALLENGE LEARNING CONTRACT
**Version:** 0.1-scalp-bounded-learning
**Authority:** StrategyMemory, entry/exit learning, bounded adaptive influence, AI limits, evidence isolation, persistence/local backup and per-scope ownership.

## 1. Purpose

Learning may observe verified experience, remember it, explain it and propose bounded changes. It must not turn the live scalper into a self-mutating broker client.

> Learning may observe, remember, research and propose. Production changes only through governed promotion.

Hard monetary risk, account/runtime mode identity, market/news safety, controller fencing, reconciliation, broker execution safety and UNKNOWN fail-closed semantics cannot be learned away.

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

No learning record/candidate/AI explanation can call MT5Writer or grant broker authority.

## 3. Allowed influence levels

| Level | Output | Direct broker authority |
|---|---|---:|
| L0 observation | metrics/explanation/journal | none |
| L1 recommendation | hypothesis/candidate idea | none |
| L2 validated bounded adjustment | ranking/timing input | none until promotion |
| L3 Shadow | hypothetical result | none |
| L4 DEMO Canary | governed candidate | ordinary gates only |
| L5 approved policy | explicit versioned config | no safety bypass |

## 4. Evidence identities remain separate

Do not silently combine:

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

Counterfactual R is never broker P/L. A broker/system failure is not a reason to mutate strategy logic.

Unknown manual exposure is never bot learning evidence. A manual close of an already-known ManagedTrade remains a bot-originated trade with explicit EXTERNAL/MIXED close origin.

## 5. StrategyMemory durability

Primary durable namespace:

```text
strategy_learning_memory
```

A scoped record contains:

- LearningConfig/policy identity;
- chronological raw observations;
- deterministic summaries;
- stable source IDs;
- account/symbol scope where applicable;
- environment identity;
- code/data/policy lineage.

Rules:

```text
same source + same evidence → idempotent no-op
same source + changed evidence → explicit integrity conflict
```

Summaries are recomputed/verified from raw observations on load. Policy/config changes never rewrite historical evidence silently.

## 6. Small samples and confidence

A small sample does not become strong evidence because win rate looks high.

Minimum evidence, confidence/shrinkage and context grouping remain research-policy questions.

For a scalper, larger trade counts are possible, but correlated trades from one session/regime cannot be treated as independent simply because N is higher.

## 7. Bounded adaptive influence

A validated memory effect may eventually produce a small, versioned analytical ranking/timing adjustment.

Example only:

```text
base opportunity score
+ bounded validated family/session adjustment
```

It must not create silent hard rules such as:

```text
one weak recent London sample → never trade London again
```

Adaptive influence requires explicit bounds, minimum samples, policy identity and OFF/DEGRADED state.

If learning is unavailable while frozen baseline logic remains valid, the bot can continue without adaptive influence. If persistence/recovery/broker truth itself is corrupt, normal hard authorities block as documented.

## 8. Scalp entry learning

Entry learning may study:

- signal/approved reference versus actual fill;
- adverse slippage in R and absolute price;
- spread at signal/check/send/fill where observable;
- early/optimal/late/chased classification;
- distance/time since causal event;
- pullback/retest depth;
- breakout acceptance timing;
- MFE/MAE after entry;
- second-chance/re-arm outcomes;
- MISSED opportunity cost;
- family/session/regime performance;
- optional confluence marginal value;
- decision-to-send and send-to-ack latency diagnostics.

Learning may propose an Entry Policy Challenger. It cannot directly rewrite live thresholds.

## 9. Scalp exit/management learning

Exit learning may study:

- MFE versus realized R;
- MAE;
- Capture Efficiency;
- premature-exit cost;
- time-in-trade and bars-to-target;
- time/efficiency exits;
- structural trail/protect quality;
- Primary versus Expansion outcome;
- runner capture / profit giveback;
- spread/slippage around exit;
- regime/session/family effects on HOLD/PROTECT/TRAIL/RUNNER/EXIT.

A profitable trade may still have poor capture. A normal losing trade may still be a valid setup. One outcome never justifies self-modification.

## 10. Actual DEMO learning identity

When write-capable DEMO is eventually implemented, a verified OPEN freezes at least:

```text
strategy family
approved entry reference
policy version
direction
original R
actual entry/fill
position ticket
TradePlan / Opportunity / Episode IDs
```

Later policy changes may not relabel the historical trade.

If older/pre-upgrade data lacks required learning identity, keep it manageable/recoverable but do not invent missing family/reference/policy facts for learning.

## 11. Close durability and exactly-once ingestion

Distinct durable records:

```text
closed_trade_learning_queue      pending post-close processing
managed_trade_closure_receipt    durable lifecycle-close proof
```

Crash-safe order:

```text
verified close
→ persist learning queue
→ persist closure receipt
→ clear active ManagedTrade
→ retire matching entry context safely
→ reconstruct broker/path outcome
→ save exactly one MAIN_DEMO observation
→ remove queue only after durable StrategyMemory success
```

An unresolved `SUBMITTING`/`ACCEPTED_UNKNOWN` Intent reconciles first.

## 12. Causal path metrics

For scalp metrics using M5/M1 history, only fully causal bars may contribute.

For a completed-bar excursion estimate:

```text
bar_open >= verified entry time
AND
bar_close <= verified exit time
```

Boundary bars containing pre-entry or post-exit price action are excluded unless a future tick-accurate evidence source proves exact path.

The system prefers conservative incomplete path measurement over lookahead-contaminated precision.

Exact broker exit price remains independent broker truth.

## 13. Learning metrics

Where evidence supports it, store:

```text
realized R
entry efficiency
MFE_R
MAE_R
capture efficiency
trade duration / M5 bars
signal-to-fill drift
spread/slippage diagnostics
entry session
causal entry regime
family/direction/policy version
close origin BOT / EXTERNAL / MIXED
```

Transaction-cost-sensitive metrics are especially important for scalping.

Account-level P/L is never substituted for missing trade-level evidence.

## 14. AI supervisor boundary

AI may:

- explain BUY/SELL/WAIT/MISSED/BLOCK from stored facts;
- summarize audits/research;
- identify recurring labelled clusters;
- propose declarative candidates;
- draft documentation/research recommendations.

AI may not:

- call MT5/raw broker writer;
- alter risk ceilings/daily lock/original R;
- turn UNKNOWN into PASS;
- execute arbitrary generated production Python;
- self-promote candidates;
- hide failed experiments/holdout evidence;
- treat unknown manual trades as bot outcomes;
- create GitHub commits/pushes from the trading runtime.

AI output is untrusted research input until schema/provenance/chronology/governance checks pass.

## 15. Discovery handoff

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

## 16. Local persistence and backup

Learning lives in the canonical StateStore and is included in complete local checkpoints/recovery packages.

Important namespaces include:

```text
strategy_learning_memory
closed_trade_learning_queue
managed_trade_closure_receipt
research_episode_journal
strategy_candidate_registry
discovery_cycle_status
candidate_promotion_registry
```

GoldScalpTrader has **no automatic GitHub publication on graceful shutdown**.

The active trading/learning loop has no repository-write authority. Local final checkpoint/backup is the shutdown durability boundary; deliberate development/source backup remains separate.

## 17. Per-scope ownership

Production learning ownership is per account/symbol scope.

```text
Account A / XAUUSDm → one active PRIMARY may mutate Scope A learning
Account B / XAUUSDm → independent PRIMARY may run with separate state
Second writer for Scope A → prohibited
Offline research DB → separate non-production scope
```

Source IDs expose duplicate/conflicting evidence; they do not safely merge independently-mutated same-scope SQLite histories.

Same-scope laptop movement is sequential handoff only.

## 18. Dashboard

Show separately:

```text
Strategy Memory   READY / DEGRADED / OFFLINE / PENDING
Entry Learning    ACTIVE / OBSERVATION / PENDING
Exit Learning     ACTIVE / OBSERVATION / PENDING
Discovery Health  IDLE / HEALTHY / DEGRADED
Champion          version
Challenger        ID / type / stage
Adaptive Impact   BOUNDED / DISABLED
Broker Authority  NONE for research/shadow
```

A research recommendation must never be rendered as active policy.

## 19. Planned implementation ownership

```text
src/gold_scalp_trader/research/learning.py
src/gold_scalp_trader/research/live_learning.py
src/gold_scalp_trader/research/episode_journal.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
src/gold_scalp_trader/research/promotion.py
src/gold_scalp_trader/management/models.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/persistence/*
```

## 20. Planned proof

Tests must prove idempotent/conflicting source handling, summary recomputation, evidence-environment isolation, frozen entry identity, verified-close queue/receipt semantics, causal path boundaries, exact-once memory ingestion, no self-promotion, no broker authority and local-backup preservation.

Connected DEMO evidence still proves real broker close/deal timing and path-history availability.

## 21. Non-goals / pre-challenge calibration

Learning does not promise self-improving profitability, remove hard safety, mutate after a few trades, auto-merge laptop histories or acquire GitHub/broker credentials.

Open calibration: memory windows, minimum samples, confidence/shrinkage, maximum adaptive effect, clustering, latency/cost metrics and context-specific confluence value.
