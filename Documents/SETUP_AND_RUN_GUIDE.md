# GoldScalpTrader — Setup and Run Guide

**Status:** POST-AUDIT-1 OPERATOR TARGET — IMPLEMENTATION PENDING
**Version:** 1.1-cache-aware-local-pull-zip
**Authority:** Intended installation, configuration, runtime modes, News provider/cache operation, shutdown, local source/runtime backup, restore/migration and operator commands.

## 1. Current truth

Fresh-Zero Audit 1 is complete. The final package/runtime described here is still not yet implemented or proven runnable. Commands become proof only after implementation and exact-version verification.

## 2. Intended V1 modes

```text
READINESS  explicit read-only diagnostic
DRY_RUN    governed analytical/runtime path with zero broker writes
PRIMARY    later one active governed DEMO runtime per account/symbol scope
REAL       deferred V1 / separate future governance
STANDBY    not supported for same-scope local-state V1
```

## 3. Frozen timeframe/operator meaning

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar scalp setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health
```

## 4. Intended prerequisites after implementation

- Windows + MetaTrader 5;
- intended Exness account/server for selected mode;
- supported Python version verified against current MetaTrader5 package;
- local repository checkout;
- disk space for local state/backups and News cache;
- network for MT5 and approved optional News source, not for safe local shutdown;
- real `.env`/machine credentials kept local and uncommitted.

Trading runtime does not require GitHub credentials.

## 5. Intended install shape

Target operator interface after packaging, for example:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,mt5]"
Copy-Item .env.example .env
```

Current repository packaging is still provisional until implementation phase fixes `pyproject.toml`/src launch design.

## 6. Configuration families

Expected configuration covers runtime mode, preferred/resolved Gold symbol, allowed account/server identity, magic/comment/deviation policy, state/backup paths, News/session provider, News cache path/TTL/refresh cadence, controller settings, STANDARD risk policy version, log level and manual daily-loss reset disabled by default.

Hard trading thresholds come from frozen/versioned policy, not dashboard toggles.

## 7. STANDARD risk operator truth

V1 does **not** auto-select SMALL/MEDIUM/NORMAL risk tiers by balance.

One STANDARD production policy owns preferred per-trade risk target, hard ceiling, daily loss limit, one-position capacity and durable cooldown/re-entry state. Exact numbers remain calibration pending.

A small account still receives truthful min-lot evaluation from actual equity/tick/stop/volume facts. Structural SL is never tightened to make 0.01 fit.

Historical aggressive 8%/16% values are not active policy. Any future aggressive experiment remains explicit and disabled by default.

## 8. News operator truth / API outage

For new entry:

```text
OPEN + accepted News CLEAR    → may proceed to other authorities
OPEN + accepted News BLACKOUT → BLOCK
OPEN + NEWS_SAFETY_UNKNOWN   → BLOCK / LIMITED
```

Temporary provider/API failure semantics:

```text
refresh fails + valid last-known-good cache
→ keep cached event truth
→ provider health may show DEGRADED
→ no unnecessary entry block solely because refresh failed

refresh fails + expired/invalid/no cache
→ NEWS_SAFETY_UNKNOWN
→ new entry blocked
```

The cache must keep its original fetch/as-of/coverage/valid-until timestamps. A failed refresh never makes old data look fresh.

Operator/dashboard should show provider source, health, last successful refresh, cache age/valid-until and current News state separately where implemented.

Existing-position protection/mandatory CLOSE remains action-sensitive.

## 9. READINESS

Read-only intended path:

```text
initialize MT5 read boundary
→ verify account/server/symbol
→ read SymbolSpec / Bid/Ask / positions
→ verify completed H1/M15/M5 data (+ optional H4, diagnostic M1 if enabled)
→ read/revalidate session/news provider and LKG cache
→ report data/session/news/recovery/controller readiness
```

No broker write lifecycle exists here.

## 10. DRY_RUN

```text
market facts
→ intelligence
→ six strategy families / fusion
→ Opportunity / completed-M5 timing
→ TradePlan gross + cost-aware room
→ STANDARD monetary Risk
→ permission/Gate diagnostics
→ STOP before irreversible writer
```

DRY_RUN preserves “would otherwise proceed / blocker” evidence but cannot prove fills/slippage/reconciliation/live learning.

## 11. Future governed DEMO PRIMARY

When deliberately implemented:

```text
MT5 initialize
→ identity / MarketSnapshot
→ StateStore integrity
→ risk-day/cash-flow reconciliation
→ controller lease/epoch
→ Session/News provider + cache validation
→ startup recovery/reconciliation
→ READY / RECONCILING / BLOCKED
→ governed M5/event loop
```

## 12. Dashboard sizing / authority

Intended primary terminal uses read-only renderers plus safe fallback. Presentation never changes trading logic.

Troubleshooting distinguishes upstream TradePlan/Risk stop from actual central Gate BLOCK.

## 13. Graceful shutdown

Required concept:

```text
stop new work
→ resolve/record safe lifecycle obligations
→ persist state
→ release controller / MT5 resources
→ create fresh verified LOCAL checkpoint
→ integrity/secret scan as applicable
→ update local backup catalog
→ report success/failure
```

There is deliberately no Git fetch/add/commit/push in runtime shutdown.

## 14. Development/source backup — normal low-usage workflow

Do not pull after every tiny patch.

After a major coherent documentation/code bulk, use the checkpoint commit supplied by ChatGPT and run:

```powershell
cd "D:\Trading Bot\GoldScalpTrader"
git pull --ff-only
```

That single pull updates the local clone and preserves full Git history.

## 15. Optional local ZIP after pull

For another offline copy, a helper may later create:

```text
GoldScalpTrader_backup_<date>_<short-commit>.zip
```

Default archive excludes `.env`, credentials/private keys, virtualenvs, caches, logs, runtime databases/checkpoints and nested backup folders.

ZIP is preferred over RAR for default Windows-native workflow.

## 16. Runtime backup root

Conceptual external directories:

```text
C:\GoldScalpTrader_Backups\runtime\
C:\GoldScalpTrader_Backups\learning\
C:\GoldScalpTrader_Backups\recovery-packages\
C:\GoldScalpTrader_Backups\source-zips\
```

Optional second physical drive/USB can provide stronger device-failure protection.

## 17. Runtime restore / laptop handoff

Full runtime checkpoint/recovery package is separate from source ZIP/Git clone.

Restore goes to a new DB/path, credentials are configured separately, then fresh broker account/symbol/positions/deals/quote truth is reconciled before controller/write authority.

Same-scope second simultaneous PRIMARY is unsupported.

## 18. Intended local verification

After tooling exists:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

GitHub Actions are not required.

## 19. Explicit Swing → Scalp differences

For the permanent exact list read:

`Documents/90-governance/DOCUMENTATION_COMPARISON.md`

## 20. Proof boundary

A future clean install/launch is proven only on the exact implemented revision/environment. Deterministic software proof, connected MT5 readiness, News-provider/cache proof, governed DEMO lifecycle, live learning, local restore and future strategy performance are separate evidence classes.