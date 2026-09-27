# GoldScalpTrader

Safety-first local MetaTrader 5 gold scalping project.

## Current runtime

`python bot.py` routes by runtime mode:

- `DRY_RUN` → analytical/read-only cycle, zero broker writes.
- `DEMO` → continuous guarded demo trading with local SQLite state.
- `REAL` → disabled in this release.

The connected MT5 account must explicitly report DEMO mode before any DEMO broker write. The runtime blocks on stale/incomplete required data, occupied/unknown exposure, unresolved Intents, controller conflicts, persistence failure, disabled expert trading, failed broker prechecks, or unknown/closed hard Session authority.

Hard broker Session facts come from the scoped local runtime provider file `runtime/session_news.json`. `OPEN` must be positively verified for new exposure; `PRE_CLOSE` blocks new OPENs; provider absence/expiry/scope mismatch fails closed. News remains soft context only.

Verified bot positions use the governed lifecycle:

```text
OPEN → ManagedTrade → HOLD / PROTECT / TRAIL / RUNNER / EXIT
     → MODIFY/CLOSE Intent → broker reconciliation
     → exact exit-deal proof → close receipt + learning queue
```

A bot-magic position without durable ManagedTrade lineage is never silently adopted. A missing known position is not called closed until exit-deal volume proof exists.

## Production strategy routing

GoldScalpTrader evaluates all six family definitions from the same causal intelligence snapshot, then production routes **one structurally qualified family**.

```text
market-first six-family detection
→ qualified structural candidates
→ opposite directions? WAIT / fail closed
→ otherwise structural semantic priority
→ exactly one ACTIVE_EXECUTION routed family
→ remaining families SHADOW_ONLY research
```

Production does **not** select a family by highest score and does **not** use `ACTIVE_STRATEGY_FAMILY` as broker authority. That setting is retained only as optional legacy/research focus compatibility.

Current structural priority:

```text
FAILED_BREAKOUT_REVERSAL
LIQUIDITY_SWEEP_REVERSAL
BREAKOUT_RETEST_CONTINUATION
COMPRESSION_EXPANSION
BREAKOUT_EXPANSION
TREND_PULLBACK_CONTINUATION
```

Scores remain explanatory/research facts.

## Timing Intelligence and governed learning

M5 remains setup/thesis authority; M1 is subordinate entry timing only after a valid M5 Opportunity. Verified timing and management evidence is preserved locally for governed efficiency research. Autonomous research may propose improvements, but cannot change Risk/Gate, promote itself into runtime authority, or gain broker-write authority.

The live DEMO research path records actual learning evidence plus causal SHADOW_ONLY hypothetical plans/outcomes without granting shadow records Risk, Gate, position capacity or broker authority.

Candidate promotion requires immutable stage-specific evidence bound to candidate fingerprint, target stage, dataset/code/config identity, execution realism and artifact hashes. Stage skipping is forbidden. `APPROVAL_REQUIRED → PRODUCTION` still requires explicit operator approval and rollback lineage, and registry promotion still does not directly activate runtime trading.

## Dashboard hierarchy

GoldScalpTrader follows the GoldSwing operator hierarchy and uses the completed GoldSwingTrader dashboard source as the read-only presentation reference:

```text
PRIMARY   = VS Code / terminal live trading floor
SECONDARY = localhost browser visual floor (optional, read only)
```

Primary renderer stack:

```text
96+ columns   → Swing-derived institutional line floor
64–95 columns → narrow stacked floor
render fault  → compact crash-safe fallback
```

The wide primary floor follows the Swing live-dashboard hierarchy: top market/action strip, Market Picture + Trade Setup cards, Current Decision, Trade Plan, Strategy/Setup Board, Risk + Activity + System row, managed-trade view when present, and Learning/Discovery footer. It is presentation-only and consumes the canonical Scalp dashboard DTO; it does not recalculate strategy, routing, Risk, Gate, Session authority or broker actions.

Operational bilingual cues use **English + Roman Urdu**, for example:

```text
WAIT / Intazar
BUY / Kharid
SELL / Farokht
WHY / Wajah
Market Picture / Market Jaiza
Trade Setup / Setup aur Route
Risk & Account / Risk aur Account
```

Urdu script is not used for operational dashboard labels/statuses. The Arabic invocation may remain as decorative masthead text in the secondary browser.

`DASHBOARD_MODE=GUI` means primary terminal **plus** secondary browser. The browser binds to `127.0.0.1`, has no BUY/SELL/MODIFY/CLOSE controls and cannot own trading authority.

The browser floor contains:

- Swing-style masthead, clock and role;
- Symbol / hard market state / Soft Context / live price / spread / M5 countdown;
- Market Analysis / Trend / Session-News / Timing rail;
- completed-candle M1/M5/M15/H1/H4 chart;
- Indicators / Drawings / Settings / Bars presentation-only controls;
- Current Signal / Trade Plan / Blocker-Gate / Multi-Timeframe-Setup rail;
- Risk & Account / one Strategy-Setup Board / Open Managed Trade;
- Execution / Activity / Learning / System / Recent Verified Closes / discipline floor.

Hard Session and Soft Context are displayed separately so `NEW_YORK` context can never be mistaken for verified hard Session OPEN.

The dashboard is fail-visible and market-state independent. CLOSED, UNKNOWN, stale provider data, MT5 failures and governed safety blocks remain visible; trading remains fail-closed.

## REAL / DEMO mode engineering guide

See [`REAL_AND_DEMO_MODE_ARCHITECTURE.md`](REAL_AND_DEMO_MODE_ARCHITECTURE.md) for the as-built mode hierarchy, DEMO account verification, Gate/precheck layers, sole MT5 writer, persistence/reconciliation and connected certification boundary.

## Live DEMO quick start

Keep MetaTrader 5 open and logged into the intended demo account, then:

```powershell
cd "D:\Trading Bot\GoldScalpTrader"
git pull --ff-only
Copy-Item .env.demo.example .env -Force
python bot.py
```

The supplied DEMO profile uses structural production routing. `ACTIVE_STRATEGY_FAMILY` is not required for production. REAL broker execution remains hard-disabled.

`Ctrl+C` stops the local runtime safely. Mutable runtime state stays under `runtime/` and is not published to GitHub.

## Non-negotiable project rules

- Trading runs locally on Windows with MetaTrader 5.
- GitHub is source/history backup only, never runtime authority.
- No runtime Git commit/push/pull.
- REAL execution remains disabled until its future governed release gate.
- Credentials, account numbers, passwords, tokens and `.env` files are never committed.
- One independently risk-bearing Gold position at a time initially.
- No martingale, uncontrolled grid or averaging-down rescue.
- Hard Session, Risk ceilings, Gate, one-writer, persist-before-send and reconciliation safety are non-learnable.

> Automated trading can lose money. Connected DEMO evidence is still required before any future REAL release is considered.
