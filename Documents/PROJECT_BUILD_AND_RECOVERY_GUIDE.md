# GoldScalpTrader — Project Build and Recovery Guide

**Status:** POST-AUDIT-1 AGENT OPERATING MANUAL — PRESERVATION-FIRST CORRECTED, IMPLEMENTATION NOT STARTED
**Version:** 1.1-preserved-feature-build-recovery
**Authority:** AI/developer build sequence, documentation-first implementation, context recovery, safe continuation and completion classification.

## 1. Mission / current stage

Work from canonical `Documents/` as durable project truth.

```text
64-file manual                    COMPLETE
Fresh-Zero Audit 1                COMPLETE + preservation correction
Affected-graph sync               CURRENT
Metadata/cross-link normalization PENDING
Implementation                    NOT STARTED
```

## 2. Preservation-first agent rule

GoldSwingTraderAI is the default feature/default baseline.

Before changing an inherited behavior ask:

```text
Is the change directly required by scalping?
OR explicitly instructed by the operator?
OR a proven reference defect correction?
```

If no, preserve it. If uncertain, preserve now and add it to the final documentation discussion rather than redesigning early.

## 3. Agent loop

```text
ORIENT → SCOPE → TRACE → CONTRACT → IMPLEMENT → VERIFY → SYNC → HANDOFF
```

Before coding identify purpose, owner, typed/fresh inputs, outputs/state, bounded-parallel vs ordered authority, fail-closed cases, persistence/recovery, operator view, research, reference-preservation status and proof boundaries.

## 4. Canonical recovery order after context loss

```text
inspect current main HEAD
→ Documents/README
→ Documentation Standard + Preservation Ledger + Comparison
→ System Contract + Architecture
→ relevant topic + active Decisions/Open Questions
→ Module Structure + File/Test Catalog
→ current source/tests/evidence
→ continue first incomplete dependency
```

Repository truth beats remembered chat.

## 5. Architecture orientation

- H1 soft regime; M15 Opportunity/location; M5 completed setup/timing/management; H4 optional; M1 diagnostic/research.
- six reference strategy families preserved.
- bounded analytical concurrency preserved with deterministic one-worker fallback/parity.
- TradePlan owns structural geometry + gross/cost-adjusted room.
- Risk preserves SMALL/MEDIUM/NORMAL profiles and reference bands.
- optional `AGGRESSIVE_SMALL_ACCOUNT` is preserved, disabled by default: 8% max SL-risk ceiling, 16% aggregate/open-risk cap, 16% daily ceiling.
- manual daily-loss reset feature preserved but disabled by default.
- baseline one fresh re-entry + three-loss/30-minute cooldown preserved.
- true News UNKNOWN blocks new scalp entry; valid LKG cache can carry accepted truth across temporary refresh failure.
- provider TTL baseline 1800s.
- Daily PRE_CLOSE T-20/T-10; weekend T-60/T-30; daily reopen 1 clean M5; weekend 2 + gap assessment.
- controlled DEMO before future governed REAL.
- no trading-runtime Git operations.

## 6. Implementation packet

Every material feature packet includes:

- owning contract;
- reference-preservation/delta classification;
- source owner;
- typed inputs/outputs;
- chronology/freshness;
- parallel/serial boundary;
- failure/UNKNOWN behavior;
- persistence/restart effect;
- tests;
- operator mapping;
- research effect;
- evidence boundary;
- full affected documentation graph.

## 7. Docs/code/test disagreement

- frozen contract correct/code wrong → fix code + regression;
- accepted behavior newer/docs stale → repair full graph;
- source/test map stale → correct catalog;
- true design conflict → stop and classify;
- reference differs but no authorized scalp/operator reason exists → preserve reference and repair Scalp docs;
- safer code exposes stale docs → update docs, do not weaken safety.

## 8. Test failure loop

```text
reproduce
→ identify invariant/owner
→ root-cause fix + regression
→ focused proof
→ module/integration proof
→ full local verification
→ affected graph sync
```

Never replace UNKNOWN with optimistic defaults merely to make tests green.

## 9. Broker-write crash rule

If later Intent is `SUBMITTING`/ack ambiguous:

```text
DO NOT RESEND
→ restore Intent identity
→ query positions/orders/deals
→ reconcile exact lifecycle
→ only then allow another governed Intent
```

## 10. Corrupt/missing runtime state

Block affected writes, preserve diagnostics, restore last verified checkpoint to a new DB/path, connect intended MT5 scope, reconcile broker/lifecycle/risk/learning truth and remain RECONCILING while critical facts are unresolved.

Never delete state and invent zero exposure/risk.

## 11. Runtime backup / machine recovery

```text
safe old PRIMARY stop
→ release controller/MT5 authority
→ final local checkpoint/package
→ deliberate transfer
→ restore NEW DB/path
→ configure credentials separately
→ current broker positions/deals/quote/identity
→ reconcile durable lifecycle
→ acquire new controller
→ READY only after hard authorities pass
```

Same-scope simultaneous writers are unsupported without a separate shared-fencing architecture.

## 12. Development/source backup

```text
one coherent remote bulk commit
→ user git pull --ff-only
→ local clone = latest project + full Git history
→ optional secret-clean ZIP milestone copy
```

No pull after every micro-patch. Runtime source publication is absent.

## 13. Runtime capability progression

```text
READINESS / DRY_RUN
→ controlled DEMO PRIMARY
→ future governed REAL
```

REAL is a preserved future capability, disabled/unavailable until its separate evidence/release/explicit-approval gate passes.

## 14. Audit/evidence order

Audit 1 is architecture evidence corrected by preservation-first governance. Audit 2 later checks Documents→Code→Tests. Corrective Audits 3–7 run only when implementation/connected evidence triggers their scope.

A phase is complete only when source exists, focused/full proof actually passes, failure/restart paths are explicit, catalogs/current docs are synchronized, secret/manual gates pass and evidence classes remain honest.

## 15. Next safe dependency

After final documentation audit and operator scalp-delta discussion, implementation begins with package/config/domain/read-only MT5 market truth and bounded analytical foundations—not broker order execution.