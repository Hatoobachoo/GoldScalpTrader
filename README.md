# GoldScalpTrader

Safety-first local MetaTrader 5 gold scalping project.

## Current runtime

`python bot.py` routes by runtime mode:

- `DRY_RUN` → analytical/read-only cycle, zero broker writes.
- `DEMO` → continuous guarded demo trading with local SQLite state.
- `REAL` → disabled in this release.

The connected MT5 account must explicitly report DEMO mode before any DEMO broker write. The runtime blocks on stale/incomplete required data, occupied/unknown exposure, unresolved Intents, controller conflicts, persistence failure, disabled expert trading, or failed broker prechecks.

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

Implementation hierarchy, current evidence wiring, autonomous/governed promotion boundaries and remaining learning gaps are documented in:

[`TIMING_INTELLIGENCE_AND_GOVERNED_LEARNING_IMPLEMENTATION.md`](TIMING_INTELLIGENCE_AND_GOVERNED_LEARNING_IMPLEMENTATION.md)

## Approved graphical dashboard

DEMO uses the approved local graphical dashboard by default. It is one-screen/no-scroll and includes a live candlestick chart, M1/M5/M15/H1/H4 buttons, Indicators, Drawings and Settings controls, Detected Setup, Active Test Family, shadow setups, TradePlan, Risk, ManagedTrade, Execution and Gate information.

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
