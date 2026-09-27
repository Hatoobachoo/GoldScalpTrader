# GoldScalpTrader — Live Dashboard Contract

**Status:** IMPLEMENTED — PRIMARY TERMINAL LIVE FLOOR / SECONDARY GRAPHICAL PROJECTION  
**Version:** 4.0-live-presentation  
**Authority:** Live presentation cadence, dashboard liveness, bilingual/emoji hierarchy, failure visibility, and authority separation.

## 1. Primary surface

The VS Code/terminal dashboard is the primary live operator surface.

Renderer order:

```text
96+ columns  → Rich institutional floor
64–95        → narrow stacked floor
render fault → compact crash-safe fallback
```

All renderers remain presentation-only and preserve English/Urdu safety cues plus emoji markers when supported.

The browser is secondary and localhost-only.

## 2. Liveness contract

The dashboard remains visible through:

```text
startup/readiness
market OPEN
PRE_CLOSE
CLOSED
Session UNKNOWN
no valid setup
Timing WAIT/MISSED
TradePlan unavailable
Risk/Gate block
reconciliation wait
MT5/data/provider fault
runtime exception
secondary graphical failure
```

Market closure is not an application-exit signal.

## 3. Fail-visible / fail-closed

```text
presentation → fail visible
trading      → fail closed
```

A failed runtime cycle cannot produce an unverified broker write. The terminal frame shows the exact failure and continues safe polling where allowed. Configuration/startup failure renders a complete safety frame rather than disappearing behind a traceback.

## 4. Same-facts rule

Both surfaces consume normalized `DashboardData`/snapshot facts. Presentation never independently creates:

- Setup;
- Opportunity;
- Timing decision;
- TradePlan;
- monetary Risk;
- central Gate permission;
- Intent;
- management action;
- candidate production authority.

Missing facts stay missing.

## 5. Primary information hierarchy

The wide primary frame exposes, where available:

```text
Market / Session / Symbol / SELL / BUY
Spread / M5 countdown / Action / News / Gate
H4/H1/M15/M5 structure + EMA20/EMA50/RSI/ATR
Detected Setup + Active Family + M1 Timing
BUY/SELL desk scores + coverage + exact reason
TradePlan
1 ACTIVE + 5 SHADOW Strategy Isolation board
Risk & Account
Today / Activity
System / Execution
ManagedTrade
Learning / Discovery / Backup
```

The narrow/fallback floors retain the same critical truths in stacked form.

## 6. Secondary browser hierarchy

The graphical floor adds only presentation richness:

- robot/brand masthead;
- Arabic invocation and English/Urdu wording;
- PKT clock and DEMO/SECONDARY role;
- market/live-price/countdown strip;
- completed-candle chart with M1/M5/M15/H1/H4 tabs;
- Indicators / Drawings / Bars controls;
- Timing Intelligence;
- Signal/Decision;
- Trade Plan;
- Blocker/Gate;
- six-family strategy board;
- Risk/Account and ManagedTrade;
- Activity/Learning/Discovery/Execution/System;
- stale/offline overlay.

It explicitly has no BUY/SELL/MODIFY/CLOSE controls.

## 7. `DASHBOARD_MODE`

```text
TERMINAL → primary terminal only
GUI      → primary terminal + secondary localhost browser
```

GUI never replaces the primary runtime path.

## 8. Presentation cadence

Fast visual refresh may update already-owned clock/quote/countdown/cached facts. It may not rerun strategy, Opportunity, Risk, Gate or broker execution simply because the screen refreshed.

The completed M5 decision cadence remains independent from visual refresh cadence.

## 9. Failure examples

### MT5 unavailable

```text
Bot Status    DEGRADED
Action        WAIT
Market        UNKNOWN
Reason        exact MT5 initialize/login/read error
Execution     NO BROKER ACTION FROM FAILED CYCLE
System        DASHBOARD ALIVE • TRADING FAIL-CLOSED
```

### Market CLOSED

```text
Market        CLOSED
Action        WAIT / runtime-owned state
Dashboard     full terminal + browser floor remains visible
```

### Browser unavailable

```text
Primary       ACTIVE
Graphical     SECONDARY UNAVAILABLE
Trading       unchanged
```

## 10. No fabricated truth

Unavailable account/Risk/plan/performance/strategy facts must remain `—`, `UNKNOWN`, `WAIT`, or `NOT EVALUATED`. Presentation must never turn absence into zero just to fill a card.

## 11. Final invariant

> **The operator can always see what the bot knows, what it does not know, why it is waiting or blocked, and whether presentation is degraded. Both dashboards reveal the same authority truth; neither dashboard owns trading authority.**
