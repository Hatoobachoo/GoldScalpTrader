# GoldScalpTrader

Safety-first local MetaTrader 5 gold scalping project.

## Current runtime

`python bot.py` routes by runtime mode:

- `DRY_RUN` → analytical/read-only cycle, zero broker writes.
- `DEMO` → continuous guarded demo trading with local SQLite state.
- `REAL` → disabled in this release.

The connected MT5 account must explicitly report DEMO mode before any DEMO broker write. The runtime blocks on stale/incomplete required data, occupied/unknown exposure, unresolved Intents, controller conflicts, persistence failure, disabled expert trading, failed broker prechecks, or unknown/closed hard Session authority.

Hard broker Session facts are now consumed from the scoped local runtime provider file `runtime/session_news.json` (beside the configured state DB). `OPEN` must be positively verified for new exposure; `PRE_CLOSE` blocks new OPENs and preserves the governed flatten thresholds; provider absence/expiry/scope mismatch fails closed. A conservative Saturday floor displays `CLOSED` but never fabricates weekday `OPEN`. News remains soft context only.

Verified bot positions use the governed lifecycle:

```text
OPEN → ManagedTrade → HOLD / PROTECT / TRAIL / RUNNER / EXIT
     → MODIFY/CLOSE Intent → broker reconciliation
     → exact exit-deal proof → close receipt + learning queue
```

A bot-magic position without durable ManagedTrade lineage is never silently adopted. A missing known position is not called closed until exit-deal volume proof is available.

## REAL / DEMO mode engineering guide

For the detailed as-built hierarchy of runtime modes, configuration locks, DEMO account verification, Gate/precheck layers, sole MT5 writer, persistence/reconciliation, connected certification, REAL hard-disable behavior, code locations and current integration boundaries, read:

[`REAL_AND_DEMO_MODE_ARCHITECTURE.md`](REAL_AND_DEMO_MODE_ARCHITECTURE.md)

## Timing Intelligence and governed learning

Timing Intelligence is a first-class subsystem: M5 remains the setup/thesis authority, M1 refines entry timing, and verified timing evidence is preserved locally for governed efficiency research. Autonomous research may propose improvements, but cannot change Risk/Gate, promote itself to live execution, or gain broker authority.

A qualified M5 Opportunity now has durable local Opportunity/Episode identity across repeated WAIT/READY cycles and restart. The same causal terminal episode cannot silently re-arm merely because an in-memory cycle generated a new random ID; only a fresh causal M5 identity may create a new episode. Once the irreversible OPEN send is consumed, the durable Opportunity becomes `TRIGGERED`.

For governed DEMO OPENs, the causal Opportunity/episode, TradePlan, M5 event lineage and TimingDecision profile/ages/chase/extension are frozen into durable OPEN context **before the irreversible broker send**. After verified OPEN reconciliation the same lineage is stored in `ManagedTrade`, then carried through exact verified close into the exactly-once learning queue/StrategyMemory.

The live DEMO presentation paths also write **research-only** management-path evidence and same-market shadow-family counterfactual evidence. This records management action/open-R progression and shadow candidates without granting those research records Risk, Gate, broker-write or automatic promotion authority.

### Efficiency learning measurement

Closed-trade learning distinguishes **provable causal measurements** from hindsight estimates.

When durable evidence exists, the learning path can preserve:

```text
Opportunity first-seen / armed time
first READY timing-decision time
M1 trigger time
actual broker-open time
trigger → entry delay
READY → entry delay
Opportunity → entry delay
M5 event → entry delay
approved-entry-reference drift in R
observed management-path MFE / MAE in R
time to first PROTECT
time to first TRAIL
time to observed Primary Target
time to observed Expansion Target
time to observed MFE
initial monetary R from SymbolSpec economics
after-cost realized R
observed capture efficiency
observed profit giveback
management sample count
```

Important evidence rule:

> `observed_mfe_r`, `observed_mae_r` and `observed_capture_efficiency` are based on durable runtime observation samples. They are **not** silently relabelled as true intrabar MFE/MAE or an ideal hindsight path.

If the necessary runtime evidence is absent, the field remains `None`/UNKNOWN rather than becoming zero or an inferred value. `entry_efficiency` and canonical full-path `capture_efficiency` remain unpopulated unless a separately approved causal definition and sufficient path evidence exist.

This lets research ask useful questions such as “are entries consistently late?”, “does PROTECT happen too early?”, or “how much observed MFE is commonly given back?” without teaching the live system to weaken Risk or execution safety.

Implementation hierarchy, current evidence wiring, autonomous/governed promotion boundaries and remaining learning gaps are documented in:

[`TIMING_INTELLIGENCE_AND_GOVERNED_LEARNING_IMPLEMENTATION.md`](TIMING_INTELLIGENCE_AND_GOVERNED_LEARNING_IMPLEMENTATION.md)

## Approved graphical dashboard

DEMO uses the approved local graphical dashboard by default. It is one-screen/no-scroll and includes a live candlestick chart, M1/M5/M15/H1/H4 buttons, Indicators, Drawings and Settings controls, Detected Setup, Active Test Family, shadow setups, Opportunity/Timing, TradePlan, Risk, hard Session/News-source state, ManagedTrade, Execution and Gate information.

Chart/UI controls are presentation-only. They redraw the cached dashboard snapshot and cannot trigger broker writes. The governed trading cycle advances only on its fixed runtime timer.

## Live DEMO quick start

Keep MetaTrader 5 open and logged into the intended demo account, then:

```powershell
cd "D:\Trading Bot\GoldScalpTrader"
git pull --ff-only
Copy-Item .env.demo.example .env -Force
python bot.py
```

The supplied DEMO profile uses the preserved one-active-family evaluation model. REAL broker execution remains hard-disabled.

`Ctrl+C` stops terminal mode safely; closing the graphical window writes a local runtime checkpoint. Runtime state stays under `runtime/` and is not published to GitHub.

## Non-negotiable project rules

- Trading runs locally on Windows with MetaTrader 5.
- GitHub is source/history backup only, never runtime authority.
- No runtime Git commit/push/pull.
- REAL execution remains disabled until its future governed release gate.
- Credentials, account numbers, passwords, tokens and `.env` files are never committed.
- One independently risk-bearing Gold position at a time initially.
- No martingale, uncontrolled grid or averaging-down rescue.

> Automated trading can lose money. Connected DEMO evidence is still required before any future REAL release is considered.
