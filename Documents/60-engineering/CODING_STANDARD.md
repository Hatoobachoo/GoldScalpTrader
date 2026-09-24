# GoldScalpTrader — Expert Coding Standard

**Status:** DRAFT PRE-CHALLENGE ENGINEERING STANDARD
**Version:** 0.1-scalp-engineering
**Authority:** Code quality, architecture boundaries, complexity, dependencies, typing, comments, performance, errors, persistence and tests.

## 1. Engineering objective

Write the smallest clear production-grade code that fully expresses the documented behaviour.

Expert code is auditable, bounded, typed where identity matters, explicit about failure and aligned with canonical `Documents/` contracts. Architectural size is not a quality metric.

## 2. Language and dependency policy

- Target a currently supported Python version compatible with MetaTrader5; exact minimum is verified before implementation freeze rather than guessed from the reference.
- Prefer standard library unless a dependency materially reduces complexity or provides required capability.
- Keep MetaTrader5 calls at broker adapter boundaries.
- Rich/wcwidth, if used, are presentation-only dependencies.
- Secondary graphical dashboard remains local/read-only.
- Research may use heavier numerical/statistical tools only inside research boundary.
- Dependency identity is part of release evidence.
- No cloud service is required for runtime correctness.

## 3. Functions, classes and modules

Prefer pure functions for deterministic calculations with explicit inputs/outputs.

Use classes when they own real state/resource/lifecycle, such as:

- MT5 connection;
- StateStore;
- controller lease;
- Intent lifecycle;
- recovery;
- Trade Manager;
- runtime loop.

Split by responsibility/authority, not arbitrary line count.

```text
facts in → normalized typed contract → deterministic result/state → evidence
```

No duplicate policy owners through convenience wrappers.

## 4. Typed domain boundaries

Use stable enums, frozen dataclasses and typed IDs where identity mistakes are costly.

Normalize raw MT5/JSON/env/CLI inputs once:

```text
presence/type
→ units/symbol/direction/UTC normalization
→ finite/domain validation
→ typed fact or explicit UNKNOWN/CORRUPT
```

Missing/corrupt required truth never becomes zero, false exposure or PASS.

## 5. Ownership direction

| Rule | Owner |
|---|---|
| raw MT5 read | market_data |
| descriptive evidence | intelligence |
| family hypotheses | strategies |
| fusion/Opportunity/timing/TradePlan | decisions |
| affordability/risk-day | risk |
| final permission/Intent/reconcile/controller | execution |
| raw irreversible broker write | execution/mt5_writer.py only |
| ManagedTrade lifecycle | management |
| durable state/checkpoint/local backup | persistence |
| runtime/provider/DTO | app |
| human presentation | operator |
| replay/learning/candidates | research/scripts |

Strategies cannot import raw MetaTrader5. Dashboards cannot recalculate permission. Research cannot call writer. Persistence cannot become broker truth.

## 6. Snapshot, concurrency and ordered authority

Build one verified immutable cycle snapshot and share it.

Dependency-independent intelligence/family jobs may use **bounded** concurrency only where semantics remain deterministic.

```text
bounded analysis
→ deterministic BUY/SELL fusion
→ Opportunity + timing
→ structural TradePlan
→ monetary Risk
→ hard authorities
→ Gate
→ durable Intent
→ sole writer
→ reconciliation
```

A one-worker fallback must produce the same result ordering/semantics.

Workers cannot mutate lifecycle, size money, acquire controller authority or write to broker.

## 7. Chronology and determinism

- UTC internally; PKT only for operator display.
- Completed-candle authority for structural facts.
- Preserve pivot/event geometry time versus knowledge/confirmation time.
- No future-confirmed fact in live/replay decisions.
- M1 role follows the final challenged contract; no hidden timeframe authority.
- Explicit deterministic sorting/tie-breaking for tickets/events/candidates/family reports.
- Same facts/policy/clock → same deterministic analytical result.

## 8. Safety-sensitive implementation

For every durable or broker action define:

- identity/scope;
- legal previous states;
- transition/event;
- transaction boundary;
- restart/retry semantics;
- broker contradiction handling;
- idempotency/fencing identity;
- operator evidence.

One Intent ID sends at most once. Ambiguous acknowledgement becomes reconciliation. Controller expiry blocks writes. Original R is immutable. Unknown exposure/P&L is not zero.

## 9. Scalping-sensitive implementation

Scalp correctness additionally requires explicit treatment of:

- quote age;
- event/trigger age;
- signal-to-submit drift;
- spread and transaction-cost diagnostics;
- analysis/order-check/order-send/reconciliation timings;
- min-lot affordability;
- trade-duration/time-efficiency state.

Do not create fake HFT guarantees. If a trigger is stale, rebuild/wait/block according to policy rather than sending late.

## 10. Error taxonomy

| Situation | Treatment |
|---|---|
| invalid caller input | boundary validation failure |
| unavailable required truth | UNKNOWN/UNAVAILABLE; fail closed where required |
| corrupt state/data | integrity/fault result with context |
| normal policy rejection | stable reason, not exception-driven flow |
| ambiguous broker result | durable unresolved Intent + reconciliation |
| programming invariant | fail loudly while preserving durable state |
| shutdown/cancellation | stop at safe boundary + report local backup result |

Catch exceptions only when adding useful context or converting to safe typed result.

Secondary presentation may isolate its own failure because it has no trading authority.

## 11. Configuration and thresholds

Every threshold has one owner:

- frozen topic policy;
- calibrated versioned research/config value;
- validated operational setting;
- local technical invariant with documented rationale.

No dashboard toggle, AI candidate or convenience path overrides hard safety.

Pre-challenge values are never silently treated as production constants.

## 12. Persistence and idempotency

SQLite/checkpoints/JSON are external boundaries. Validate schema/types/finite values, preserve explicit null and reject malformed required fields.

Portable restore is context only, not broker permission.

Fresh broker reconciliation/controller authority is required after restore.

Trading runtime performs **no automatic Git commit/push**.

## 13. Comments/docstrings

Comments explain why, especially for:

- chronology;
- one-shot write;
- fencing;
- immutable R;
- small-account/min-lot handling;
- scheduler cadence;
- strict recovery;
- actual vs counterfactual evidence;
- local backup safety;
- cost/freshness rules.

Core/public APIs have concise purpose/failure docstrings.

## 14. Logging and secrets

Use structured concise redacted logs.

Never log/commit:

- broker credentials;
- passwords;
- PATs/tokens;
- private keys;
- authority-bearing URLs.

Secret scanning is defense-in-depth, not permission to store secrets.

## 15. Presentation contract

Presentation is read-only.

```text
DashboardData
→ truthful normalization
→ width dispatcher
→ terminal renderer
→ optional atomic graphical snapshot
```

Nominal one-second pulse may refresh quote/clock/spread/countdown but not trading authority.

## 16. Tests and fakes

Safety-sensitive changes normally need:

- positive;
- negative/BLOCK;
- UNKNOWN/stale/corrupt;
- chronology;
- restart/persistence;
- duplicate/idempotency;
- cost/freshness boundary cases.

Fakes model real production failure modes. Never bypass gates simply to make tests easy.

## 17. Required verification — intended

After packaging/tooling is implemented, verification should include equivalent checks to:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

Do not claim any command PASS before it is actually run on the exact revision/environment.

## 18. Prohibited shortcuts

No:

- silent hard-safety fallback;
- score bypass;
- raw MetaTrader5 import in strategies;
- raw broker write outside sole writer;
- blind retry;
- secret in source/logs/backups;
- lookahead;
- arbitrary generated production code;
- martingale/uncontrolled grid/averaging rescue;
- dashboard authority;
- duplicate policy ownership;
- implicit state reset;
- undocumented dependency;
- runtime Git commit/push.

## 19. Research/runtime separation

Research may replay, measure, learn and propose. It cannot write broker, self-promote, turn counterfactual R into actual P/L or load arbitrary generated code into production.

Production consumes compact versioned validated policy artifacts only.

## 20. Change discipline

A coherent change packet identifies:

- authoritative contract;
- source owner;
- focused tests;
- persistence/recovery effect;
- operator effect;
- research effect;
- release/external evidence.

Update `MODULE_STRUCTURE.md`, `FILE_AND_TEST_CATALOG.md` and affected docs together when ownership changes.

## 21. Expert review questions

Reviewer must be able to answer:

- which functions are pure;
- who owns lifecycle;
- what is shared versus freshly reread;
- what is workload bound;
- what happens on UNKNOWN/ambiguity;
- what identity prevents duplicate action;
- what survives restart;
- what operator sees;
- what research may claim;
- what requires connected proof.

## 22. Scope rule

V1 is not a microservice platform, generic multi-broker framework, dependency-heavy live ML stack or design-pattern showcase.

Material expansion/relaxation requires Design Decision + affected-doc sync + proof.
