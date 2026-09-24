# GoldScalpTrader — Setup and Run Guide

**Status:** POST-AUDIT-1 OPERATOR TARGET — PRESERVATION-FIRST CORRECTED / IMPLEMENTATION PENDING
**Version:** 1.2-profiled-risk-preserved-capabilities
**Authority:** Intended installation, configuration, runtime modes, Risk profiles/aggressive option, News provider/cache, shutdown, local source/runtime backup, restore/migration and operator commands.

## 1. Current truth

The canonical design is still pre-implementation. Commands become proof only after exact code/environment verification.

GoldSwingTraderAI features/defaults remain the baseline unless Scalp docs explicitly classify a direct scalp-specific or operator-directed difference.

## 2. Intended capability stages

```text
READINESS  explicit read-only diagnostic
DRY_RUN    governed analytical/runtime path with zero irreversible broker writes
PRIMARY    controlled governed DEMO runtime after its evidence gate
REAL       preserved future governed capability; disabled/unavailable until separate DEMO/release/explicit-approval gate
```

Same-scope simultaneous PRIMARY writers remain unsupported without a separate shared-fencing architecture.

## 3. Scalp timeframe/operator meaning

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
- intended Exness account/server;
- supported Python version verified against current MetaTrader5 package;
- local repository checkout;
- disk space for state/backups/News cache;
- network for MT5 and optional News source, not for safe local shutdown;
- `.env`/credentials kept local and uncommitted.

Trading runtime does not require GitHub credentials.

## 5. Intended install shape

Example target after packaging:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,mt5]"
Copy-Item .env.example .env
```

Current repository packaging remains provisional until implementation phase.

## 6. Configuration families

Expected settings include:

- runtime stage/mode;
- preferred/resolved Gold symbol;
- allowed account/server identity;
- magic/comment/deviation policy;
- state/backup paths;
- bounded analytical worker configuration with one-worker fallback;
- News/session provider + LKG cache path;
- provider TTL baseline 1800s;
- controller settings;
- SMALL/MEDIUM/NORMAL Risk policy version;
- explicit aggressive-small-account enable flag, default false;
- manual daily-loss reset enable flag, default false;
- log level.

Hard policy is not a dashboard toggle.

## 7. Risk operator truth

Automatic profile selection is preserved:

```text
SMALL   positive DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

| Profile | Normal / target | Elevated | Hard ceiling | Daily loss lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

Profile is fixed from DayStartEquity for the UTC risk day.

If theoretical lot is below broker minimum, evaluate actual minimum-lot risk against the active hard policy. Structural SL is never tightened merely to make 0.01 fit.

### 7.1 Aggressive small-account option

Preserved feature, **disabled by default**.

When explicitly enabled and eligible:

```text
8%  = MAXIMUM monetary SL risk per trade — NOT TARGET
16% = maximum aggregate open risk
16% = daily loss ceiling
```

It never auto-enables merely because balance/equity is below $1,000. All other hard authorities remain.

### 7.2 Daily reset / cooldown

Manual daily-loss reset capability is preserved but disabled by default.

Preserved cooldown/re-entry baseline:

- one genuinely fresh same-episode re-entry;
- three consecutive closed bot losses → at least 30 minutes global cooldown;
- release also requires fresh/healthy conditions owned by Risk policy.

## 8. News operator truth / API outage

```text
OPEN + accepted News CLEAR    → may proceed to other authorities
OPEN + accepted News BLACKOUT → BLOCK
OPEN + true NEWS_SAFETY_UNKNOWN → BLOCK / LIMITED
```

```text
refresh fails + valid LKG cache
→ keep cached accepted event truth
→ provider may show DEGRADED

refresh fails + expired/invalid/no cache
→ NEWS_SAFETY_UNKNOWN
```

Cache original timestamps/coverage/validity are never extended on failure.

Preserved baseline TTL:

```text
1800 seconds
```

## 9. Session safety baseline

Until current broker proof supersedes factual schedule assumptions:

```text
Daily no-entry / flatten    T-20 / T-10
Weekend no-entry / flatten  T-60 / T-30
Daily reopen                1 clean completed M5
Weekend reopen              2 clean completed M5 + gap assessment
```

Special holiday/schedule uncertainty fails safely rather than inventing hours.

## 10. READINESS

```text
initialize MT5 read boundary
→ verify account/server/symbol
→ read SymbolSpec / Bid/Ask / positions
→ verify completed H1/M15/M5 data (+ optional H4, diagnostic M1)
→ validate state/risk-day profile/overlay identity
→ read/revalidate session/news provider + LKG cache
→ report readiness/recovery/controller state
```

No irreversible broker write.

## 11. DRY_RUN

```text
market facts
→ bounded-parallel intelligence/families
→ fusion / Opportunity / completed-M5 timing
→ TradePlan gross + cost-aware room
→ profiled monetary Risk
→ permission/Gate diagnostics
→ STOP before irreversible writer
```

## 12. Controlled DEMO PRIMARY

Future implemented path:

```text
MT5 initialize
→ identity / MarketSnapshot
→ StateStore integrity
→ risk-day/profile/cash-flow reconciliation
→ controller lease/epoch
→ Session/News provider + cache validation
→ startup recovery/reconciliation
→ READY / RECONCILING / BLOCKED
→ governed M5/event loop
```

## 13. Future REAL capability

REAL is not removed, but is not an initial operator shortcut.

Activation requires a separate future policy/release packet after required DEMO lifecycle, recovery, risk, execution and operator evidence plus explicit approval.

## 14. Graceful shutdown

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

No Git fetch/add/commit/push in runtime shutdown.

## 15. Development/source backup

After a major coherent bulk:

```powershell
cd "D:\Trading Bot\GoldScalpTrader"
git pull --ff-only
```

One pull updates source + full Git history. No need to pull after every tiny patch.

Optional secret-clean ZIP may be created after major milestones.

## 16. Runtime restore / laptop handoff

Restore uses a new DB/path, credentials configured separately, then fresh broker account/symbol/positions/deals/quote truth is reconciled before controller/write authority.

## 17. Intended local verification

After tooling exists:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

## 18. Explicit Swing → Scalp differences

Read `90-governance/DOCUMENTATION_COMPARISON.md`.

It now distinguishes genuine scalp-specific deltas from operator-directed differences and lists earlier non-scalp simplifications that have been restored.

## 19. Proof boundary

Clean install/launch, deterministic tests, current broker reads, provider/cache behavior, DEMO lifecycle, recovery, future REAL release and future profitability are separate evidence classes.