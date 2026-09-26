# GoldScalpTrader — Timing Intelligence, Learning Efficiency and Governed Strategy Improvement

**Status:** IMPLEMENTATION-SYNC GUIDE — TIMING EVIDENCE FOUNDATION ACTIVE / DEEP LEARNING LOOP STILL INTEGRATION WORK
**Version:** 1.0-timing-learning-governance
**Scope:** as-built timing hierarchy, durable timing evidence, efficiency-learning objectives, autonomous strategy research, governed promotion, safety boundaries and remaining integration work.

## 1. Core motive

GoldScalpTrader is not intended to improve merely by taking more trades. The intended improvement loop is:

```text
right setup
→ right active strategy
→ right direction
→ right structural geometry
→ right entry time
→ right risk
→ right management timing
→ right exit time
→ verified broker outcome
→ durable evidence
→ governed research
→ validated policy improvement
```

Timing Intelligence is therefore a first-class subsystem. Its job is not only to say whether a setup exists; it must help determine when an otherwise-valid M5 opportunity is efficient to enter, when it should wait, when it has been chased/missed, and—through downstream verified learning—whether entry and management timing can be improved.

The learning motive is equally important: components that benefit from empirical improvement should become more efficient from verified evidence, while hard safety authorities remain stable and non-self-modifying.

## 2. Authority hierarchy

```text
H1 context
  ↓
M15 location/path context
  ↓
M5 setup + thesis authority
  ↓
Persistent Opportunity concept
  ↓
M1 subordinate timing refinement
  ↓
TimingDecision
  ↓
TradePlan
  ↓
Executable Quality
  ↓
Risk
  ↓
Session / other hard authorities
  ↓
Gate
  ↓
ExecutionIntent
  ↓
sole MT5 writer
```

Timing never grants monetary or broker authority.

M1 cannot invent a standalone live trade. A valid M5 Opportunity must exist first.

## 3. Current timing implementation

Primary code:

```text
src/gold_scalp_trader/decisions/timing.py
```

Current `TimingPolicy` supports versioned calibration dimensions including:

- maximum micro extension in ATR;
- optional M5 event-age limit;
- optional M1 trigger-age limit;
- optional chase-distance limit.

Current `TimingDecision` preserves:

```text
outcome
reason
trigger_time
micro_extension_atr
m5_event_age_seconds
m5_event_age_bars
trigger_age_seconds
chase_atr
profile
policy_version
```

Current outcomes are:

```text
READY_BUY
READY_SELL
WAIT
MISSED
INVALID
```

The timing engine contains family-aware refinement behavior. Reversal families use reversal-oriented micro evidence, while continuation families use continuation/resumption evidence. Exact thresholds remain governed calibration variables rather than automatically self-edited live parameters.

## 4. Runtime position of Timing Intelligence

Primary orchestration:

```text
src/gold_scalp_trader/app/cycle.py
```

Current order is:

```text
build IntelligenceSnapshot
→ detect setup families
→ isolate one ACTIVE_EXECUTION family
→ independent directional fusion
→ create M5 Opportunity
→ timing.evaluate(...)
→ if WAIT/MISSED/INVALID: no TradePlan
→ if READY: build TradePlan
→ Executable Quality
→ Risk
→ hard-authority Gate later in guarded runtime
```

Therefore M1 timing is subordinate to an already-qualified active-family M5 thesis and cannot bypass TradePlan, Quality, Risk or Gate.

## 5. New durable timing-evidence layer

Implemented owner:

```text
src/gold_scalp_trader/research/timing_learning.py
```

Persistent event namespace:

```text
timing_decision_evidence
```

This is a **research-only evidence namespace**. It has no MT5 writer and no ability to approve a trade.

For each meaningful timing decision it records a normalized evidence payload containing, where available:

```text
stable causal episode fingerprint
family
direction
M5 source event IDs
active strategy policy version
M5 event time
coverage
timing outcome
timing reason
timing profile
timing policy version
M1 trigger time
M5 event age in seconds/bars
M1 trigger age
chase ATR
micro extension ATR
spread
downstream cycle status
live action
whether that returned runtime cycle observed a broker write
```

Identical evidence is idempotent. The event key is content-addressed, so unchanged repeated GUI/terminal refresh cycles do not create conflicting duplicate evidence.

## 6. Stable timing episode fingerprint

The current analytical `Opportunity` object may be recreated by the stateless cycle path. Research evidence therefore must not depend only on a transient random Opportunity ID.

The timing-evidence layer derives a stable causal fingerprint from:

```text
family
direction
source_event_ids
strategy policy version
M5 event time
preferred M1 timing profile
```

This allows repeated timing observations for the same causal setup to be grouped for research even before full durable Opportunity lifecycle integration is completed.

Important limitation:

> This fingerprint is a research grouping mechanism, not a substitute for the canonical persistent Opportunity lifecycle required by `ENTRY_TIMING.md`.

Full durable Opportunity WAIT/READY/MISSED/INVALIDATED identity remains a separate integration item and must not be falsely marked complete.

## 7. DEMO runtime wiring

Timing evidence is now wired into both approved DEMO presentation paths.

Terminal path:

```text
python bot.py
→ app.main
→ run_live_demo
→ run_guarded_demo_cycle
→ record_runtime_timing
→ terminal presentation
```

Graphical path:

```text
python bot.py
→ app.main
→ run_live_demo
→ run_graphical_demo
→ RuntimeDashboardProvider
→ run_guarded_demo_cycle
→ record_runtime_timing
→ immutable graphical snapshot
```

Files:

```text
src/gold_scalp_trader/app/demo_runner.py
src/gold_scalp_trader/app/graphical_demo_runner.py
```

The recording step happens after the governed cycle returns and writes only to local `StateStore` research evidence.

It does not perform a broker call.

## 8. What timing learning should ultimately measure

The desired evidence model should support questions such as:

- Was the bot consistently one M1 candle late?
- Did waiting for a reclaim improve expectancy for a specific family?
- Did entry after a particular chase distance reduce realized R?
- Which M1 timing profile works better for each strategy family?
- Does a timing rule improve entry efficiency but reduce opportunity capture excessively?
- Are winners being protected too early?
- Are exits systematically late after momentum/structure deterioration?
- Which session/context produces the best after-cost timing behavior?
- How much edge is lost to spread, slippage, trigger age and decision latency?

The eventual evidence set should include, when causally verifiable:

```text
setup detected time
M5 event knowledge time
Opportunity armed time
M1 trigger time
READY time
actual send time
actual fill time
entry delay
entry reference drift
M5 setup age
M1 trigger age
chase ATR
spread / SL
spread / target
slippage
MAE / MFE
time to primary target
time to expansion target
time to protect
time to trail
exit decision time
actual close time
profit giveback
realized R
entry efficiency
capture efficiency
management efficiency
```

Missing evidence must remain UNKNOWN/None. It must never be fabricated just to complete a learning sample.

## 9. Three learning layers

The project should keep three learning classes separated.

### 9.1 Operational learning

Examples:

- spread distributions;
- slippage;
- deviation/fill behavior;
- decision→send→ack→reconcile latency;
- broker/session operational behavior.

Operational learning may inform calibrated execution assumptions, but cannot bypass Gate or safety limits.

### 9.2 Trading learning

Examples:

- timing profile efficiency;
- family performance;
- BUY/SELL asymmetry;
- session/context performance;
- entry efficiency;
- management timing;
- exit/capture efficiency;
- missed-opportunity cost.

### 9.3 Research learning

Examples:

- ablation;
- walk-forward validation;
- stress testing;
- candidate discovery;
- strategy invention;
- promotion evidence.

These layers must not be collapsed into one opaque self-modifying AI process.

## 10. What may learn and improve

Evidence-driven improvement is appropriate for:

```text
Timing Intelligence calibration
family-specific M1 profiles
setup-quality estimation
entry efficiency
exit efficiency
capture efficiency
management timing
context/session specialization
shadow-strategy evaluation
cost/slippage expectations
candidate strategy discovery
```

Any change that can influence live decisions must be versioned and governed.

## 11. What must not self-modify

Hard safety/governance authorities are not adaptive targets:

```text
REAL release lock
risk hard ceilings
daily-loss hard ceilings
persist-before-send
sole MT5 writer
exactly-once execution semantics
account identity verification
one-position rule
no martingale
no uncontrolled grid
no averaging down
reconciliation requirements
verified-close requirement
research/live authority separation
```

Central rule:

> **The bot may learn how to trade better; it may not learn how to bypass its safety system.**

## 12. Actual verified learning pipeline

Current actual trade-learning owners:

```text
management/closure.py
research/live_learning.py
research/learning.py
```

Current verified-close ordering preserves:

```text
verified full close
→ closed_trade_learning_queue
→ closure receipt
→ later LearningObservation
→ StrategyMemory
→ queue consumed only after durable save
```

`LearningObservation` already supports:

```text
realized_r
entry_efficiency
capture_efficiency
```

but missing values remain `None`; the system does not fabricate them.

A future integration packet must connect richer timing/path evidence to the immutable ManagedTrade/verified-close learning lineage so those metrics can be calculated from real causal evidence rather than merely existing as optional fields.

## 13. Autonomous strategy invention

Primary code:

```text
src/gold_scalp_trader/research/invention.py
```

Autonomous invention is declarative. It does not generate executable Python trading code.

Allowed primitives include concepts such as:

```text
M5_SETUP
M1_ENTRY_TIMING
EXECUTABLE_COST
MANAGEMENT_EFFICIENCY
structure
liquidity
technical location
session/news context
```

A recipe produces a research `Candidate` with deterministic identity and semantics.

Autonomous discovery may propose:

- new feature combinations;
- timing variants;
- management variants;
- regime/context specializations;
- candidate family semantics.

It may not grant itself broker authority.

## 14. Governed promotion hierarchy

Primary code:

```text
src/gold_scalp_trader/research/promotion.py
```

Current promotion stages include:

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

Automated stage skipping is forbidden.

Production promotion requires explicit operator approval and a rollback target.

Timing evidence may become research evidence for a candidate, but collecting timing evidence does not itself advance a candidate or alter the active strategy.

## 15. Desired governed improvement loop

```text
verified actual + shadow evidence
→ StrategyMemory / episode journal
→ timing/family/context analysis
→ hypothesis
→ candidate
→ replay
→ ablation
→ walk-forward
→ holdout
→ stress
→ shadow
→ DEMO candidate
→ explicit approval boundary
→ versioned policy
```

Every step must preserve evidence lineage.

## 16. Shadow strategy role

The five non-active families should eventually provide same-episode counterfactual evidence:

```text
active family actual decision/outcome
vs
shadow family hypothetical setup/timing/plan/outcome
```

Shadow results are research counterfactuals, never broker P/L.

This comparison is essential for deciding whether an active strategy, timing profile or management rule is genuinely more efficient than alternatives under the same market episode.

Current strategy isolation prevents shadow families from broker authority. Deep shadow outcome/learning integration remains an audit and implementation area.

## 17. Current packet: implemented vs pending

### Implemented in this packet

- durable append-only timing-decision evidence;
- stable causal timing episode fingerprint;
- timing policy/profile/version preservation in research evidence;
- M5/M1 age/chase/extension preservation;
- downstream status/action association;
- GUI DEMO evidence wiring;
- terminal DEMO evidence wiring;
- idempotent duplicate handling;
- governed research summary by outcome/family/profile;
- dedicated tests for evidence stability/idempotency/separation.

### Still pending / must be challenged

- canonical persistent Opportunity identity across WAIT/READY cycles;
- explicit durable READY/TRIGGERED transition ownership;
- timing lineage frozen into ManagedTrade at verified OPEN;
- actual fill/reference/slippage linkage;
- causal M1/M5 path reconstruction for entry efficiency;
- MAE/MFE and capture-efficiency calculation from verified path;
- management timing evidence journal;
- shadow timing/outcome learning loop;
- timing-evidence consumption by replay/ablation/walk-forward tooling;
- evidence-bound candidate generation from efficiency findings;
- policy package generation/promotion integration;
- connected DEMO timing proof;
- dashboard timing-learning analytics panel;
- Session authority integration remains separately required.

None of these pending items should be described as complete merely because supporting modules exist.

## 18. Testing ownership

New focused test:

```text
tests/test_timing_learning_lineage.py
```

It proves:

- same causal setup produces the same research episode fingerprint;
- identical timing evidence is idempotent;
- family, policy, trigger age and chase survive persistence;
- READY and WAIT evidence remain distinguishable;
- research summary can associate broker-write-returning cycles without granting authority.

Full offline verification must still be run locally with:

```powershell
python scripts/verify_offline_release.py
```

## 19. Safety boundaries

The timing evidence module:

- imports no MT5 writer;
- calls no `order_send`;
- cannot enable REAL;
- cannot alter Risk;
- cannot alter Gate;
- cannot change active strategy;
- cannot promote a research candidate;
- writes only local checksummed research events through `StateStore`.

## 20. Next implementation priority

The next coherent work should connect timing evidence to the immutable trade lifecycle without weakening safety:

```text
READY timing evidence
→ persisted OPEN context
→ verified broker OPEN
→ ManagedTrade timing lineage
→ verified close
→ learning queue
→ LearningObservation timing/path metrics
→ governed efficiency report
```

After that, management timing and shadow counterfactual learning can be deepened.

## 21. Final invariant

> **Timing Intelligence must improve the quality of WHEN the bot acts, but never become an independent trade inventor or broker authority. Learning must convert verified evidence into governed, versioned improvement—not uncontrolled self-modification. Autonomous research may propose; validation and governance decide what is allowed to affect live execution.**
