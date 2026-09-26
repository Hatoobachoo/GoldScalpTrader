# GoldScalpTrader — Timing Intelligence, Efficiency Learning and Governed Improvement

**Status:** IMPLEMENTATION-SYNC GUIDE — CAUSAL TIMING/TRADE LEARNING ACTIVE / CONNECTED CALIBRATION PENDING  
**Version:** 2.0-causal-efficiency-governance  
**Scope:** as-built Timing Intelligence, persistent Opportunity lifecycle, timing/management learning, actual-vs-shadow evidence, counterfactual discipline, candidate governance and remaining connected proof.

## 1. Core motive

GoldScalpTrader is designed around:

```text
right setup
→ right strategy
→ right direction
→ right structural geometry
→ right risk
→ right time
→ right management
→ verified outcome
→ causal evidence
→ governed improvement
```

The objective is not maximum trade count. It is better decision and management efficiency under stable safety authority.

## 2. Authority hierarchy

```text
H1 / M15 context
→ market-first M5 setup detection
→ one ACTIVE_EXECUTION family + five SHADOW_ONLY families
→ independent BUY / SELL thesis + Red Team
→ persistent M5 Opportunity/Episode
→ subordinate M1 TimingDecision
→ structural TradePlan
→ Executable Quality
→ monetary Risk
→ hard Session authority
→ Gate
→ durable Intent
→ sole MT5 writer
→ broker reconciliation
→ ManagedTrade
→ verified close
→ exactly-once learning
```

M1 cannot invent a production trade. Timing cannot bypass TradePlan, Risk, Session, Gate or execution safety.

## 3. Entry Timing Intelligence

Primary implementation:

```text
src/gold_scalp_trader/decisions/timing.py
src/gold_scalp_trader/app/opportunity_lifecycle.py
src/gold_scalp_trader/research/timing_learning.py
```

Timing outcomes:

```text
READY_BUY
READY_SELL
WAIT
MISSED
INVALID
```

Timing evidence preserves, where available:

```text
Opportunity ID
Episode ID
Opportunity created/updated time
Timing decision time
family / direction
M5 source-event IDs
strategy policy version
M5 event time
M1 trigger time
timing profile / policy version
M5 event age
M1 trigger age
chase ATR
micro-extension ATR
spread
downstream cycle status
broker-write association
```

The persistent Opportunity lifecycle keeps the same causal identity across repeated WAIT/READY refreshes and restart. A terminal causal episode cannot silently re-arm merely because a fresh in-memory object receives another random ID.

## 4. Entry-to-trade lineage

Before the irreversible OPEN send, the governed runtime freezes the causal entry context. After verified broker reconciliation the same context is carried into `ManagedTrade` and then through verified close into StrategyMemory.

Durable trade lineage includes:

```text
opportunity_id
episode_id
trade_plan_id
approved entry reference
M5 source-event IDs / event time
timing profile / version
M1 trigger time
M5 event age
trigger age
chase ATR
micro extension ATR
strategy family / policy version
```

Missing lineage remains `None`; it is not backfilled from hindsight.

## 5. Management Timing Intelligence

Research-only management observations are recorded by:

```text
src/gold_scalp_trader/research/runtime_evidence.py
```

Each observed governed management cycle may preserve:

```text
trade / position identity
family / policy / direction
captured time
HOLD / PROTECT / TRAIL / RUNNER / EXIT action
reason
observed open R
initial monetary R when broker symbol economics are available
bars in trade
spread
current/original SL
primary/expansion targets
Opportunity / Episode / TradePlan lineage
Timing profile/version
```

These observations do not decide live policy. They form causal research evidence for whether protection, trailing or exits occur too early or too late.

## 6. Verified-close efficiency learning

`management/closure.py` now derives post-trade metrics only from evidence that can be supported by the durable trade path.

When evidence exists, StrategyMemory can preserve:

```text
initial_risk_money
after-cost realized_r
entry_reference_drift_r
observed_mfe_r
observed_mae_r
observed_capture_efficiency
observed_giveback_r
opportunity_to_entry_seconds
ready_to_entry_seconds
trigger_to_entry_seconds
m5_event_to_entry_seconds
time_to_first_protect_seconds
time_to_first_trail_seconds
time_to_observed_primary_target_seconds
time_to_observed_expansion_target_seconds
time_to_observed_mfe_seconds
management_samples
```

### Evidence-label rule

`observed_mfe_r` / `observed_mae_r` are **runtime-observed path statistics**, not claims of perfect tick-by-tick or intrabar extrema.

`observed_capture_efficiency` is based on observed MFE and verified after-cost realized R. It is deliberately named `observed_...` so research cannot silently treat sampled runtime visibility as complete market truth.

Canonical `entry_efficiency` and full-path `capture_efficiency` remain `None` until a separately governed, causal definition has sufficient evidence. Missing values are never replaced with zero.

## 7. Exactly-once actual learning

Current path:

```text
exact broker close proof
→ close archive
→ closed_trade_learning_queue
→ immutable source validation
→ StrategyMemory save with allow_replace=False
→ queue consume only after durable save
```

Actual learning cannot originate from an unverified close.

## 8. Shadow evidence versus shadow outcome

The live runtime records same-market SHADOW_ONLY candidate snapshots, but a candidate snapshot is **not** automatically hypothetical P/L.

Snapshot evidence includes candidate family/direction/qualification/score/coverage/source events/context without broker authority.

A genuine counterfactual outcome requires explicit hypothetical geometry and a causal replay path:

```text
episode / family / direction
+ entry
+ initial SL
+ primary target
+ timezone-aware entry time
+ explicit cost in R
+ chronological completed candles beginning no earlier than entry time
```

Research owner:

```text
src/gold_scalp_trader/research/outcomes.py
```

Rules:

- result remains `SHADOW_ONLY` and `executed=False`;
- cost is subtracted explicitly in R;
- pre-entry candles are rejected;
- non-chronological candles are rejected;
- if one OHLC bar touches SL and TP, order is unknowable → `AMBIGUOUS_INTRABAR_ORDER`, no invented P/L;
- incomplete paths remain `UNRESOLVED`;
- counterfactual evidence is stored separately from broker P/L.

Actual and shadow P/L metrics are also separated in `research/metrics.py`; shadow R is never silently merged into actual execution metrics.

## 9. Three learning layers

### Operational learning

```text
spread
slippage
deviation/fill behavior
latency
broker/session operational behavior
```

### Trading learning

```text
M1 timing quality
entry delay/drift
family/context performance
management timing
observed MFE/MAE/giveback
actual-vs-shadow differences
```

### Research learning

```text
replay
ablation
walk-forward
one-shot holdout
stress
counterfactual evaluation
candidate discovery
promotion evidence
```

These layers are intentionally separate.

## 10. What may improve

Governed research may propose changes to:

- TimingPolicy calibration;
- family-specific M1 profiles;
- setup-quality estimation;
- entry/management/exit timing;
- context specialization;
- strategy-family selection evidence;
- cost/slippage assumptions;
- declarative candidate strategy variants.

A research result never changes production merely because it scores better.

## 11. What must remain non-adaptive safety authority

```text
REAL release lock
Risk hard ceilings
daily-loss ceilings
persist-before-send
one-shot financial execution
sole MT5 writer
account identity verification
one-position rule
no martingale/grid/averaging-down rescue
reconciliation requirements
Session hard-authority semantics
verified-close requirement
recovery safety
```

> The bot may learn how to trade better; it may not learn how to bypass its safety system.

## 12. Autonomous invention and candidate identity

Autonomous invention remains declarative; it does not generate live Python strategy code.

Candidate semantics receive deterministic fingerprints. Source observations can come from actual StrategyMemory, timing evidence, management evidence, shadow snapshots and governed shadow-counterfactual outcomes.

Source evidence means “this observation exists.” It does **not** mean “the candidate passed a validation stage.”

## 13. Typed governed promotion evidence

Promotion owner:

```text
src/gold_scalp_trader/research/candidate_registry.py
src/gold_scalp_trader/research/promotion.py
src/gold_scalp_trader/research/evidence.py
src/gold_scalp_trader/research/packages.py
```

Promotion stages:

```text
PROPOSED
→ RESEARCHING
→ VALIDATED
→ LOCKED
→ HOLDOUT_PASSED
→ STRESS_PASSED
→ SHADOW
→ DEMO_CANDIDATE
→ APPROVAL_REQUIRED
→ PRODUCTION
```

Every step requires typed evidence bound to:

```text
candidate ID
candidate fingerprint
exact next target stage
dataset SHA-256
code revision
config fingerprint
policy version
execution realism
evidence identity SHA-256
artifact SHA-256
limitations
```

A normal Timing event or shadow snapshot cannot masquerade as HOLDOUT/STRESS/DEMO proof.

Evidence identities are recomputed on verification. Candidate and dataset identity fields must be real SHA-256 digests.

`APPROVAL_REQUIRED → PRODUCTION` additionally requires explicit operator approval and rollback lineage. Even `PRODUCTION` in the research registry has no direct runtime activation authority.

## 14. Replay / bias controls already present

Research replay uses completed candles and chronological prefixes. M1 is visible only after its candle close is knowable at the replay decision timestamp.

Validation helpers enforce non-overlapping chronological windows and a one-shot final holdout identity.

Counterfactual replay refuses unknown intrabar SL/TP ordering instead of choosing the profitable interpretation.

These protections reduce look-ahead leakage but do not prove a candidate is robust; dataset quality, regime coverage and connected DEMO evidence still matter.

## 15. Recovery / persistence

Timing evidence, management evidence, StrategyMemory, candidate stage evidence and shadow-counterfactual outcomes live in `StateStore` namespaces.

Full checkpoint export defaults to all existing namespaces, so these research/governance records are included in normal full checkpoints. Recovery still requires fresh broker reconciliation before financial authority resumes.

## 16. Connected DEMO evidence visibility

Read-only connected certification/reporting can expose:

- hard Session state;
- Timing sample counts;
- broker-write-associated Timing samples;
- management evidence counts;
- shadow candidate counts;
- actual learning counts.

These counts improve observability but do not automatically PASS canonical connected drills. Real Exness schedule, fill/slippage/latency, lifecycle, restart and statistically meaningful learning remain external evidence.

## 17. Current limitations / intentionally unproven items

The implementation deliberately does **not** claim:

- an “ideal entry” derived from hindsight;
- perfect tick-level MFE/MAE from polling observations;
- true counterfactual broker fills from OHLC candles;
- shadow P/L without explicit TradePlan-like geometry;
- candidate quality merely because promotion bookkeeping is valid;
- automatic live deployment of a research candidate;
- connected DEMO certification from offline tests;
- profitability.

Further calibration should be driven by accumulated DEMO evidence rather than by adding self-modifying authority.

## 18. Focused proof owners

```text
tests/test_timing_learning_lineage.py
tests/test_runtime_research_evidence.py
tests/test_live_learning_pipeline.py
tests/test_research_integrity.py
tests/test_candidate_registry.py
tests/test_full_checkpoint.py
```

Full regression remains:

```powershell
python scripts/verify_offline_release.py
```

## 19. Final invariant

> Timing Intelligence improves **WHEN** a valid setup acts. Management learning measures **HOW** the trade was managed. Shadow research asks **WHAT IF** without pretending counterfactuals were broker trades. Autonomous research proposes **WHAT TO TEST**. Evidence and governance decide what advances. Hard safety authority remains outside the learning search space.
