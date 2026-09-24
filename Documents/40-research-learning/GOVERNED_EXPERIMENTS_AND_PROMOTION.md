# GoldScalpTrader — Governed Experiments and Promotion

**Status:** DRAFT PRE-CHALLENGE GOVERNANCE CONTRACT — NO CANDIDATE PROMOTED BY DEFAULT
**Version:** 0.1-scalp-evidence-bound-promotion
**Authority:** Champion/Challenger lifecycle, semantic locking, durable evidence lineage, holdout, stress, Shadow, DEMO Canary, approval and rollback.

## 1. Purpose

Research can discover promising scalp changes. Production policy changes only after staged evidence, explicit approval and a known rollback target.

> A candidate can recommend itself. It cannot promote itself.

Hard safety is not an experiment parameter.

## 2. Lifecycle

```text
PROPOSED
→ RESEARCHING
→ VALIDATED
→ LOCKED
→ HOLDOUT_PASSED / HOLDOUT_FAILED
→ STRESS_PASSED / STRESS_FAILED
→ SHADOW
→ DEMO_CANARY
→ PROMOTION_READY
→ PROMOTED only with explicit approval + evidence + rollback target
→ ROLLED_BACK / DISABLED when required
```

A candidate may be REJECTED at appropriate pre-promotion stages.

Every transition carries durable evidence rather than relying only on enum order.

## 3. Evidence-bound transition

Each transition records:

```text
from_stage / to_stage
candidate identity
evidence_id
evidence_sha256
code_revision
policy_version
data_version
actor
reason
recorded_at_utc
```

Stage labels without supporting evidence do not constitute promotion proof.

## 4. Champion and Challenger

`CHAMPION` is currently approved production policy.

`CHALLENGER` is a proposed improvement evaluated against Champion, not merely against zero.

Candidate types may include:

- bounded parameter/family variant;
- Entry Policy;
- Exit/management policy;
- declarative new family.

Risk ceilings, daily lock, identity, reconciliation and broker safety are never challengers.

## 5. Semantic lock

Before final holdout, candidate semantics are frozen to a durable fingerprint.

If recipe, parameter set, data handling, cost model or other meaning changes after lock, it becomes a new candidate/version and restarts the evidence path.

## 6. One-shot final holdout

A final holdout is consumed once by the locked candidate.

Repeated tuning against the same holdout destroys the untouched-holdout claim.

A failed holdout ends that candidate version's holdout claim.

## 7. Scalping stress

A holdout-passing scalp candidate faces declared stress including:

- wider spread;
- adverse slippage;
- execution delay/trigger aging;
- commission/fee assumptions;
- minimum-lot granularity;
- parameter perturbation;
- volatility/regime/session slices;
- News/dislocation contexts where dataset supports them;
- missing optional confluence;
- trade-frequency and sample sensitivity;
- data gaps/chronology checks.

Stress cannot rewrite structural invalidation/targets/original R.

Fragility may fail a candidate even when headline Net R is positive.

## 8. Shadow

Shadow consumes live/forward facts with zero raw broker authority.

It records hypothetical:

- entries/exits;
- missed/extra opportunities;
- cost-adjusted R;
- MAE/MFE/capture;
- hold duration;
- disagreement with Champion;
- session/regime/family differences.

Shadow P/L is not broker P/L.

## 9. DEMO Canary

A DEMO Canary candidate still uses the ordinary governed production path:

```text
TradePlan
→ Monetary Risk
→ Session/News/system authorities
→ DEMO identity/guard
→ Controller/fencing
→ Central Gate
→ one-shot Intent / sole writer
→ reconciliation
```

Promotion registry grants no raw broker authority.

## 10. Explicit approval

`PROMOTION_READY` is not production permission.

Promotion requires:

- complete evidence-bound stage chain;
- exact current semantic fingerprint;
- explicit operator/governed approval;
- approval evidence identity/hash/version/actor/reason;
- known rollback target;
- UTC approval timestamp.

Missing historical evidence is never fabricated from stage labels.

## 11. Rollback / disable

Rollback is durable, explicit and evidence-bound.

Safety violation can disable a candidate immediately through governed failure handling.

Performance rollback should not react blindly to one normal losing streak. It needs documented evidence review.

## 12. Candidate evidence packet

A promotion packet should include/reference:

- hypothesis/non-goals;
- parent family/type;
- required/optional primitives;
- timing/freshness/invalidation/target model;
- dataset/train/validation/holdout boundaries;
- code/policy/schema versions;
- Net/Avg R / Profit Factor / drawdown;
- trade frequency and capacity-admitted trades;
- Opportunity Recall/missed moves;
- Entry/Capture efficiency and premature-exit cost;
- hold duration;
- spread/slippage/transaction-cost burden;
- stress robustness;
- complexity/ablation;
- limitations/reviewer records.

Base and base+optional-confluence metrics remain separate.

## 13. Persistence/local recovery

Candidate stage, fingerprint, holdout consumption, rejection reason, rollback target and full transition ledger persist in canonical StateStore/local checkpoint.

Restore preserves evidence identity. Unsafe migration blocks promotion rather than starting an empty clean registry.

There is no runtime GitHub push/promotion dependency.

## 14. Dashboard

Show:

```text
Champion
Challenger
Candidate stage
semantic fingerprint
evidence age/health
holdout used/not used
stress/shadow/canary status
approval / rollback state
Broker Authority NONE unless ordinary DEMO runtime independently grants it
```

A generic “learning active” label must never hide actual promotion stage.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/research/promotion.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
```

## 16. Planned proof

Tests must prove no stage skipping, evidence-bound transitions, chronological ledger persistence, semantic lock, one-shot holdout, stress/shadow/canary order, zero raw broker authority in research/shadow, normal gates in canary, self-promotion denial, incomplete legacy evidence cannot promote, rollback target/evidence requirement and restart/local-backup continuity.

## 17. Evidence boundary / open items

Software tests prove governance mechanics, not human authentication, market edge or future profitability.

Open items: minimum samples, material-improvement thresholds, Shadow/Canary duration, final approval UX and degradation-alert policy.
