# GoldScalpTrader — Module Structure and File Map

**Status:** FROZEN V1 MODULE MAP — PRESERVATION-FIRST CORRECTED / IMPLEMENTATION TREE PLANNED
**Version:** 1.2-profiled-risk-bounded-parallel
**Authority:** File ownership, dependency direction and placement.

## 1. Dependency direction

```text
config + domain + diagnostics + security
→ market_data
→ intelligence — staged bounded-parallel analytical work
→ strategies — six independent family teams
→ decisions — BUY/SELL + Opportunity + completed-M5 timing + TradePlan
→ risk — SMALL/MEDIUM/NORMAL profile authority + optional explicit aggressive overlay
→ execution — hard authority + Gate + Intent + sole writer + reconcile
→ management
→ app composition
→ operator read-only presentation

research/learning → downstream evidence/proposals only
persistence → durable context/checkpoints/local runtime backup; never broker truth
```

Financial/broker authority remains serial.

## 2. Package ownership

| Package | Owns | Must not own |
|---|---|---|
| `config` | validated settings/modes/profile/aggressive/provider/cache policy IDs | hidden policy override |
| `domain` | enums/IDs/typed facts | MT5 calls |
| `diagnostics` | logs/reasons/health | trading decisions |
| `security` | secret detection/redaction | credentials |
| `market_data` | sole normalized MT5 read boundary/activity | raw write |
| `intelligence` | causal descriptive evidence + normalized News facts | monetary/write authority |
| `strategies` | six independent hypotheses + bounded scheduler | Risk/Gate |
| `decisions` | fusion/Opportunity/M5 timing/TradePlan | MT5/final permission |
| `risk` | profiles, aggressive overlay, affordability, risk-day/capacity/permission substates | strategy rewrite/send |
| `execution` | Gate/checks/Intent/controller/sole writer/reconcile | strategy invention |
| `management` | ManagedTrade decision/lifecycle + broker-valid partial-management decisions | raw writer |
| `persistence` | typed state/checkpoint/runtime recovery package | broker truth/Git operations |
| `app` | startup/runtime/provider/cache/composition/DTO | duplicate policy |
| `operator` | read-only mapping/render/snapshot | authority mutation/cache validity calculation |
| `research` | replay/learning/discovery/promotion | production broker authority |
| `graphical_dashboard` | localhost read-only UI | MT5/trading mutation |

## 3. Data/timeframe owner rule

H1/M15/M5 production data and optional H4 are read through `market_data`. M1 may be acquired only for explicit diagnostics/research.

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
app/session_news.py      session/news provider + LKG cache boundary
config/settings.py       READINESS/DRY_RUN/DEMO/future-REAL refs,
                         Risk profile + aggressive overlay refs,
                         provider/cache baseline refs
```

`app/session_news.py` owns bounded fetch/refresh, accepted LKG cache persistence/loading, scope/schema/coverage/TTL/integrity validation, atomic replacement and provider health/source reporting.

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

## 6. Planned strategies / decisions

```text
strategies/floor.py
strategies/parallel.py       # preserved bounded analytical concurrency
strategies/confluence.py

decisions/fusion.py
decisions/snapshot.py
decisions/opportunity.py
decisions/timing.py
decisions/family_trade_plan.py
decisions/trade_plan.py
```

Bounded-parallel scheduler must preserve immutable inputs, deterministic output order, bounded workers and one-worker fallback/parity.

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
execution/mt5_writer.py
execution/reconcile.py
execution/controller.py
execution/sqlite_coordination.py
```

Risk owner implements:

- fixed UTC-day SMALL/MEDIUM/NORMAL profile resolution;
- reference target/elevated/hard/daily bands;
- explicit disabled-by-default aggressive small-account overlay;
- 8% max SL-risk ceiling, 16% aggregate and daily ceilings when enabled;
- min-lot actual-risk evaluation;
- manual reset disabled by default;
- preserved cooldown/re-entry state.

`risk/permissions.py` also composes current News state and session states.

No irreversible writer until controlled DEMO milestone. Future REAL capability is preserved but gated separately.

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

Optional partial management remains a management capability where volume is broker-valid/divisible.

No runtime Git publisher is planned.

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

Presentation displays owned profile/overlay/provider/cache facts and never recalculates authority.

## 10. Planned scripts

```text
scripts/run_walk_forward.py
scripts/acquire_mt5_dataset.py
scripts/report_demo_learning_evidence.py
scripts/restore_runtime_checkpoint.py
scripts/create_local_recovery_package.py
scripts/create_source_zip.py
scripts/scan_financial_secrets.py
scripts/verify_documents_manual.py
```

## 11. Forbidden dependency directions

```text
strategy/intelligence worker → raw MT5 write                 NO
analytical worker → lifecycle persistence/Risk/Gate          NO
operator/dashboard → authority recalculation                  NO
operator/dashboard → News cache TTL extension                 NO
research/learning → broker authority                          NO
unknown position → empty exposure                             NO
ambiguous broker result → blind retry                         NO
trading runtime → Git commit/push/pull                        NO
backup package → credentials by default                       NO
M1 diagnostic → hidden production trigger                     NO
failed News refresh → rewrite cache timestamp/TTL              NO
strategy score → select higher monetary Risk                   NO
equity alone → silently enable aggressive mode                NO
simple implementation preference → remove reference feature  NO
```

## 12. Intended runtime trace

```text
app/main.py
→ validated Settings / MT5Reader
→ immutable MarketSnapshot
→ startup/recovery authorities
→ app/session_news.py provider/cache validation
→ staged bounded-parallel intelligence/families
→ BUY/SELL + Red Team
→ Opportunity / completed-M5 timing
→ TradePlan gross + cost-adjusted room
→ profiled Risk + optional explicit overlay
→ hard authorities
→ central Gate
→ Intent → sole MT5Writer → reconciliation
→ ManagedTrade / Trade Manager
→ learning / local runtime backup / presentation
```

## 13. Proof map

| Boundary | Minimum deterministic proof |
|---|---|
| raw reads | normalization/freshness/completed chronology |
| intelligence | causal evidence/UNKNOWN semantics |
| analytical scheduling | bounded-parallel + one-worker parity |
| strategies/fusion | six families, BUY/SELL, correlation control |
| Opportunity/timing | identity, event freshness, M1 non-authority |
| TradePlan | family geometry + gross/cost-room calculations |
| Risk | profile resolution/bands, aggressive overlay, min-lot, cooldown/reset/daily state |
| provider/cache | 1800s baseline, refresh failure reuse, expiry → UNKNOWN, no timestamp laundering |
| session/news | PRE_CLOSE/reopen + fresh/cache CLEAR/BLACKOUT/UNKNOWN matrix |
| execution | Gate, one-shot Intent, writer/reconcile |
| operator | blocker vs Gate + profile/overlay/provider/cache truth |
| management | protection/time-efficiency/partial handling/verified close |
| persistence | strict restore/checkpoint/local backup |
| learning/research | exactly-once/no-lookahead/cost/holdout integrity |

## 14. Synchronization rule

Any source/test addition/removal/rename or proof-owner change updates this map, `FILE_AND_TEST_CATALOG.md`, owning contract and affected operator/governance surfaces in the same coherent packet.