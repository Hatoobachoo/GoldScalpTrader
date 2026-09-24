# GoldScalpTrader — Final Build / Replication Prompt

**Status:** DRAFT PRE-CHALLENGE AI IMPLEMENTATION + REPLICATION BRIEF
**Version:** 0.1-full-manual-draft
**Authority:** Whole-project handoff for a capable coding AI/developer with no chat history. This prompt summarizes the canonical manual and never overrides a topic contract.

## 1. Mission

Design, challenge, build, verify, operate or reconstruct **GoldScalpTrader**, a local Exness MT5 Gold scalping system for XAUUSD/XAUUSDm.

It is a governed institutional-style multi-desk scalping floor, not a simple EMA bot and not an HFT system.

Current stage is documentation-first and pre-implementation freeze.

Preserve this intended production path:

```text
one MT5 read boundary
→ immutable MarketSnapshot
→ staged bounded-parallel market intelligence
→ independent scalp strategy families
→ independent BUY / SELL fusion + Red Team
→ persistent Opportunity
→ scalp Entry Timing + event freshness
→ family-aware structural TradePlan
→ independent monetary Risk
→ hard session/news/system/account/controller authorities
→ central Execution Gate
→ durable one-shot Intent
→ sole MT5Writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close
→ exactly-once verified learning
→ persistent StrategyMemory
→ research/discovery/promotion
→ local backup/recovery
```

Do not recreate the old simple scalper, invent hidden shortcuts, convert research into broker authority or claim deterministic tests prove connected broker behaviour/profitability.

## 2. Replication standard

The target is semantic, architectural and behavioural identity with the **frozen GoldScalpTrader canonical manual**, not byte-for-byte imitation of GoldSwingTraderAI.

Replication bundle:

1. complete current `Documents/` tree;
2. this `FINAL_BUILD_PROMPT.md`;
3. `60-engineering/FILE_AND_TEST_CATALOG.md`;
4. current tests/evidence when they exist;
5. current source as implementation evidence, never undocumented authority;
6. verified local recovery artifacts where lifecycle continuation is required.

A rebuilding AI must preserve module ownership, typed boundaries, chronology, persistence namespaces, failure modes, safety decisions and operator semantics.

## 3. Authority order

When behaviour conflicts:

1. `00-foundation/SYSTEM_CONTRACT.md`;
2. authoritative topic contract;
3. `90-governance/DESIGN_DECISIONS.md`;
4. `90-governance/OPEN_QUESTIONS.md`;
5. `ARCHITECTURE.md` / `TRADING_FLOOR_ARCHITECTURE.md`;
6. `60-engineering/CODING_STANDARD.md`;
7. `90-governance/DOCUMENTATION_STANDARD.md`;
8. `MODULE_STRUCTURE.md` / `FILE_AND_TEST_CATALOG.md`;
9. operator/testing/recovery guides;
10. this prompt.

`Documents/` is the only active manual. Chat history and GoldSwingTraderAI reference text do not override current scalp topic contracts.

If canonical documents conflict, stop affected implementation and repair the graph before coding.

## 4. Required project loop

For every material change:

1. identify behavioural authority and single source owner;
2. inspect upstream/downstream contracts, source/tests/persistence/current evidence;
3. define typed inputs/outputs, chronology, scope/freshness/failure behaviour;
4. separate analytical concurrency from ordered authority;
5. implement smallest deterministic change;
6. add positive, negative, UNKNOWN/stale/corrupt, chronology, restart/idempotency tests where applicable;
7. synchronize full affected `Documents/` graph;
8. run exact local verification on current revision;
9. classify deterministic, replay, connected, calibration and external evidence separately;
10. report exact revision and next dependency.

Dashboard labels, test fakes or config switches may never hide a design/safety contradiction.

## 5. Current product/timeframe draft

Current **pre-challenge baseline**, not frozen truth:

- Platform/broker target: local Windows + Exness MT5.
- Primary symbol: `XAUUSDm`; explicit aliases such as `XAUUSD` only through configured resolution.
- H1: broad regime/important structure.
- M15: opportunity/location/path/session context.
- M5: primary scalp setup, timing and local management.
- H4: optional major context.
- M1: diagnostic baseline; Audit 1 must decide whether it gains explicit timing authority.
- quote/tick: current executable condition, not retroactive structural authority.
- completed candles own bar-based structural proof.
- one normalized immutable MarketSnapshot is shared per analytical cycle.

## 6. Trading floor draft

Starting family decomposition:

1. Trend Pullback Continuation
2. Breakout Expansion
3. Breakout Retest Continuation
4. Liquidity Sweep Reversal
5. Failed Breakout Reversal
6. Compression Expansion

This is the starting reference decomposition, not frozen merely by inheritance.

Families evaluate independently. BUY and SELL are independent theses. No filter-soup/unanimity requirement. Red-Team conflict remains visible.

Bounded analytical concurrency is permitted only with immutable inputs, canonical result order and one-worker semantic parity.

> Parallel analysis, serial authority.

TradePlan → Risk → hard permission → Gate → Intent → writer → reconciliation remains ordered.

## 7. Opportunity / timing / freshness

Opportunity and entry timing are separate.

Draft lifecycle:

```text
DISCOVERED → ARMED → WAITING / READY
→ TRIGGERED after governed broker lifecycle
→ MISSED if efficient window passes
→ INVALIDATED if thesis fails
```

A terminal/MISSED Opportunity does not reset on the next polling cycle. Re-arm requires a genuinely fresh causal event plus surviving thesis.

Timing considers event age, distance travelled since trigger, M5 extension/momentum, remaining target room, current spread/cost context and approved-entry drift.

Exact thresholds remain challenge/calibration items.

## 8. TradePlan

TradePlan exists before monetary Risk.

Keep separate:

```text
Signal Price
Approved Entry Reference
fresh Executable Quote
Actual Fill
```

Family-specific invalidation may prefer exact proven M5 event/retest boundaries only when the event/candle lineage is causal and on the correct side of entry. Otherwise use conservative structural fallback.

Never invent a tight level to improve R.

Objectives are:

```text
Immediate Obstacle
Primary Scalp Target
optional Expansion
exceptional Runner when fresh continuation supports it
```

Original R is immutable after verified fill/initial structural stop.

**Do not hard-code GoldSwingTraderAI's 1.20R floor as scalp truth.** Final structural R and cost-adjusted room policy must be decided/challenged/calibrated in GoldScalpTrader.

## 9. Monetary Risk

Risk is independent from strategy score.

Preserve broker-aware sizing:

```text
structural TradePlan
→ theoretical volume
→ broker min/step/max normalization
→ actual all-in risk at executable volume
→ margin/exposure/risk-day checks
→ PASS / BLOCK / UNKNOWN
```

If raw volume is below minimum 0.01, evaluate the real minimum-lot risk. Do not tighten structural SL merely to fit a small account.

Hard principles:

- no martingale;
- no uncontrolled grid;
- no averaging-down rescue;
- one independently risk-bearing Gold position per scope in initial V1;
- unknown financial/exposure truth fails closed;
- manual reset disabled by default.

Exact SMALL/MEDIUM/NORMAL boundaries, risk bands, hard ceilings, daily-loss limits, cooldown and optional aggressive mode are **not frozen by reference inheritance**.

The provisional old scaffold's 0.50% is not the final policy merely because it exists.

## 10. Session / News draft

Session is hard broker-market authority. News provider truth remains separately typed.

Current fixed principles:

```text
known Market CLOSED / PRE_CLOSE / WARMUP → no new entry
Session UNKNOWN                          → fail closed
known high-impact News BLACKOUT          → hard new-entry block
News UNKNOWN                             → never relabel CLEAR
```

The final `Market OPEN + News UNKNOWN` new-entry policy is a FIX-BEFORE-BUILD decision for the scalper. Do not silently inherit Swing's adaptive PASS.

Exact news windows, pre-close cutoffs and reopen clean-bar counts remain calibration/external items until frozen.

## 11. Execution safety

Current development is DRY_RUN first.

When controlled DEMO writer phase is later implemented:

```text
analytical ENTER
→ TradePlan READY
→ Risk PASS
→ hard authorities/fresh execution checks
→ central Gate ALLOW
→ persist APPROVED Intent
→ fresh native broker permission/order checks
→ persist SUBMITTING before irreversible call
→ exactly one writer call
→ classify acknowledgement
→ broker reconciliation
```

`MT5Writer` is the sole irreversible boundary.

Ambiguous acknowledgement never gets a blind retry.

Controller holder/epoch must be fresh for the intended account/symbol scope.

Unknown manual/foreign positions are never adopted.

REAL trading requires a separate explicit governance decision; it cannot be enabled by a casual hidden flag.

## 12. Scalp execution realism

Execution/research must treat these as first-class:

- quote age;
- event/trigger age;
- spread relative to target/stop/healthy context;
- approved-entry drift;
- adverse slippage;
- commission/fees where known;
- analysis/check/send/reconcile latency diagnostics;
- minimum-lot affordability.

Do not claim HFT/zero latency.

If the trigger is stale, rebuild/wait/block rather than sending late.

## 13. Trade Manager

Actions:

```text
HOLD | PROTECT | TRAIL | RUNNER | EXIT
```

Potential time/efficiency exit is first-class for scalping so a failed short-duration thesis does not silently become a swing.

Protection/trailing follows earned causal structure and never intentionally widens approved risk.

Runner is exceptional, requires fresh continuation/new objective and is not default scalp behaviour.

Exact management thresholds remain calibration pending.

## 14. ManagedTrade / verified close

Unknown external positions are never adopted.

If an already-known ManagedTrade disappears:

1. unresolved Intent reconciliation takes precedence;
2. require exact known position-ticket lineage;
3. require official exit role and complete original exit volume;
4. partial/ambiguous evidence remains RECONCILING;
5. exact bot SL/TP or exact known manual close may complete lifecycle;
6. close origin remains BOT/EXTERNAL/MIXED.

Crash-safe close order:

```text
closed_trade_learning_queue
→ managed_trade_closure_receipt
→ clear active ManagedTrade
→ retire matching TradePlan/Opportunity safely
→ exactly-once learning later
→ remove queue only after durable learning save
```

## 15. Learning / research / AI

Verified OPEN freezes family/policy/direction/original R/Entry Reference/actual fill/ticket/lineage.

Learning may observe, remember, research and propose. It cannot alter hard Risk/session/controller/reconciliation or call writer.

Replay is chronological/no-lookahead and must declare transaction-cost assumptions.

Scalp research emphasizes:

- Net/Avg R and Profit Factor;
- drawdown/streaks;
- MAE/MFE;
- Entry/Capture Efficiency;
- hold duration;
- spread/slippage/commission burden;
- latency;
- Opportunity Recall/missed moves;
- capacity-admitted trades;
- family/session/regime attribution;
- small-account min-lot blocks.

Autonomous invention creates bounded declarative candidates only.

Candidate path:

```text
proposal
→ validation
→ semantic lock
→ one-shot holdout
→ stress
→ Shadow
→ governed DEMO Canary
→ PROMOTION_READY
→ explicit approval
```

Candidate cannot self-promote.

## 16. Persistence and local backup

GoldScalpTrader intentionally does **not** copy the reference runtime shutdown Git publication feature.

Runtime durability:

```text
strict typed SQLite/StateStore candidate
→ rolling local checkpoints
→ graceful-shutdown final verified LOCAL checkpoint
→ portable recovery package when requested
```

Source durability:

```text
normal local Git clone + .git
→ optional deliberate local Git bundle at development/release milestone
```

Conceptual external backup root:

```text
C:\GoldScalpTrader_Backups\
```

Backups/recovery packages exclude real `.env`, broker passwords, GitHub PATs/tokens, private keys and credential-bearing URLs.

Restore goes into a **new** DB/path, then fresh broker reconciliation/controller authority is required.

There is no:

```text
shutdown git add
shutdown commit
shutdown push
runtime GitHub credential dependency
```

## 17. Multi-machine scope

Initial V1:

```text
one active PRIMARY per account/symbol scope
sequential same-scope handoff only
different independent scopes may run separately
```

Git/Drive/Dropbox sync is not controller fencing.

True simultaneous same-scope failover is deferred until shared atomic fencing plus globally ordered lifecycle/learning state exists and is certified.

## 18. Primary terminal dashboard

Primary operator console is presentation only.

It should surface:

- Market/Session/News;
- XAU Bid/Ask/spread/quote age/M5 countdown/PKT clock;
- H1/M15/M5 analysis and enabled optional context;
- BUY/SELL/Floor Edge/leading family;
- Opportunity/timing/event freshness;
- actual TradePlan geometry only when it exists;
- Risk/account/activity;
- true Current Blocker and actual Gate state;
- ManagedTrade state;
- verified actual performance only;
- learning/discovery/local-backup health.

`ENTRY_BLOCKED` must never automatically render as `Gate BLOCKED`.

## 19. Secondary graphical dashboard

Optional local browser dashboard:

```text
PRIMARY authoritative DTO
→ atomic read-only snapshot
→ localhost-only server
→ browser monitor
```

It has no MT5 writer, strategy/Risk/controller authority or trade controls. Failure cannot stop the PRIMARY.

## 20. Documentation and verification

`Documents/` stays synchronized with source/tests through the affected-graph rule.

Expected local verification after implementation includes equivalent to:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

No GitHub Actions requirement.

Report separately:

- documentation/frozen-design proof;
- deterministic software proof;
- replay/research/calibration evidence;
- connected MT5 read proof;
- controlled DEMO lifecycle proof;
- actual learning proof;
- restart/reconciliation proof;
- local recovery-package/fresh-machine proof.

Never reuse old test counts/revisions as current evidence.

## 21. Current completion boundary

At the time of this draft:

```text
complete canonical Documents draft → being finalized
fresh-zero Audit 1                → next phase
implementation from frozen manual → not started
connected broker proof            → not run
profitability claim                → none
```

GoldSwingTraderAI's historical audits are design lessons, not GoldScalpTrader evidence.

The next correct action after the 64-file inventory is verified is to **challenge the entire design from zero**, synchronize findings and freeze accepted contracts—only then implement.