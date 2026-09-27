# GoldScalpTrader — Graphical Dashboard

**Status:** IMPLEMENTED SECONDARY LOCAL VISUAL FLOOR — SWING-STYLE / READ ONLY  
**Version:** 4.0-swing-parity-browser-floor  
**Authority:** Secondary graphical composition, chart interaction, snapshot presentation, stale/offline visibility, and local-only read-only behavior.

## 1. Role and authority

```text
runtime facts → PRIMARY terminal dashboard
             ↘ atomic read-only snapshot → SECONDARY localhost browser
```

The browser may be visually richer, but it is not a second trading engine. It owns no Risk, Gate, Opportunity, strategy-selection, promotion or broker-write authority.

It binds to `127.0.0.1`, serves read-only GET/HEAD presentation, rejects state-changing HTTP methods, and may be closed/crashed without affecting the bot or primary terminal floor.

## 2. Implemented visual composition

The visual floor deliberately follows the completed GoldSwingTrader institutional layout family while adapting content to Scalp:

```text
ROBOT / GoldScalpTraderAI        Arabic invocation        Motto / PKT / DEMO role
SYMBOL | MARKET | LIVE PRICE / BID / ASK / SPREAD | M5 COUNTDOWN | BOT STATUS

MARKET ANALYSIS   |                 COMPLETED-CANDLE CHART                 | CURRENT SIGNAL
TREND DIRECTION   |       M1 M5 M15 H1 H4 / Indicators / Drawings / Bars | TRADE PLAN
SESSION / NEWS    |                                                        | BLOCKER / GATE
TIMING INTELLIGENCE                                                       | 1 ACTIVE + 5 SHADOW

RISK & ACCOUNT | STRATEGY RESEARCH BOARD | OPEN / MANAGED TRADE
TODAY / ACTIVITY | LEARNING | DISCOVERY | EXECUTION | SYSTEM | MOTIVATION
```

Visual language:

- dark navy/black background;
- cyan/teal structure and live-data accents;
- gold identity/plan emphasis;
- green/red directional state;
- emojis plus English/Urdu operator cues;
- Arabic invocation retained as presentation-only masthead text;
- dense one-screen desktop floor.

## 3. Chart

Presentation-only chart controls:

```text
M1 | M5 | M15 | H1 | H4
Indicators ON/OFF
Drawings ON/OFF
Bars 30 / 60 / 120
```

The chart renders completed candles from the atomic snapshot. No forming candle is invented. Selecting a tab or visual control cannot alter strategy cadence or create a trade.

Trading roles remain:

```text
M5  primary setup/thesis/Opportunity
M1  subordinate timing refinement
M15 path/location
H1  broad regime
H4  major context
```

## 4. Strategy isolation

The browser carries the six-family research board but keeps live authority explicit:

```text
1 family  ACTIVE_EXECUTION
5 families SHADOW_ONLY
```

Each row may show qualification, direction, score and coverage where those facts exist. Missing values remain unknown/blank rather than fabricated. Shadow results are research facts, never broker-realized P/L.

## 5. Trade / Risk / blocker truth

Trade Plan, Risk, Gate, ManagedTrade and execution fields come from normalized runtime facts. The browser does not recompute them.

No actual plan → `WAITING` / `—`.
No open trade → explicit flat-state card.
Missing account/Risk fact → `—` / `UNKNOWN` / `NOT EVALUATED`.

Current blocker and central Gate remain visually distinct.

## 6. Liveness

```text
fresh snapshot  → normal floor
stale snapshot  → BOT OFFLINE / SNAPSHOT STALE + dimmed retained facts
missing snapshot→ visible waiting state
runtime failure → DEGRADED/WAIT snapshot when available
market CLOSED   → full floor remains visible
```

Snapshot staleness never changes the underlying market state to fake OPEN/CLOSED.

## 7. Security

Hard requirements:

- localhost only;
- atomic snapshot publication;
- secret scan before publication;
- no credentials in browser state;
- no public/cloud dashboard dependency;
- no broker-mutating endpoint;
- **no BUY/SELL/MODIFY/CLOSE controls**;
- browser availability never determines trading authority.

## 8. Launch semantics

`DASHBOARD_MODE=GUI` means:

> **Run the normal primary terminal trading floor and additionally start this secondary localhost visual floor.**

It never means browser-primary runtime.

## 9. Final invariant

> **The browser is a Swing-style secondary projection of the same Scalp runtime facts. It improves visibility only; it cannot create, change, retry, approve or execute a trade.**
