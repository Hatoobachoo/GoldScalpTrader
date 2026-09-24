# GoldScalpTrader — Open Questions and Closure Plan

**Status:** DRAFT QUESTION REGISTER — PRE-CHALLENGE
**Version:** 0.2-full-manual-draft
**Authority:** Unresolved choices, required evidence and completion boundaries.

## 1. Why this file exists

An open question is not automatically a design failure. Some choices require architecture review, historical calibration, connected broker/machine proof or deliberate deferral.

Classes:

```text
FIX BEFORE BUILD
IMPLEMENTATION CHOICE
CALIBRATE IN RESEARCH
EXTERNAL PROOF
DEFERRED V1
```

Nothing in this register may be silently guessed during coding.

## 2. FIX BEFORE BUILD

### OQ-001 — Final timeframe authority

Decide final roles for H4/H1/M15/M5/M1 and quote/tick context.

Current baseline: H1 broad regime, M15 opportunity/location, M5 primary setup/timing, H4 optional major context, M1 diagnostic only.

Closure: fresh-zero review + cross-document sync.

### OQ-002 — Strategy-family decomposition

Do all six starting families remain independent and useful for scalping, or should any be merged/split/replaced?

Closure: fresh-zero review, logic decomposition and initial replay design.

### OQ-003 — `OPEN + News UNKNOWN` policy

Reference Swing system allowed adaptive continuation. Scalping may need stronger caution.

Closure: architecture decision plus replay/connected evidence plan; no implementation guess.

### OQ-004 — Minimum structural R / cost-adjusted room

Swing's 1.20R Primary floor is not automatically inherited.

Closure: define structural quality metric before implementation, numerical threshold may remain CALIBRATE.

### OQ-005 — Risk-policy shape

Define final account-profile model and whether an optional aggressive small-account mode should exist at all.

Closure: fresh-zero challenge before build; exact percentages may remain CALIBRATE.

### OQ-006 — Runtime mode scope

Confirm V1 build target after DRY_RUN documentation phase: read-only/DRY_RUN only first, then governed DEMO writer; REAL remains separately governed/out-of-scope unless explicitly decided.

Closure: architecture decision.

## 3. IMPLEMENTATION CHOICES

### OQ-020 — Python/package layout

Choose supported Python version based on current MetaTrader5 compatibility and fix provisional `src/` package launch/install design.

Closure: verify current package/platform compatibility, update setup docs, implement installable package.

### OQ-021 — SQLite detail

Confirm SQLite/WAL/synchronous/checksum/schema/migration implementation.

Architecture currently favors simple local SQLite but does not freeze low-level settings yet.

### OQ-022 — Bounded parallel scheduler

Choose worker implementation/limits while preserving one-worker semantic parity and deterministic output order.

### OQ-023 — Dashboard stack

Confirm Rich/wcwidth dependency and when secondary browser dashboard enters build sequence.

### OQ-024 — Secret scanner / Documents verifier implementation

Choose smallest dependable local scripts and tests; no cloud/Actions requirement.

### OQ-025 — Local backup implementation

Choose SQLite backup API/export mechanism, manifest format, catalog naming, free-space handling and optional second-drive copy.

## 4. CALIBRATE IN RESEARCH

### OQ-040 — Event freshness

Family/event-specific M5 age, distance-travelled and extension thresholds.

### OQ-041 — Entry/chase policy

Maximum acceptable drift from approved entry, trigger age and processing delay.

### OQ-042 — Spread / execution friction

Healthy baseline method, spread-to-stop/target thresholds, slippage reserve and broker deviation policy.

### OQ-043 — Structural target quality

Minimum gross R, cost-adjusted room and objective hierarchy thresholds.

### OQ-044 — Risk percentages

Preferred/elevated/hard-ceiling bands and daily-loss limits for SMALL/MEDIUM/NORMAL profile if profiles survive challenge.

Current 0.50% scaffold is provisional; reference aggressive bands are not frozen.

### OQ-045 — Cooldown / same-episode re-entry

Loss-streak threshold, cooldown time/conditions and maximum fresh re-entry count.

### OQ-046 — Session specialization

Whether Asia/London/NY/overlap receive family/timing conditioning and whether this improves out-of-sample net expectancy after costs.

### OQ-047 — News blackout/warmup

Event tiers, pre/post windows and post-news clean-bar/spread-normalization requirements.

### OQ-048 — Reopen/pre-close timing

Exact daily/weekend no-entry and flatten cutoffs plus clean completed-M5 reopen requirement.

### OQ-049 — Trade Manager time efficiency

Normal hold-duration distribution, soft/hard time exit and target/protection timing.

### OQ-050 — Runner/Expansion policy

How often a scalp may extend beyond Primary and what fresh evidence is required.

### OQ-051 — Optional confluence

FVG/OB/Fib/Trendline/POC/M1/macro marginal value by ablation.

### OQ-052 — Research sample/confidence thresholds

Walk-forward/holdout sizes, minimum samples, shrinkage/confidence, Monte Carlo/bootstrap methodology.

### OQ-053 — Discovery/invention limits

Cluster/sample/similarity/complexity/resource thresholds.

### OQ-054 — Backup retention

Rolling checkpoint interval, hourly/daily/milestone retention, disk-space thresholds, optional encryption-at-rest.

## 5. EXTERNAL PROOF

### OQ-070 — Exness symbol facts

Verify real XAUUSDm digits/point/tick-size/tick-value/min/max/step/stops/freeze/filling/margin behaviour on intended account.

### OQ-071 — Broker schedule

Verify current normal daily/weekend session hours, DST handling and special-holiday behaviour.

### OQ-072 — Execution metadata

Verify AutoTrading/trade API/account/symbol permission surfaces and actual `order_check`/retcode semantics.

### OQ-073 — Spread/slippage/latency

Observe real DEMO distributions across sessions/news/reopen conditions.

### OQ-074 — Connected lifecycle

Natural governed OPEN/MODIFY/CLOSE, broker SL/TP, exact known manual close and restart/reconciliation.

### OQ-075 — Fresh-machine recovery

Prove local recovery package → new DB/path → fresh broker reconciliation/controller → READY without duplicate exposure.

### OQ-076 — Actual learning

Verify exact-close queue/receipt and exactly-once MAIN_DEMO observation from real broker history.

## 6. DEFERRED V1

- same-scope simultaneous cross-laptop PRIMARY/STANDBY;
- active-active or distributed DB/fencing;
- generic multi-broker abstraction;
- mandatory paid news/macro data;
- cloud hosting;
- self-deploying AI/generated code;
- ungoverned REAL trading;
- HFT claims/infrastructure;
- partial-profit requirement for 0.01 indivisible volume.

## 7. Closure discipline

Every closed question must update:

```text
this register
DESIGN_DECISIONS
owning topic contract
Architecture/Module/Coder/Testing docs if affected
operator/research/persistence consequences
relevant tests/evidence plan
```

Marking an item closed without affected-graph synchronization is not closure.
