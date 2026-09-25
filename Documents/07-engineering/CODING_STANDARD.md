# GoldScalpTrader — Expert Coding Standard

**Status:** FINAL ENGINEERING STANDARD — IMPLEMENTATION PENDING
**Version:** 2.0-institutional-scalp
**Authority:** Code quality, architecture boundaries, comments/docstrings, typing, deterministic concurrency, error handling, persistence, performance, testing and security.

## 1. Engineering objective

Write production-grade code that completely expresses the canonical feature set while remaining understandable to a new expert developer/AI.

Quality priorities:

```text
correct authority boundaries
→ causal/deterministic behaviour
→ explicit failure semantics
→ recoverability
→ measured performance
→ maintainability
```

Shorter code is not better if it hides policy or removes a preserved feature.

## 2. Documentation-first rule

Before implementing a behaviour, identify its canonical owner and current status.

If code and Documents disagree:

- frozen/current contract wins unless a newer approved change exists;
- repair the full affected documentation graph before intentionally changing behaviour;
- never silently “fix” policy inside source only.

## 3. Module documentation

Every material module should explain:

- purpose;
- authority owned;
- authority explicitly not owned;
- key inputs/outputs;
- chronology/freshness expectations;
- state/concurrency model;
- failure/UNKNOWN behavior;
- persistence/broker implications.

## 4. Function/class documentation

Document non-trivial interfaces with:

- input types/units/timezone;
- return-state semantics;
- side effects;
- idempotency;
- exceptions versus normal policy rejection;
- thread/concurrency guarantees;
- broker/persistence consequences;
- critical invariants.

## 5. Inline comments

Comments explain **why**, especially:

- no-lookahead/knowledge-time logic;
- event lineage/correlation control;
- why a family setup is or is not valid;
- why M1 cannot create the thesis;
- one-shot Intent semantics;
- controller fencing;
- recovery ordering;
- structural-stop preservation;
- cost double-count prevention;
- broker quirks;
- measured optimization decisions.

Avoid noise such as `# increment x` above `x += 1`.

## 6. Types / domain boundaries

Prefer:

- `dataclass(frozen=True)` or equivalent immutable DTOs for analytical facts;
- enums for finite states;
- typed IDs for Opportunity/Episode/Plan/Intent/Trade/Candidate;
- explicit `Decimal`/float policy where precision matters;
- timezone-aware UTC datetimes internally;
- stable reason codes.

Normalize raw MT5/env/file inputs once:

```text
presence/type
→ units/scope/time normalization
→ finite/domain validation
→ typed fact or explicit UNAVAILABLE/CORRUPT
```

Missing required truth never becomes zero, `False`, empty exposure or PASS.

## 7. Strategy coding rule — market first

Never implement:

```text
active family
→ force chart into that family
```

Implement:

```text
IntelligenceSnapshot
→ family setup detectors
→ qualified SetupCandidate(s) or NONE
→ Strategy Isolation eligibility
```

The active family may proceed only if its own setup qualifies. Shadow candidates remain research-only.

Family evidence must distinguish required/supportive/opposing/not-relevant/unknown.

## 8. Timeframe / chronology

```text
H4 optional
H1 soft broad context
M15 location/path
M5 production setup/thesis
M1 subordinate timing after M5 Opportunity
quote current executable truth
```

Rules:

- forming bars never leak into confirmed history;
- pivot time and confirmation/knowledge time stay distinct;
- M1 cannot create production Opportunity alone;
- replay uses identical causal availability rules;
- deterministic sort/tie-breaking required.

## 9. Shared calculations / performance

Optimize in this order:

```text
remove duplicate work
→ vectorize/cache immutable calculations
→ serial deterministic baseline
→ profile
→ bounded concurrency where measured critical-path improvement exists
```

Concurrency rules:

- immutable inputs;
- bounded workers/resources;
- deterministic output order;
- no broker/lifecycle mutation in workers;
- visible failure/degradation;
- semantic parity with one-worker mode.

Never parallelize money/broker authority.

## 10. Decision / TradePlan / quality separation

Do not collapse:

```text
setup qualification
Opportunity
M1 timing
TradePlan
Executable Quality
Risk
Gate
```

Each owner must produce reason-rich typed output.

TradePlan structural SL/objectives are not modified to improve monetary affordability or cost ratios.

Executable Quality owns:

- emergency spread;
- spread/SL;
- spread/target;
- recent spread baseline;
- cost/reward;
- slippage allowance;
- drift/chase;
- latency revalidation.

## 11. Preserved Risk implementation

Implement the exact canonical SMALL/MEDIUM/NORMAL profile model and current documented bands.

Implement disabled-by-default aggressive-small-account capability with documented 8%/16% ceilings.

Never:

- auto-enable aggressive mode from balance;
- choose higher monetary risk because score/confidence is high;
- tighten structural SL to fit minimum volume;
- reset risk-day/cooldown/re-entry state on process restart.

## 12. News / session coding

News/Fundamental is soft context only.

Provider/cache code may report freshness/health, but it must not directly create News-only trading permission/cooldown/warmup.

Broker session state remains separate hard authority.

Do not infer broker OPEN from News availability or vice versa.

## 13. Broker-write safety

Every irreversible action defines:

- exact identity/scope;
- legal previous states;
- persistence boundary;
- fresh broker checks;
- one send allowance;
- acknowledgement classification;
- reconciliation;
- restart semantics.

One Intent sends at most once.

```text
SUBMITTING / ACCEPTED_UNKNOWN
→ reconcile
→ never blind resend
```

Only `execution/mt5_writer.py` may own raw irreversible MT5 calls.

## 14. Controller / ownership

Before every irreversible action verify current controller holder/epoch/lease.

Unknown/manual/foreign exposure is never adopted.

Same-account active-active distributed execution is not implemented in the current architecture.

## 15. Persistence / recovery

StateStore parsers reject malformed required data rather than coercing.

Portable restore:

```text
restore context
→ fresh MT5 facts
→ reconcile
→ acquire controller
→ hard authorities
→ READY
```

Trading runtime performs no Git operation.

## 16. Learning / AI coding boundary

Research code may:

- create/tune candidates;
- train ML candidates;
- run evidence stages;
- generate recommendations.

It may not:

- import/call raw MT5 writer;
- mutate production policy silently;
- change preserved Risk/safety;
- self-approve production promotion.

Candidate progression stops at `APPROVAL_REQUIRED`.

## 17. Dashboard coding standard

Dashboard architecture:

```text
atomic read-only DashboardData
→ terminal renderer / graphical snapshot
→ UI interactions that only alter presentation/chart state
```

Functional chart buttons must not be fake decorations.

M1/M5/M15/H1/H4 controls change displayed timeframe/data view. Indicators/Drawings/Settings affect UI/chart state according to approved boundaries.

No scrollbar in the primary desktop layout. Responsive fallback must preserve all critical information without changing authority.

## 18. Error taxonomy

| Situation | Treatment |
|---|---|
| invalid external/caller input | validation error |
| unavailable required truth | typed UNKNOWN/UNAVAILABLE; fail closed where owner requires |
| corrupt state/data | integrity/fault state |
| normal strategy/Risk rejection | stable reason, not exception flow |
| ambiguous broker result | durable unresolved Intent + reconcile |
| programming invariant violation | fail loudly after preserving durable state/diagnostics |
| optional context unavailable | reduced coverage/degraded context, not fabricated zero |
| shutdown/cancellation | stop at safe boundary and preserve lifecycle state |

Catch exceptions only to add context or convert to an explicitly safe typed result.

## 19. Configuration / thresholds

Every threshold must have one owner and status:

```text
preserved production default
approved calibrated value
operational setting
external broker fact
research candidate value
```

No magic numbers duplicated across modules.

## 20. Logging / secrets

Use structured, concise, redacted logs.

Never log/commit:

- broker password;
- GitHub token;
- API secret;
- private/recovery key;
- credential-bearing URL;
- `.env` content.

Reason codes and IDs should support debugging without revealing secrets.

## 21. Dependency policy

Prefer standard library and narrow dependencies. External packages must materially improve required capability.

Runtime correctness must not depend on:

- GitHub Actions;
- Codespaces;
- paid cloud compute;
- mandatory paid News API;
- distributed DB/consensus.

Research may use heavier local numerical/ML libraries if isolated from the trading-runtime authority path.

## 22. Testing expectations

Safety-sensitive features normally require:

- positive path;
- negative/policy rejection;
- UNKNOWN/unavailable;
- corrupt/stale input;
- chronology/no-lookahead;
- restart/persistence;
- duplicate/idempotency;
- boundary/units;
- integration proof;
- external/DEMO proof classification where mocks cannot suffice.

## 23. Intended verification commands

After tooling exists:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

Never claim PASS before executing the exact revision/environment.

## 24. Prohibited shortcuts

No:

- forced strategy fit;
- filter soup/global unanimity;
- M1-only hidden production trigger;
- lookahead;
- blind retry;
- hidden raw writer;
- safety UNKNOWN→PASS;
- score→higher Risk;
- stop distortion;
- martingale/grid/averaging down;
- dashboard authority;
- runtime Git publication;
- self-promoting candidate/ML policy;
- convenience-based deletion of preserved reference features.
