# GoldScalpTrader — Documentation Content Coverage Matrix

**Status:** POST-AUDIT-1 FREEZE-PREPARATION COVERAGE MAP — STRUCTURAL COVERAGE VERIFIED
**Version:** 1.0-cache-aware-coverage
**Authority:** Proof that the canonical manual covers the intended design, implementation, proof and operator surface.

## 1. Purpose

This is a loss-prevention/navigation map.

Every substantive subject has a canonical destination, intended implementation owner and proof route. A row is structurally covered only when the destination exists and explains purpose through evidence/failure boundary.

This matrix is not a substitute for semantic/documentation audit.

## 2. Coverage matrix

| Subject | Canonical destination | Planned implementation | Main proof route |
|---|---|---|---|
| product purpose/non-goals | `00-foundation/PROJECT_VISION.md` | app/domain | system/integration review |
| highest-level invariants | `00-foundation/SYSTEM_CONTRACT.md` | whole runtime | cross-module tests/audits |
| runtime topology | `00-foundation/ARCHITECTURE.md` | app/* | integration/architecture review |
| parallel trading floor | `TRADING_FLOOR_ARCHITECTURE.md` | intelligence/strategies | parity tests |
| build dependency order | `BUILD_PHASES.md` | whole repo | phase exit gates |
| MT5 facts/history | `10-market-intelligence/MARKET_DATA_AND_HISTORY.md` | market_data | market-data tests + connected read |
| candle/structure | `CANDLE_STRUCTURE.md` | intelligence/candle_structure | chronology/no-lookahead |
| technical zones/room | `TECHNICAL_STRUCTURE_AND_LEVELS.md` | intelligence/technical | geometry tests |
| liquidity/SMC | `LIQUIDITY_AND_SMC.md` | intelligence/liquidity | causal liquidity tests |
| EMA/RSI/ATR/volatility | `INDICATORS_AND_VOLATILITY.md` | intelligence/indicators | chronological quant tests |
| soft sessions | `SESSION_CONTEXT.md` | intelligence/session | DST/range replay tests |
| news/macro intelligence | `FUNDAMENTAL_AND_NEWS.md` | intelligence/news | provider/event/cache tests |
| News LKG cache / provider failure | `FUNDAMENTAL_AND_NEWS.md`, `SESSION_NEWS_PROVIDER_CONTRACT.md` | app/session_news + intelligence/news | cache TTL/scope/coverage/no-laundering/restart tests |
| strategy families | `20-trading-decisions/STRATEGY_FLOOR.md` | strategies | family tests/replay |
| BUY/SELL fusion | `SCORING_AND_DECISION_FUSION.md` | decisions/fusion | fusion/conflict tests |
| Opportunity/timing/freshness | `ENTRY_TIMING.md` | decisions/opportunity,timing | lifecycle/freshness tests |
| structural plan | `TRADE_PLAN.md` | decisions/trade_plan | geometry/R/cost tests |
| breakout retest geometry | `BREAKOUT_RETEST_GEOMETRY.md` | family_trade_plan | event/fallback tests |
| reversal event geometry | `REVERSAL_EVENT_GEOMETRY.md` | family_trade_plan | event-extreme tests |
| open-trade management | `TRADE_MANAGER_AND_EXIT.md` | management | manager/execution tests |
| monetary risk | `30-risk-execution/RISK_CONTRACT.md` | risk | lot/min-lot/margin/risk-day tests |
| manual/external activity | `BROKER_ACTIVITY_AND_MANUAL_TRADES.md` | market_data/activity | activity/accounting tests |
| hard state composition | `SESSION_AND_RISK_STATE_MACHINE.md` | risk/permissions | permission + cache-aware News matrix tests |
| persistence/recovery/local backup | `PERSISTENCE_RESTART_AND_RECOVERY.md` | persistence/app recovery | checkpoint/restore drills |
| provider acquisition/cache | `SESSION_NEWS_PROVIDER_CONTRACT.md` | app/session_news | provider/cache/retry/expiry tests |
| broker-write safety | `EXECUTION_AND_BROKER_SAFETY.md` | execution | one-shot/reconcile/controller + DEMO |
| learning boundaries | `40-research-learning/LEARNING_AND_AI_BOUNDARIES.md` | research | learning/governance tests |
| chronological research | `RESEARCH_AND_VALIDATION.md` | research/replay | replay/holdout/stress evidence |
| actual DEMO learning | `LIVE_DEMO_LEARNING_PIPELINE.md` | research/live_learning | exact-close learning tests + DEMO |
| learning backup/machines | `LEARNING_BACKUP_AND_MULTI_MACHINE.md` | persistence/research | local recovery/handoff |
| promotion | `GOVERNED_EXPERIMENTS_AND_PROMOTION.md` | research/promotion | stage/evidence tests |
| discovery | `GOVERNED_STRATEGY_DISCOVERY.md` | research/discovery | candidate tests |
| invention | `AUTONOMOUS_STRATEGY_INVENTION.md` | research/invention | primitive/complexity tests |
| primary dashboard | `50-operator/DASHBOARD_AND_UX.md` | app/operator | dashboard authority + provider/cache truth tests |
| graphical dashboard | `GRAPHICAL_DASHBOARD.md` | graphical_dashboard/operator | local/read-only tests |
| live terminal extension | `LIVE_DASHBOARD_CONTRACT.md` | operator | width/pulse/Gate truth tests |
| file/test map | `60-engineering/FILE_AND_TEST_CATALOG.md` | whole repo | tree audit |
| module ownership | `MODULE_STRUCTURE.md` | whole repo | dependency review |
| coding quality | `CODING_STANDARD.md` | whole repo | lint/static/code review |
| testing/evidence ladder | `TESTING_AND_VERIFICATION.md` | tests/scripts | verification reports |
| diagnostics | `SYSTEM_HEALTH_AND_DIAGNOSTICS.md` | diagnostics/operator | health/reason tests |
| release gate | `RELEASE_CHECKLIST.md` | release process | exact evidence checklist |
| final audit | `FINAL_RELEASE_AUDIT.md` | audit process | scoped sign-off |
| fresh-zero challenge | `AUDIT_1_FRESH_DESIGN_REVIEW.md` | pre-build governance | architecture verdicts |
| doc→code→tests | `AUDIT_2_DOCUMENT_CODE_TEST_COMPLIANCE.md` | post-build audit | traceability matrix |
| Gate/presentation sync | `AUDIT_3_GATE_PRESENTATION_AND_DOCUMENT_SYNC.md` | operator/execution | focused audit |
| zero-trade geometry | `AUDIT_4_ZERO_TRADE_GEOMETRY_REVIEW.md` | decision/plan | connected corrective audit |
| deep zero-trade/freshness | `AUDIT_5_DEEP_ZERO_TRADE_GATE_AND_EVENT_FRESHNESS.md` | full entry chain | causal audit |
| live geometry/freshness | `AUDIT_6_LIVE_GEOMETRY_AND_ENTRY_FRESHNESS.md` | intelligence/decisions | corrective audit |
| individual components | `AUDIT_7_INDIVIDUAL_COMPONENT_REVIEW.md` | all components | module-by-module review |
| design rationale | `90-governance/DESIGN_DECISIONS.md` | governance | decision audit |
| unresolved work | `OPEN_QUESTIONS.md` | governance | closure records |
| documentation method | `DOCUMENTATION_STANDARD.md` | whole repo | documentation audit |
| preservation | `PRESERVATION_LEDGER.md` | governance | reference comparison |
| documentation audit | `DOCUMENTATION_AUDIT.md` | governance | reconstructability review |
| explicit Swing→Scalp delta | `DOCUMENTATION_COMPARISON.md` | governance | reference change audit |
| legacy topology | `LEGACY_DOCS_RETIREMENT.md` | governance | one-authority review |
| full subject coverage | this file | governance | semantic audit |
| developer navigation | `CODER_GUIDE.md` | whole repo | build handoff review |
| build/recovery continuation | `PROJECT_BUILD_AND_RECOVERY_GUIDE.md` | whole repo | context-recovery test |
| installation/operation | `SETUP_AND_RUN_GUIDE.md` | operator | clean-machine setup proof |
| human use | `USER_MANUAL.md` | operator | connected operation review |
| whole-project AI handoff | `FINAL_BUILD_PROMPT.md` | development handoff | reconstructability review |
| manual entry/read order | `Documents/README.md` | docs | doc audit |
| canonical vocabulary | `GLOSSARY.md` | whole repo | terminology review |

## 3. Scalp-specific coverage additions

The manual explicitly covers:

- event/trigger freshness;
- cost-adjusted target room;
- spread/slippage/drift;
- latency observability;
- short hold/time efficiency;
- min-lot affordability;
- same-episode re-arm;
- cost-aware replay;
- cache-aware News provider failure without timestamp laundering;
- conservative News UNKNOWN new-entry policy after cache expiry;
- local-only runtime backup;
- low-GitHub development pull/ZIP backup;
- no runtime Git publication;
- explicit Swing→Scalp change ledger.

## 4. Current completeness state

Verified now:

1. canonical tree has the expected 64-file inventory;
2. each major subject has a canonical destination;
3. Fresh-Zero Audit 1 classified the major architecture choices;
4. architecture questions are closed or remaining work is classified implementation/calibration/external/deferred;
5. explicit reference delta is durable in `DOCUMENTATION_COMPARISON.md`.

Still required before final documentation freeze:

- normalize legacy pre-challenge metadata/statuses in untouched documents;
- finish semantic/cross-link reconstructability scan;
- close `DOCUMENTATION_AUDIT.md` only when those checks are clean.
