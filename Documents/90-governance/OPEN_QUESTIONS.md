# GoldScalpTrader — Open Questions and Closure Plan

**Status:** POST-AUDIT-1 QUESTION REGISTER — PRESERVATION-FIRST CORRECTION APPLIED
**Version:** 1.2-preserved-reference-defaults
**Authority:** Unresolved implementation choices, genuinely scalp-specific calibration, external proof and future governed capabilities.

## 1. Classification

```text
CLOSED ARCHITECTURE
PRESERVED REFERENCE DEFAULT
IMPLEMENTATION CHOICE
SCALP CALIBRATION
EXTERNAL PROOF
FUTURE GOVERNED CAPABILITY
```

Rule: a reference feature/default is not made open merely because a simpler architecture exists. If no direct scalp reason or explicit operator instruction justifies a change, preserve it.

## 2. CLOSED ARCHITECTURE

### OQ-001 — Final timeframe authority — CLOSED

```text
H1   broad soft regime / major directional-volatility context
M15  opportunity location/path/session/liquidity context
M5   primary completed-bar setup, entry timing and normal management structure
H4   optional major context only
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health only
```

### OQ-002 — Strategy-family decomposition — CLOSED

Retain six independent reference families. Manage overlap with explicit event-lineage/correlation bounding.

### OQ-003 — `OPEN + News UNKNOWN` policy — CLOSED

True `NEWS_SAFETY_UNKNOWN` blocks new entries. Existing-position management/protection/mandatory CLOSE remains action-sensitive.

Temporary provider/API failure with a still-valid accepted last-known-good cache is not automatically UNKNOWN.

### OQ-004 — Structural R / cost-room architecture — CLOSED

TradePlan preserves gross structural quality plus explicit cost-adjusted executable-room diagnostics. Swing 1.20R is not a hard inherited scalp floor. Exact scalp thresholds remain calibration.

### OQ-005 — Risk-policy shape — CLOSED / CORRECTED

Preserve automatic reference profiles:

```text
SMALL   positive DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

Preserve their reference target/elevated/hard-ceiling/daily-loss bands.

Also preserve operator-requested `AGGRESSIVE_SMALL_ACCOUNT` as an explicit operational option disabled by default:

```text
eligible baseline < $1,000
8% max monetary SL risk ceiling — NOT target
16% max aggregate open risk
16% daily loss ceiling
```

It is never silently auto-enabled merely because equity is small.

### OQ-006 — Runtime mode scope — CLOSED / CORRECTED

```text
READINESS / DRY_RUN
→ controlled governed DEMO writer after deterministic proof
→ future governed REAL capability remains preserved
```

REAL is disabled/unavailable until DEMO evidence, release gates and explicit operator approval satisfy a separate REAL policy. The feature is not removed.

### OQ-007 — Trade Manager time action — CLOSED

No separate `TIME_EXIT` action. Time/efficiency is a first-class reason that may produce normal `EXIT`.

### OQ-008 — Physical analytical concurrency — CLOSED / CORRECTED

Preserve bounded physical concurrency for dependency-independent analysis as a target reference feature. A deterministic one-worker fallback is mandatory and must be parity-equivalent.

### OQ-009 — Development/source backup — CLOSED

```text
major remote bulk commit
→ operator git pull --ff-only
→ local clone becomes source + Git-history backup
→ optional secret-clean ZIP milestone copy
```

No runtime Git operation.

### OQ-010 — News API/provider outage and cache semantics — CLOSED

```text
refresh fails + valid LKG cache
→ keep accepted cached event truth
→ provider may be DEGRADED
→ never rewrite fetch/as-of/valid-until

refresh fails + no valid cache
→ NEWS_SAFETY_UNKNOWN
→ new-entry BLOCK / LIMITED
```

## 3. PRESERVED REFERENCE DEFAULTS — NOT OPEN BY DEFAULT

### PRD-001 — Account risk bands

| Profile | Normal / target | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0%–4.5% | >4.5%–6.5% | 7% | 12% |
| MEDIUM | 2.0%–3.0% | >3.0%–4.5% | 5% | 9% |
| NORMAL | 1.0%–2.0% | >2.0%–3.5% | 4% | 7% |

A future change requires a specific scalp justification and documentation discussion.

### PRD-002 — Cooldown / same-episode re-entry

Preserve one genuinely fresh same-episode re-entry and the reference three-consecutive-loss / at-least-30-minute global cooldown plus freshness/health release requirements.

### PRD-003 — Manual daily-loss reset

Capability preserved but disabled by default. If explicitly enabled later, it remains bounded/auditable/persistent and cannot clear unrelated faults.

### PRD-004 — PRE_CLOSE / reopen

```text
Daily:   T-20 no new entry, T-10 mandatory flatten
Weekend: T-60 no new entry, T-30 mandatory flatten
Daily reopen:   1 clean completed M5
Weekend reopen: 2 clean completed M5 + gap assessment
```

These remain subject to current broker schedule proof; a proven broker schedule change is not a scalp-policy change.

### PRD-005 — Provider TTL

Use the reference 1800-second baseline unless a direct provider/scalp reason is later approved.

### PRD-006 — Bounded analytical concurrency

Target feature preserved. Implementation must also provide deterministic one-worker fallback/parity.

## 4. IMPLEMENTATION CHOICES

### OQ-020 — Python/package layout

Verify current MetaTrader5/Python compatibility, choose supported Python version and replace provisional launch/import layout with a simple installable package.

### OQ-021 — SQLite detail

Choose WAL/synchronous/checksum/schema/migration implementation while preserving transactional/crash-safe semantics.

### OQ-022 — Analytical scheduler implementation

Implement the preserved bounded analytical scheduler with immutable inputs, bounded workers, deterministic canonical output order and one-worker fallback/parity. Exact worker count is an implementation/performance choice, not permission to remove concurrency as a feature.

### OQ-023 — Dashboard stack

Confirm Rich/wcwidth dependency and implementation timing of optional browser dashboard.

### OQ-024 — Secret scanner / Documents verifier

Choose smallest dependable local scripts/tests; no cloud/Actions requirement.

### OQ-025 — Local runtime backup implementation

Choose SQLite backup API/export method, manifest/checksum format, catalog naming, free-space handling and optional second-drive copy.

### OQ-026 — Local source ZIP helper

Decide whether to provide a repository script/PowerShell helper. Default archive excludes `.env`, credentials, virtualenvs, logs, runtime DB/checkpoints and nested backup folders.

### OQ-027 — News LKG cache implementation

Use the preserved 1800-second baseline TTL initially; choose cache file/path, atomic replacement, integrity marker and restart loading. Original timestamps/coverage may never be extended on failure.

### OQ-028 — Aggressive small-account configuration surface

Choose explicit config name/confirmation/visibility for the preserved disabled-by-default 8%/16% overlay. It must never auto-enable from balance alone.

## 5. SCALP CALIBRATION

These remain open because they directly concern short-horizon scalp behaviour:

### OQ-040 — Event freshness
Family/event-specific M5 age, distance-travelled and extension thresholds.

### OQ-041 — Entry/chase policy
Maximum acceptable drift from approved entry, trigger age and processing delay.

### OQ-042 — Spread / execution friction
Healthy baseline method, spread-to-stop/target thresholds, slippage reserve and broker deviation policy.

### OQ-043 — Structural target quality
Minimum gross R, cost-adjusted room/Net-R equivalent and objective hierarchy thresholds. Swing 1.20R is not automatically the hard scalp floor.

### OQ-044 — Session specialization
Whether Asia/London/NY/overlap conditioning improves out-of-sample net expectancy after costs.

### OQ-045 — News blackout/post-event stabilization
Only changes specifically justified by scalp event sensitivity are open. The provider/session mechanisms themselves remain preserved.

### OQ-046 — Trade Manager time efficiency
Normal hold-duration distribution, time-efficiency EXIT conditions and protection timing.

### OQ-047 — Runner/Expansion policy
How often a scalp may extend beyond Primary and what fresh evidence is required.

### OQ-048 — Optional confluence
FVG/OB/Fib/Trendline/POC/M1/macro marginal value by ablation.

### OQ-049 — Research sample/confidence thresholds
Walk-forward/holdout sizes, minimum samples, shrinkage/confidence and Monte Carlo/bootstrap methodology.

### OQ-050 — Discovery/invention limits
Cluster/sample/similarity/complexity/resource thresholds.

## 6. EXTERNAL PROOF

### OQ-070 — Exness symbol facts
Verify intended XAUUSDm digits/point/tick size/tick value/min/max/step/stops/freeze/filling/margin behaviour.

### OQ-071 — Broker schedule
Verify current normal daily/weekend hours, DST handling and special-holiday behaviour. External broker fact may supersede an outdated reference schedule without being a strategy change.

### OQ-072 — Execution metadata
Verify AutoTrading/trade API/account/symbol permission surfaces and actual `order_check`/retcode semantics.

### OQ-073 — Spread/slippage/latency
Observe real DEMO distributions across sessions/news/reopen conditions.

### OQ-074 — Connected lifecycle
Natural governed OPEN/MODIFY/CLOSE, broker SL/TP, known manual close and restart/reconciliation.

### OQ-075 — Fresh-machine recovery
Prove recovery package → new DB/path → fresh broker reconciliation/controller → READY without duplicate exposure.

### OQ-076 — Actual learning
Verify exact-close queue/receipt and exactly-once approved-environment observation from real broker history.

### OQ-077 — News provider/cache behaviour
Verify zero-cost provider failure modes, LKG survival, 1800-second baseline TTL behaviour, expiry handling and coverage validation.

## 7. FUTURE GOVERNED CAPABILITIES

Preserved future capabilities are not silently deleted merely because initial implementation is narrower:

- REAL trading after DEMO/release/explicit approval;
- broker-valid partial management when volume is divisible;
- future M1/tick-history production authority only if separately justified;
- future same-scope distributed fencing only if a proper shared authority architecture is added;
- optional provider adapters without making paid services mandatory.

## 8. Closure discipline

Every later change must update:

```text
this register
DESIGN_DECISIONS
owning topic contract
Architecture/Module/Coder/Testing docs if affected
operator/research/persistence consequences
reference Comparison + Preservation Ledger
relevant tests/evidence plan
```

At final documentation review, remaining genuine scalp-specific differences are discussed explicitly with the operator before implementation begins.