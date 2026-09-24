# GoldScalpTrader — System Contract

**Status:** FROZEN V1 SYSTEM CONTRACT — PRESERVATION-FIRST CORRECTION / EXTERNAL PROOF PENDING
**Version:** 1.1-preserved-reference-features
**Authority:** Highest-level behavioural, chronology, ownership, accounting, recovery, learning and broker-safety invariants.

## 1. Constitution / conflict rule

Every runtime mode, intelligence desk, strategy family, decision component, Risk authority, broker operation, persistence workflow, learning path and operator view preserves this contract.

A material reference difference is allowed only when it is:

1. directly required by the scalp horizon/market geometry;
2. explicitly instructed by the operator; or
3. a separately proven defect correction.

Otherwise GoldSwingTraderAI feature/default behaviour remains the baseline. Uncertainty resolves to preservation and later discussion, not silent simplification.

## 2. Whole lifecycle

```text
verified broker/provider facts
→ one immutable MarketSnapshot
→ causal independent evidence
→ bounded-parallel six attributable scalp hypotheses
→ independent BUY / SELL theses + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing / event freshness
→ structural TradePlan + gross/cost-adjusted room
→ profiled monetary RiskEvaluation
   SMALL / MEDIUM / NORMAL
   + optional explicit AGGRESSIVE_SMALL_ACCOUNT overlay
→ hard authorities
→ central ExecutionPermissionGate
→ durable one-shot ExecutionIntent
→ sole MT5Writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close/accounting
→ durable downstream learning/research
```

No downstream component may retroactively invent upstream truth.

## 3. Scalp timeframe / chronology invariants

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote current executable condition only
```

- candle-derived production facts use completed bars and causal knowledge time;
- forming candles cannot masquerade as completed facts;
- current quote/tick may invalidate executability but not fabricate historical structure;
- replay uses only information available at simulated decision time;
- UNKNOWN required truth is never guessed into PASS/CLEAR/zero;
- restored local state is context, not broker truth;
- unknown exposure is never zero.

## 4. One-read-boundary invariant

A governed cycle begins from one normalized snapshot assembled through the MT5 read boundary. Analytical desks/families do not make hidden independent MT5 reads.

## 5. Bounded analytical concurrency invariant

Dependency-independent analytical desks/families preserve the bounded-parallel capability of the reference architecture.

Any concurrent implementation must use:

- immutable shared inputs;
- bounded workers/resources;
- deterministic canonical output ordering;
- visible failure/degradation;
- no lifecycle/persistence/broker mutation from workers;
- semantic parity with a deterministic one-worker fallback.

The one-worker path is required for fallback/testing but does not remove bounded analytical concurrency as a feature.

## 6. Serial authority invariant

```text
TradePlan
→ active monetary Risk profile/overlay
→ session/news/system/account/controller authorities
→ central Gate
→ durable Intent
→ fresh broker checks
→ sole writer
→ reconciliation
```

No strategy, dashboard, research, learning or analytical worker bypasses this chain.

## 7. Strategy / geometry / Risk separation

Strategy determines whether a thesis is worth pursuing. Entry Timing decides current M5 readiness. TradePlan defines structural entry/invalidation/objectives and gross/cost-adjusted room. Risk decides monetary affordability for that already-defined geometry.

Risk never moves structural stop or increases because analytical confidence is high.

## 8. Scalp cost / freshness invariants

Scalping distinguishes Signal Price, Approved Entry Reference, executable Bid/Ask, Actual Fill, structural stop/target, spread, explicit reserves and actual slippage/fees.

Costs are counted exactly once. Event/trigger age, chase distance and entry drift are first-class. A setup whose remaining edge is consumed by friction is not equivalent to the same chart geometry under low costs.

Swing's 1.20R hard floor is not automatically imposed as the scalp hard floor; this does not alter unrelated Risk features.

## 9. Opportunity invariants

Opportunity identity, causal event lineage, trigger age and late-entry state are explicit/durable. Terminal thesis does not become new merely because another polling cycle arrives. Re-arm requires genuinely new causal evidence.

## 10. Preserved Risk invariants

Profile is fixed from positive DayStartEquity at the UTC risk-day boundary:

```text
SMALL   < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

| Profile | Normal / target | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0%–4.5% | >4.5%–6.5% | 7% | 12% |
| MEDIUM | 2.0%–3.0% | >3.0%–4.5% | 5% | 9% |
| NORMAL | 1.0%–2.0% | >2.0%–3.5% | 4% | 7% |

Further invariants:

- broker min/max/step and actual normalized-volume risk;
- structural-stop-aware sizing;
- margin/affordability/exposure checks;
- one independently risk-bearing Gold position per scope in initial V1;
- fail closed on missing critical financial truth;
- no martingale, uncontrolled grid or averaging-down rescue;
- governed manual daily-loss reset capability is preserved but disabled by default;
- one genuinely fresh same-episode re-entry under the preserved baseline;
- three consecutive closed bot losses trigger at least 30 minutes global cooldown plus required fresh/healthy release conditions.

### 10.1 Aggressive small-account invariant

Preserved explicit operator-requested option:

```text
disabled by default
eligibility baseline: positive DayStartEquity < $1,000
8%  maximum monetary SL-risk ceiling per trade — NOT target
16% maximum aggregate open risk
16% daily loss ceiling
```

It never auto-enables merely from equity and does not weaken structural/session/news/execution safeguards.

The provisional 0.50% scaffold is not canonical policy.

## 11. Session / News invariant

For new scalp entry:

```text
OPEN + NEWS_CLEAR       → may proceed
OPEN + NEWS_BLACKOUT    → BLOCK
OPEN + NEWS_UNKNOWN     → BLOCK / LIMITED
```

A temporary provider failure with a still-valid accepted LKG cache does not automatically create UNKNOWN. Failure never extends or rewrites cache timestamps/TTL.

Preserved baselines:

```text
provider TTL 1800 seconds
Daily PRE_CLOSE T-20 no entry / T-10 flatten
Weekend PRE_CLOSE T-60 no entry / T-30 flatten
Daily reopen 1 clean completed M5
Weekend reopen 2 clean completed M5 + gap assessment
```

Current broker schedule/holiday truth remains an external verification requirement.

## 12. Intent / execution invariants

Every irreversible broker action has durable identity before send. One Intent has at most one irreversible send allowance. Raw MT5 write boundary is singular. Timeout/uncertain acknowledgement becomes reconciliation, never blind resend. Local lifecycle changes only from broker-verified truth.

Capability progression:

```text
READINESS / DRY_RUN
→ controlled DEMO
→ future governed REAL
```

REAL remains a preserved future capability but is disabled/unavailable until its DEMO, release and explicit approval gate is satisfied.

## 13. Position-management invariant

Trade Manager owns:

```text
HOLD / PROTECT / TRAIL / RUNNER / EXIT
```

Scalp-specific management differences:

- time/efficiency failure is an EXIT reason;
- Runner is exceptional and requires fresh continuation/new objective.

Broker-valid partial management remains a preserved optional capability where volume is divisible; correctness at minimum indivisible volume never depends on it.

## 14. Accounting / ownership

Bot-owned activity, external/manual activity and non-trading cash flow remain distinguishable. Bot performance requires verified lineage. Unknown external positions are never silently adopted.

## 15. Persistence / recovery

Restart is not a fresh day. Durable state preserves risk-day/profile/overlay identity, Opportunity/TradePlan, Intent, ManagedTrade, close/reconciliation, learning queue/receipt and policy/schema identity as applicable.

Startup reconciles current broker truth before write authority. Current broker truth outranks restored local context.

## 16. Runtime local backup

Runtime checkpoints/recovery packages are local recovery artifacts, not broker authority. Backup root is outside repo by default; secrets are excluded; consistent snapshots are required; failure is explicit.

Graceful shutdown may create a verified local checkpoint but performs no Git commit/push/pull.

## 17. Development/source backup

```text
one coherent remote commit
→ operator git pull --ff-only
→ local clone contains latest source + full Git history
→ optional secret-clean ZIP milestone copy
```

This is an explicit operator-directed workflow difference from the reference publication path.

## 18. Learning / research / AI

Learning may observe, remember, research and propose. It cannot relax hard Risk, bypass identity/session/news/controller/reconciliation, call writer or self-promote production policy.

## 19. Dashboard invariant

Terminal/browser dashboards consume authoritative state and are read-only. They show the active Risk profile/overlay and provider/cache truth rather than recalculating them.

## 20. Evidence invariant

Keep separate:

- preserved reference default;
- scalp-specific documented change;
- implementation proof;
- replay/calibration evidence;
- connected DEMO evidence;
- future REAL release evidence;
- profitability.

No test count or documentation decision proves future profitability.