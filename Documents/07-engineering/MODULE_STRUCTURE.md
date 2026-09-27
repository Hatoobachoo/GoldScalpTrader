# GoldScalpTrader — Module Structure and File Map

**Status:** IMPLEMENTED ARCHITECTURE MAP — CURRENT HEAD REQUIRES OFFLINE RE-VERIFICATION / CONNECTED DEMO PENDING  
**Version:** 2.8-bounded-discovery-runtime-governance  
**Authority:** Actual package/file ownership and dependency direction.

## 1. Dependency direction

```text
config/domain
→ market_data
→ intelligence
→ strategies: market-first six-family detection + isolation
→ decisions: independent BUY/SELL + Red Team + durable M5 Opportunity + subordinate M1 timing + structural TradePlan
→ durable Risk-day authority / monetary sizing
→ app/runtime: hard Session + Risk + lifecycle composition
→ execution: Gate / Intent / sole writer / reconciliation
→ management / verified close
→ actual learning + causal SHADOW_ONLY outcomes
→ verified-learning triggers + bounded discovery
→ governed research + verified stage-proof packages
→ operator presentation

persistence supplies durable context to runtime/execution/management/research.
```

Broker/financial authority remains serial.

## 2. Package authority

| Package | Owns | Must never own |
|---|---|---|
| `config` | validated settings and frozen policy defaults | hidden live mutation |
| `domain` | typed facts/IDs/enums | MT5 calls |
| `market_data` | normalized MT5 reads/account/activity facts | irreversible writes |
| `intelligence` | causal market evidence | money/Gate |
| `strategies` | six-family setup detection/isolation | Risk/broker writes |
| `decisions` | Opportunity/Timing/TradePlan/quality | raw MT5 writes |
| `risk` | durable UTC Risk-day, sizing, daily lock/cooldown | strategy mutation/broker write |
| `app` | sole public guarded DEMO composition, recovery/cadence | duplicate execution authority |
| `execution` | Gate/controller/Intent/checks/sole writer/reconcile | strategy invention |
| `management` | ManagedTrade and governed mutations/close proof | raw writer |
| `persistence` | checksummed local records/events/checkpoints | current broker truth |
| `research` | actual/shadow evidence, trigger classification, bounded discovery, replay, invention, verified stage proof | runtime/broker authority |
| `operator` / `graphical_dashboard` | read-only presentation | authority recomputation |

## 3. Material source map

```text
src/gold_scalp_trader/
├── config/settings.py
├── domain/{enums,ids,market,models}.py
├── market_data/{account_mode,mt5_reader,activity,snapshot}.py
├── intelligence/{candle_structure,indicators,technical,liquidity,confluence,session,news,snapshot}.py
├── strategies/{floor,setup_detector,isolation,scheduler,confluence}.py
├── decisions/{fusion,snapshot,opportunity,timing,family_trade_plan,trade_plan,executable_quality}.py
├── risk/{engine,state,runtime,permissions}.py
├── execution/{models,checks,gate,intent_store,service,mt5_writer,reconcile,controller,sqlite_coordination}.py
├── management/{models,manager,execution,closure,store}.py
├── persistence/{store,runtime_state,checkpoint,backup,local_recovery_package}.py
├── research/
│   ├── learning.py / live_learning.py
│   ├── timing_learning.py / runtime_evidence.py
│   ├── outcomes.py / shadow_runtime.py
│   ├── replay.py / management_replay.py / session_history.py
│   ├── stress.py / validation.py / ablation.py / metrics.py
│   ├── datasets.py / acquisition.py / evidence.py / packages.py
│   ├── episode_journal.py / triggers.py / discovery.py / invention.py / models.py
│   ├── promotion.py / candidate_registry.py
│   └── stage_orchestrator.py
├── operator/{presentation,terminal_dashboard,rich_dashboard,narrow_dashboard,compact_dashboard,graphical_snapshot}.py
└── app/
    ├── runtime.py              # sole public guarded DEMO composer
    ├── runtime_core.py         # narrow broker-safe mechanics only
    ├── session_news.py / session_authority.py
    ├── opportunity_lifecycle.py
    ├── startup.py / recovery.py / recovery_mt5.py
    ├── cycle.py / loop.py / demo_runner.py
    └── dashboard/live_presentation/graphical runner presentation plumbing
```

## 4. Runtime authority split

`app/runtime.py` is the only public guarded DEMO financial composer. It internally resolves hard Session authority and durable Risk-day authority. There is no caller `market_open` override.

`app/runtime_core.py` owns narrow mechanics only: symbol capability, broker-safe checks, causal OPEN context, unresolved Intent reconciliation, verified-close recovery and already-authorized managed-trade mutation mechanics. It must not expose another full guarded DEMO cycle.

Existing exposure management is not blocked merely because a new-entry Risk-day bootstrap/lock cannot pass; protection/exit continues through Session + Gate + writer safety.

## 5. Risk ownership

```text
risk/runtime.py
→ reconstruct/freeze UTC DayStartEquity
→ account cash-flow attribution
→ apply verified close outcomes
→ daily loss lock / 3-loss cooldown
→ PASS/BLOCK/UNKNOWN Risk authority

app/runtime.py
→ only after RiskAuthority PASS, run monetary sizing using authority.state.day_start_equity
```

Current equity cannot silently re-profile the account intraday.

## 6. Session / News ownership

```text
app/session_news.py      → typed provider facts
app/session_authority.py → hard OPEN/PRE_CLOSE/CLOSED/UNKNOWN permission
intelligence/news.py     → soft context only
```

News never grants/denies hard broker permission. Session UNKNOWN fails closed.

## 7. Execution / controller ownership

Only `execution/mt5_writer.py` may call raw `order_send`.

```text
Gate
→ Intent persisted
→ local + broker order_check
→ execute_once verifies current controller lease/fencing
→ SUBMITTING persisted
→ exactly one writer call
→ ACK classification
→ reconciliation
```

GoldScalp uses mutation-scoped controller leases. An independent long-lived heartbeat is not required by this design because fencing is re-verified immediately before irreversible send.

## 8. SHADOW_ONLY ownership

`research/shadow_runtime.py` is research-only. For each qualified SHADOW family it may:

```text
stable causal shadow episode identity
→ subordinate M1 TimingDecision
→ family-aware structural hypothetical plan
→ freeze contemporaneous entry/SL/primary target + quoted-spread cost in R
→ evaluate only future completed M1 candles
→ TARGET / STOP / AMBIGUOUS / unresolved
→ durable counterfactual outcome
```

It imports no Risk, Gate, Intent or MT5 writer. One terminal shadow episode cannot be recreated and counted again.

## 9. Continuous discovery ownership

`research/triggers.py` converts only verified StrategyMemory observations into idempotent research episodes. Its thresholds are research-trigger thresholds, not live trading parameters.

`research/discovery.py` groups recurring independent episodes. A candidate is registered only when the cluster has enough independent evidence and immutable source lineage. Automatic live-derived candidates bind to the underlying StrategyMemory source IDs. Missing lineage produces a durable suppression reason instead of a guessed candidate.

Broker/system faults and hard-safety blocks are explicitly non-strategy evidence and are suppressed rather than optimized around.

`app/demo_runner.py` invokes trigger classification/discovery only inside the best-effort research boundary, and only reruns discovery when new derived research episodes were appended.

## 10. Governed research ownership

`research/candidate_registry.py` owns durable candidate identity/stage chain but does not manufacture PASS proof.

`research/stage_orchestrator.py` is the only stage-proof issuer protocol. It verifies immutable package integrity, exact candidate fingerprint, exact next stage, evidence identity, manifest SHA and stage-specific required checks. No undeclared profitability threshold is invented.

Candidate stage never directly activates runtime; production research stage still requires explicit operator approval + rollback lineage, and REAL remains separately hard-disabled.

## 11. Research failure isolation

`app/demo_runner.py` records Timing/management/shadow/discovery research evidence best-effort after the governed broker cycle. A research persistence/evaluation failure is surfaced as research degradation; it cannot erase/relabel a completed broker result or trigger a broker retry.

## 12. Persistence / recovery

StateStore records/events are checksummed. Checkpoint includes all namespaces by default, including shadow plans/terminal markers/outcomes, discovery episodes/status/suppressions, candidate transition history and candidate-stage evidence. Restored state never substitutes for fresh broker truth; reconciliation remains mandatory before financial authority resumes.

## 13. Forbidden directions

```text
intelligence/strategy/research/dashboard → MT5Writer       NO
caller/test flag → hard Session permission                 NO
runtime_core → second public full guarded cycle            NO
current equity → silent intraday Risk profile reset        NO
shadow family → live Intent/Risk/Gate                      NO
research/discovery failure → broker retry/runtime rewrite  NO
fault/safety episode → candidate that weakens safety       NO
candidate registry → self-activation                       NO
News failure → hard News kill switch                       NO
ambiguous broker ACK → blind retry                         NO
```

## 14. Synchronization

Any authority/source/test change updates this map, `FILE_AND_TEST_CATALOG.md`, affected audit/status docs, and `scripts/verify_contract_sync.py`. Offline PASS never substitutes for connected Exness DEMO proof.
