# GoldScalpTrader — Module Structure and File Map

**Status:** FROZEN V1 MODULE MAP — IMPLEMENTATION TREE STILL PLANNED
**Version:** 1.1-cache-aware-source-ownership
**Authority:** File ownership, dependency direction and placement.

## 1. Dependency direction

```text
config + domain + diagnostics + security
→ market_data
→ intelligence — staged logically independent analytical work
→ strategies — six independent scalp families
→ decisions — BUY/SELL + debate + Opportunity + M5 timing + TradePlan
→ risk — STANDARD monetary authority
→ execution — hard authority + Gate + Intent + sole writer + reconcile
→ management
→ app composition
→ operator read-only presentation

research/learning → downstream evidence/proposals only
persistence → durable context/checkpoints/local runtime backup; never broker truth
```

Physical analytical concurrency is optional/profiling-driven. TradePlan → Risk → hard authority → Gate → Intent → writer → reconciliation remains serial.

## 2. Package ownership

| Package | Owns | Must not own |
|---|---|---|
| `config` | validated settings/modes/policy IDs/provider/cache configuration | hidden policy override |
| `domain` | enums/IDs/typed facts | MT5 calls |
| `diagnostics` | logs/reasons/health | trading decisions |
| `security` | secret detection/redaction | credentials |
| `market_data` | sole normalized MT5 read boundary/activity | raw write |
| `intelligence` | causal descriptive evidence + normalized News facts | monetary/write authority |
| `strategies` | six independent hypotheses/scheduler | Risk/Gate |
| `decisions` | fusion/Opportunity/M5 timing/TradePlan | MT5/final permission |
| `risk` | STANDARD affordability/risk-day/capacity/permission substates | strategy rewrite/send |
| `execution` | Gate/checks/Intent/controller/sole writer/reconcile | strategy invention |
| `management` | ManagedTrade decision/lifecycle | raw writer |
| `persistence` | typed state/checkpoint/runtime recovery package | broker truth/Git operations |
| `app` | startup/runtime/provider/cache/composition/DTO | duplicate domain policy |
| `operator` | read-only mapping/render/snapshot | authority mutation/cache validity calculation |
| `research` | replay/learning/discovery/promotion | production broker authority |
| `graphical_dashboard` | localhost read-only UI | MT5/trading mutation |

## 3. Frozen data/timeframe owner rule

H1/M15/M5 production data and optional H4 are read through `market_data`. M1 may be acquired only for explicit diagnostics/research and cannot become hidden strategy/timing authority.

## 4. Planned application/config

```text
app/main.py              launcher/modes; no runtime Git
app/runtime.py           dependency composition
app/startup.py           ordered startup authorities
app/recovery.py          lifecycle recovery
app/recovery_mt5.py      broker recovery adapter
app/cycle.py             one governed entry/management cycle
app/loop.py              M5/event cadence + maintenance/presentation
app/dashboard.py         authoritative DTO mapping
app/live_presentation.py read-only enrichment
app/session_news.py      session/news provider + last-known-good cache boundary
config/settings.py       READINESS/DRY_RUN/PRIMARY-DEMO + STANDARD policy + provider/cache refs
```

`app/session_news.py` owns provider acquisition/cache transport semantics, including:

- bounded fetch/refresh;
- accepted normalized last-known-good cache persistence/loading;
- scope/schema/coverage/TTL/integrity validation;
- atomic cache replacement;
- preserving original timestamps/validity after failed refresh;
- provider health/source reporting.

It does **not** own final News permission policy. `intelligence/news.py` normalizes accepted event facts; `risk/permissions.py` owns CLEAR/BLACKOUT/UNKNOWN permission composition.

## 5. Planned domain / data / intelligence

```text
domain/enums.py
domain/ids.py
domain/market.py
domain/models.py
diagnostics/logging.py
diagnostics/reasons.py
diagnostics/health.py
security/financial_secrets.py

market_data/mt5_reader.py
market_data/activity.py
market_data/snapshot.py

intelligence/candle_structure.py
intelligence/indicators.py
intelligence/technical.py
intelligence/liquidity.py
intelligence/confluence.py
intelligence/session.py
intelligence/news.py
intelligence/snapshot.py
```

`intelligence/news.py` owns event normalization/tier/window facts and consumes already-validated provider/cache inputs. It must not refresh cache TTL or perform broker permission.

## 6. Planned strategies / decisions

```text
strategies/floor.py
strategies/parallel.py
strategies/confluence.py

decisions/fusion.py
decisions/snapshot.py
decisions/opportunity.py
decisions/timing.py
decisions/family_trade_plan.py
decisions/trade_plan.py
```

Frozen families: Trend Pullback, Breakout Expansion, Breakout Retest, Liquidity Sweep Reversal, Failed Breakout Reversal and Compression Expansion.

Family geometry adapters can prefer exact proven event boundaries but cannot invent tighter stops or override gross/cost-room/Risk policy.

## 7. Planned Risk / execution

```text
risk/engine.py
risk/state.py
risk/permissions.py

execution/models.py
execution/checks.py
execution/gate.py
execution/intent_store.py
execution/service.py
execution/mt5_writer.py       # sole irreversible boundary; later milestone
execution/reconcile.py
execution/controller.py
execution/sqlite_coordination.py
```

`risk/permissions.py` consumes normalized current News state. It owns the V1 rule that true `NEWS_SAFETY_UNKNOWN` blocks new entry while valid LKG cache may preserve accepted CLEAR/BLACKOUT truth.

No irreversible writer implementation until its deliberate DEMO milestone.

## 8. Planned management / persistence / research

```text
management/models.py
management/manager.py
management/execution.py
management/store.py

persistence/store.py
persistence/runtime_state.py
persistence/checkpoint.py
persistence/backup.py
persistence/local_recovery_package.py

research/learning.py
research/live_learning.py
research/replay.py
research/management_replay.py
research/session_history.py
research/stress.py
research/validation.py
research/datasets.py
research/acquisition.py
research/evidence.py
research/packages.py
research/metrics.py
research/outcomes.py
research/ablation.py
research/episode_journal.py
research/discovery.py
research/invention.py
research/promotion.py
```

Provider cache is current safety context, not broker truth. Restart revalidates it through `app/session_news.py`; runtime recovery cannot mark an expired cache current.

No runtime `shutdown_publish.py` / Git publisher is planned.

## 9. Planned operator

```text
operator/presentation.py
operator/narrow_dashboard.py
operator/live_dashboard.py
operator/rich_dashboard.py
operator/compact_dashboard.py
operator/graphical_snapshot.py
operator/__init__.py

graphical_dashboard/ui.py
graphical_dashboard/server.py
graphical_dashboard/__main__.py
```

Presentation displays provider health/source/cache age/validity facts received from owners and never recalculates authority.

## 10. Planned scripts

```text
scripts/run_walk_forward.py
scripts/acquire_mt5_dataset.py
scripts/report_demo_learning_evidence.py
scripts/restore_runtime_checkpoint.py
scripts/create_local_recovery_package.py
scripts/create_source_zip.py           # optional development helper
scripts/scan_financial_secrets.py
scripts/verify_documents_manual.py
```

A manual Git bundle command/helper may exist later as advanced tooling, but it is not a normal runtime/source-backup dependency.

## 11. Forbidden dependency directions

```text
strategy/intelligence worker → raw MT5 write          NO
analytical worker → lifecycle persistence/Risk/Gate   NO
operator/dashboard → authority recalculation           NO
operator/dashboard → News cache TTL extension          NO
research/learning → broker authority                   NO
checkpoint restore → broker permission                 NO
unknown position → empty exposure                      NO
ambiguous broker result → blind retry                  NO
trading runtime → Git commit/push/pull                 NO
backup package → credentials by default                NO
M1 diagnostic → hidden production trigger              NO
failed News refresh → rewrite cache timestamp/TTL       NO
```

## 12. Intended runtime trace

```text
app/main.py
→ validated Settings / MT5Reader
→ immutable MarketSnapshot
→ startup/recovery authorities
→ app/session_news.py provider/cache validation
→ app/cycle.py
   → staged intelligence
   → six family evaluations (serial or bounded-parallel)
   → BUY/SELL + Red Team
   → Opportunity / completed-M5 timing
   → TradePlan gross + cost-adjusted room
   → STANDARD Risk + cache-aware News permission
   → hard authorities
   → central Gate
   → Intent → sole MT5Writer → reconciliation
   → ManagedTrade / Trade Manager
→ app/loop.py safe learning/local-runtime-backup/presentation
→ graceful stop releases MT5/controller
→ final verified local checkpoint only
```

## 13. Proof map

| Boundary | Minimum deterministic proof |
|---|---|
| raw reads | normalization/freshness/completed chronology |
| intelligence | causal evidence/UNKNOWN semantics |
| News provider/cache | accepted cache creation, atomic replace, TTL/scope/coverage, refresh failure reuse, expiry → UNKNOWN, no timestamp laundering |
| analytical scheduling | one-worker/canonical-order parity; bounded-parallel parity if implemented |
| strategies/fusion | six families, BUY/SELL, correlation control |
| Opportunity/timing | identity, event freshness, M1 non-authority |
| TradePlan | family geometry + gross/cost-room calculations |
| Risk | STANDARD sizing/min-lot/hard ceiling/daily state |
| session/news | fresh-source/cache CLEAR, BLACKOUT, true UNKNOWN matrix |
| execution | Gate, one-shot Intent, writer/reconcile |
| operator | upstream blocker vs actual Gate + provider/cache truth |
| management | monotonic protection/time-efficiency EXIT/verified close |
| persistence | strict restore/checkpoint/local backup |
| learning | exact close + exactly-once observation |
| research | no-lookahead/cost/holdout/package integrity |

## 14. Synchronization rule

Any added/renamed/removed source/test or proof owner updates this map and `FILE_AND_TEST_CATALOG.md` in the same affected-graph packet.