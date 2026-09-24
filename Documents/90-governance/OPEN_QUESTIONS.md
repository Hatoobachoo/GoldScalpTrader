# GoldScalpTrader — Open Questions and Closure Plan

**Status:** POST-AUDIT-1 QUESTION REGISTER — ARCHITECTURE CLOSED, CALIBRATION/IMPLEMENTATION/EXTERNAL PROOF REMAIN
**Version:** 1.1-cache-aware-news
**Authority:** Unresolved implementation choices, numerical calibration, external proof and deliberate V1 deferrals.

## 1. Classification

```text
CLOSED ARCHITECTURE
IMPLEMENTATION CHOICE
CALIBRATE IN RESEARCH
EXTERNAL PROOF
DEFERRED V1
```

A closed architecture question may still have calibratable numbers. Coding may not guess unresolved implementation/calibration/external items.

## 2. CLOSED ARCHITECTURE — Audit 1 + post-audit sync

### OQ-001 — Final timeframe authority — CLOSED

```text
H1   broad soft regime / major directional-volatility context
M15  opportunity location/path/session/liquidity context
M5   primary completed-bar setup, entry timing and normal management structure
H4   optional major context only
M1   diagnostic/research only in V1
quote current executable Bid/Ask/spread/drift/health only
```

Promoting M1/tick-history authority later requires a governed design change.

### OQ-002 — Strategy-family decomposition — CLOSED

Retain six independent families. Manage overlap with explicit correlation/event-lineage bounding rather than merging distinct hypotheses prematurely.

### OQ-003 — `OPEN + News UNKNOWN` policy — CLOSED

News UNKNOWN blocks **new entries** in V1. It does not rename itself CLEAR and does not automatically prevent safe management/protection/mandatory CLOSE of an existing bot trade.

### OQ-004 — Structural R / cost-room architecture — CLOSED

TradePlan preserves gross structural quality plus explicit cost-adjusted executable-room diagnostics. Exact numerical floors remain calibration.

### OQ-005 — Risk-policy shape — CLOSED

V1 uses one explicit `STANDARD` production risk policy rather than automatic SMALL/MEDIUM/NORMAL equity tiers. Any future aggressive small-account experiment is explicit/research-governed, disabled by default and never auto-selected. Historical 8%/16% values are not active V1 policy.

### OQ-006 — Runtime mode scope — CLOSED

```text
READINESS / DRY_RUN
→ controlled governed DEMO writer after deterministic implementation proof
REAL → DEFERRED V1, separate future governance decision
```

### OQ-007 — Trade Manager time action — CLOSED

No separate `TIME_EXIT` lifecycle action in V1. Time/efficiency is a first-class reason that may produce normal `EXIT` once calibrated.

### OQ-008 — Physical analytical concurrency — CLOSED

Logical independence is architectural. Physical worker concurrency is optional/profiling-driven. One-worker execution is canonical semantic fallback and must be parity-equivalent.

### OQ-009 — Development/source backup — CLOSED

```text
major remote bulk commit
→ operator git pull --ff-only
→ local clone becomes complete source + Git-history backup
→ optional secret-clean ZIP source snapshot after milestone
```

No runtime Git operation. Git bundle is optional advanced/manual tooling only.

### OQ-010 — News API/provider outage and cache semantics — CLOSED

A temporary provider/API refresh failure does **not** automatically make News UNKNOWN if a previously accepted last-known-good calendar still passes its original scope/schema/coverage/TTL/integrity checks.

Rules:

```text
refresh fails + valid LKG cache
→ keep cached accepted event truth
→ provider may be DEGRADED
→ no TTL/timestamp rewriting

refresh fails + no valid current cache
→ NEWS_SAFETY_UNKNOWN
→ V1 new-entry BLOCK / LIMITED
```

## 3. IMPLEMENTATION CHOICES

### OQ-020 — Python/package layout

Verify current MetaTrader5/Python compatibility, choose supported Python version and replace provisional launch/import layout with a simple installable package.

### OQ-021 — SQLite detail

Choose WAL/synchronous/checksum/schema/migration implementation while preserving transactional/crash-safe semantics.

### OQ-022 — Analytical scheduler implementation

Choose serial default vs bounded worker pool after profiling. Deterministic one-worker parity is mandatory either way.

### OQ-023 — Dashboard stack

Confirm Rich/wcwidth dependency and implementation timing of optional browser dashboard.

### OQ-024 — Secret scanner / Documents verifier

Choose smallest dependable local scripts/tests; no cloud/Actions requirement.

### OQ-025 — Local runtime backup implementation

Choose SQLite backup API/export method, manifest/checksum format, catalog naming, free-space handling and optional second-drive copy.

### OQ-026 — Local source ZIP helper

Decide whether to provide a repository script/PowerShell helper. Default archive excludes `.env`, credentials, virtualenvs, logs, runtime DB/checkpoints and nested backup folders. Including `.git` is not required because the pulled local clone already preserves history.

### OQ-027 — News last-known-good cache implementation

Choose smallest local cache format/path, atomic replacement method, integrity marker and restart loading path. Implementation must preserve original fetch/as-of/coverage/valid-until values and never extend validity on refresh failure.

## 4. CALIBRATE IN RESEARCH

### OQ-040 — Event freshness

Family/event-specific M5 age, distance-travelled and extension thresholds.

### OQ-041 — Entry/chase policy

Maximum acceptable drift from approved entry, trigger age and processing delay.

### OQ-042 — Spread / execution friction

Healthy baseline method, spread-to-stop/target thresholds, slippage reserve and broker deviation policy.

### OQ-043 — Structural target quality

Minimum gross R, cost-adjusted room/Net-R equivalent and objective hierarchy thresholds.

### OQ-044 — STANDARD risk values

Preferred per-trade risk target, hard per-trade ceiling and daily-loss limit. Current 0.50% scaffold is provisional.

### OQ-045 — Cooldown / same-episode re-entry

Loss-streak threshold, cooldown time/conditions and maximum genuinely fresh re-entry count.

### OQ-046 — Session specialization

Whether Asia/London/NY/overlap conditioning improves out-of-sample net expectancy after costs.

### OQ-047 — News blackout/warmup

Event tiers, pre/post windows and post-news clean-bar/spread-normalization requirements.

### OQ-048 — Reopen/pre-close timing

Exact no-entry/flatten cutoffs and clean completed-M5 reopen requirement.

### OQ-049 — Trade Manager time efficiency

Normal hold-duration distribution, soft/hard time-efficiency EXIT conditions and protection timing.

### OQ-050 — Runner/Expansion policy

How often a scalp may extend beyond Primary and what fresh evidence is required.

### OQ-051 — Optional confluence

FVG/OB/Fib/Trendline/POC/M1/macro marginal value by ablation.

### OQ-052 — Research sample/confidence thresholds

Walk-forward/holdout sizes, minimum samples, shrinkage/confidence and Monte Carlo/bootstrap methodology.

### OQ-053 — Discovery/invention limits

Cluster/sample/similarity/complexity/resource thresholds.

### OQ-054 — Runtime-backup retention

Rolling checkpoint interval, hourly/daily/milestone retention, disk-space thresholds and optional encryption-at-rest.

### OQ-055 — Aggressive risk experiment

Whether an explicit disabled-by-default aggressive small-account research profile should exist at all; historical 8%/16% remains legacy context only.

### OQ-056 — News cache TTL / refresh cadence

Calibrate the bounded validity TTL, proactive refresh interval, retry/backoff behaviour and current-coverage rule. Swing's 1800-second provider TTL is reference evidence only, not automatically frozen for scalping.

## 5. EXTERNAL PROOF

### OQ-070 — Exness symbol facts
Verify intended account XAUUSDm digits/point/tick size/tick value/min/max/step/stops/freeze/filling/margin behaviour.

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

### OQ-077 — News provider/cache behaviour
Verify chosen zero-cost provider failure modes, cache survival across temporary outage, expiry handling, current-week/coverage validation and realistic refresh behaviour on the intended Windows runtime.

## 6. DEFERRED V1

- REAL trading;
- M1/tick-history production decision authority;
- same-scope simultaneous cross-laptop PRIMARY/STANDBY;
- active-active/distributed DB/fencing;
- generic multi-broker abstraction;
- mandatory paid news/macro data;
- cloud hosting;
- self-deploying generated code;
- HFT claims/infrastructure;
- mandatory partial-profit logic for indivisible 0.01 volume.

## 7. Closure discipline

Every remaining question closed later must update:

```text
this register
DESIGN_DECISIONS
owning topic contract
Architecture/Module/Coder/Testing docs if affected
operator/research/persistence consequences
relevant tests/evidence plan
```

Marking an item closed without affected-graph synchronization is not closure.