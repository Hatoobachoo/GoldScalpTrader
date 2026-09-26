# GoldScalpTrader — REAL and DEMO Mode Architecture, Safety Hierarchy & Code Map

**Status:** AS-BUILT ENGINEERING GUIDE — CURRENT RELEASE

**Scope:** Runtime-mode hierarchy, DEMO write authority, REAL hard-disable boundary, MT5 account verification, execution safety, dashboard routing, persistence/recovery, connected certification, code locations, tests, and known integration boundaries.

**Current release position:** `DRY_RUN` is read-only, `DEMO` is the only write-capable runtime when all explicit guards pass, and `REAL` is deliberately unavailable.

---

## 1. Why this document exists

GoldScalpTrader treats runtime mode as a safety architecture, not as a cosmetic configuration option. `DEMO` and `REAL` are financially significant states because they determine whether irreversible MetaTrader 5 writes may ever be reached.

This guide documents the actual code as it exists now. It explains:

- what `DRY_RUN`, `DEMO`, and `REAL` mean;
- where each mode is defined;
- how environment/configuration values become validated `Settings`;
- every important mode/account/write check before an MT5 order can be sent;
- how the startup hierarchy routes into read-only, DEMO terminal, or DEMO graphical paths;
- where the sole irreversible MT5 write boundary lives;
- how DEMO account identity is independently verified from MT5 itself;
- how durable Intent, Gate, precheck, reconciliation, ManagedTrade, checkpoint and certification layers interact;
- why setting `MODE=REAL` or `REAL_TRADING_CONFIRM` cannot enable REAL in this release;
- what is not yet implemented for a future REAL release;
- current known integration boundaries that must not be mistaken for completed behavior.

This is an **as-built map**, not permission to weaken the frozen system contracts.

---

## 2. Mode vocabulary

Runtime modes are defined in:

`src/gold_scalp_trader/domain/enums.py`

```python
class RuntimeMode(StrEnum):
    DRY_RUN = "DRY_RUN"
    DEMO = "DEMO"
    REAL = "REAL"
```

### DRY_RUN

Purpose:

- analytical/read-only operation;
- normal market-data and decision pipeline can execute;
- broker writes are not enabled.

### DEMO

Purpose:

- connected Exness/MT5 DEMO trading;
- may send OPEN/MODIFY/CLOSE only after all runtime guards pass;
- requires explicit operator confirmation and a broker account that MT5 itself positively reports as DEMO;
- uses durable local state and reconciliation.

### REAL

Purpose:

- reserved future real-money release mode.

Current status:

- **HARD DISABLED**;
- no supported current release path may enable REAL broker writes;
- `REAL_RELEASE_ENABLED = False` is a build-level release lock;
- `validate_settings()` rejects `MODE=REAL` while that lock is false.

---

## 3. High-level hierarchy

```text
python bot.py
    |
    v
src/gold_scalp_trader/app/main.py
    |
    +--> load_settings()
    |       |
    |       +--> parse MODE
    |       +--> validate Settings
    |       +--> DEMO requirements
    |       +--> REAL hard release lock
    |
    +--> mt5_session()
            |
            +--> MODE=DRY_RUN
            |       |
            |       +--> run_read_cycle()
            |               |
            |               +--> MT5 reads
            |               +--> analytical run_cycle()
            |               +--> NO broker writer
            |
            +--> MODE=DEMO
            |       |
            |       +--> run_live_demo()
            |               |
            |               +--> DEMO confirmation check
            |               |
            |               +--> DASHBOARD_MODE=GUI
            |               |       |
            |               |       +--> run_graphical_demo()
            |               |               |
            |               |               +--> fixed timer provider
            |               |               +--> run_guarded_demo_cycle()
            |               |
            |               +--> terminal/headless path
            |                       |
            |                       +--> run_guarded_demo_cycle()
            |
            +--> MODE=REAL
                    |
                    +--> currently rejected during Settings validation
                        because REAL_RELEASE_ENABLED=False
```

The key architectural rule is:

> Only `run_guarded_demo_cycle()` is the current write-capable governed runtime path, and it only accepts explicitly confirmed DEMO mode on an account positively verified by MT5 as DEMO.

---

## 4. Configuration ownership

Canonical settings live in:

`src/gold_scalp_trader/config/settings.py`

Compatibility import:

`src/gold_scalp_trader/config.py`

The compatibility module only re-exports the canonical configuration surface.

### Build-level REAL lock

```python
REAL_RELEASE_ENABLED = False
```

This is intentionally a source-level release policy constant rather than an environment variable.

### Important Settings fields

| Setting | Current role |
|---|---|
| `mode` | `DRY_RUN`, `DEMO`, or `REAL` |
| `demo_trading_confirm` | explicit DEMO operator approval token |
| `real_trading_confirm` | future REAL approval token; not sufficient today |
| `active_strategy_family` | required for write-capable modes |
| `target_risk_percent` | required for DEMO |
| `state_db_path` | local durable runtime state |
| `dashboard_mode` | `GUI` or `TERMINAL` |
| `bot_magic` | ownership/attribution marker |
| `bot_comment_prefix` | broker comment lineage prefix |
| `max_quote_age_seconds` | quote freshness boundary |
| `loop_interval_seconds` | governed runtime cadence |

---

## 5. Computed write permissions

`Settings` does not treat mode alone as permission.

### DEMO write property

```python
@property
def demo_write_enabled(self) -> bool:
    return (
        self.mode is RuntimeMode.DEMO
        and self.demo_trading_confirm == "YES_I_APPROVE_DEMO"
    )
```

Therefore:

```text
MODE=DEMO
```

alone is insufficient.

It must also have:

```text
DEMO_TRADING_CONFIRM=YES_I_APPROVE_DEMO
```

### REAL write property

```python
@property
def real_write_enabled(self) -> bool:
    return (
        REAL_RELEASE_ENABLED
        and self.mode is RuntimeMode.REAL
        and self.real_trading_confirm == "YES_I_APPROVE_REAL"
    )
```

Three conditions would be required:

1. source/build release lock enabled;
2. `MODE=REAL`;
3. exact REAL confirmation token.

But the current source has condition 1 fixed to false.

### Combined broker permission

```python
@property
def broker_write_enabled(self) -> bool:
    return self.demo_write_enabled or self.real_write_enabled
```

Safe defaults therefore have `broker_write_enabled == False`.

---

## 6. Environment files and safe defaults

### `.env.example`

Safe default profile:

```text
MODE=DRY_RUN
DEMO_TRADING_CONFIRM=NO
REAL_TRADING_CONFIRM=NO
```

It has zero intended broker-write capability.

### `.env.demo.example`

Explicit connected DEMO profile:

```text
MODE=DEMO
ACTIVE_STRATEGY_FAMILY=TREND_PULLBACK_CONTINUATION
TARGET_RISK_PERCENT=1.00
DEMO_TRADING_CONFIRM=YES_I_APPROVE_DEMO
REAL_TRADING_CONFIRM=NO
```

This file contains placeholders/configuration only and no account credential.

### No REAL example profile

There is intentionally no approved current REAL `.env` profile because REAL is not released.

---

## 7. Settings validation hierarchy

`validate_settings()` in `src/gold_scalp_trader/config/settings.py` enforces mode-level invariants before startup continues.

### Shared write-capable-mode requirements

For both DEMO and REAL modes:

- `ACTIVE_STRATEGY_FAMILY` must exist.

### DEMO-specific checks

DEMO requires:

- a target risk percentage;
- valid DEMO confirmation token value;
- later, at runtime, exact approval token and verified DEMO account.

### REAL-specific checks

```python
if settings.mode is RuntimeMode.REAL:
    if not REAL_RELEASE_ENABLED:
        raise ValueError("REAL trading release is not approved/enabled in this build")
    if settings.real_trading_confirm != "YES_I_APPROVE_REAL":
        raise ValueError("REAL mode requires explicit confirmation")
```

Because `REAL_RELEASE_ENABLED=False`, current `MODE=REAL` fails during configuration loading/validation before the normal trading runtime is entered.

---

## 8. Startup route

Beginner-facing launcher:

`bot.py`

Its only important responsibility is making `src/` importable from a checkout and calling:

`gold_scalp_trader.app.main.main`

Actual mode routing is owned by:

`src/gold_scalp_trader/app/main.py`

Simplified logic:

```text
load_settings()
↓
if real_write_enabled:
    refuse current release
↓
initialize MT5
↓
if mode == DEMO:
    run_live_demo()
else:
    run_read_cycle()
```

Because `validate_settings()` currently refuses REAL first, the non-DEMO branch is effectively the safe DRY_RUN path in the supported release.

`app.main` also includes a defensive `settings.real_write_enabled` refusal. In the current build this is normally unreachable because REAL validation already fails earlier; it is still a useful second defensive layer.

---

## 9. MT5 lifecycle

MT5 initialization is owned by:

`src/gold_scalp_trader/app/startup.py`

`mt5_session()`:

1. imports MetaTrader5;
2. calls `mt5.initialize()`;
3. refuses startup if initialization fails;
4. yields the MT5 module/API;
5. always calls `mt5.shutdown()` on exit.

This layer establishes connectivity but **does not itself grant trading permission**.

---

## 10. DRY_RUN call path

Current read-only route:

```text
bot.py
→ app.main.run()
→ load_settings()
→ mt5_session()
→ run_read_cycle()
→ Mt5Reader.read()
→ run_cycle()
→ presentation
```

`run_read_cycle()` is in:

`src/gold_scalp_trader/app/runtime.py`

It:

- reads normalized MT5 market/account data;
- executes the analytical decision cycle;
- returns `RuntimeResult(..., wrote_broker=False)`;
- does not construct/use `Mt5Writer`.

Therefore DRY_RUN has no normal broker-write route.

---

## 11. DEMO launcher hierarchy

DEMO is routed from `app.main` to:

`src/gold_scalp_trader/app/demo_runner.py::run_live_demo()`

The first DEMO runner check is:

```python
if settings.mode is not RuntimeMode.DEMO or not settings.demo_write_enabled:
    raise PermissionError(...)
```

This ensures both:

- actual enum mode is DEMO;
- exact DEMO confirmation token was supplied.

### GUI mode

Default:

```text
DASHBOARD_MODE=GUI
```

When GUI is selected and the run is unbounded:

```text
run_live_demo()
→ run_graphical_demo()
→ RuntimeDashboardProvider
→ run_guarded_demo_cycle()
→ immutable graphical snapshot
→ DashboardApp
```

Graphical adapter:

`src/gold_scalp_trader/app/graphical_demo_runner.py`

UI package:

`graphical_dashboard/`

Important rule:

- UI/chart controls are presentation-only;
- governed runtime advances via the provider/fixed refresh cycle;
- chart buttons do not directly invoke broker actions.

### Terminal/headless mode

When terminal mode or a bounded test run is requested:

```text
run_live_demo()
→ StateStore
→ repeated run_guarded_demo_cycle()
→ terminal presentation
→ sleep(loop interval)
```

On stop, a local checkpoint is exported and the StateStore is closed.

---

## 12. `run_guarded_demo_cycle()` — primary financial safety boundary

Location:

`src/gold_scalp_trader/app/runtime.py`

This is the central current write-capable orchestration function.

### Check 1 — explicit DEMO mode and confirmation

```python
if settings.mode is not RuntimeMode.DEMO or not settings.demo_write_enabled:
    raise PermissionError(...)
```

Failure result:

- no cycle trading action is allowed;
- no broker writer should be reached.

### Check 2 — REAL defensive refusal

```python
if settings.real_write_enabled:
    raise PermissionError("REAL write path is disabled in this release")
```

Again, current settings validation should already make this unreachable, but runtime contains the defensive refusal.

### Check 3 — read broker/account/market truth

```text
Mt5Reader(settings, api).read()
```

This reads:

- account facts;
- symbol specification;
- quote;
- completed candles;
- positions.

### Check 4 — connected account must positively be DEMO

```python
if not demo_account_verified(api):
    raise PermissionError(...)
```

This is distinct from `MODE=DEMO`.

The local config saying DEMO is not trusted as proof that the broker account is DEMO.

---

## 13. DEMO account identity verification

Location:

`src/gold_scalp_trader/market_data/account_mode.py`

Function:

`demo_account_verified(api)`

Behavior:

1. calls `api.account_info()`;
2. fails closed if unavailable;
3. reads account `trade_mode`;
4. fails closed if trade mode is missing;
5. accepts only MT5's DEMO constant or explicit DEMO string representation;
6. rejects REAL/contest/unknown modes.

This produces the essential two-key model:

```text
LOCAL INTENT:
MODE=DEMO + explicit confirmation

AND

BROKER TRUTH:
MT5 account positively reports DEMO

BOTH REQUIRED
```

A user cannot safely turn a REAL account into DEMO authority merely by changing `.env`.

---

## 14. DEMO governed cycle after account verification

Once the connected account is verified as DEMO:

```text
read market
↓
run analytical cycle
↓
reconcile unresolved Intents
↓
if ManagedTrade exists → manage it
↓
block orphan bot-magic exposure
↓
require complete TradePlan + passing Risk + volume
↓
acquire controller lease
↓
resolve symbol action capability
↓
Gate
↓
local precheck
↓
broker order_check
↓
durable ExecutionIntent
↓
persist-before-send service
↓
sole Mt5Writer
↓
reconciliation
↓
ManagedTrade / durable unresolved state
```

Each layer serves a separate purpose; `MODE=DEMO` is not itself an order permission.

---

## 15. Unresolved Intent protection

Before attempting a fresh trade, runtime calls:

`_reconcile_unresolved_intents()`

If durable unresolved Intents remain after reconciliation, the cycle returns:

```text
UNRESOLVED_INTENT_RECONCILIATION_REQUIRED
NO RESEND
```

This protects against duplicate financial actions after ambiguous acknowledgements or restart.

Execution Intent states include:

- `CREATED`
- `APPROVED`
- `SUBMITTING`
- `ACCEPTED_UNKNOWN`
- `ACCEPTED_VERIFIED`
- `FAILED`

Definitions:

`src/gold_scalp_trader/domain/enums.py`

---

## 16. Existing ManagedTrade path

If a durable ManagedTrade exists for the connected scope, the runtime does not evaluate it as a new OPEN.

It routes to:

`_run_managed_demo_cycle()`

The management path verifies:

- position data is available;
- known ticket still exists or exact close proof is available;
- symbol matches;
- direction matches;
- magic ownership matches;
- volume has not unexpectedly changed;
- management action is HOLD/PROTECT/TRAIL/RUNNER/EXIT;
- action-specific Gate/precheck requirements pass before MODIFY/CLOSE.

A missing known position is not automatically considered closed. Exact deal-history proof is required before archival/learning.

---

## 17. Orphan bot-magic position protection

If MT5 reports a position with the bot's magic number but durable ManagedTrade lineage does not exist, runtime refuses silent adoption.

It returns a recovery state similar to:

```text
ORPHAN_BOT_MAGIC_POSITION_REQUIRES_RECOVERY
```

Reason:

- broker truth and local durable lineage disagree;
- automatically assuming ownership/lifecycle state could cause duplicate or unsafe management.

---

## 18. TradePlan and Risk prerequisite

A new DEMO OPEN cannot proceed unless the analytical cycle produced:

- a valid TradePlan;
- a Risk result;
- `RiskDecision.PASS`;
- a concrete approved volume.

Missing/incomplete/blocked analytical output returns without broker write.

---

## 19. Controller lease

Before execution the runtime attempts to acquire a controller lease for the account/server/symbol scope.

Purpose:

- prevent competing local financial controllers from acting as though both own the same authority;
- provide fencing input to the execution service.

If acquisition fails:

- `controller_ready=False`;
- Gate blocks or execution does not proceed.

---

## 20. Symbol trade-mode check

Runtime normalizes MT5 symbol trade capability through:

- `symbol_allows_action()`
- `symbol_allows_open()`

Location:

`src/gold_scalp_trader/app/runtime.py`

For OPEN it distinguishes:

- FULL;
- LONGONLY;
- SHORTONLY;
- DISABLED;
- unknown.

Direction matters.

MODIFY/CLOSE are treated as exposure-management operations and use separate action semantics, while still facing broker `order_check`.

---

## 21. Gate hierarchy

The Gate receives multiple independent authority facts.

For OPEN, current inputs include:

- Risk decision;
- effective market-open fact;
- required data readiness;
- account/identity readiness;
- exposure clear state;
- persistence integrity;
- controller readiness;
- conflicting unresolved Intent state;
- action type.

Only `GateState.ALLOW` may continue to financial execution.

This prevents configuration mode from becoming equivalent to execution permission.

---

## 22. Quote/data freshness

`_data_ready()` requires required timeframes to be healthy and quote age to satisfy:

```text
0 <= quote_age <= MAX_QUOTE_AGE_SECONDS
```

A stale quote therefore blocks a new OPEN through data readiness.

For managed actions, `_management_data_ready()` applies action-appropriate requirements.

---

## 23. Important current Session integration boundary

A typed Session/News provider exists at:

`src/gold_scalp_trader/app/session_news.py`

It models states such as:

- OPEN;
- PRE_CLOSE;
- CLOSED;
- REOPEN_WARMUP;
- UNKNOWN;

and validates scoped, expiring schedule/provider facts.

However, **as of this document's current as-built revision, `run_guarded_demo_cycle()` does not automatically load that provider and use it as its normal `market_open` authority.**

Current function signature accepts:

```python
market_open: bool | None = None
```

When no explicit `market_open` value is provided, runtime currently falls back to symbol trade-mode capability for `effective_market_open`.

Therefore:

- Session provider code exists;
- Session provider tests exist;
- but full Session → guarded runtime → Gate integration remains a separate integration/audit item;
- stale quote rejection still protects data freshness;
- stale quote must **not** be interpreted as authoritative CLOSED-session proof.

This distinction must remain explicit until runtime wiring is completed and connected broker-schedule evidence exists.

---

## 24. Local and broker prechecks

After Gate ALLOW and before irreversible send, runtime performs:

### Local precheck

`execution/checks.py` via `local_precheck(...)`

It uses normalized account/symbol/quote/volume facts.

### Broker precheck

`broker_order_check(api, writer.build_request(intent))`

This asks the connected broker/MT5 environment whether the specific request is acceptable without yet using `order_send`.

Both must pass before `execute_once()` is allowed to send.

---

## 25. Durable Intent and persist-before-send

Execution service:

`src/gold_scalp_trader/execution/service.py`

Function:

`execute_once()`

Core sequence:

```text
assert Intent not previously consumed
↓
save CREATED/APPROVED Intent
↓
verify Gate
↓
verify controller lease
↓
verify prechecks
↓
save SUBMITTING with send_count=1
↓
call writer.send_once()
↓
persist outcome
```

The critical safety concept is:

> Irreversible broker send is preceded by durable execution identity and a one-shot send count.

If acknowledgement is ambiguous, the system stores `ACCEPTED_UNKNOWN` rather than blindly resending.

---

## 26. Sole irreversible MT5 writer

Location:

`src/gold_scalp_trader/execution/mt5_writer.py`

Class:

`Mt5Writer`

The writer owns raw irreversible:

```python
api.order_send(...)
```

for:

- OPEN;
- MODIFY;
- CLOSE.

It is intentionally retry-free.

### Important design fact

`Mt5Writer` itself is **mode-agnostic**. It does not read `MODE`, `DEMO_TRADING_CONFIRM`, or `REAL_RELEASE_ENABLED`.

Its safety relies on architecture:

```text
validated Settings
→ guarded DEMO runtime
→ broker DEMO identity verification
→ Gate
→ controller
→ prechecks
→ execute_once
→ Mt5Writer
```

This is an important audit invariant: no alternate runtime/module may be allowed to instantiate/use `Mt5Writer` in a way that bypasses those authorities.

The repository-wide audit should continue checking that `order_send` has no competing write path.

---

## 27. Broker acknowledgement semantics

`Mt5Writer.send_once()` classifies broker results as:

- success acknowledgement;
- explicit rejection;
- ambiguous transport/None/unknown acknowledgement.

Even a successful broker ACK is not immediately treated as final verified trade truth.

Execution service stores it as reconciliation-required state, then runtime re-reads MT5 and verifies the actual broker position/action.

This creates the distinction:

```text
ACK received
!=
financial state fully reconciled
```

---

## 28. Post-send reconciliation

After send:

- OPEN attempts matching against fresh positions;
- MODIFY verifies protective levels;
- CLOSE verifies position absence and later exact exit deal proof.

If fresh MT5 read fails after a send:

- the send is not repeated;
- durable `ACCEPTED_UNKNOWN` survives;
- a later cycle reconciles it.

This is central to crash/transport ambiguity safety.

---

## 29. DEMO state persistence

Default state DB:

```text
runtime/gold_scalp_demo.sqlite3
```

It is local and ignored by source-publication policy.

State persistence supports items including:

- ExecutionIntents;
- ManagedTrade lineage;
- controller state;
- risk/runtime state;
- closure receipts;
- learning state;
- recovery/reconciliation evidence.

GitHub is not runtime storage and is not queried for trading authority.

---

## 30. Shutdown and checkpoint behavior

### Terminal DEMO

`run_live_demo()` exports a checkpoint in `finally`, then closes StateStore.

### Graphical DEMO

`graphical_demo_runner.py::_DashboardResources.close()` exports the checkpoint and closes the store.

This means UI close and normal local stop preserve a local recovery artifact.

A checkpoint is not broker truth by itself; restart/recovery must still reconcile with current MT5 state.

---

## 31. Graphical DEMO hierarchy

Current approved route is:

```text
python bot.py
→ MODE=DEMO
→ run_live_demo()
→ DASHBOARD_MODE=GUI
→ run_graphical_demo()
→ RuntimeDashboardProvider
→ run_guarded_demo_cycle()
→ from_runtime(...)
→ DashboardApp render
```

This is important because the dashboard is not intended to maintain a separate trading engine.

The graphical provider advances the **same governed DEMO runtime** used by the terminal path.

---

## 32. Connected DEMO certification is separate from DEMO trading

Certification tooling:

- `scripts/certify_connected_demo.py`
- `scripts/monitor_connected_demo.py`
- `src/gold_scalp_trader/diagnostics/connected_demo.py`

The certification collector is explicitly read-only.

Before collecting evidence it requires:

- `MODE=DEMO`;
- MT5 account positively verified as DEMO.

It records facts such as:

- connected identity;
- symbol specification;
- quote freshness;
- durable lifecycle state;
- observed verified OPEN/MODIFY/CLOSE;
- unresolved Intent state;
- operator drill evidence.

It reports:

```text
broker_write_performed_by_this_tool = False
real_release_enabled = False
```

Certification tooling must never be confused with the broker-writing runtime.

---

## 33. DEMO certification hierarchy

```text
OFFLINE verification
    |
    +--> compile
    +--> docs/manual topology
    +--> contract sync
    +--> secret scan
    +--> pytest

CONNECTED DEMO evidence
    |
    +--> real MT5 DEMO identity
    +--> real symbol facts
    +--> quote freshness
    +--> durable state integrity
    +--> controlled lifecycle evidence
    +--> schedule/session evidence
    +--> spread/slippage/deviation evidence
    +--> latency evidence
    +--> restart/recovery drills
    +--> strategy attribution
    +--> learning evidence

FULL CONNECTED CERTIFICATION
    |
    +--> only PASS when all canonical evidence is PASS
```

Offline PASS is not REAL approval.

Connected DEMO PASS is also not automatic REAL approval.

---

## 34. REAL mode — current execution reality

Current source-level state:

```text
REAL_RELEASE_ENABLED = False
```

Therefore:

```text
MODE=REAL
↓
load_settings()
↓
validate_settings()
↓
ValueError: REAL trading release is not approved/enabled in this build
↓
normal trading runtime does not start
↓
Mt5Writer is not reached through supported entrypoint
```

Setting:

```text
REAL_TRADING_CONFIRM=YES_I_APPROVE_REAL
```

cannot override this build lock.

Likewise, GUI controls do not enable REAL.

---

## 35. Why REAL is more than “DEMO with a different account”

A future governed REAL release must not simply change:

```python
REAL_RELEASE_ENABLED = True
```

and call the work complete.

Before future REAL authority can exist, the project requires evidence/governance including:

- successful connected DEMO lifecycle certification;
- stable symbol/spec/broker behavior evidence;
- schedule/session authority integrated and proven;
- spread/slippage/deviation calibration;
- latency calibration;
- recovery/restart drills;
- ambiguity/no-duplicate proof;
- risk-state persistence proof;
- manual/broker-side close attribution;
- strategy-isolation evidence;
- security and secret review;
- explicit operator approval;
- dedicated release audit.

A future REAL implementation should be treated as a separate release engineering phase, not an environment-file edit.

---

## 36. Current check matrix — where mode/write safety is enforced

| Layer | File / function | DEMO check | REAL check | Failure behavior |
|---|---|---|---|---|
| Domain vocabulary | `domain/enums.py::RuntimeMode` | Defines DEMO | Defines REAL | No authority by itself |
| Settings properties | `config/settings.py::demo_write_enabled` | mode + exact confirmation | — | False permission |
| Settings properties | `config/settings.py::real_write_enabled` | — | build lock + REAL mode + exact confirmation | False permission |
| Settings validation | `validate_settings()` | active family, target risk, valid token | hard rejects while release disabled | startup/config error |
| App startup | `app/main.py::run()` | routes DEMO to live runner | defensive current-release refusal | runtime stopped |
| DEMO runner | `app/demo_runner.py::run_live_demo()` | exact DEMO mode + permission | not accepted | PermissionError |
| GUI DEMO runner | `app/graphical_demo_runner.py::run_graphical_demo()` | exact DEMO mode + permission | not accepted | PermissionError |
| Guarded cycle | `app/runtime.py::run_guarded_demo_cycle()` | DEMO + confirmation required | defensive refusal | PermissionError |
| Broker account truth | `market_data/account_mode.py::demo_account_verified()` | MT5 must positively report DEMO | REAL/non-DEMO rejected | PermissionError in runtime |
| Account permissions | `runtime.py::_identity_ready()` | `trade_allowed`, `trade_expert`, DEMO account | no REAL path | Gate cannot allow |
| Symbol permission | `runtime.py::symbol_allows_action/open()` | action/direction compatibility | same normalized fact only; no REAL runtime | Gate blocks/unknown |
| Data readiness | `runtime.py::_data_ready()` | healthy required data + fresh quote | no REAL runtime | Gate blocks |
| Exposure | guarded runtime/Gate | requires exposure clear for OPEN | no REAL runtime | Gate blocks |
| Persistence | `StateStore.integrity_check()` | integrity required | no REAL runtime | Gate blocks |
| Controller | execution controller | valid lease required | no REAL runtime | Gate/service blocks |
| Precheck | `execution/checks.py` | local + broker order_check | no REAL runtime | service returns FAILED |
| Durable execution | `execution/service.py::execute_once()` | one-shot persist-before-send | mode assumed already governed | no send on failed authority |
| Raw write | `execution/mt5_writer.py::send_once()` | no mode knowledge | no mode knowledge | retry-free ACK classification |
| Connected certifier | `scripts/certify_connected_demo.py` | requires DEMO + verified DEMO account | records REAL disabled | read-only, no order_send |

---

## 37. Source-code hierarchy by responsibility

```text
bot.py
└── beginner-friendly launcher

src/gold_scalp_trader/
├── config/
│   └── settings.py
│       ├── Runtime settings
│       ├── DEMO permission
│       ├── REAL release lock
│       └── validation
│
├── domain/
│   └── enums.py
│       └── DRY_RUN / DEMO / REAL vocabulary
│
├── app/
│   ├── main.py
│   │   └── top-level mode route
│   ├── startup.py
│   │   └── MT5 initialize/shutdown
│   ├── demo_runner.py
│   │   └── continuous DEMO launcher + GUI/terminal route
│   ├── graphical_demo_runner.py
│   │   └── governed DEMO ↔ GUI adapter
│   ├── runtime.py
│   │   ├── read-only cycle
│   │   ├── guarded DEMO cycle
│   │   ├── account/symbol/Gate orchestration
│   │   ├── reconciliation
│   │   └── managed trade actions
│   └── session_news.py
│       └── typed Session/News provider boundary
│
├── market_data/
│   ├── mt5_reader.py
│   │   └── normalized read-only MT5 boundary
│   └── account_mode.py
│       └── positive DEMO account verification
│
├── execution/
│   ├── gate.py
│   ├── checks.py
│   ├── controller.py
│   ├── intent_store.py
│   ├── service.py
│   │   └── persist-before-send / one-shot
│   ├── reconcile.py
│   └── mt5_writer.py
│       └── sole raw order_send boundary
│
├── management/
│   └── ManagedTrade lifecycle / closure proof
│
├── persistence/
│   ├── store.py
│   └── checkpoint.py
│
└── diagnostics/
    └── connected_demo.py
        └── connected evidence aggregation

graphical_dashboard/
└── presentation-only graphical UI

scripts/
├── certify_connected_demo.py
└── monitor_connected_demo.py
```

---

## 38. Test coverage map for mode safety

Important tests include:

### `tests/test_settings.py`

Verifies:

- safe default is DRY_RUN;
- default has no broker write capability;
- aggressive mode default false;
- manual daily-loss reset default false;
- DEMO requires active family.

### `tests/test_demo_launcher.py`

Verifies:

- application DEMO route enters `run_live_demo()` through the normal startup path.

### `tests/test_guarded_demo_runtime.py`

Verifies important guarded runtime behavior including:

- connected non-DEMO account is hard refused;
- refusal produces zero order sends;
- symbol direction/trade-mode handling;
- governed DEMO lifecycle behavior under fake MT5.

### `tests/test_graphical_runtime.py`

Covers graphical runtime/provider boundaries.

### `tests/test_execution_intent.py`

Covers durable execution Intent behavior.

### `tests/test_action_reconciliation.py`

Covers action-specific reconciliation.

### `tests/test_writer_attribution.py`

Covers writer attribution/magic/comment behavior.

### `tests/test_connected_demo_evidence.py`

Covers connected certification evidence rules and DEMO-only evidence semantics.

### `tests/test_session_news_provider.py`

Covers Session/News provider contract itself; this must not be mistaken for proof that the provider is already fully wired into the guarded runtime.

---

## 39. Known mode-related audit points

These points must remain visible until resolved/proven.

### A. Session authority wiring

Status:

`IMPLEMENTED_BUT_RUNTIME_INTEGRATION_REQUIRES_AUDIT/COMPLETION`

Provider exists and is tested, but current guarded DEMO runtime does not automatically load it as the canonical market-open authority.

### B. Raw writer mode awareness

Status:

`ARCHITECTURE_DEPENDS_ON_UPSTREAM_GOVERNANCE`

`Mt5Writer` intentionally has no mode check. This is safe only while all reachable calls remain behind the governed runtime/execution hierarchy. Repository-wide audit must continuously prove no bypass exists.

### C. REAL runtime implementation

Status:

`NOT_RELEASED / HARD_DISABLED`

There is no approved current REAL runner. REAL must not be described as merely dormant DEMO functionality.

### D. Connected proof

Status:

`OFFLINE TESTS DO NOT SUBSTITUTE FOR CONNECTED DEMO EVIDENCE`

Mode logic can pass pytest while broker-specific schedule, fill, latency, restart and lifecycle evidence remain unproven.

---

## 40. What happens for common configurations

### Case 1 — untouched safe defaults

```text
MODE=DRY_RUN
DEMO_TRADING_CONFIRM=NO
REAL_TRADING_CONFIRM=NO
```

Result:

- settings valid;
- broker_write_enabled false;
- read-only runtime.

### Case 2 — MODE=DEMO but no confirmation

```text
MODE=DEMO
DEMO_TRADING_CONFIRM=NO
```

Assuming other required DEMO settings are present:

- `demo_write_enabled` false;
- DEMO runner/guarded cycle refuses write-capable runtime.

### Case 3 — confirmed DEMO config but MT5 logged into REAL account

```text
MODE=DEMO
DEMO_TRADING_CONFIRM=YES_I_APPROVE_DEMO
```

but broker account reports non-DEMO.

Result:

- config alone does not grant authority;
- `demo_account_verified()` returns false;
- guarded runtime raises PermissionError;
- no governed order send.

### Case 4 — confirmed DEMO + verified DEMO account, but stale data

Result:

- data readiness fails;
- Gate does not ALLOW new OPEN.

### Case 5 — confirmed DEMO + verified DEMO account + unresolved Intent

Result:

- reconciliation takes priority;
- no blind resend.

### Case 6 — MODE=REAL

Current result:

- `validate_settings()` rejects startup because REAL release lock is false.

### Case 7 — MODE=REAL + REAL confirmation token

Current result remains:

- rejected because confirmation cannot override `REAL_RELEASE_ENABLED=False`.

---

## 41. Security relationship

No runtime mode requires GitHub authority.

GitHub policy requires:

- no runtime git pull/push;
- no GitHub API trade decisions;
- no live DB/checkpoint publication;
- no credentials in repository;
- no paid hosted compute dependency.

Runtime truth sources are:

```text
configuration
+ local durable state
+ MT5 broker/account/market truth
```

not GitHub.

---

## 42. Recovery relationship

Mode safety continues after restart.

A recovered local database/checkpoint cannot itself prove:

- current broker account mode;
- current positions;
- current order/deal truth;
- current market session.

Therefore fresh MT5 reconciliation remains required.

For DEMO specifically, runtime again verifies the connected account is DEMO on each guarded cycle before broker actions.

A future REAL release must preserve the same principle with its own explicit real-account/release authority instead of trusting restored local state alone.

---

## 43. Future REAL release expectations

A future implementation should include a separately audited REAL hierarchy. At minimum it must answer:

1. What exact release artifact enables REAL?
2. What independent account-mode verification proves a REAL account is intended?
3. What explicit operator approval is required?
4. Which code path is the canonical REAL runner?
5. Does REAL reuse guarded orchestration without weakening DEMO protections?
6. How is REAL distinguished in persistence/database paths?
7. How are checkpoints prevented from accidental cross-account/cross-mode reuse?
8. What evidence package proves DEMO certification before REAL enablement?
9. What emergency kill/disable authority exists?
10. Which tests would fail if the REAL lock were accidentally removed?
11. Is the raw writer still reachable from exactly one governed financial path?
12. Can any UI/env/config value bypass release governance?

Until those questions have implemented, tested and approved answers, REAL remains blocked.

---

## 44. Operator quick reference

### Safe analytical run

```text
MODE=DRY_RUN
```

Launch:

```powershell
python bot.py
```

### Approved connected DEMO profile

Use `.env.demo.example` as the template, keep MT5 open on the intended DEMO account, and launch:

```powershell
python bot.py
```

The runtime still performs broker-side DEMO account verification and all downstream gates.

### Connected DEMO evidence monitor

```powershell
python scripts/monitor_connected_demo.py
```

This monitor is read-only and does not create broker writes.

### Full connected certificate check

```powershell
python scripts/certify_connected_demo.py --require-complete
```

This also does not itself perform broker writes.

### REAL

There is **no approved REAL start command in the current release**.

---

## 45. Final invariants

The current release should satisfy these invariants:

1. Safe defaults cannot broker-write.
2. `MODE=DEMO` alone cannot broker-write.
3. DEMO confirmation alone cannot broker-write.
4. DEMO config on a non-DEMO MT5 account cannot broker-write through the governed path.
5. REAL confirmation alone cannot enable REAL.
6. `MODE=REAL` cannot start the current trading runtime.
7. A new OPEN requires Risk + Gate + identity + data + exposure + persistence + controller + precheck approval.
8. Broker writes pass through durable Intent and the sole raw MT5 writer.
9. Ambiguous acknowledgement must reconcile instead of resend.
10. Dashboard controls must not become direct broker authority.
11. GitHub must never become runtime authority.
12. Connected DEMO evidence and future REAL approval remain separate gates.
13. Session provider existence must not be falsely presented as full Session runtime integration until the call path is actually wired and proven.

The governing principle is:

> **Mode selects the permitted operating domain, but no mode string by itself grants financial authority. DEMO requires layered local approval plus positive broker DEMO identity and execution gates; REAL remains a separate unreleased capability whose build-level lock cannot be overridden by normal configuration.**
