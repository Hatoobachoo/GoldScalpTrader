# GoldScalpTrader — Graphical Dashboard

**Status:** IMPLEMENTED SECONDARY LOCAL VISUAL FLOOR — SWING-STYLE / READ ONLY  
**Version:** 4.1-swing-parity-browser-floor  
**Authority:** Secondary graphical composition, chart interaction, snapshot presentation, stale/offline visibility, and localhost-only read-only behavior.

## 1. Role and authority

```text
runtime facts → PRIMARY terminal dashboard
             ↘ atomic read-only snapshot → SECONDARY localhost browser
```

The browser may be visually richer, but it is not a trading engine. It owns no Risk, Gate, Opportunity, family-routing, promotion or broker-write authority. It binds to `127.0.0.1`; closing it cannot stop trading or the primary terminal floor.

## 2. Implemented Swing-style composition

```text
ROBOT / GoldScalpTraderAI       Arabic invocation       Motto / PKT / DEMO role
SYMBOL | MARKET + Soft Context | LIVE PRICE / BID / ASK / SPREAD | M5 COUNTDOWN | BOT STATUS

MARKET ANALYSIS |              COMPLETED-CANDLE CHART               | CURRENT SIGNAL
TREND DIRECTION | M1 M5 M15 H1 H4 / Indicators / Drawings / Settings| TRADE PLAN
SESSION / NEWS  |                                                     | BLOCKER / GATE
TIMING INTEL    |                                                     | MULTI-TIMEFRAME / SETUP

RISK & ACCOUNT | STRATEGY / SETUP BOARD | OPEN / MANAGED TRADE
EXECUTION | ACTIVITY | LEARNING & DISCOVERY | SYSTEM & DATA | RECENT VERIFIED CLOSES | DISCIPLINE
```

The Strategy/Setup board appears once. The right rail is reserved for multi-timeframe/setup context rather than duplicating the board.

## 3. Language

Operational text uses English + Roman Urdu, for example:

```text
WAIT / Intazar
BUY / Kharid
SELL / Farokht
Wajah
Mansuba
Market Jaiza
Khula Trade
Pehle nizam, phir raftaar
```

Urdu script is not used for operational statuses or reasons. The Arabic invocation may remain as decorative masthead text.

## 4. Session presentation

Hard authority and contextual session are visibly separate:

```text
Hard Session → runtime authority
Soft Context → NEW_YORK / other descriptive context only
Schedule     → VERIFIED / UNVERIFIED
News         → contextual health
```

A soft label is never presented as proof that the broker Session is OPEN.

## 5. Chart

Presentation-only controls:

```text
M1 | M5 | M15 | H1 | H4
Indicators ON/OFF
Drawings ON/OFF
Settings ON/OFF
Bars 60 / 120
```

The chart renders completed candles from the atomic snapshot. Controls are local UI state only and cannot alter the trading cadence.

## 6. Strategy routing display

The browser displays:

```text
Routed production family → ACTIVE_EXECUTION
remaining families       → SHADOW_ONLY
```

Production routing comes from structural semantics, not highest score and not the legacy `ACTIVE_STRATEGY_FAMILY` setting. Opposite qualified directions produce no routed production family.

Scores and coverage remain explanatory research facts.

## 7. Trade / Risk / blocker truth

Trade Plan, Risk, Gate, ManagedTrade and execution fields come from normalized runtime facts. The browser does not recompute them.

No actual plan → `WAITING` / `—`.  
No open trade → explicit flat-state card.  
Missing account/Risk fact → `—` / `UNKNOWN` / `NOT EVALUATED`.

## 8. Liveness

```text
fresh snapshot   → normal floor
stale snapshot   → BOT OFFLINE / SNAPSHOT STALE + retained dimmed facts
missing snapshot → visible waiting state
runtime failure  → DEGRADED/WAIT facts when available
market CLOSED    → full floor remains visible
```

## 9. Security

- localhost only;
- atomic snapshot publication;
- secret scan before publication;
- no credentials in browser state;
- no cloud dependency;
- no broker-mutating endpoint;
- **no BUY/SELL/MODIFY/CLOSE controls**;
- browser availability never determines trading authority.

## 10. Launch semantics

`DASHBOARD_MODE=GUI` means primary terminal **plus** this secondary browser. It never means browser-primary runtime.

## 11. Final invariant

> **The browser is a Swing-style secondary projection of Scalp runtime truth, with English + Roman Urdu cues. It improves visibility only; it cannot create, approve, modify, retry or execute a trade.**
