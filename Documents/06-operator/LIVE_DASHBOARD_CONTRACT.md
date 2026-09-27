# GoldScalpTrader — Live Dashboard Contract

**Status:** IMPLEMENTED — PRIMARY TERMINAL LIVE FLOOR / SECONDARY GRAPHICAL PROJECTION  
**Version:** 4.1-live-presentation-roman-urdu  
**Authority:** Live presentation cadence, dashboard liveness, English + Roman Urdu hierarchy, failure visibility, and authority separation.

## 1. Primary surface

The VS Code/terminal dashboard is primary.

```text
96+ columns  → Rich institutional floor
64–95        → narrow stacked floor
render fault → compact crash-safe fallback
```

All renderers are presentation-only. Operational bilingual cues use English + Roman Urdu (`WAIT / Intazar`, `WHY / Wajah`, `Trade Plan / Mansuba`). The browser is secondary and localhost-only.

## 2. Liveness

The dashboard remains visible through startup, OPEN, PRE_CLOSE, CLOSED, Session UNKNOWN, no setup, Timing WAIT/MISSED, unavailable TradePlan, Risk/Gate block, reconciliation, MT5/provider faults, runtime exceptions and secondary browser failure.

> **Presentation fails visible; trading fails closed.**

## 3. Same-facts rule

Both surfaces consume normalized presentation facts. Presentation never independently creates Setup, routed family, Opportunity, Timing, TradePlan, Risk, Gate, Intent, management action or candidate production authority. Missing facts remain missing.

## 4. Primary hierarchy

```text
IDENTITY HEADER
M5 thesis / M1 timing / structural routing / governed execution
MARKET STRIP: hard market state / Soft Context / prices / spread / M5 countdown / action / Gate
MARKET PICTURE | TRADE SETUP / ROUTE
CURRENT DECISION / Maujooda Faisla
TRADE PLAN / Mansuba
STRATEGY / SETUP BOARD
RISK & ACCOUNT | TODAY / ACTIVITY | SYSTEM / EXECUTION
OPEN / MANAGED TRADE
LEARNING / DISCOVERY
```

The identity header and market strip are separate to avoid crowding.

## 5. Routing truth

The dashboard shows the **structurally routed** production family, not a manually configured active family. Scores do not select broker authority. If qualified directions conflict, the dashboard shows WAIT/no routed family.

## 6. Session truth

`Hard Session` is authority. `Soft Context` is descriptive only. A contextual `NEW_YORK` label may not be displayed as if it proves hard Session OPEN.

## 7. Secondary browser

The graphical floor adds presentation richness only:

- robot/brand masthead, invocation, Roman Urdu discipline line, PKT clock;
- market/live-price/countdown strip;
- completed-candle M1/M5/M15/H1/H4 chart;
- Indicators / Drawings / Settings / Bars local controls;
- Market Analysis / Trend / Session-News / Timing;
- Signal/Decision / Trade Plan / Blocker-Gate / Multi-Timeframe-Setup;
- one Strategy/Setup board;
- Risk/Account / ManagedTrade;
- Execution / Activity / Learning / System / Recent Verified Closes / discipline tile;
- stale/offline overlay.

It has no BUY/SELL/MODIFY/CLOSE controls.

## 8. `DASHBOARD_MODE`

```text
TERMINAL → primary terminal only
GUI      → primary terminal + secondary localhost browser
```

## 9. Cadence

Fast visual refresh may update already-owned quote/clock/countdown/cached facts. It may not rerun strategy routing, Opportunity, Risk, Gate or broker execution. M5 decision cadence remains independent.

## 10. No fabricated truth

Unavailable account/Risk/plan/performance/strategy facts stay `—`, `UNKNOWN`, `WAIT` or `NOT EVALUATED`.

## 11. Final invariant

> **The operator can always see what the bot knows, what it does not know, why it is waiting/blocked and whether presentation is degraded. Both dashboards reveal the same authority truth; neither dashboard owns trading authority.**
