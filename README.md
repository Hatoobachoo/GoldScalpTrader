# GoldScalpTrader

Safety-first local MetaTrader 5 gold scalping project.

## Current runtime

The offline architecture is implemented. `python bot.py` now routes by runtime mode:

- `DRY_RUN` → analytical/read-only cycle, zero broker writes.
- `DEMO` → continuous guarded demo trading loop with local SQLite state.
- `REAL` → disabled in this release.

DEMO broker writes are fail-closed. The connected MT5 account must explicitly report `ACCOUNT_TRADE_MODE_DEMO`; otherwise the runtime refuses to send an order. The Gate also blocks on stale/incomplete market data, occupied/unknown exposure, unresolved execution intents, controller conflicts, failed persistence, disabled expert trading, or failed broker `order_check`.

## Live DEMO quick start

Keep MetaTrader 5 open and logged into the intended **demo** account, then:

```powershell
cd "D:\Trading Bot\GoldScalpTrader"
git pull --ff-only
Copy-Item .env.demo.example .env
python bot.py
```

The supplied demo profile uses:

```text
MODE=DEMO
ACTIVE_STRATEGY_FAMILY=TREND_PULLBACK_CONTINUATION
TARGET_RISK_PERCENT=1.00
DEMO_TRADING_CONFIRM=YES_I_APPROVE_DEMO
```

`Ctrl+C` stops the local loop and writes a runtime checkpoint. Runtime state stays under `runtime/` and is not published to GitHub.

## Non-negotiable project rules

- Trading runs locally on the user's Windows PC and MetaTrader 5 terminal.
- GitHub is used only for source control and backup.
- GitHub Actions, Codespaces, Git LFS, paid Marketplace services, and paid external APIs are not required.
- `.env.example` remains a safe DRY_RUN template; `.env.demo.example` is the explicit live-demo template.
- REAL order execution remains disabled.
- Credentials, account numbers, passwords, tokens, and `.env` files must never be committed.
- One-position-at-a-time and hard risk controls are part of the design.
- No martingale, unlimited averaging, or uncontrolled grid logic.

> Automated trading can lose money. Connected DEMO evidence must be completed before any future REAL release is considered.
