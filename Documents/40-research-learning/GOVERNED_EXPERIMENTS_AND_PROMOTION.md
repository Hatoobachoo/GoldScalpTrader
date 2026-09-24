# GoldScalpTrader — Governed Experiments and Promotion

**Status:** FROZEN V1 PROMOTION GOVERNANCE — NO CANDIDATE PROMOTED BY DEFAULT
**Version:** 1.0-preservation-first-evidence-bound-promotion
**Authority:** Champion/Challenger lifecycle, semantic locking, durable evidence lineage, holdout, stress, Shadow, DEMO Canary, explicit approval and rollback.

## 1. Purpose

Research can discover promising scalp changes. Production policy changes only after staged evidence, explicit approval and a known rollback target.

> A candidate can recommend itself. It cannot promote itself.

Hard safety and preserved non-scalp reference defaults are not ordinary experiment parameters.

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

Candidate may be REJECTED before promotion. Every transition carries durable evidence.

## 3. Evidence-bound transition

Record from/to stage, candidate identity, evidence ID/hash, code revision, policy/data version, actor, reason and UTC timestamp. Stage label without supporting evidence is not promotion proof.

## 4. Champion / Challenger

`CHAMPION` is currently approved production policy. `CHALLENGER` is a proposed improvement evaluated against Champion.

Candidate types may include bounded family/parameter variant, Entry Policy, Exit/management policy and declarative new family.

## 5. Preservation-first promotion rule

A candidate that changes a **preserved GoldSwingTraderAI feature/default** needs more than positive research.

Before promotion it must be classified as:

```text
genuine scalp-specific change
OR explicit operator-directed change
OR proven reference defect correction
```

and the full documentation affected graph must be updated. If that classification is not established, preserved baseline remains Champion.

Hard account/broker safety such as identity, UNKNOWN fail-closed behavior, one-shot submission, reconciliation/controller fencing and secret handling cannot be promoted away.

Canonical preserved Risk/profile/session values also cannot be silently reclassified as “tunable scalp parameters.” A deliberate later change requires its own governed decision.

## 6. Semantic lock

Before final holdout, candidate semantics are frozen to a durable fingerprint. Recipe/parameter/data/cost-model meaning change after lock creates a new candidate/version.

## 7. One-shot final holdout

Final holdout is consumed once by locked candidate. Repeated tuning against same holdout destroys untouched-holdout claim. Failed holdout ends that candidate version's claim.

## 8. Scalping stress

A holdout-passing scalp candidate faces declared stress including wider spread, adverse slippage, execution delay/trigger aging, fees, min-lot granularity, parameter perturbation, volatility/session slices, News/dislocation where covered, missing optional confluence, frequency/sample sensitivity and chronology/data-gap checks.

Stress cannot rewrite structural invalidation/targets/original R or silently alter account Risk policy.

## 9. Shadow

Shadow consumes live/forward facts with zero broker authority. It records hypothetical entries/exits, missed/extra opportunities, cost-adjusted R, MAE/MFE/capture, duration, Champion disagreement and context. Shadow P/L is never broker P/L.

## 10. DEMO Canary

A DEMO Canary still uses ordinary production safety:

```text
TradePlan
→ active preserved monetary Risk profile/optional explicit overlay
→ Session/News/system authorities
→ DEMO identity
→ Controller
→ central Gate
→ one-shot Intent / sole writer
→ reconciliation
```

Promotion registry grants no raw broker authority.

## 11. Future REAL boundary

Future REAL is a preserved governed capability, but a candidate reaching DEMO Canary or even promotion does **not** automatically authorize REAL execution.

REAL requires the separate runtime/release/explicit-approval gate owned by execution/release governance.

## 12. Explicit approval

`PROMOTION_READY` is not production permission. Require complete evidence chain, exact fingerprint, explicit operator/governed approval, approval evidence identity/hash/version/actor/reason, rollback target and UTC timestamp.

Missing historical evidence is never fabricated.

## 13. Rollback / disable

Rollback is durable/evidence-bound. Safety violation can disable a candidate through governed failure handling. Performance rollback does not react blindly to one normal losing streak.

## 14. Candidate evidence packet

Include hypothesis/non-goals, parent/type, required/optional primitives, timing/freshness/invalidation/target model, dataset boundaries, code/policy/schema versions, Net/Avg R/PF/drawdown, admitted frequency, Opportunity Recall, Entry/Capture efficiency, duration, costs, stress robustness, complexity/ablation, limitations and reviewers.

## 15. Persistence/local recovery

Candidate stage, fingerprint, holdout use, rejection, rollback and transition ledger persist in canonical StateStore/local checkpoint. Restore preserves evidence identity. No runtime GitHub push/promotion dependency.

## 16. Dashboard

Show Champion, Challenger, stage, fingerprint, evidence health, holdout state, stress/shadow/canary, approval/rollback and `Broker Authority NONE` unless ordinary DEMO runtime independently grants it.

## 17. Planned implementation ownership

```text
src/gold_scalp_trader/research/promotion.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
```

## 18. Planned proof / open research

Tests prove no stage skipping, evidence-bound transitions, semantic lock, one-shot holdout, stress/shadow/canary order, zero research broker authority, canary ordinary gates, self-promotion denial, incomplete-evidence rejection, rollback requirement and restart continuity.

Open values include minimum samples, material-improvement thresholds, Shadow/Canary duration, approval UX and degradation-alert policy.