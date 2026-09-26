# GoldScalpTrader — Autonomous Research and Governed Strategy Promotion

**Status:** IMPLEMENTATION-SYNC GUIDE — DURABLE EVIDENCE-BOUND CANDIDATE REGISTRY ACTIVE
**Scope:** autonomous strategy proposal, evidence binding, validation/promotion hierarchy and live-authority separation.

## Core rule

Autonomous research may discover and propose improvements. It may not grant itself trading authority.

```text
verified actual/shadow/timing/management evidence
→ declarative hypothesis / Recipe
→ deterministic Candidate
→ durable candidate registry
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
    durable candidate identity, fingerprint, evidence chain and authority=NONE invariants

src/gold_scalp_trader/research/evidence.py
    immutable evidence identity for reproducible research packages

src/gold_scalp_trader/research/packages.py
    write-new evidence packages with broker_authority=NONE
```

## Evidence sources

Candidate registration must refer to durable evidence already present in the local StateStore. Accepted research evidence namespaces include timing-decision evidence, management-path evidence, shadow-strategy evidence and verified StrategyMemory observations.

Missing evidence IDs fail closed. Candidate semantics are fingerprinted and revalidated when loaded. Stored candidate records explicitly carry:

```text
runtime_authority = NONE
broker_authority  = NONE
```

Authority corruption is treated as state-integrity failure.

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

Automated promotion may only advance one legal stage at a time. Production requires:

- current stage `APPROVAL_REQUIRED`;
- explicit `operator_approved=True` supplied by a separate governed operator action;
- a non-empty rollback target;
- durable promotion evidence.

Even after that research/governance state transition, `runtime_activation_allowed()` remains false. The candidate registry intentionally has no function that changes live strategy configuration.

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

## Required external/deeper proof

Candidate quality still requires real research evidence from replay, ablation, walk-forward, holdout, stress, shadow and DEMO evaluation. The registry proves governance ordering and lineage; it does not prove a candidate is profitable or safe to deploy.

## Final invariant

> The bot may autonomously propose what to research. Evidence and governance decide whether the proposal advances. No research candidate can activate itself in live trading.
