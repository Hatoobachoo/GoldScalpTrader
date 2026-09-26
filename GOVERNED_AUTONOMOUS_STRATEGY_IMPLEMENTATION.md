# GoldScalpTrader — Autonomous Research and Governed Strategy Promotion

**Status:** IMPLEMENTATION-SYNC GUIDE — TYPED STAGE EVIDENCE / COUNTERFACTUAL RESEARCH HARDENED
**Scope:** autonomous strategy proposal, evidence binding, validation/promotion hierarchy, shadow counterfactuals and live-authority separation.

## Core rule

Autonomous research may discover and propose improvements. It may not grant itself trading authority.

```text
verified actual/shadow/timing/management evidence
→ declarative hypothesis / Recipe
→ deterministic Candidate
→ durable candidate registry
→ typed next-stage evidence
→ RESEARCHING
→ VALIDATED
→ LOCKED
→ HOLDOUT_PASSED
→ STRESS_PASSED
→ SHADOW
→ DEMO_CANDIDATE
→ APPROVAL_REQUIRED
→ explicit operator approval + rollback target
→ PRODUCTION research/governance stage
→ separate governed deployment/version-selection action
```

A registry stage never edits `Settings`, Risk, Gate, `ACTIVE_STRATEGY_FAMILY`, execution Intents, MT5 writer state or the REAL release lock.

## Primary implementation owners

```text
src/gold_scalp_trader/research/invention.py
    declarative recipes only; no generated executable trading code

src/gold_scalp_trader/research/promotion.py
    legal stage transition policy; no stage skipping

src/gold_scalp_trader/research/candidate_registry.py
    candidate identity, typed stage evidence and authority=NONE invariants

src/gold_scalp_trader/research/evidence.py
    recomputable evidence identity with candidate/dataset SHA-256 binding

src/gold_scalp_trader/research/packages.py
    write-new packages; verification recomputes evidence identity

src/gold_scalp_trader/research/outcomes.py
    actual/shadow outcome separation and conservative counterfactual path evaluation

src/gold_scalp_trader/research/metrics.py
    separate broker-executed metrics and shadow-counterfactual metrics
```

## Source evidence versus promotion evidence

Candidate invention may start from durable source observations such as:

- TimingDecision evidence;
- management-path evidence;
- shadow candidate snapshots;
- verified StrategyMemory observations.

These prove that an observation exists. They **do not** prove that a candidate has passed a promotion stage.

Every promotion stage now requires a typed `candidate_stage_evidence` record bound to:

```text
evidence_id
candidate_id
candidate_fingerprint
exact next target_stage
dataset_sha256
code_revision
config_fingerprint
policy_version
execution_realism
evidence_identity_sha256
artifact_sha256
limitations
result = PASS
runtime_authority = NONE
broker_authority = NONE
```

A generic timing or shadow event therefore cannot masquerade as HOLDOUT/STRESS/SHADOW/DEMO evidence. Evidence belonging to another candidate, fingerprint or target stage is rejected.

## Evidence identity integrity

`candidate_fingerprint` and `dataset_sha256` must be real 64-character SHA-256 hex digests. Evidence-package verification recomputes the identity digest from the canonical identity fields rather than trusting the stored digest alone.

Write-new evidence packages also hash their manifest files and retain `broker_authority=NONE`.

This protects against accidental identity drift and makes dataset/code/config/policy/execution-realism lineage explicit. It does not turn local files into cryptographic proof against a malicious machine owner; operator/release governance remains required.

## Shadow counterfactual discipline

A live `SHADOW_ONLY` candidate snapshot is not automatically a hypothetical trade outcome. Honest counterfactual P/L requires explicit replay geometry:

```text
Episode / family / direction
+ hypothetical entry
+ initial structural SL
+ primary target
+ entry time
+ explicit cost in R
+ chronological completed-candle path
```

`research/outcomes.py` evaluates this research-only path conservatively:

- shadow outcome is always `executed=False`;
- after-cost R is separated from broker P/L;
- chronological candle order is required;
- if one OHLC candle touches both SL and TP, the result is `AMBIGUOUS_INTRABAR_ORDER` and no P/L is invented;
- an unfinished path remains `UNRESOLVED`;
- counterfactual evidence is content-addressed and has broker authority `NONE`.

`research/metrics.py` uses a separate counterfactual summary so shadow R cannot be silently mixed into actual broker-executed R.

## Invention boundary

`Recipe` uses a bounded vocabulary of approved analytical primitives such as:

```text
M5_SETUP
M1_ENTRY_TIMING
EXECUTABLE_COST
MANAGEMENT_EFFICIENCY
STRUCTURE_BREAK
LIQUIDITY_SWEEP
TECHNICAL_LOCATION
SESSION_CONTEXT
NEWS_CONTEXT
```

Unknown primitives are rejected. Invention returns data/semantics, not Python source and not an executable strategy plugin.

## Promotion boundary

Automated promotion may only advance one legal stage at a time. `APPROVAL_REQUIRED → PRODUCTION` requires:

- exact typed PRODUCTION-stage evidence;
- current stage `APPROVAL_REQUIRED`;
- explicit `operator_approved=True`;
- a non-empty rollback target.

Even after that research/governance state transition, `runtime_activation_allowed()` remains false. The registry intentionally has no function that changes live strategy configuration.

## Safety separation

The autonomous/governed subsystem cannot modify:

- REAL hard-disable policy;
- Risk hard ceilings or daily locks;
- Session hard authority;
- Gate decisions;
- sole-writer execution;
- broker account identity checks;
- one-position policy;
- persist-before-send/exactly-once semantics;
- reconciliation requirements.

## What the governance layer does not prove

Strong evidence identity/governance does not by itself prove candidate quality. A genuine candidate still needs appropriate chronological/replay, ablation, walk-forward, one-shot holdout, stress, shadow and connected DEMO evidence.

Counterfactual results must also preserve their limitations: OHLC replay does not magically reveal unknown intrabar order, unrecorded slippage or broker fills.

## Final invariant

> The bot may autonomously propose what to research and accumulate causal evidence. A candidate advances only on stage-specific evidence bound to its immutable identity. Shadow results stay counterfactual, live money stays separate, and no research candidate can activate itself in trading.
