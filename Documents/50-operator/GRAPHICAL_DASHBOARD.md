# GoldScalpTrader — Secondary Graphical Dashboard

**Status:** DRAFT PRE-CHALLENGE SECONDARY READ-ONLY INTERFACE
**Version:** 0.1-scalp-normalized-snapshot
**Authority:** Optional local visual monitoring only. No strategy, risk, controller, lifecycle or broker-write authority.

## 1. Purpose

The graphical dashboard is a separate browser-based visual monitor for GoldScalpTrader.

The primary terminal remains the operational console. The browser is optional and must never become a dependency of trading liveness.

One screen may expose live Gold state, recent real completed candles, current decision, TradePlan, family evidence, risk/activity and system state without introducing a second trading engine.

## 2. Architecture

```text
GoldScalpTrader PRIMARY process
 market / intelligence / strategies / decisions / risk / execution / manager
                         |
                         | authoritative presentation DTO
                         v
              operator/presentation.py
            truthful read-only normalization
                         |
                         | atomic presentation-only snapshot
                         v
              .state/dashboard_snapshot.json
                         |
                         | read-only
                         v
              localhost secondary server
                         |
                         v
                 127.0.0.1:<port>
```

The primary process never waits for the browser/server.

## 3. Snapshot contract

The same presentation normalization used by the primary terminal should feed the graphical snapshot so the two views cannot contradict each other about blocker stage, Gate state, session/news truth or strategy-performance provenance.

The snapshot may contain:

- symbol/mode/runtime role/risk profile;
- hard market state + soft session;
- live Bid/Ask, spread, quote age, M5 countdown;
- H1/M15/M5 structure and enabled optional H4/M1 context;
- EMA/RSI/ATR/volatility/event-freshness summaries;
- bounded recent **real completed M5 candles** from authoritative MarketSnapshot;
- BUY/SELL thesis scores, Opportunity, timing, leading family and reason;
- compact six-family current analytical rows where useful;
- already-built TradePlan Entry/SL/Primary/Expansion/R/cost context;
- risk/account/activity/system/controller/recovery facts;
- truthful Gate state plus upstream blocker explanation;
- verified actual DEMO performance only;
- recent verified closes when available;
- open ManagedTrade facts;
- learning/discovery/local-backup health.

Missing facts display as `—`, waiting, standby or no sample. No fabricated candles/performance/permissions.

No broker password, token, secret or authority-bearing credential enters the snapshot.

## 4. Atomic publication

Snapshot publication writes a temporary sibling file then atomically replaces the live snapshot.

A browser reader sees either a previous complete frame or the next complete frame—not a deliberately partial JSON write.

Snapshot serialization/publication failure is presentation-only and cannot stop strategy/risk/execution.

## 5. Crash isolation

```text
snapshot failure
→ primary terminal continues
→ trading authorities unchanged

browser/server crash or Ctrl+C
→ PRIMARY continues
→ terminal continues
```

There are no browser-side BUY/SELL/MODIFY/CLOSE controls.

## 6. Secondary server boundary

Draft implementation rules:

- fixed bind `127.0.0.1`;
- configurable local port with safe default;
- no public/network bind option in V1;
- no MT5 import in secondary server;
- no strategy/risk/controller/execution owners imported;
- GET/HEAD only for useful interface operations;
- state-changing HTTP methods rejected;
- launch/close independently.

## 7. Truthful liveness

The browser may poll the presentation snapshot approximately once per second.

LIVE status is based on **primary snapshot age**, not the fact that the web server is running.

Exact stale threshold remains operator calibration, but semantics are:

```text
fresh primary snapshot → LIVE
old snapshot           → BOT OFFLINE / SNAPSHOT STALE
missing/corrupt        → unavailable/waiting overlay
```

## 8. Visual hierarchy

Draft hierarchy:

```text
MASTHEAD
  GoldScalpTrader / PKT clock / mode / PRIMARY

TOP MARKET STRIP
  XAUUSDm / Market / Session / Bid / Ask / Spread / M5 / Feed / Bot State

PRIMARY FLOOR
  Market Analysis | completed-M5 chart | Current Decision | TradePlan

EVIDENCE FLOOR
  Session & News | Strategy Board | Open Trade

ACCOUNT FLOOR
  Account & Risk | Trading Activity | Recent Verified Closes

SYSTEM FLOOR
  Execution & Controller | Learning & Discovery | Data/Recovery/Local Backup
```

The chart renders real completed candles carried by the snapshot. It never calls MT5 or recalculates signals.

## 9. Strategy and performance truth

Current family scores are analytical evidence only.

Historical Trades/Wins/Net R come only from verified actual production/DEMO closed samples of the approved environment.

Zero samples remain visibly unsampled.

## 10. Decision / blocker / Gate semantics

The browser preserves the exact same distinction as the terminal:

```text
TradePlan/Risk stopped candidate upstream
→ Current Blocker = owning upstream layer
→ Gate NOT EVALUATED / WAIT

actual Gate BLOCK
→ Current Blocker = Execution Gate
→ Gate BLOCKED
```

`ENTRY_BLOCKED` is never blindly converted to `Gate BLOCKED`.

If no TradePlan exists, the browser cannot fabricate Entry/SL/targets from a desk score.

## 11. Scalp-specific visuals

Useful additional visuals may include:

- latest structural/liquidity event age;
- spread versus healthy baseline;
- approved entry reference versus live executable quote;
- gross room versus cost context;
- trade age / M5 bars;
- latency diagnostics;
- Opportunity lifecycle/re-arm state.

These are displays of authoritative facts, not browser-calculated trading gates.

## 12. Local security/privacy

The server is localhost-only and snapshots contain no authority-bearing secrets.

Runtime/private account metadata should be minimized to what operator monitoring needs, especially while the source repo remains public.

The dashboard does not require cloud hosting, external analytics or paid services.

## 13. Planned implementation ownership

```text
src/gold_scalp_trader/app/live_presentation.py
src/gold_scalp_trader/operator/presentation.py
src/gold_scalp_trader/operator/graphical_snapshot.py
src/gold_scalp_trader/graphical_dashboard/server.py
src/gold_scalp_trader/graphical_dashboard/ui.py
src/gold_scalp_trader/graphical_dashboard/__main__.py
```

## 14. Planned proof

Tests must prove:

- snapshot schema and authoritative data mapping;
- real completed-candle carriage;
- atomic replacement;
- upstream blocker vs Gate truth;
- stale/offline status based on primary snapshot age;
- localhost-only server;
- no trade controls/state-changing endpoints;
- no MT5/strategy/risk/execution imports in secondary boundary;
- browser failure isolation;
- no secrets in snapshot.

## 15. Pre-challenge questions

- exact chart history depth;
- port/default launch UX;
- stale snapshot threshold;
- which current family details deserve screen space;
- whether M1 micro-chart adds value or clutter;
- how much account identity should appear visually;
- whether the graphical dashboard should be built in V1 or after the terminal dashboard is proven.
