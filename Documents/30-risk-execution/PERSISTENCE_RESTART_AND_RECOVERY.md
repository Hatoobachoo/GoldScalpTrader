# GoldScalpTrader — Persistence, Restart and Recovery

**Status:** FROZEN V1 RECOVERY ARCHITECTURE — IMPLEMENTATION / CONNECTED RESTORE PROOF PENDING
**Version:** 1.0-profiled-risk-local-recovery-no-runtime-git
**Authority:** Durable lifecycle, strict typed state, checkpoints, rolling local backup, restore, startup reconciliation, verified-close portability, crash-safe entry-context retirement, sequential machine handoff and controller/recovery boundaries.

## 1. Purpose

Restart, crash or laptop change must not erase:

- UTC Risk-day lineage and fixed DayStartEquity profile identity;
- explicit aggressive-small-account enable/policy identity;
- daily-loss lock/reset/cooldown/re-entry state;
- Opportunity/Episode identity;
- TradePlan lineage;
- ExecutionIntent state;
- ManagedTrade context and verified partial/full-close lineage;
- broker-close evidence;
- pending/complete learning;
- governed research/promotion state;
- controller/recovery obligations.

> Restart is not a fresh trading day unless the Risk Contract says so.
> Restored state is context, never current broker truth.
> Unknown exposure is never zero.

## 2. Explicit operator-directed Git boundary

GoldSwingTraderAI included graceful-shutdown repository publication. GoldScalpTrader explicitly does not.

```text
graceful shutdown
→ stop new work
→ flush/verify local durable state
→ release broker/controller authority safely
→ create final verified local checkpoint/backup
→ report local backup result
→ terminate

NO git add
NO git commit
NO git push
NO git pull/fetch requirement
NO GitHub credential dependency
```

GitHub source changes occur only through deliberate development workflow, never trading runtime.

## 3. Truth layers

| Layer | Examples | Authority |
|---|---|---|
| durable local context | Risk day/profile/overlay, Opportunity, Plan, Intent, ManagedTrade, learning/research | lifecycle/history |
| verified checkpoint | complete consistent StateStore export + manifest | transportable context |
| local recovery package | checkpoint + metadata/catalog/checksums | disaster/machine recovery |
| local working Git clone | source/Documents/tests + full `.git` history | source recovery, never broker truth |
| optional source ZIP | secret-clean milestone snapshot | extra offline source copy |
| optional Git bundle | advanced/manual Git-history archive | source history only |
| broker truth | account, positions, deals, quote, actual SL/TP | current financial/exposure truth |
| recovery decision | READY / RECONCILING / BLOCKED | continuation permission |

No restore/source artifact grants broker-write authority.

## 4. V1 StateStore architecture

V1 uses local transactional SQLite as the durable runtime-state architecture.

Implementation choices still to prove include WAL/synchronous mode, exact schema/migration mechanism, checksums/integrity metadata and checkpoint/export implementation.

Required properties:

- explicit schema version;
- typed serialization/parsing;
- finite-number checks;
- timezone-aware UTC timestamps;
- stable IDs;
- integrity metadata where useful;
- transactional lifecycle transitions;
- append-only event/audit history where needed;
- explicit corrupt/incompatible handling;
- no malformed state silently becoming `0`, `False`, empty exposure or PASS.

## 5. Durable namespaces

Complete StateStore/checkpoint preserves where implemented:

- Risk-day ID / DayStartEquity;
- fixed `SMALL / MEDIUM / NORMAL` profile identity;
- `AGGRESSIVE_SMALL_ACCOUNT` enabled/disabled state + policy version;
- Account Safety P/L / cash-flow baseline;
- loss lock / governed reset / reset count;
- consecutive-loss counter / cooldown / same-episode re-entry state;
- Opportunity / Market Episode;
- TradePlan;
- ExecutionIntent current/history;
- active ManagedTrade / objective stage / remaining volume;
- verified partial-management lineage where applicable;
- closed-trade learning queue;
- ManagedTrade closure receipt;
- StrategyMemory observations/summaries;
- research episode journal;
- candidate/discovery/promotion/rollback state;
- configuration/policy/schema identity needed to interpret records;
- every other canonical durable namespace.

A “full” backup cannot silently omit a namespace because it is inconvenient.

## 6. Crash-safe Opportunity / TradePlan ordering

A TradePlan belongs to exactly one Opportunity/Episode.

### New episode replaces terminal analytical context

```text
preserve old terminal history
→ clear mismatched old TradePlan first
→ save new active Opportunity
→ later save new TradePlan only after valid new ENTER
```

`Opportunity without TradePlan` can be valid. `TradePlan without matching active Opportunity` is recovery-invalid.

### Verified close retires entry context

```text
verified close lineage durable
→ clear TradePlan first
→ clear active Opportunity second
```

## 7. Verified-close durability

Keep separate:

```text
closed_trade_learning_queue      pending downstream learning work
managed_trade_closure_receipt    durable proof lifecycle ended
active ManagedTrade              current verified trade context
active TradePlan/Opportunity     entry context
```

Crash-safe sequence:

```text
verified full broker close
→ persist learning queue item
→ persist closure receipt
→ clear active ManagedTrade
→ retire matching TradePlan then Opportunity
→ later reconstruct causal outcome
→ exactly-once StrategyMemory save
→ remove queue only after durable learning success
```

Preserved broker-valid partial management does not count as full close until complete original managed volume is reconciled closed.

## 8. Portable full checkpoint

Canonical shape may use:

```text
checkpoint_manifest.json
records.jsonl
events.jsonl
```

or an equivalent verifiable format.

Properties:

- write-new rather than destructive overwrite;
- complete StateStore export;
- schema/policy identity;
- content hashes;
- secret scan;
- size/count metadata;
- creation time / scope identity;
- deterministic verification.

Restore:

1. verify manifest/schema/hashes/types;
2. refuse unsafe in-place overwrite of active DB;
3. restore into a new database/path;
4. restore lifecycle, Risk, learning and research together;
5. re-read current broker truth;
6. reconcile all durable lifecycle state;
7. acquire/verify controller authority;
8. grant no write permission merely because restore succeeded.

## 9. Runtime backup architecture

Conceptual root outside repository:

```text
C:\GoldScalpTrader_Backups\
    runtime\
    learning\
    recovery-packages\
    source-zips\
```

Path is configurable.

### Layer A — transactional live StateStore
Primary durable local runtime state.

### Layer B — rolling verified runtime checkpoints
Periodic/lifecycle-consistent recovery points.

### Layer C — final graceful-shutdown checkpoint
Created after new work stops and broker/controller authority is safely released/quiesced as required.

### Layer D — portable runtime recovery package
Deliberate migration/disaster-recovery artifact with manifest, checkpoint identity, source revision/config fingerprints, checksums and restore instructions; secrets excluded.

Runtime backup is independent of GitHub/network.

## 10. Development/source backup — operator-preferred normal workflow

Development source backup is separate from runtime-state backup.

After a **major coherent documentation/code bulk**:

```text
one remote fast-forward commit
→ operator runs git pull --ff-only
→ local working clone contains latest project + complete Git history
→ optional secret-clean ZIP milestone snapshot
```

The pulled working clone is the normal source/history backup.

Do not require a pull after every micro-patch.

### Optional source ZIP

May contain current source/Documents/config samples/tests/scripts while excluding `.env`, credentials/private keys, virtualenvs, caches, logs, runtime SQLite/checkpoints and nested backup folders.

### Optional Git bundle

Git bundle is **advanced/manual only** for a history-bearing offline archive. It is not a normal runtime or per-bulk dependency and is never invoked by trading runtime.

## 11. Backup destination safety

Automatic runtime backup root stays outside active repository to prevent recursion, accidental staging, repository bloat and mixing private runtime state with source history.

Optional second HDD/SSD/USB copy may improve physical-device resilience. Cloud sync is optional archival transport only, never controller fencing or live transactional coordination.

## 12. Secret/credential exclusion

Automatic/shareable artifacts exclude:

```text
real .env credentials
broker password/token
GitHub PAT/access token
API/client secret
auth/refresh token
private/recovery key
SSH private key
credential-bearing remote URL
```

Preserve only non-secret configuration templates/fingerprints. Secret scanner fails shareable/portable publication on dangerous material.

## 13. SQLite backup rule

Never copy an actively-written SQLite file as arbitrary bytes and call it verified.

Use a consistent method such as SQLite online backup API, read-consistent export/checkpoint or safely quiesced copy after writer shutdown. Exact mechanism is implementation proof.

## 14. Backup cadence / retention

```text
transactional StateStore       continuous durable state
rolling runtime checkpoint     periodic + important lifecycle milestones
final runtime checkpoint       graceful shutdown
source pull/local clone sync   after major coherent development bulk
optional source ZIP            important development/release milestone
optional Git bundle            advanced/manual milestone only
portable recovery package      deliberate operator/release/migration action
```

Exact runtime checkpoint interval, retention counts and disk thresholds are implementation/operational choices.

A power loss cannot guarantee final graceful checkpoint, so transactional state + rolling checkpoints remain crash boundary.

## 15. Backup catalog

Track backup ID, scope, source revision, policy/schema fingerprints, creation reason/time, checkpoint hash/counts, verification result and retention class.

Deletion must never remove active StateStore or last verified recovery point accidentally.

## 16. Startup recovery sequence

```text
StateStore integrity
→ strict typed runtime bundle
→ current Risk-day/profile/overlay/reset/cooldown state
→ Intent / ManagedTrade / Opportunity / TradePlan
→ pending learning queue / closure receipt
→ connect intended MT5 account/server/symbol
→ read current positions/deals/quote/SymbolSpec
→ reconcile unresolved Intent first
→ reconcile ManagedTrade with broker
→ prove exact broker close if known ticket disappeared
→ repair only exact matching stale entry context
→ rebuild/verify broker activity + Account Safety P/L truth
→ revalidate session/news/cache truth
→ acquire/verify controller ownership/epoch
→ all RecoveryAuthorities PASS
→ READY
```

Recovery performs no raw broker write.

## 17. Intent recovery

```text
terminal/none            → lifecycle may continue
APPROVED before submit   → cancel/review safely with zero sends
CREATED                  → review/reconcile
SUBMITTING / ACK_UNKNOWN → broker reconciliation only; never blind resend
```

Restart never grants a new send allowance to uncertain previous Intent.

## 18. ManagedTrade recovery

Restored ManagedTrade must match fresh broker truth by durable identity, symbol, direction, volume and broker-tolerance rules.

Known ticket absent:

- reconcile unresolved Intents first;
- query exact broker exit history;
- require full-volume close proof;
- otherwise remain RECONCILING and retain context.

Missing broker read is never verified flat.

## 19. Risk-day recovery

Restart does not reset Risk day/profile.

New DayStartEquity/profile may be created only under `RISK_CONTRACT.md` with verified equity/cash-flow/lifecycle truth.

Aggressive mode does not auto-enable after restart because equity happens to be below $1,000; explicit persisted/configured enable state and eligibility must both pass.

Manual reset count/lock/cooldown/re-entry state survives restart.

## 20. MT5 recovery truth

Reuse normal MT5 read boundary:

```text
account facts
→ resolved symbol
→ SymbolSpec
→ positions
→ relevant deals/history
→ MT5RecoveryTruth
```

```text
verified empty collection → complete zero-position truth
MT5 unavailable/None      → DATA_UNAVAILABLE
corrupt/duplicate facts   → DATA_CORRUPT
```

Unavailable/corrupt never becomes empty exposure.

## 21. Sequential fresh-machine handoff

```text
OLD PRIMARY
→ stop new broker writes
→ safe shutdown / release authority
→ final verified local checkpoint/recovery package
→ deliberate transfer
→ NEW machine restore into new DB
→ configure credentials separately
→ connect intended account/symbol
→ fresh broker reconciliation
→ validate Risk/lifecycle/learning
→ acquire controller
→ READY only after all authorities pass
```

If old writer state is uncertain, new machine remains blocked until single-writer safety is established.

## 22. Multi-machine scope rule

Different independent account/symbol scopes may run independently.

Same scope:

```text
one active PRIMARY
sequential handoff only
no active-active
no Git/Dropbox/Drive folder as fencing backend
```

True simultaneous failover would require a separate shared atomic-fencing/state architecture.

## 23. Controller/fencing recovery

Higher local fencing epoch alone is not permission. Durable lifecycle + fresh broker truth + all recovery authorities must reconcile before write-capable READY. Stale holder/epoch cannot send.

## 24. Graceful shutdown operator flow

```text
🛑 stopping new work
✅ resolving/persisting safe lifecycle state
✅ releasing trading/controller authority
💾 creating final verified local runtime checkpoint
🔐 secret/integrity scan
✅/❌ explicit local backup result
✅ safe process close
```

There is deliberately no “creating Git shutdown commit” or “pushing to GitHub” step.

## 25. Dashboard/health visibility

Expose State Integrity, active Risk profile/aggressive mode, Latest Checkpoint, Last Local Backup, Learning Evidence, current broker snapshot/exposure, Recovery reason, Intent, ManagedTrade, controller holder/epoch and backup disk/free-space warning without secrets.

Backup health is operational visibility, not signal quality.

## 26. Planned implementation ownership

```text
src/gold_scalp_trader/persistence/store.py
src/gold_scalp_trader/persistence/runtime_state.py
src/gold_scalp_trader/persistence/checkpoint.py
src/gold_scalp_trader/persistence/backup.py
src/gold_scalp_trader/persistence/local_recovery_package.py
src/gold_scalp_trader/app/recovery.py
src/gold_scalp_trader/app/recovery_mt5.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/research/learning.py
src/gold_scalp_trader/research/live_learning.py
src/gold_scalp_trader/execution/controller.py
src/gold_scalp_trader/execution/sqlite_coordination.py
```

No runtime Git publisher exists.

## 27. Planned deterministic / connected proof

Tests cover strict parsing/integrity, full namespace checkpoints, manifest/hash verification, restore-to-new-DB, secret exclusion, consistent SQLite backup, rolling/final catalog, closure-receipt crash repair, Plan/Opportunity cleanup, unresolved Intent no-resend, known-position close recovery, Risk profile/overlay/reset/cooldown persistence, controller fencing, sequential handoff, shutdown success/failure presentation, source pull/ZIP separation and absence of runtime Git operations.

Connected Windows/MT5 proof validates real restart/handoff/broker continuity.

## 28. Non-goals

Recovery must not treat backup as current broker truth, convert unknown exposure to zero, blind-resend Intent, invent ManagedTrade, clear ownership before reconciliation, merge active same-scope stores, include credentials, require GitHub for safe shutdown or silently change preserved Risk/session policy.

## 29. Implementation / external choices pending

SQLite WAL/synchronous/migration/checksum details, runtime checkpoint cadence/retention, backup free-space thresholds, optional encryption, second-drive UX, recovery-package exact file format and fresh-machine drill acceptance criteria remain implementation/external-proof choices.

The source backup workflow, no-runtime-Git rule, SQLite V1 architecture, preserved Risk identity and sequential same-scope handoff are frozen.