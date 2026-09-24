# GoldScalpTrader — Dashboard and UX Contract

**Status:** DRAFT PRE-CHALLENGE OPERATOR CONTRACT
**Version:** 0.1-scalp-truthful-operator
**Authority:** Operator visibility, typed dashboard mapping, primary terminal presentation, session context, verified performance provenance and safe read-only controls.

## 1. Purpose

The primary dashboard should let the operator understand within seconds:

1. is XAUUSDm feed/market state healthy and what are current SELL/BUY prices;
2. which soft session is active;
3. what do H1/M15/M5 structures and core quant facts show;
4. what is the current analytical decision and why;
5. does an Opportunity/TradePlan exist, and where are Entry/SL/Primary/Expansion;
6. which family leads and how BUY/SELL theses compare;
7. what are verified actual DEMO family results when such evidence later exists;
8. what are account/risk/capacity states;
9. did the setup stop upstream or did the central Execution Gate actually evaluate;
10. what is Trade Manager doing for an open managed position;
11. what are learning/discovery/local-backup/recovery states.

The dashboard is presentation—not a second trading engine.

## 2. One-way architecture

```text
market / intelligence / strategy / decision / TradePlan / risk / execution / learning facts
+ durable StateStore/local-backup health
→ app/dashboard.py + app/live_presentation.py
→ typed DashboardData
→ operator/presentation.py truthful read-only normalization
→ terminal-width dispatcher
   64–95 → narrow dashboard
   96+   → wide Rich dashboard
   failure → compact safe fallback
→ primary VS Code/terminal screen

same normalized presentation state
→ atomic graphical snapshot
→ optional localhost graphical dashboard
```

Presentation may explain already-known facts; it may not recalculate permission.

## 3. Display cadence versus decision cadence

Draft target:

```text
Display pulse: nominal 1 second
Governed analytical decision: completed M5 event/cadence unless final timing policy says otherwise
```

The live pulse may refresh:

- PKT clock;
- Bid/Ask;
- spread;
- M5 countdown;
- quote/feed age;
- account display;
- current broker/position facts already owned elsewhere.

It must not rerun families, rebuild TradePlan, resize risk, create Intent or send broker writes.

## 4. Primary versus secondary view

The terminal/VS Code dashboard is primary.

The graphical/browser dashboard is optional, local-only and read-only. Closing/crashing it must not affect trading liveness.

## 5. Always-visible truth

CLOSED, stale, sparse, warming, News outage, reconciliation, upstream plan/risk rejection or zero setup are states—not reasons to hide the dashboard.

Unknown/missing facts display `—`, `UNKNOWN`, `WAITING` or truthful equivalent. Never fabricate zero values or geometry.

## 6. Session and News presentation

Keep distinct:

```text
Soft Session   ASIA / LONDON / NEW YORK / OVERLAP / OFF HOURS
Hard Market    OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
News           CLEAR / BLACKOUT / UNKNOWN/LIMITED / POST_NEWS_WARMUP
```

The renderer does not classify session time independently.

Because GoldScalpTrader's `OPEN + News UNKNOWN` entry policy is not yet frozen, dashboard wording must display actual News UNKNOWN/LIMITED without implying ALLOW or BLOCK unless the owning permission layer has decided it.

News UNKNOWN never displays CLEAR.

## 7. Primary visual hierarchy

Draft wide hierarchy:

```text
HEADER
  🟡 GoldScalpTrader / mode / PRIMARY / PKT clock
  Market / Session / XAUUSDm / SELL / BUY
  Spread / quote age / M5 countdown / Action / News / Gate / Today P&L

MARKET PICTURE
  H1 / M15 / M5 structure
  optional H4 / M1 context when enabled
  EMA20/EMA50 / RSI / ATR / volatility / event freshness

CURRENT DECISION
  BUY thesis / SELL thesis / Opportunity / Entry Timing / coverage
  Lead family / Floor Edge / WHY

TRADE PLAN
  approved Entry Reference / current executable quote separately
  SL / Primary / Expansion / R / cost-room diagnostics / invalidation

STRATEGY PERFORMANCE
  verified actual DEMO samples only

RISK & ACCOUNT | TODAY/ACTIVITY | SYSTEM/EXECUTION

OPEN TRADE when present

LEARNING / DISCOVERY / LOCAL BACKUP footer
```

The exact layout is presentation calibration; meaning/ownership is not.

## 8. Responsive terminal rule

```text
64–95 display cells → stacked narrow renderer
96+ display cells    → Rich wide renderer
```

Every narrow line must fit the requested display-cell width. Do not force a virtual wide canvas into a small VS Code terminal.

Rich/render/import failures fall back to compact read-only rendering and must never terminate the trading process.

## 9. Emoji/colour grammar

Use expressive but meaningful cues, not decoration that obscures truth.

Suggested cues:

| Meaning | Cue |
|---|---|
| Gold/product | 🟡 / 🤖 |
| safety/mode | 🛡️ |
| time | 🕒 / ⏱️ |
| market/session | 🌐 / 🌍 |
| SELL/BUY | 🔴 / 🟢 |
| spread/cost | ↔️ |
| decision | 🎯 |
| entry/stop | ⚡ / 🛑 |
| primary/expansion | 🎯 / 🚀 |
| lead/debate | 👑 / ⚖️ |
| account/risk | 💼 / 🛡️ |
| feed/controller/backup | 🔌 / 🔐 / 💾 |
| system | 🩺 / ⚙️ |
| learning/discovery | 🧬 / 🔬 |

Plain-text fallback preserves semantics.

## 10. Current Decision and Gate truth

Human-facing actions may include:

```text
WAIT
BUY READY
SELL READY
MISSED
ENTRY BLOCKED
MANAGING TRADE
RECONCILING
```

`ENTRY BLOCKED` is a broad runtime result and is **not synonymous** with `ExecutionPermissionGate = BLOCK`.

Truthful mapping:

```text
TradePlan DEGRADED/INVALID
→ Current Blocker: Trade Plan
→ Gate: NOT EVALUATED / WAIT

Risk BLOCK/UNKNOWN before Gate
→ Current Blocker: Risk
→ Gate: NOT EVALUATED / WAIT

actual central Gate BLOCK
→ Current Blocker: Execution Gate
→ Gate: BLOCKED

actual Gate UNKNOWN
→ Gate: CHECKING / UNKNOWN
```

Machine reasons remain traceable, but human wording is concise and truthful.

No fixed R threshold is hard-coded into dashboard copy. If TradePlan says target room/R is poor, presentation describes the owning TradePlan reason/version.

## 11. Market Picture

Show only actual authoritative facts:

- structure per enabled timeframe;
- EMA20/50, RSI, ATR;
- volatility/momentum/extension;
- latest meaningful event + age/freshness;
- spread/feed age;
- session range context.

M1/H4 panels appear only if final architecture enables them.

## 12. Trade Setup / TradePlan

Trade setup displays actual governed TradePlan facts only.

If no plan exists:

```text
Bias: WAIT
No trade plan yet — Entry / SL / targets will appear after a valid setup.
```

A strong desk score alone cannot fabricate Entry/SL/TP.

Show approved entry reference and current executable Bid/Ask separately so the operator can see drift.

## 13. Verified strategy performance

Intended table:

```text
Strategy | Trades | W | L | BE | Win% | Net R | Avg R | Cost | Result
```

Canonical production source is exactly-once verified `MAIN_DEMO`/approved environment evidence from closed ManagedTrades.

Rules:

- signal != trade;
- blocked/rejected != trade;
- open != closed sample;
- replay/shadow/canary do not enter production stats;
- zero verified closes show NO SAMPLE, not fake `0%` performance;
- crown/result label grants no authority.

## 14. Spread / execution-friction presentation

Show known numerical spread whenever available.

A qualitative badge may use the authoritative execution-health/baseline result; the dashboard must not invent thresholds.

Useful facts:

```text
current spread
healthy baseline if known
ratio/status
approved-entry drift
trigger/event age
execution latency diagnostics when available
```

If baseline is missing, say `BASELINE N/A`, not generic UNKNOWN spread.

## 15. Risk & Account

Prioritize:

- balance/equity as appropriate;
- position/capacity;
- proposed actual all-in Risk %/money when a RiskEvaluation exists;
- normalized lot;
- daily loss state/remaining budget;
- loss streak/cooldown;
- external/manual exposure warning.

If no TradePlan/RiskEvaluation exists, show `Risk Standby`, not a misleading risk failure.

## 16. Today / Activity

Actual broker activity counters distinguish:

- Today verified bot Trades;
- total durable verified OPEN lifecycles;
- Bot Realized;
- Account Safety P/L;
- External/manual activity/exposure;
- funding/cash-flow truth where relevant.

Signals and rejections never count as trades.

## 17. Open Trade

When present show:

- direction/ticket/ownership;
- verified Entry;
- live executable price;
- original/current SL;
- Primary/Expansion/Runner objective if real;
- original R/current open risk;
- current R;
- trade age / M5 bars;
- Trade Manager action/reason;
- close/Intent/reconciliation status.

Dashboard grants no MODIFY/CLOSE permission.

## 18. Learning / discovery / local backup

Secondary footer may show:

```text
StrategyMemory health
Discovery health
Champion / Challenger stage
Last local runtime backup
Backup health/path shorthand
Recovery state
```

Never show a research recommendation as active production policy.

## 19. Planned implementation ownership

```text
src/gold_scalp_trader/app/dashboard.py
src/gold_scalp_trader/app/live_presentation.py
src/gold_scalp_trader/operator/presentation.py
src/gold_scalp_trader/operator/narrow_dashboard.py
src/gold_scalp_trader/operator/rich_dashboard.py
src/gold_scalp_trader/operator/compact_dashboard.py
src/gold_scalp_trader/operator/live_dashboard.py
src/gold_scalp_trader/operator/__init__.py
src/gold_scalp_trader/app/loop.py
```

## 20. Planned proof

Tests cover upstream blocker vs actual Gate truth, terminal width bounds, one-second presentation without new decisions, session/news truth, no-plan geometry, verified performance provenance, PKT/M5 countdown, fallback isolation, open-trade mapping and read-only authority.

Connected Windows screenshots remain useful for scanability/emoji/font evidence only.

## 21. Change rule

Any change to visible metric meaning, blocker/Gate wording, hierarchy, session/news labels, performance provenance, width/fallback or operator authority updates this contract and affected tests/docs together.
