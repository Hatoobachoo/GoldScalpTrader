# GoldScalpTrader — Setup and Run Guide

**Status:** DRAFT PRE-CHALLENGE OPERATOR GUIDE — IMPLEMENTATION PENDING
**Version:** 0.1-local-backup-scalp
**Authority:** Intended installation, configuration, launcher modes, dashboard sizing, shutdown, local restore, migration and operator commands.

## 1. Purpose and current truth

This guide defines the intended clean-Windows operator path for GoldScalpTrader.

The project is still in documentation/challenge phase. The final package/launcher/runtime described below is **not yet claimed implemented or runnable**. Commands become operational proof only after the implementation phase and exact-version verification.

## 2. Intended V1 topology

```text
READINESS  explicit read-only diagnostic
DRY_RUN    governed analytical/runtime path with zero broker writes
PRIMARY    future one active governed DEMO runtime per account/symbol scope
STANDBY    not supported for same-scope local-SQLite V1
REAL       no implicit V1 path; separate governance required
```

Different independent accounts/scopes may each run a PRIMARY on different laptops. Two laptops must not concurrently control the same account/symbol scope.

## 3. Main planned source/proof owners

| Operator concern | Planned source owner | Main proof |
|---|---|---|
| settings / launcher | `config/settings.py`, `app/main.py` | settings/app suites |
| MT5 facts / recovery | `market_data/mt5_reader.py`, `app/recovery_mt5.py`, `app/recovery.py` | market/recovery suites |
| session/news | `app/session_news.py`, `risk/permissions.py` | session/news suites |
| dashboard facts | `app/dashboard.py`, `app/live_presentation.py` | dashboard suites |
| blocker/Gate truth | `operator/presentation.py` | operator presentation tests |
| narrow/wide terminal | `operator/narrow_dashboard.py`, `operator/rich_dashboard.py` | width/fallback tests |
| persistent runtime | `app/runtime.py`, `app/loop.py`, `app/cycle.py` | runtime-loop suites |
| checkpoint/local backup | `persistence/checkpoint.py`, `backup.py`, `local_recovery_package.py` | backup/restore suites |
| live learning | `research/live_learning.py`, `research/learning.py`, `management/store.py` | learning/recovery suites |

No planned runtime source owns automatic Git commit/push.

## 4. Intended prerequisites after implementation

- Windows with MetaTrader 5 installed;
- intended Exness account/server connected for the chosen mode;
- supported Python version verified against current MetaTrader5 package;
- local repository checkout;
- sufficient disk space for `.state` and external local backup root;
- network required for MT5 and any approved optional News source, **not** for safe shutdown/local backup;
- real `.env` or machine configuration kept local and uncommitted.

GitHub credentials are not required by the trading runtime.

## 5. Planned install shape

Once packaging is implemented and verified, intended setup should be simple, for example:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,mt5]"
Copy-Item .env.example .env
```

**Current note:** the provisional repository does not yet have the final `pyproject.toml`/package layout, so this block is a target interface, not present-tense proof.

## 6. Intended configuration families

Final names are fixed during implementation. Configuration should cover:

```text
runtime mode
preferred XAUUSDm symbol + explicit aliases
allowed account/server identity
MT5 magic/comment prefix/deviation policy
state directory
external local-backup root
manual daily-loss reset enabled=false by default
log level
session/news provider input + TTL
controller/lease settings
risk policy version
```

Rules:

- no broker password/PAT/private key committed;
- restored state never grants broker authority by itself;
- same-scope second PRIMARY is rejected;
- Account A state cannot become Account B authority;
- hard trading thresholds come from frozen contracts/versioned configuration, not dashboard toggles.

## 7. Intended local backup configuration

Conceptual default:

```text
C:\GoldScalpTrader_Backups\runtime\
C:\GoldScalpTrader_Backups\learning\
C:\GoldScalpTrader_Backups\recovery-packages\
C:\GoldScalpTrader_Backups\source\
```

The actual path is configurable and normally outside the repository.

Optional second physical drive/USB copy can provide disk-failure protection.

Automatic artifacts exclude secrets and real `.env` content.

## 8. READINESS mode

READINESS is read-only.

Intended work:

```text
initialize MT5 read boundary
→ verify account/server/symbol identity
→ read SymbolSpec / Bid/Ask / positions
→ verify required completed timeframe data
→ report data/session/news/recovery/controller readiness facts
→ keep operator dashboard alive if configured
```

READINESS cannot create TradePlan→Risk→Intent broker-writing lifecycle.

## 9. DRY_RUN mode

DRY_RUN is the mandatory first functional runtime milestone.

It may exercise:

```text
market facts
→ intelligence
→ strategy/fusion
→ Opportunity/timing
→ TradePlan
→ monetary Risk
→ permission/Gate diagnostics
```

but stops before irreversible broker writer calls.

It records truthful “would otherwise proceed / blocker” evidence and never fabricates actual fill/reconciliation/MAIN_DEMO proof.

## 10. Future governed PRIMARY startup

When DEMO broker-write phase is explicitly implemented:

```text
MT5 initialize
→ intended identity / MarketSnapshot
→ scoped StateStore integrity
→ risk-day/cash-flow reconciliation
→ local controller lease/epoch
→ Session/News observation
→ startup recovery/reconciliation
→ READY / RECONCILING / BLOCKED
→ persistent governed M5/event loop
```

Positive account/server/symbol identity, fresh required truth, monetary Risk, capacity/exposure, hard permission, controller and broker checks remain hard.

## 11. Data/timeframe baseline before challenge freeze

Current draft only:

```text
H1   broad regime
M15  opportunity/location/path
M5   primary scalp setup/timing/management
H4   optional major context
M1   diagnostic baseline — fresh-zero challenge may change it
```

Do not treat these as frozen operator guarantees until Audit 1 is closed.

## 12. Session / News operator rule

Always read separately:

```text
Soft Session
Hard Market State
News State
Entry Permission
```

Known blackout remains a hard new-entry condition in the draft.

`OPEN + News UNKNOWN` final entry treatment is still a FIX-BEFORE-BUILD/architecture decision; the dashboard must show UNKNOWN truthfully rather than assuming the Swing project's policy.

## 13. Dashboard sizing

Intended primary terminal behaviour:

```text
64–95 display cells → stacked narrow renderer
96+ display cells    → wide Rich renderer
render failure       → compact safe fallback
```

Sizing is presentation-only and cannot change trading logic.

Human-facing time uses PKT where useful; broker/risk/persistence/research timestamps remain UTC internally.

## 14. Current Blocker versus Gate

Operator troubleshooting must distinguish:

```text
TradePlan DEGRADED / Risk BLOCK
→ Current Blocker = owning upstream layer
→ Gate NOT EVALUATED / WAIT

actual ExecutionPermissionGate BLOCK
→ Current Blocker = Execution Gate
→ Gate BLOCKED
```

A broad `ENTRY_BLOCKED` label is not proof the Gate stopped the setup.

## 15. TradePlan / Risk display

Structural Entry/SL/objectives exist before monetary lot sizing.

Do not use Swing reference values as operator truth while they remain unresolved. In particular:

- final minimum structural R/cost-room threshold is challenge/calibration pending;
- final small-account risk bands/daily limits are challenge/calibration pending;
- current provisional 0.50% scaffold is not yet the frozen profile contract.

Minimum 0.01 lot is evaluated against actual all-in risk; the structural stop is never tightened merely to make volume affordable.

## 16. Manual trades and counts

Manual/foreign positions are never silently adopted.

`Today Trades` / verified trade counts refer to actual bot entry lineages, not signals, WAIT/MISSED/BLOCK, MODIFY/CLOSE actions or manual trades.

An exact manual close of an already-known bot ManagedTrade can complete that bot lifecycle only after exact ticket/full-volume broker proof and explicit EXTERNAL/MIXED close attribution.

## 17. Intended graceful shutdown

Use governed stop/Ctrl+C when the runtime exists.

Required sequence:

```text
stop new work
→ resolve/reconcile lifecycle as allowed
→ persist state
→ release controller
→ shut down MT5 write/read resources safely
→ create fresh verified LOCAL checkpoint
→ secret/integrity scan
→ update local backup catalog
→ report success/failure explicitly
```

There is deliberately:

```text
NO git fetch requirement
NO git add
NO git commit
NO git push
```

Safe shutdown/local backup must work even when GitHub/network is unavailable after broker authority is released.

## 18. Local backup and restore

Planned commands may eventually resemble:

```powershell
python scripts/create_local_recovery_package.py ...
python scripts/restore_runtime_checkpoint.py <checkpoint> <new-db>
python scripts/create_source_git_bundle.py ...
```

These command names are planned until scripts exist.

Full runtime checkpoint/recovery package is machine-recovery authority. A focused learning export or Git bundle alone is not.

Restore always goes to a new DB/path and still requires fresh broker reconciliation/controller authority.

## 19. Same-scope laptop handoff

Allowed:

```text
Laptop A → Account A → PRIMARY
Laptop B → Account B → PRIMARY
```

Not supported:

```text
Laptop A → Account A → PRIMARY
Laptop B → same Account A → second active production writer
```

Supported movement:

```text
old PRIMARY safe stop
→ final verified local recovery package
→ deliberately transfer package
→ restore NEW DB on second machine
→ configure credentials separately
→ connect same intended account/symbol
→ reconcile positions/deals/quote/lifecycle/risk/learning
→ acquire controller
→ new PRIMARY only when safe
```

## 20. Intended research commands

Future research tooling may provide commands equivalent to:

```powershell
python scripts/acquire_mt5_dataset.py ...
python scripts/run_walk_forward.py ...
python scripts/report_demo_learning_evidence.py ...
```

Research evidence has no broker authority and does not prove future profitability.

## 21. Intended repository verification

After tooling exists, local verification should include equivalent to:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

GitHub Actions are not required.

## 22. Troubleshooting principle

If runtime is waiting:

1. read Current Blocker;
2. read Gate separately;
3. read human explanation;
4. inspect structured logs/health if needed;
5. inspect data/session/news/risk/reconciliation state;
6. never disable safety merely to make a trade happen.

Do not delete state, edit SQLite to clear locks, run a same-scope second PRIMARY, commit credentials or force a broker write.

## 23. Proof boundary

A future clean install/launch is proven only on the exact implemented revision/environment.

Deterministic software proof, connected MT5 readiness, governed DEMO lifecycle, actual learning and fresh-machine local recovery are separate evidence classes.