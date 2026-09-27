# GoldScalpTrader — Graphical Dashboard

**Status:** APPROVED SECONDARY LOCAL VISUAL FLOOR
**Version:** 3.0-secondary-browser-floor
**Authority:** Secondary graphical layout, chart interaction, snapshot presentation, stale/offline visibility, and local-only read-only behavior.

## 1. Role

The graphical/browser dashboard is **secondary**. The primary operator surface is the terminal dashboard.

```text
runtime facts → primary terminal dashboard
             ↘ atomic read-only snapshot → secondary localhost browser
```

The browser may look richer, but it never becomes a second trading engine and never replaces the terminal runtime path.

## 2. Isolation

The graphical dashboard:

- binds to localhost only;
- consumes presentation snapshots only;
- has no MetaTrader5 dependency;
- cannot call MT5Writer;
- cannot alter Risk/Gate/Opportunity/strategy policy;
- cannot enable REAL;
- cannot place, modify, or close positions;
- may be closed or crash without affecting the bot or primary dashboard.

## 3. Visual target

Retain the GoldSwingTrader institutional visual family adapted for Scalp:

- dark navy/black background;
- cyan/teal framing and status accents;
- gold emphasis for Gold-specific labels and plan highlights;
- dense one-screen hierarchy;
- no page/panel scroll bars in normal supported desktop layouts;
- truthful unknown/stale/degraded states;
- no decorative element may obscure trading facts.

Target layouts:

```text
1920×1080 full floor
1600×900 compact floor
smaller screens → density reduction, never hidden critical safety state
```

## 4. Panels

The secondary floor should project the same authoritative facts shown by the primary terminal dashboard:

```text
masthead / clock / mode
market state / session / Bid / Ask / spread / countdown
market analysis and MTF context
central XAU chart
Detected Setup / Active Family / Signal
Opportunity / Timing / M1 refinement
Trade Plan / executable quality / blocker
Risk/account
shadow strategy board
ManagedTrade
execution/controller/reconciliation
activity
learning/discovery
data/system health
recent verified closes when available
```

## 5. Chart controls

Functional local controls:

```text
M1 | M5 | M15 | H1 | H4
Indicators
Drawings
Settings
zoom / pan / reset
```

They affect presentation only.

Production authority remains:

```text
M5  primary setup/thesis
M1  subordinate entry refinement
M15 path/location
H1  broad context
H4  optional major context
```

Selecting another chart timeframe cannot change strategy cadence or create a trade.

## 6. Stale / offline / degraded behavior

The browser remains meaningful when its snapshot is missing or stale:

```text
fresh snapshot → normal visual floor
stale snapshot → BOT OFFLINE / SNAPSHOT STALE
missing snapshot → waiting/unavailable state
runtime failure snapshot → DEGRADED / WAIT / exact reason
market CLOSED → full floor visible with CLOSED state
```

A previous snapshot may remain visible only if clearly marked stale/degraded. It must never be presented as fresh broker truth.

## 7. Detected setup / shadow truth

The graphical dashboard must not blend all six strategy families into one production vote.

- active family + genuine own setup → live-eligible progression may be shown;
- shadow family setup → `SHADOW ONLY`;
- no valid setup → `WAIT / NO VALID SETUP`;
- shadow results never appear as broker-realized P/L.

## 8. Trade and Risk truth

No fabricated plan, Risk, performance, or account values.

Missing authoritative value → `—`, `UNKNOWN`, `NOT EVALUATED`, or `NO SAMPLE`.

Current blocker and central Gate must remain separate concepts.

## 9. Security

No credentials or financial secrets in snapshots. No public bind. No state-changing HTTP endpoints. No paid/cloud dashboard dependency.

## 10. Launch semantics

`DASHBOARD_MODE=GUI` means:

> **run the normal primary terminal dashboard and additionally publish/start this secondary browser floor.**

It does not mean browser-primary runtime.

## 11. Final invariant

> **The graphical dashboard is a rich secondary projection of the same trading facts. It may improve visibility, but it owns no trading authority and its availability can never determine whether the bot or primary terminal dashboard remains alive.**
