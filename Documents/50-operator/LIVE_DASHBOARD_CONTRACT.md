# GoldScalpTrader — Live Dashboard Contract

**Status:** DRAFT PRE-CHALLENGE CANONICAL EXTENSION
**Version:** 0.1-responsive-truthful-scalp-ux
**Authority:** Primary terminal presentation, nominal one-second read-only liveness, authoritative session context, verified strategy-performance visibility, terminal-width behaviour and presentation crash isolation.

## 1. Relationship to main dashboard contract

This document extends `DASHBOARD_AND_UX.md` and creates no trading authority.

The dashboard consumes facts already owned by runtime, market data, intelligence, strategy, TradePlan, risk, execution, learning and persistence/local-backup modules.

## 2. Intended implementation owners

```text
operator/presentation.py      read-only blocker/Gate normalization and human wording
operator/narrow_dashboard.py  64–95 cell stacked primary renderer
operator/rich_dashboard.py    96+ cell wide primary renderer
operator/compact_dashboard.py dependency-light fallback
operator/live_dashboard.py    shared DTO/helpers/emoji vocabulary
operator/__init__.py          width dispatcher + optional graphical publication
app/live_presentation.py      quote/account enrichment + performance aggregation
app/loop.py                   presentation pulse separate from trading cadence
```

The terminal is the primary operational dashboard. Browser dashboard is secondary.

## 3. Width and fallback

```text
64–95 display cells → narrow stacked renderer
96+ cells           → wide Rich renderer
Rich/render failure → compact fallback
```

A renderer must respect real display width. Presentation failure cannot terminate the trading process.

## 4. Core timing rule

```text
Presentation pulse: nominal 1 second
Trading decision: governed completed-M5/event cadence
```

The pulse may update PKT clock, live Bid/Ask, spread, M5 countdown, quote age and read-only account facts.

It may not rerun strategy families, alter fusion, create Opportunity, rebuild TradePlan, resize Risk, change Gate, create Intent or call broker writes.

## 5. Session / News display

The header surfaces already-computed soft session context and separate hard market state.

The renderer never independently decides session time.

News labels remain truthful:

```text
CLEAR
BLACKOUT
UNKNOWN / LIMITED
POST-NEWS WARMUP
```

Because the scalp `OPEN + News UNKNOWN` policy is not frozen yet, presentation reflects the owning permission result rather than inheriting Swing's adaptive-pass assumption.

UNKNOWN is never rendered CLEAR.

## 6. Draft terminal hierarchy

Wide screen:

```text
╔════ 🟡 GoldScalpTrader • SCALP TRADING FLOOR • MODE • PRIMARY ════╗
║ Market • Session • XAUUSDm • SELL • BUY • Spread • Quote Age      ║
║ M5 countdown • Action • News • Gate • Today P/L • PKT clock       ║
╚═════════════════════════════════════════════════════════════════════╝

🌐 MARKET PICTURE        📐 TRADE SETUP
🎯 CURRENT DECISION
📐 TRADE PLAN
🏆 VERIFIED STRATEGY PERFORMANCE

🛡️ RISK & ACCOUNT   📊 TODAY   ⚙️ SYSTEM / EXECUTION
📈 OPEN TRADE — only when present
🧬 LEARNING / 🔬 DISCOVERY / 💾 LOCAL BACKUP — compact footer
```

Narrow layout preserves meaning in stacked form, not exact geometry.

## 7. Strategy visibility

All production families remain active internally.

The primary screen may omit noisy full live family rows and instead prioritize:

- BUY thesis;
- SELL thesis;
- Opportunity state;
- Entry Timing result;
- coverage;
- leading family;
- Floor Edge/Red-Team conflict;
- concise reason.

Verified per-family closed-trade performance answers a separate historical question and may remain visible.

## 8. Verified strategy performance

Canonical production performance comes only from exactly-once verified actual closed ManagedTrades in the approved production/DEMO environment.

Rules:

```text
signal != trade
blocked entry != trade
open position != closed sample
replay/shadow/canary != production performance
zero samples → NO SAMPLE, not fake 0.0%
```

Potential table:

```text
Strategy | Trades | W | L | BE | Win% | Net R | Avg R | Result
```

Any cost metric shown must come from verified learning records.

## 9. Current decision / blocker / Gate truth

Possible operator actions:

```text
WAIT
BUY READY
SELL READY
MISSED
ENTRY BLOCKED
MANAGING TRADE
RECONCILING
```

Truth table:

```text
TradePlan DEGRADED/INVALID
→ blocker TradePlan
→ Gate WAIT / NOT EVALUATED

Risk rejected before Gate
→ blocker Risk
→ Gate WAIT / NOT EVALUATED

actual central Gate BLOCK
→ blocker Execution Gate
→ Gate BLOCKED

actual central Gate UNKNOWN
→ Gate CHECKING / UNKNOWN
```

`ENTRY_BLOCKED` is never automatically mapped to `Gate BLOCKED`.

No dashboard sentence hard-codes a 1.20R scalp floor; it surfaces the TradePlan's actual versioned reason/policy.

## 10. Trade setup truth

Trade Setup displays only actual governed TradePlan geometry.

If no plan exists:

```text
Bias WAIT
🛡 Structure  Waiting for valid setup
No trade plan yet — Entry / SL / targets will appear after a valid setup.
```

A high score cannot fabricate geometry.

If a plan exists but timing waits, wording makes clear that the plan exists and fresh trigger confirmation is pending.

## 11. Scalping-specific live facts

Where authoritative, show:

- event/trigger age;
- M5 freshness state;
- approved Entry Reference vs current executable quote;
- spread and baseline/status;
- remaining target room/cost context;
- decision/execution latency diagnostics;
- Opportunity lifecycle/re-arm state;
- open-trade age/bars.

These displays do not create thresholds.

## 12. Risk/account presentation

Prioritize:

- balance/equity as useful;
- current position/capacity;
- proposed actual all-in risk and lot only when RiskEvaluation exists;
- daily loss state/remaining budget;
- loss streak/cooldown;
- external/manual exposure.

No plan/risk proposal → `Risk Standby`, not false failure.

## 13. Footer noise rule

Learning, discovery, local backup, engine and News/provider states remain visible but secondary.

Do not repeat the exact same decision/execution reason in multiple prime panels. Detailed machine diagnostics belong in logs/health view.

## 14. Open Trade

Show only verified facts:

- direction/ticket;
- actual Entry;
- current price;
- original/current SL;
- actual broker target plus analytical Primary/Expansion/Runner where present;
- original/current R/open risk;
- trade age/bars;
- Trade Manager action/reason;
- Intent/reconciliation/close state.

Dashboard never grants MODIFY/CLOSE authority.

## 15. Secondary graphical boundary

The graphical dashboard consumes a read-only atomic snapshot with the same normalized blocker/Gate meaning.

It cannot import/own MT5, strategy, risk, controller, Intent or management mutation. Browser failure must not impact PRIMARY.

## 16. Planned proof

Tests should cover:

- blocker-vs-Gate truth;
- narrow width limits;
- live pulse without new decision;
- session/news provenance;
- no-plan geometry;
- human wording;
- Rich fallback;
- verified performance;
- PKT/M5 countdown;
- read-only dashboard authority;
- graphical snapshot consistency.

Connected screenshots prove scanability only, not trading correctness.

## 17. Pre-challenge questions

- final terminal hierarchy and bilingual English/Urdu wording extent;
- which M1/H4 facts merit primary screen space;
- strategy-performance columns;
- spread/latency visual prominence;
- compact vs detailed operator modes without adding user-controlled trading logic;
- final emoji density.
