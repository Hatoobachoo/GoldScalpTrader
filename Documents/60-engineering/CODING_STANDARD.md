# GoldScalpTrader — Expert Coding Standard

**Status:** FROZEN V1 ENGINEERING STANDARD — IMPLEMENTATION EVIDENCE PENDING
**Version:** 1.0-preservation-first-scalp-engineering
**Authority:** Code quality, architecture boundaries, preservation discipline, bounded concurrency, dependencies, typing, errors, persistence and tests.

## 1. Engineering objective

Write the smallest clear production-grade code that **fully expresses the documented feature set**.

“Smaller” does not justify removing a preserved GoldSwingTraderAI feature/default. Implementation follows current canonical Documents.

Expert code is auditable, bounded, typed where identity matters, explicit about failure and aligned with authority boundaries.

## 2. Preservation-first implementation rule

Before changing inherited behavior:

```text
direct scalp requirement?
OR explicit operator instruction?
OR proven reference defect?
```

If no, preserve it. If uncertain, preserve behavior and surface a documentation question rather than simplify code silently.

## 3. Language / dependency policy

- target a currently supported Python version compatible with MetaTrader5, verified before implementation;
- prefer standard library unless dependency materially reduces complexity/provides required capability;
- MetaTrader5 calls stay at read/writer adapters;
- Rich/wcwidth presentation-only where used;
- secondary graphical dashboard local/read-only;
- research may use heavier numerical tools only in research boundary;
- dependency identity is release evidence;
- no cloud service is required for runtime correctness.

## 4. Functions/classes/modules

Prefer pure functions for deterministic calculations. Use classes when they own real resource/state/lifecycle such as MT5 connection, StateStore, controller, Intent, recovery, Trade Manager or runtime loop.

Split by responsibility/authority, not arbitrary line count.

```text
facts in → normalized typed contract → deterministic result/state → evidence
```

No duplicate policy owners.

## 5. Typed domain boundaries

Use stable enums, frozen dataclasses and typed IDs where identity mistakes are costly.

Normalize raw MT5/JSON/env/CLI inputs once:

```text
presence/type
→ units/symbol/direction/UTC normalization
→ finite/domain validation
→ typed fact or explicit UNKNOWN/CORRUPT
```

Missing/corrupt required truth never becomes zero, false exposure or PASS.

## 6. Ownership direction

| Rule | Owner |
|---|---|
| raw MT5 read | market_data |
| descriptive evidence | intelligence |
| family hypotheses / analytical scheduler | strategies |
| fusion/Opportunity/timing/TradePlan | decisions |
| profile/overlay affordability/risk-day | risk |
| final permission/Intent/reconcile/controller | execution |
| raw irreversible broker write | execution/mt5_writer.py only |
| ManagedTrade lifecycle | management |
| durable state/checkpoint/local backup | persistence |
| runtime/provider/DTO | app |
| human presentation | operator |
| replay/learning/candidates | research/scripts |

Strategies cannot import raw MetaTrader5 writer. Dashboards cannot recalculate permission. Research cannot call writer. Persistence cannot become broker truth.

## 7. Snapshot, bounded concurrency and ordered authority

Build one verified immutable cycle snapshot and share it.

Dependency-independent intelligence/family work **preserves bounded physical concurrency as a target capability**:

- immutable inputs;
- bounded workers/resources;
- dependency-respecting stages;
- deterministic canonical result ordering;
- visible worker failure;
- zero lifecycle/Risk/Gate/broker side effects;
- mandatory one-worker fallback with semantic parity.

Worker count may be tuned after profiling; concurrency itself is not silently removed.

Financial/broker spine stays serial:

```text
TradePlan
→ SMALL/MEDIUM/NORMAL Risk + optional explicit aggressive overlay
→ hard authorities
→ Gate
→ durable Intent
→ fresh broker checks
→ sole writer
→ reconciliation
```

## 8. Chronology / determinism

- UTC internally; PKT only display;
- completed-candle structural authority;
- preserve geometry time vs knowledge/confirmation time;
- no future-confirmed fact in live/replay decisions;
- current M1 role is diagnostic/research only;
- deterministic sorting/tie-breaking for tickets/events/candidates/family reports;
- same facts/policy/clock → same analytical semantics.

## 9. Preserved Risk implementation

Do not implement one generic `STANDARD` policy in place of canonical profiles.

Implement fixed UTC-day DayStartEquity profile:

```text
SMALL   < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

with canonical target/elevated/hard/daily bands.

Implement `AGGRESSIVE_SMALL_ACCOUNT` as explicit operational capability **disabled by default**:

```text
8% max monetary SL-risk ceiling — NOT target
16% aggregate open-risk cap
16% daily-loss ceiling
```

Never auto-enable from equity. Manual reset remains disabled by default. Preserve one fresh same-episode re-entry and three-loss / at-least-30-minute cooldown baseline unless a later governed scalp-specific change supersedes it.

The provisional 0.50% scaffold is not canonical policy.

## 10. Safety-sensitive implementation

For every durable/broker action define identity/scope, legal previous states, transition/event, transaction boundary, restart/retry semantics, broker contradiction handling, idempotency/fencing identity and operator evidence.

One Intent sends at most once. Ambiguous acknowledgement reconciles. Controller expiry fences writes. Original R immutable. Unknown exposure/P&L never zero.

## 11. Scalping-sensitive implementation

Explicitly handle quote age, event/trigger age, signal-to-submit drift, spread/cost diagnostics, analysis/check/send/reconcile timings, min-lot affordability and trade-duration/time-efficiency state.

No fake HFT guarantees. Stale trigger rebuilds/waits/blocks instead of late send.

## 12. Session / News implementation baseline

Current canonical baselines include:

```text
Provider TTL 1800s
Daily PRE_CLOSE T-20 / T-10
Weekend PRE_CLOSE T-60 / T-30
Daily reopen 1 clean M5
Weekend reopen 2 clean M5 + gap assessment
```

Current broker schedule remains external fact. News refresh failure may use valid LKG cache without timestamp laundering; expired/invalid/no cache → News UNKNOWN → new-entry block/limited.

## 13. Error taxonomy

| Situation | Treatment |
|---|---|
| invalid caller input | boundary validation failure |
| unavailable required truth | UNKNOWN/UNAVAILABLE; fail closed where required |
| corrupt state/data | integrity/fault result |
| normal policy rejection | stable reason, not exception flow |
| ambiguous broker result | durable unresolved Intent + reconcile |
| programming invariant | fail loudly while preserving durable state |
| shutdown/cancellation | stop at safe boundary + report local backup result |

Catch exceptions only to add useful context or convert to safe typed result.

## 14. Configuration / thresholds

Every threshold has one owner: frozen topic policy, calibrated versioned scalp value, validated operational setting or documented local invariant.

Do not relabel preserved reference defaults as “pre-challenge” or “tunable” merely because implementation has not started.

No dashboard/AI/convenience path overrides hard safety.

## 15. Persistence / idempotency

Validate SQLite/checkpoint/JSON schema/types/finite values, preserve explicit null and reject malformed required fields.

Portable restore is context only; fresh broker reconciliation/controller authority follows restore.

Trading runtime performs **no automatic Git commit/push/pull**.

## 16. Comments / logs / secrets

Comments explain chronology, one-shot write, fencing, immutable R, min-lot handling, scheduler, recovery, evidence attribution, local backup and cost/freshness rules.

Use concise structured redacted logs. Never log/commit broker credentials, passwords, PATs/tokens, private keys or authority-bearing URLs.

## 17. Presentation contract

Presentation is read-only:

```text
DashboardData
→ truthful normalization
→ terminal renderer
→ optional atomic graphical snapshot
```

Fast display pulse may refresh quote/clock/spread/countdown without rerunning trading authority.

## 18. Tests/fakes

Safety-sensitive work normally tests positive, negative/BLOCK, UNKNOWN/stale/corrupt, chronology, restart/persistence, duplicate/idempotency and cost/freshness boundaries.

Also prove bounded-parallel ↔ one-worker parity and preserved Risk/profile/aggressive/reset/cooldown/session defaults.

Fakes model real failure modes; never bypass gates to make tests easy.

## 19. Intended verification

After packaging/tooling exists:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

Never claim PASS before running exact revision/environment.

## 20. Runtime capability stages

```text
READINESS
DRY_RUN
controlled DEMO PRIMARY
future governed REAL
```

Future REAL capability is preserved but cannot be enabled without its separate DEMO/release/explicit-approval gate.

## 21. Prohibited shortcuts

No silent safety fallback, score bypass, raw writer outside sole boundary, blind retry, secret leakage, lookahead, arbitrary generated production code, martingale/grid/averaging rescue, dashboard authority, duplicate policy ownership, implicit reset, undocumented dependency, runtime Git operation, equity-auto-enabling aggressive mode or convenience-based deletion of preserved feature.

## 22. Change discipline / scope

Each coherent change identifies authoritative contract, preservation/delta classification, source owner, focused tests, persistence/operator/research effects and release/external evidence.

Update Module Structure, File/Test Catalog and affected Documents together.

V1 is not a microservice platform or generic multi-broker framework, but that simplicity rule cannot be used to remove the preserved feature set.