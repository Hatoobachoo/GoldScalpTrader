# GoldScalpTrader — Persistence, Restart and Recovery

**Status:** DRAFT PRE-CHALLENGE RECOVERY CONTRACT
**Version:** 0.2-local-backup-no-auto-push
**Authority:** Durable lifecycle, strict typed state, checkpoints, rolling local backup, restore, startup reconciliation, verified-close portability, crash-safe entry-context retirement, sequential machine handoff and controller/recovery boundaries.

## 1. Purpose

Restart, crash or laptop change must not erase:

- Risk-day lineage;
- Opportunity/Episode identity;
- TradePlan lineage;
- ExecutionIntent state;
- ManagedTrade context;
- broker-close evidence;
- pending/complete learning;
- governed research/promotion state;
- controller/recovery obligations.

> Restart is not a fresh trading day unless the Risk Contract says so.
> Restored state is context, never current broker truth.
> Unknown exposure is never zero.

## 2. GoldScalpTrader difference from the reference project

GoldSwingTraderAI included graceful-shutdown repository commit/push publication.

GoldScalpTrader explicitly **does not**.

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
NO GitHub credential dependency
```

GitHub source commits occur only through deliberate development workflow, not the trading runtime.

## 3. Truth layers

| Layer | Examples | Authority |
|---|---|---|
| durable local context | RiskDay, Opportunity, TradePlan, Intent, ManagedTrade, learning/research | lifecycle/history |
| portable checkpoint | complete verified records/events + manifest | transportable context |
| local backup package | verified checkpoint + metadata/catalog/checksums | disaster recovery |
| local Git history/bundle | source/document history | source recovery, never broker truth |
| broker truth | account, positions, deals, quote, actual SL/TP | current exposure/outcome |
| recovery decision | READY / RECONCILING / BLOCKED traces | continuation permission |

Neither restore nor Git history grants broker-write authority.

## 4. StateStore contract

Initial V1 should use standard-library SQLite unless the fresh-zero audit identifies a materially better zero-cost option.

Required properties:

- explicit schema version;
- typed serialization/parsing;
- finite-number checks;
- timezone-aware UTC timestamps;
- stable IDs;
- SHA-256 or equivalent integrity metadata where useful;
- WAL/synchronous durability appropriate to the final design;
- transactional lifecycle transitions;
- append-only event/audit history where needed;
- corruption/incompatibility is explicit and fail closed.

Malformed state must never silently become `0`, `False`, empty exposure or PASS.

## 5. Durable namespaces

The complete StateStore should preserve, where implemented:

- risk-day / Account Safety P/L / cash-flow baseline / lock / reset / cooldown;
- Opportunity and Market Episode;
- TradePlan;
- ExecutionIntent/current and history;
- active ManagedTrade and objective stage;
- closed-trade learning queue;
- managed-trade closure receipt;
- StrategyMemory observations/summaries;
- research episode journal;
- candidate/discovery/promotion state;
- rollback/disable/holdout evidence;
- configuration/policy/schema identity needed to interpret records;
- every other canonical runtime namespace.

A backup may not silently omit a namespace merely because it is inconvenient.

## 6. Crash-safe Opportunity / TradePlan ordering

A TradePlan belongs to exactly one Opportunity/Episode.

### New episode replaces terminal analytical context

```text
preserve old terminal event history
→ clear mismatched old TradePlan first
→ save new active Opportunity
→ later save a new TradePlan only if new timing ENTERs
```

`Opportunity without TradePlan` can be a valid intermediate state.

`TradePlan without a matching active Opportunity` is invalid/recovery-required.

### Verified close retires entry context

```text
verified close lineage durable
→ clear TradePlan first
→ clear active Opportunity second
```

This ordering prevents stale plan attachment after crashes.

## 7. Verified-close durability

A verified managed-trade close has separate durable needs:

```text
closed_trade_learning_queue      pending downstream work
managed_trade_closure_receipt    durable proof lifecycle ended
active ManagedTrade              current-position context
active TradePlan/Opportunity     entry context to retire safely
```

Draft crash-safe sequence:

```text
verified broker close
→ persist learning queue item
→ persist closure receipt
→ clear active ManagedTrade
→ retire matching TradePlan then Opportunity
→ later reconstruct path/outcome
→ save exactly-once learning observation
→ remove queue item only after durable learning success
```

The closure receipt remains after queue consumption so restart can explain an old verified OPEN lifecycle.

An unrelated/older receipt never clears a newer Opportunity.

## 8. Portable full checkpoint

Canonical checkpoint shape may use:

```text
checkpoint_manifest.json
records.jsonl
events.jsonl
```

or an equivalent fully verifiable format.

Properties:

- write-new, never destructive overwrite;
- complete StateStore export;
- schema/policy identity;
- content hashes;
- secret scan;
- size/count metadata;
- creation time / scope identity;
- deterministic verification.

Restore:

1. verifies manifest/schema/hashes/types;
2. refuses unsafe in-place overwrite of an active DB;
3. restores into a new database/path;
4. restores lifecycle, risk, learning and research together;
5. requires fresh broker reconciliation;
6. grants no write authority merely because restore succeeded.

## 9. Local backup architecture

Default conceptual destination:

```text
C:\GoldScalpTrader_Backups\
    runtime\
    source\
    recovery-packages\
```

Actual root is configurable and should preferably sit outside the repository.

### Layer A — working local Git clone

The development machine's repository plus `.git` history is the normal local source copy.

### Layer B — rolling runtime checkpoints

Consistent verified StateStore checkpoints provide crash/restart recovery.

### Layer C — source-history bundle

At deliberate project milestones, an operator/development utility may create a local Git bundle or equivalent offline source-history package.

This is **not** required on every bot shutdown.

### Layer D — portable recovery package

A recovery package may combine:

- verified runtime checkpoint;
- backup manifest/catalog;
- source revision identity;
- optional local Git bundle reference or copy;
- configuration template/fingerprint without secrets;
- dependency/environment identity;
- checksums;
- restore instructions.

It remains context, not broker authority.

## 10. Backup destination safety

The automatic runtime backup root should be outside the active repository to prevent:

- recursive backups;
- accidental Git staging;
- repository bloat;
- mixing runtime private state with public/private source history.

A second HDD/SSD/USB destination may be configured for stronger physical-device failure protection.

Cloud sync is not required and must not become a broker/controller coordination backend.

## 11. Secret/credential exclusion

Automatic backups and portable packages must not contain authority-bearing secrets such as:

```text
.env real credentials
broker password/token
GitHub PAT/access token
API/client secret
auth/refresh token
private/recovery key
SSH private key
credential-bearing remote URL
```

The system may preserve non-secret configuration fingerprints/templates.

A secret scanner should fail closed on dangerous credential-shaped material before creating a supposedly shareable/portable package.

Logs/errors should redact credential-bearing URLs or values.

## 12. SQLite backup rule

Do not copy an actively-written SQLite database as arbitrary raw bytes and call it safe.

Use a consistent mechanism such as:

- SQLite online backup API;
- verified checkpoint/export from a read-consistent transaction;
- safely quiesced copy after writer shutdown.

The final implementation must document which mechanism owns each backup mode.

## 13. Backup cadence

Draft distinction:

```text
rolling runtime checkpoint → periodic + lifecycle milestones
final runtime checkpoint   → graceful shutdown
source Git bundle          → deliberate development/release milestone, not every shutdown
portable recovery package  → deliberate operator/release/migration action
```

Exact interval/retention remains pre-challenge.

A power loss cannot guarantee the final graceful checkpoint, so rolling durable state/checkpoints remain the crash boundary.

## 14. Retention/catalog

Backups should have stable versioned names and a catalog containing:

- backup ID;
- scope identity;
- source revision/policy/schema fingerprints;
- creation reason/time;
- checkpoint hash/counts;
- verification result;
- previous/parent lineage if useful;
- retention class.

Retention should be bounded and auditable. Exact number of hourly/daily/milestone packages remains an open decision.

Deleting old backups must never delete the active StateStore or the last verified recovery point accidentally.

## 15. Startup recovery sequence

```text
StateStore integrity
→ strict typed runtime bundle
→ current Intent / ManagedTrade / Opportunity / TradePlan
→ pending close queue / closure receipt
→ connect intended MT5 account/server/symbol
→ read current positions/deals/quote/SymbolSpec
→ reconcile unresolved Intent first
→ reconcile ManagedTrade with broker position
→ prove exact broker-side close if known ticket disappeared
→ repair only exact matching stale entry context
→ rebuild/verify Risk-day and broker-activity truth
→ refresh session/news truth
→ acquire/verify controller ownership/epoch
→ all RecoveryAuthorities PASS
→ READY
```

`app/recovery.py` performs no raw broker write.

## 16. Intent recovery

Draft semantics:

```text
terminal/none              → lifecycle may continue
APPROVED before submit     → can be cancelled/reviewed safely with zero sends
CREATED                    → review/reconcile
SUBMITTING / ACK_UNKNOWN   → broker reconciliation only; never blind resend
```

An uncertain previous send cannot be retried simply because the process restarted.

## 17. ManagedTrade recovery

A restored ManagedTrade must match fresh broker truth by exact durable identity, symbol, direction, volume and appropriate broker-derived tolerance.

If the known ticket is absent:

- reconcile unresolved Intents first;
- query exact broker exit history;
- require complete full-volume close proof;
- otherwise remain RECONCILING and retain ManagedTrade context.

Missing broker read is not verified flat.

## 18. Risk-day recovery

A new risk-day baseline may be created only under the final Risk Contract rules and with verified current equity/cash-flow/lifecycle truth.

Restart is not a risk reset.

Unknown required cash-flow truth can block new entry while a verified existing ManagedTrade remains management-capable.

## 19. MT5 recovery truth

Recovery reuses the normal MT5 read boundary; it does not create a second raw client.

```text
account facts
→ resolved symbol
→ SymbolSpec
→ positions
→ relevant deals/history
→ MT5RecoveryTruth
```

Critical distinction:

```text
MT5 verified empty collection → complete zero-position truth
MT5 unavailable/None          → DATA_UNAVAILABLE
corrupt/duplicate facts       → DATA_CORRUPT
```

Unavailable/corrupt never becomes empty exposure.

## 20. Sequential fresh-machine handoff

For the same account/symbol scope:

```text
OLD PRIMARY
→ stop new broker writes
→ safely shut down and release authority
→ create final verified local checkpoint/recovery package
→ transfer package by deliberate operator method
→ NEW machine restore into new DB
→ connect intended MT5 account/symbol
→ fresh broker reconciliation
→ validate risk/learning/lifecycle state
→ acquire local controller ownership
→ READY only after every authority passes
```

Credentials are configured separately and never transported inside the backup package by default.

## 21. Multi-machine scope rule

Different independent account/symbol scopes may run independently with separate state/learning/controller/backup lineage.

For the **same scope**, two independent local databases cannot safely act as one live bot.

Initial V1 therefore supports:

```text
one active PRIMARY per account/symbol scope
sequential handoff only
no active-active
no Git/Dropbox/Drive folder as fencing backend
```

True simultaneous failover would require certified shared atomic fencing **and** globally ordered lifecycle/learning state. It is future architecture, not current V1.

## 22. Controller/fencing recovery

A higher local fencing epoch alone is not permission.

After any takeover-like event, durable lifecycle + fresh broker truth + all recovery authorities must reconcile before write-capable READY.

Stale holder/epoch cannot send.

## 23. Graceful shutdown lifecycle

Human-visible shutdown sequence should eventually resemble:

```text
🛑 GoldScalpTrader is closing safely...
✅ New entry work stopped
✅ Trading/controller authority released
💾 Creating final verified local runtime checkpoint...
🔐 Backup secret/integrity scan passed
✅ Local runtime backup created: <backup-id/path>
✅ GoldScalpTrader closed safely.
```

If final local backup fails, show explicit failure and preserve the last known verified backup/state. Do not print a false success line.

There is deliberately no “creating Git shutdown commit” and no “pushing to GitHub” step.

## 24. Dashboard/health visibility

Expose where authoritative:

```text
State Integrity
Latest Checkpoint
Backup Catalog / Last Local Backup
Learning Evidence
Live Broker Snapshot
Open Gold Positions count / UNKNOWN
Recovery State / reason
Execution Intent state
ManagedTrade state
Controller holder/epoch
Backup root / free-space warning without secrets
```

Backup health is operational visibility, not trading signal quality.

## 25. Planned implementation ownership

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

There is no runtime `shutdown_publish.py` GitHub publisher in the intended GoldScalpTrader architecture.

## 26. Planned deterministic proof

Tests must cover:

- strict typed parsing/integrity failure;
- full StateStore checkpoint completeness;
- manifest/hash verification;
- restore-to-new-DB;
- secret exclusion/redaction;
- safe SQLite backup consistency;
- rolling/final local backup catalog;
- exact closure-receipt crash repair;
- plan-first Opportunity cleanup;
- unresolved Intent no-resend;
- known-position close recovery;
- risk-day persistence;
- local controller fencing;
- sequential handoff semantics;
- graceful shutdown local-backup success/failure presentation;
- explicit absence of runtime Git commit/push dependency.

Connected Windows/MT5 proof remains required for real restart/handoff/broker continuity.

## 27. Non-goals

Recovery must not:

- treat backup as current broker truth;
- convert unknown exposure to zero;
- blind-resend uncertain Intent;
- invent ManagedTrade context;
- clear ownership before reconciliation;
- use unrelated closure receipt for cleanup;
- merge two active same-scope production stores automatically;
- include credentials in backup packages;
- require GitHub/network availability for safe shutdown;
- auto-commit/push from the trading runtime.

## 28. Pre-challenge questions

- SQLite remains final V1 store or not;
- checkpoint cadence;
- retention tiers/counts;
- backup free-space threshold;
- second-drive replication UX;
- portable package exact contents;
- local Git bundle cadence;
- encryption-at-rest option for private runtime backups without complicating recovery;
- checksum/catalog format;
- fresh-machine restore drill acceptance criteria.
