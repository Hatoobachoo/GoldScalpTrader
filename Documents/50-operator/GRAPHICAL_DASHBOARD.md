# GoldScalpTrader — Secondary Graphical Dashboard

**Status:** FROZEN V1 SECONDARY READ-ONLY INTERFACE — IMPLEMENTATION / PRESENTATION PROOF PENDING
**Version:** 1.0-profiled-risk-normalized-snapshot
**Authority:** Optional local visual monitoring only. No strategy, Risk, controller, lifecycle or broker-write authority.

## 1. Purpose

The graphical dashboard is an optional browser-based local monitor. The primary terminal remains the operational console; browser availability is never a trading-liveness dependency.

It may expose live Gold state, recent real completed candles, current decision, TradePlan, family evidence, account/Risk and system state without introducing a second trading engine.

## 2. Architecture

```text
GoldScalpTrader PRIMARY process
market / intelligence / strategies / decisions / Risk / execution / manager
                         ↓
             authoritative presentation DTO
                         ↓
              operator/presentation.py
                         ↓
          atomic read-only dashboard snapshot
                         ↓
               localhost-only server
                         ↓
                 127.0.0.1:<port>
```

Primary never waits for browser/server.

## 3. Snapshot contract

Use the same presentation normalization as terminal so views cannot contradict blocker/Gate, session/News, Risk-profile/overlay or performance provenance.

Snapshot may contain:

- symbol/capability stage/runtime role;
- SMALL/MEDIUM/NORMAL Risk profile + actual proposal;
- aggressive-small-account mode ENABLED/DISABLED and active ceilings when applicable;
- hard Market State + soft Session;
- News provider/cache truth;
- Bid/Ask/spread/quote age/M5 countdown;
- H1/M15/M5 structure + optional H4 and clearly labelled diagnostic M1;
- EMA/RSI/ATR/volatility/event freshness;
- bounded recent real completed M5 candles;
- BUY/SELL theses, Opportunity, timing, leading family/reason;
- six-family analytical rows where useful;
- governed TradePlan geometry + gross/cost-adjusted room;
- account/activity/controller/recovery facts;
- truthful Gate/upstream blocker;
- verified actual DEMO performance/recent closes;
- open ManagedTrade including remaining volume/verified partial-management state;
- learning/discovery/local-backup health.

Missing facts show waiting/standby/`—`/NO SAMPLE. No fabricated candles, Risk, performance, geometry or permissions.

No secret enters snapshot.

## 4. Atomic publication / crash isolation

Write temporary sibling then atomically replace live snapshot. Reader sees complete previous or next frame.

Snapshot/browser/server failure is presentation-only:

```text
secondary UI failure
→ PRIMARY + terminal continue
→ trading authorities unchanged
```

No browser BUY/SELL/MODIFY/CLOSE controls exist.

## 5. Server boundary

- bind `127.0.0.1` only;
- configurable safe local port;
- no public/network bind option in current V1;
- no raw MT5 import;
- no strategy/Risk/controller/execution owners imported;
- GET/HEAD only as needed;
- state-changing methods rejected;
- launch/close independently.

## 6. Truthful liveness

Browser may poll snapshot at a presentation cadence such as ~1 second. LIVE depends on **primary snapshot age**, not web-server process existence.

```text
fresh snapshot   → LIVE
old snapshot     → BOT OFFLINE / SNAPSHOT STALE
missing/corrupt  → unavailable/waiting
```

Exact UI stale threshold is implementation/operator calibration, not trading authority.

## 7. Frozen timeframe presentation

```text
H1   broad soft context
M15  opportunity/location/path
M5   primary completed setup/timing/management
H4   optional major context
M1   diagnostic/research only
```

M1 chart/details may be omitted for clutter, but if shown they must be labelled diagnostic and cannot imply production authority.

## 8. Visual hierarchy

Conceptual layout:

```text
MASTHEAD
TOP MARKET / SESSION / NEWS STRIP
PRIMARY FLOOR — market picture / completed-M5 chart / decision / TradePlan
RISK FLOOR — profile / overlay / proposed risk / daily state / cooldown
EVIDENCE FLOOR — strategy / open trade
ACCOUNT FLOOR — activity / verified closes
SYSTEM FLOOR — execution / controller / learning / recovery / local backup
```

Exact layout remains presentation calibration.

## 9. Risk truth

Never collapse canonical Risk into a generic `STANDARD` label.

If aggressive mode enabled, explicitly show:

```text
8%  MAX SL-risk ceiling — NOT TARGET
16% aggregate open-risk cap
16% daily-loss ceiling
```

If disabled, say `DISABLED`.

## 10. Decision / blocker / Gate semantics

```text
TradePlan/Risk/session owner stops upstream
→ Current Blocker = owning layer
→ Gate NOT EVALUATED / WAIT

actual central Gate BLOCK
→ Current Blocker = Execution Gate
→ Gate BLOCKED
```

No plan means no fabricated Entry/SL/targets.

## 11. Scalp-specific visuals

May show event/trigger age, approved reference vs live quote, spread/healthy baseline, gross vs cost-adjusted room, trade age/M5 bars, latency and Opportunity/re-arm state. All are presentation of authoritative facts.

## 12. Runtime capability display

```text
READINESS
DRY_RUN
DEMO PRIMARY
REAL — FUTURE/GATED
```

Browser cannot activate or bypass future REAL release gate.

## 13. Local security/privacy

Localhost only, no authority-bearing secrets, minimal private account metadata. No cloud hosting, external analytics or paid services required.

## 14. Planned implementation ownership

```text
src/gold_scalp_trader/app/live_presentation.py
src/gold_scalp_trader/operator/presentation.py
src/gold_scalp_trader/operator/graphical_snapshot.py
src/gold_scalp_trader/graphical_dashboard/server.py
src/gold_scalp_trader/graphical_dashboard/ui.py
src/gold_scalp_trader/graphical_dashboard/__main__.py
```

## 15. Planned proof / presentation choices

Tests prove schema/mapping, completed-candle carriage, atomic publication, profile/overlay truth, blocker-vs-Gate, stale/offline status, localhost-only server, no state-changing controls, import isolation, browser failure isolation and secret exclusion.

Chart depth, port/launch UX, snapshot stale threshold, exact family screen detail and account-identity visibility remain presentation choices. Whether secondary UI is implemented in the first code milestone or after terminal proof is a build-order choice, not feature removal.