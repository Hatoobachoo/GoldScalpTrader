# GoldScalpTrader — Documentation Content Coverage Matrix

**Status:** FINAL 66-DOCUMENT COVERAGE MATRIX — DOCUMENTATION FREEZE BASELINE
**Version:** 2.0-final-coverage
**Authority:** Canonical subject ownership, implementation owner, proof route, reference-preservation classification and reconstructability coverage.

## 1. Final documentation inventory

Final canonical Markdown inventory:

```text
Top-level manuals/policies       9
01-foundation                    5
02-market-intelligence           7
03-trading-decisions             7
04-risk-execution                6
05-research-learning             7
06-operator                      3
07-engineering                  14
08-governance                    8
TOTAL                           66
```

The previously missing top-level documents are included:

```text
GITHUB_STRICT_USE_POLICY.md
BACKUP_SYNC_AND_RECOVERY_ARCHITECTURE.md
```

## 2. Foundation coverage

| Subject | Canonical owner | Planned source | Main proof |
|---|---|---|---|
| product objective / optimization | `01-foundation/PROJECT_VISION.md` | app/domain | architecture review + metrics |
| whole-system invariants | `SYSTEM_CONTRACT.md` | all layers | integration/audit |
| runtime topology / ordering | `ARCHITECTURE.md` | app/runtime | architecture/integration |
| specialist floor / authority | `TRADING_FLOOR_ARCHITECTURE.md` | intelligence/strategies/decisions | component/parity audits |
| build dependency order | `BUILD_PHASES.md` | whole repo | phase exit gates |

## 3. Market Intelligence coverage

| Subject | Owner | Planned source | Proof |
|---|---|---|---|
| candle anatomy/structure/BOS/MSS | `02-market-intelligence/CANDLE_STRUCTURE.md` | intelligence/candle_structure | chronology/no-lookahead |
| zones/location/Fib/trendline/POC | `TECHNICAL_STRUCTURE_AND_LEVELS.md` | intelligence/technical+confluence | geometry/lifecycle/ablation |
| liquidity/sweep/FVG/OB/path | `LIQUIDITY_AND_SMC.md` | intelligence/liquidity | causal-event tests |
| EMA/RSI/ATR/volatility | `INDICATORS_AND_VOLATILITY.md` | intelligence/indicators | chronological quant tests |
| session context | `SESSION_CONTEXT.md` | intelligence/session | DST/range/session research |
| MT5 data/history/quotes | `MARKET_DATA_AND_HISTORY.md` | market_data | normalization + connected reads |
| News/Fundamental soft context | `FUNDAMENTAL_AND_NEWS.md` | intelligence/news | provider/context/non-authority tests |

## 4. Trading Decisions coverage

| Subject | Owner | Planned source | Proof |
|---|---|---|---|
| six families + market-first setup detection + isolation | `03-trading-decisions/STRATEGY_FLOOR.md` | strategies/floor+setup_detector+isolation | detector/isolation tests |
| active BUY/SELL + Red Team | `SCORING_AND_DECISION_FUSION.md` | decisions/fusion | independent cases/correlation |
| Opportunity/M1 timing/freshness | `ENTRY_TIMING.md` | decisions/opportunity+timing | lifecycle/no-M1-alone/rearm |
| structural plan / gross geometry | `TRADE_PLAN.md` | decisions/trade_plan | family geometry/original R |
| breakout retest special geometry | `BREAKOUT_RETEST_GEOMETRY.md` | decisions/family_trade_plan | retest boundary/fallback |
| reversal event special geometry | `REVERSAL_EVENT_GEOMETRY.md` | decisions/family_trade_plan | sweep/failed-break proof |
| post-entry management | `TRADE_MANAGER_AND_EXIT.md` | management | HOLD/PROTECT/TRAIL/RUNNER/EXIT |

Executable Quality is a distinct implementation owner defined across TradePlan/System/Execution/Engineering docs and planned as `decisions/executable_quality.py`.

## 5. Risk / Execution coverage

| Subject | Owner | Planned source | Proof |
|---|---|---|---|
| monetary profiles/sizing/cooldown | `04-risk-execution/RISK_CONTRACT.md` | risk/* | exact-value/min-lot/state tests |
| session/risk hard permission | `SESSION_AND_RISK_STATE_MACHINE.md` | risk/permissions | state-machine + connected schedule |
| session + News provider separation | `SESSION_NEWS_PROVIDER_CONTRACT.md` | app/session_news | provider/cache/authority tests |
| Gate/Intent/writer/reconciliation | `EXECUTION_AND_BROKER_SAFETY.md` | execution/* | one-shot/no-retry/DEMO |
| broker/manual activity/cash flow | `BROKER_ACTIVITY_AND_MANUAL_TRADES.md` | market_data/activity + risk | attribution/accounting |
| persistence/restart/recovery | `PERSISTENCE_RESTART_AND_RECOVERY.md` | persistence/app recovery | crash/restore/handoff |

## 6. Research / Learning coverage

| Subject | Owner | Planned source | Proof |
|---|---|---|---|
| AI/learning authority boundaries | `05-research-learning/LEARNING_AND_AI_BOUNDARIES.md` | research/* | no-writer/approval tests |
| replay/walk-forward/holdout | `RESEARCH_AND_VALIDATION.md` | research/replay+validation | no-lookahead/holdout/stress |
| actual verified trade learning | `LIVE_DEMO_LEARNING_PIPELINE.md` | research/live_learning | exact-close/exactly-once |
| learning backup/machine safety | `LEARNING_BACKUP_AND_MULTI_MACHINE.md` | persistence/research | checkpoint/handoff |
| experiments/promotion | `GOVERNED_EXPERIMENTS_AND_PROMOTION.md` | research/promotion | stage/evidence/approval |
| discovery | `GOVERNED_STRATEGY_DISCOVERY.md` | research/discovery | candidate/liveness |
| autonomous invention | `AUTONOMOUS_STRATEGY_INVENTION.md` | research/invention/models | bounded primitives/complexity |

## 7. Operator coverage

| Subject | Owner | Planned source | Proof |
|---|---|---|---|
| primary dashboard/operator UX | `06-operator/DASHBOARD_AND_UX.md` | app/operator | DTO/read-only/layout |
| live dashboard state contract | `LIVE_DASHBOARD_CONTRACT.md` | operator | pulse/state/reason tests |
| approved graphical UI | `GRAPHICAL_DASHBOARD.md` | graphical_dashboard/* | no-scroll + functional controls |

Approved UX explicitly covers:

```text
Detected Setup
Active Test Family
Shadow status
M1/M5/M15/H1/H4 functional chart controls
Indicators / Drawings / Settings
exact Current Blocker vs Gate
```

## 8. Engineering coverage

| Subject | Owner |
|---|---|
| package/source ownership | `07-engineering/MODULE_STRUCTURE.md` |
| source/test map | `FILE_AND_TEST_CATALOG.md` |
| coding quality | `CODING_STANDARD.md` |
| test/evidence ladder | `TESTING_AND_VERIFICATION.md` |
| health/reasons/latency | `SYSTEM_HEALTH_AND_DIAGNOSTICS.md` |
| release checklist | `RELEASE_CHECKLIST.md` |
| final release audit | `FINAL_RELEASE_AUDIT.md` |
| 100-challenge architecture review | `AUDIT_1_FRESH_DESIGN_REVIEW.md` |
| docs→code→tests trace | `AUDIT_2_DOCUMENT_CODE_TEST_COMPLIANCE.md` |
| blocker/Gate truth | `AUDIT_3_GATE_PRESENTATION_AND_DOCUMENT_SYNC.md` |
| low/zero trade geometry | `AUDIT_4_ZERO_TRADE_GEOMETRY_REVIEW.md` |
| setup/event freshness | `AUDIT_5_DEEP_ZERO_TRADE_GATE_AND_EVENT_FRESHNESS.md` |
| live geometry/executable freshness | `AUDIT_6_LIVE_GEOMETRY_AND_ENTRY_FRESHNESS.md` |
| component-by-component audit | `AUDIT_7_INDIVIDUAL_COMPONENT_REVIEW.md` |

## 9. Governance coverage

| Subject | Owner |
|---|---|
| approved decisions | `08-governance/DESIGN_DECISIONS.md` |
| remaining calibration/external/deferred items | `OPEN_QUESTIONS.md` |
| reference feature preservation | `PRESERVATION_LEDGER.md` |
| documentation quality/visual standard | `DOCUMENTATION_STANDARD.md` |
| final documentation audit | `DOCUMENTATION_AUDIT.md` |
| exact Swing→Scalp changes | `DOCUMENTATION_COMPARISON.md` |
| single-manual / legacy topology | `LEGACY_DOCS_RETIREMENT.md` |
| complete subject matrix | this file |

## 10. Top-level manual/policy coverage

| File | Purpose |
|---|---|
| `README.md` | entry point / current final architecture |
| `GLOSSARY.md` | canonical vocabulary |
| `GITHUB_STRICT_USE_POLICY.md` | remote/security/billing/source-use policy |
| `BACKUP_SYNC_AND_RECOVERY_ARCHITECTURE.md` | full source/runtime recovery topology |
| `CODER_GUIDE.md` | developer navigation |
| `PROJECT_BUILD_AND_RECOVERY_GUIDE.md` | continuation/context/machine recovery |
| `FINAL_BUILD_PROMPT.md` | no-chat-history reconstruction prompt |
| `USER_MANUAL.md` | human operator description |
| `SETUP_AND_RUN_GUIDE.md` | intended install/modes/recovery/operator commands |

## 11. Critical final architecture coverage

Explicit coverage exists for:

- market-first setup detection; active family cannot force setup;
- one active live family / five shadow families;
- six families all preserved;
- family-specific important evidence without global filter soup;
- M5 setup + M1 subordinate timing;
- persistent Opportunity/fresh re-arm;
- family-aware TradePlan;
- no automatic inherited Swing 1.20R hard Scalp floor;
- emergency spread + spread/SL + spread/target + cost/reward;
- slippage/deviation/latency revalidation;
- preserved monetary profiles/aggressive mode/reset/cooldown/re-entry;
- News soft-only / no News cooldown-warmup;
- hard broker/session separation;
- central Gate/one-shot Intent/sole writer/reconciliation;
- time-efficiency management / exceptional Runner;
- continuous invention/tuning/ML with production approval gate;
- ~120/day research benchmark;
- approved Swing-style no-scroll graphical dashboard;
- no runtime Git;
- local runtime checkpoint/recovery;
- sequential same-scope machine handoff;
- distributed active-active deferred.

## 12. Visual documentation coverage

Major lifecycle/dependency/authority documents contain appropriate Mermaid flow/state/sequence diagrams and contract tables.

Empirical performance charts are intentionally not fabricated before real replay/DEMO data. Research contracts require reproducible charts once evidence exists.

## 13. Evidence classification

This matrix proves **documentation coverage only**.

It does not claim:

```text
final implementation exists
all tests pass
Scalp replay is profitable
connected Exness DEMO lifecycle is proven
recovery drill has passed
future REAL is authorized
```

Those are later evidence stages.

## 14. Final coverage verdict

```text
66-file canonical topology                 COVERED
all major product subjects                 COVERED
Swing preservation / explicit deltas       COVERED
market-first setup routing                 COVERED
operator graphical dashboard               COVERED
source/test/proof ownership                 COVERED
100-challenge architecture review          COVERED
documentation reconstructability           COVERED
implementation evidence                     PENDING
connected external proof                    PENDING
```
