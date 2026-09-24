# GoldScalpTrader — Documentation Content Coverage Matrix

**Status:** POST-AUDIT-1 FREEZE-PREPARATION COVERAGE MAP — STRUCTURAL + PRESERVATION COVERAGE VERIFIED
**Version:** 1.1-preservation-first-coverage
**Authority:** Proof that the canonical manual covers intended design, preserved reference features/defaults, scalp-specific deltas, implementation ownership, proof and operator surfaces.

## 1. Purpose

This is a loss-prevention/navigation map, not a substitute for semantic audit.

Every substantive subject must have a canonical destination, intended implementation owner and proof route. Inherited behaviour must also be classifiable as preserved, genuine scalp-specific, operator-directed or defect-corrected.

## 2. Core coverage matrix

| Subject | Canonical destination | Planned implementation | Main proof route |
|---|---|---|---|
| product purpose / preservation boundary | `00-foundation/PROJECT_VISION.md` | app/domain | system review |
| highest-level invariants | `00-foundation/SYSTEM_CONTRACT.md` | whole runtime | cross-module tests/audits |
| runtime topology | `00-foundation/ARCHITECTURE.md` | app/* | integration/architecture review |
| bounded-parallel trading floor | `TRADING_FLOOR_ARCHITECTURE.md` | intelligence/strategies | one-worker ↔ bounded-parallel parity |
| build dependency order | `BUILD_PHASES.md` | whole repo | phase exit gates |
| MT5 facts/history | `10-market-intelligence/MARKET_DATA_AND_HISTORY.md` | market_data | normalization + connected read |
| candle/structure | `CANDLE_STRUCTURE.md` | intelligence/candle_structure | chronology/no-lookahead |
| technical zones/room | `TECHNICAL_STRUCTURE_AND_LEVELS.md` | intelligence/technical | geometry/lifecycle tests |
| liquidity/SMC | `LIQUIDITY_AND_SMC.md` | intelligence/liquidity | causal liquidity tests |
| EMA/RSI/ATR/volatility | `INDICATORS_AND_VOLATILITY.md` | intelligence/indicators | chronological quant tests |
| soft sessions | `SESSION_CONTEXT.md` | intelligence/session | DST/range replay |
| news/macro intelligence | `FUNDAMENTAL_AND_NEWS.md` | intelligence/news | event/cache tests |
| provider/LKG cache / 1800s baseline | `FUNDAMENTAL_AND_NEWS.md`, `SESSION_NEWS_PROVIDER_CONTRACT.md` | app/session_news | TTL/scope/coverage/no-laundering |
| six strategy families | `20-trading-decisions/STRATEGY_FLOOR.md` | strategies | family tests/replay |
| BUY/SELL fusion | `SCORING_AND_DECISION_FUSION.md` | decisions/fusion | conflict/correlation tests |
| Opportunity/timing/freshness/re-arm | `ENTRY_TIMING.md` | decisions | lifecycle/freshness/re-entry tests |
| structural plan / cost-adjusted room | `TRADE_PLAN.md` | decisions/trade_plan | geometry/R/cost tests |
| breakout retest geometry | `BREAKOUT_RETEST_GEOMETRY.md` | family_trade_plan | event/fallback tests |
| reversal event geometry | `REVERSAL_EVENT_GEOMETRY.md` | family_trade_plan | event-extreme tests |
| open-trade management / optional partial | `TRADE_MANAGER_AND_EXIT.md` | management | manager/execution tests |
| monetary Risk profiles/bands | `30-risk-execution/RISK_CONTRACT.md` | risk | profile/lot/min-lot/margin tests |
| aggressive 8%/16% option | `RISK_CONTRACT.md` | risk/config | default-disabled/ceiling tests |
| manual reset / re-entry / cooldown | `RISK_CONTRACT.md` | risk/state | persistence/policy tests |
| manual/external activity / cash flow | `BROKER_ACTIVITY_AND_MANUAL_TRADES.md` | market_data/activity | activity/accounting tests |
| PRE_CLOSE/reopen + permission composition | `SESSION_AND_RISK_STATE_MACHINE.md` | risk/permissions | state-machine tests + connected schedule |
| persistence/restart/local recovery | `PERSISTENCE_RESTART_AND_RECOVERY.md` | persistence/app recovery | checkpoint/restore drills |
| no-runtime-Git + source pull/ZIP workflow | persistence/learning-backup/setup guides | persistence/scripts/operator | source/runtime separation review |
| broker-write safety + future REAL gate | `EXECUTION_AND_BROKER_SAFETY.md` | execution | one-shot/reconcile/DEMO/release |
| learning boundaries | `40-research-learning/LEARNING_AND_AI_BOUNDARIES.md` | research | learning/governance tests |
| chronological research | `RESEARCH_AND_VALIDATION.md` | research/replay | replay/holdout/stress |
| actual DEMO learning | `LIVE_DEMO_LEARNING_PIPELINE.md` | research/live_learning | exact-close exactly-once DEMO |
| learning backup/machines | `LEARNING_BACKUP_AND_MULTI_MACHINE.md` | persistence/research | recovery/handoff |
| promotion | `GOVERNED_EXPERIMENTS_AND_PROMOTION.md` | research/promotion | stage/evidence tests |
| discovery | `GOVERNED_STRATEGY_DISCOVERY.md` | research/discovery | candidate/preservation tests |
| invention | `AUTONOMOUS_STRATEGY_INVENTION.md` | research/invention | primitive/complexity tests |
| primary dashboard | `50-operator/DASHBOARD_AND_UX.md` | app/operator | read-only/profile/cache truth |
| live terminal extension | `LIVE_DASHBOARD_CONTRACT.md` | operator | width/pulse/Gate truth |
| graphical dashboard | `GRAPHICAL_DASHBOARD.md` | graphical_dashboard/operator | localhost/read-only isolation |
| module ownership | `60-engineering/MODULE_STRUCTURE.md` | whole repo | dependency review |
| file/test map | `FILE_AND_TEST_CATALOG.md` | whole repo | tree audit |
| coding quality | `CODING_STANDARD.md` | whole repo | lint/static/code review |
| testing/evidence ladder | `TESTING_AND_VERIFICATION.md` | tests/scripts | verification reports |
| diagnostics | `SYSTEM_HEALTH_AND_DIAGNOSTICS.md` | diagnostics/operator | state/reason tests |
| release gate | `RELEASE_CHECKLIST.md` | release process | exact checklist evidence |
| final release audit | `FINAL_RELEASE_AUDIT.md` | audit process | scoped sign-off |
| fresh-zero + preservation review | `AUDIT_1_FRESH_DESIGN_REVIEW.md` | governance | architecture verdicts |
| Documents→Code→Tests | `AUDIT_2_DOCUMENT_CODE_TEST_COMPLIANCE.md` | post-build audit | traceability matrix |
| Gate/presentation sync | `AUDIT_3_GATE_PRESENTATION_AND_DOCUMENT_SYNC.md` | operator/execution | focused audit |
| zero-trade geometry | `AUDIT_4_ZERO_TRADE_GEOMETRY_REVIEW.md` | decision/plan | connected corrective audit |
| deep zero-trade/freshness | `AUDIT_5_DEEP_ZERO_TRADE_GATE_AND_EVENT_FRESHNESS.md` | full entry chain | causal audit |
| live geometry/freshness | `AUDIT_6_LIVE_GEOMETRY_AND_ENTRY_FRESHNESS.md` | intelligence/decisions | corrective audit |
| component review | `AUDIT_7_INDIVIDUAL_COMPONENT_REVIEW.md` | all components | component traversal |
| design rationale | `90-governance/DESIGN_DECISIONS.md` | governance | decision audit |
| unresolved work / preserved defaults | `OPEN_QUESTIONS.md` | governance | closure records |
| documentation method | `DOCUMENTATION_STANDARD.md` | whole repo | documentation audit |
| preservation | `PRESERVATION_LEDGER.md` | governance | reference-preservation audit |
| explicit Swing→Scalp delta | `DOCUMENTATION_COMPARISON.md` | governance | reference-change audit |
| documentation audit | `DOCUMENTATION_AUDIT.md` | governance | reconstructability review |
| legacy topology | `LEGACY_DOCS_RETIREMENT.md` | governance | one-authority review |
| full subject coverage | this file | governance | semantic audit |
| developer navigation | `CODER_GUIDE.md` | whole repo | build handoff |
| build/recovery continuation | `PROJECT_BUILD_AND_RECOVERY_GUIDE.md` | whole repo | context recovery |
| installation/operation | `SETUP_AND_RUN_GUIDE.md` | operator | clean-machine setup |
| human use | `USER_MANUAL.md` | operator | connected operation review |
| whole-project AI handoff | `FINAL_BUILD_PROMPT.md` | development | reconstructability review |
| canonical vocabulary | `GLOSSARY.md` | whole repo | terminology review |

## 3. Genuine scalp-specific coverage

The manual explicitly covers:

- H1/M15/M5 scalp hierarchy with H4 optional and M1 diagnostic only;
- event/trigger freshness and anti-chase;
- gross + cost-adjusted target room;
- no automatic inherited 1.20R hard scalp floor;
- spread/slippage/drift/latency observability;
- News UNKNOWN new-entry block with valid-LKG-cache resilience;
- exceptional Runner;
- time/efficiency EXIT;
- cost/latency/duration/capture research.

## 4. Preserved reference-default coverage

The manual also explicitly preserves:

- SMALL/MEDIUM/NORMAL Risk profiles and canonical bands;
- disabled-by-default aggressive small-account operational option;
- 8% maximum SL-risk ceiling as ceiling, not target;
- 16% aggregate/daily aggressive ceilings;
- disabled-by-default manual daily-loss reset capability;
- one genuinely fresh same-episode re-entry;
- three-loss / at-least-30-minute cooldown + release conditions;
- bounded physical analytical concurrency + deterministic one-worker parity;
- provider TTL baseline 1800 seconds;
- Daily PRE_CLOSE T-20/T-10;
- Weekend PRE_CLOSE T-60/T-30;
- daily one-clean-M5 reopen;
- weekend two-clean-M5 + gap assessment;
- optional broker-valid partial management;
- future governed REAL capability and separate release gate.

## 5. Operator-directed non-scalp differences

Coverage exists for:

- no trading-runtime Git operation;
- development backup through coherent remote commit → `git pull --ff-only` → optional clean ZIP;
- runtime-state backup independently local/network-free.

## 6. Current completeness state

Verified in the current freeze-preparation work:

1. 64-file canonical inventory exists;
2. every major subject has a destination/owner/proof route;
3. Audit 1 is preservation-first corrected;
4. Foundation, Market Intelligence, Trading Decisions, Risk/Execution, Research/Learning, Operator and core Engineering governance have been semantically normalized in the reviewed packets;
5. Audits 2–7 are protocols only and remain NOT RUN until their evidence stage;
6. explicit reference delta/preservation records are durable;
7. non-scalp preserved defaults are no longer intentionally classified as generic scalp calibration.

Still required before final documentation freeze:

- final manual-wide contradiction/cross-link/reconstructability pass;
- verify no stale metadata/reference survives in any untouched summary/template;
- update `DOCUMENTATION_AUDIT.md` with that final result;
- present remaining genuine scalp-specific deltas/calibration questions to the operator;
- obtain final documentation decisions before implementation.

Structural coverage is verified; final semantic freeze is **not yet declared complete**.