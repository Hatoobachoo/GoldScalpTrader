# GoldScalpTrader — Persistence, Restart and Recovery

**Status:** DRAFT PRE-CHALLENGE RECOVERY CONTRACT
**Version:** 0.1-local-recovery
**Authority:** Durable lifecycle, strict state, checkpoint, local backup, restore, startup reconciliation and current V1 coordination boundaries.

## 1. Purpose

Restart, crash or laptop change must not erase obligations, risk lineage, Intent identity, Opportunity state, managed-trade context, pending closure evidence or learning history.

Two rules dominate:

> Restart is not a fresh trading day unless the documented Risk rules say so.

> Restored state is context, never broker truth. Unknown exposure is never zero.

## 2. Durable-state classes

Candidate durable classes include:

- runtime identity/policy/schema version;
- account/symbol scope identity;
- risk-day baseline and safety state;
- cooldown/loss-lock state;
- persistent Opportunity lifecycle;
- current structural Trade Plan lineage where needed;
- ExecutionIntent and submission/reconciliation state;
- managed bot-trade context;
- broker activity attribution/closure receipts;
- learning queue and exactly-once receipts;
- governed research/promotion state where applicable;
- backup/restore manifests and health records.

Exact schemas belong to implementation/module contracts later.

## 3. State store candidate

SQLite is the initial V1 candidate because it is local, transactional, portable and zero-cost.

The fresh-zero challenge may change implementation technology, but the semantics remain:

- atomic durable transitions;
- explicit schema/policy versions;
- integrity/checksum verification where appropriate;
- corruption must be visible;
- no silent “start empty” fallback when required state cannot be trusted.

## 4. Startup recovery order

```text
validated config
→ open/verify durable store
→ connect/read MT5
→ verify account + resolved Gold symbol
→ read current positions/orders/deals as required
→ reconcile pending/uncertain Intents
→ recover broker-side closures
→ reconcile managed-trade ownership
→ rebuild/verify risk-day state
→ validate Opportunity/Trade Plan freshness against current truth
→ validate session/provider/system state
→ expose unresolved required truth as UNKNOWN/BLOCKED
→ only then allow new-entry authority
```

## 5. Broker truth wins

Examples:

- Local state says flat but broker shows exposure → do not open a new trade; reconcile ownership/exposure.
- Local state says active managed trade but broker is flat → search/verify close lineage before retiring state/learning.
- Local Intent says submission uncertain → reconcile before any resend.
- Restored old Opportunity exists but originating event is no longer fresh → retire/expire according to timing contract rather than resurrect it blindly.

## 6. Checkpoint philosophy

Checkpointing is a recovery optimization, not a substitute for durable transition/event truth.

Preferred semantics:

1. create/write a new checkpoint artifact;
2. validate it;
3. atomically mark/adopt it where implementation permits;
4. never destructively overwrite the only known-good recovery artifact first.

## 7. Rolling local runtime backup

Runtime backup protects against database corruption/operator mistakes and supports machine recovery.

Default design:

```text
<configured backup root>\runtime\
    latest-known-good\
    rolling\YYYYMMDD-HHMMSS\
```

Backup creation must use a transactionally safe method. For SQLite, implementation should use SQLite backup semantics or an equivalent consistent snapshot rather than copying a live database file unsafely.

## 8. Backup triggers

Pre-challenge candidate triggers:

- controlled startup baseline after state verification;
- periodic rolling snapshot when durable state has materially changed;
- after critical lifecycle milestones if justified by I/O testing;
- mandatory graceful-shutdown runtime snapshot when durable state exists;
- explicit operator/manual backup command.

Exact cadence/retention is an implementation/research decision, not yet frozen.

## 9. Graceful shutdown

Target shutdown path:

```text
stop new-entry acceptance
→ finish/record safe in-flight local obligations
→ flush durable store/events/logs
→ create verified local runtime snapshot
→ write shutdown/backup receipt
→ release controller/MT5 resources
→ terminate
```

The shutdown path MUST NOT automatically commit or push to GitHub.

Runtime does not require repository credentials.

## 10. Local source-history backup

Source/history backup is separate from runtime-state backup.

Preferred zero-cloud mechanism:

- normal local `.git` history exists in the working clone;
- at controlled milestones or explicit operator command, create a local `git bundle` containing repository history/refs;
- store the bundle outside the working tree;
- optionally copy it to a second local physical drive/USB.

Creating a Git bundle on every trading-loop event or every shutdown is not required by the current design.

## 11. Portable recovery package

A portable package may combine:

- local Git bundle or approved source snapshot;
- verified runtime-state snapshot;
- policy/schema/version manifest;
- checksums/fingerprints;
- non-secret configuration template;
- selected logs/evidence where explicitly requested.

Automatic package creation excludes:

- `.env`;
- passwords;
- access tokens;
- GitHub credentials;
- MT5 credentials;
- unrelated personal files.

## 12. Secret recovery boundary

Secret recovery is an operator-managed process separate from ordinary backup archives.

The project should document how to restore required credentials on a fresh machine without ever committing or automatically packaging them in source/recovery artifacts.

## 13. Restore order

A restore must create/validate a recoverable copy rather than overwriting the only current state blindly.

Candidate flow:

1. select backup by manifest;
2. verify checksum/fingerprint/schema compatibility;
3. restore into a new location/state file;
4. start runtime in READINESS/recovery mode;
5. connect to MT5;
6. reconcile restored context against current broker truth;
7. repair/retire stale obligations under explicit contracts;
8. only then promote restored state to normal runtime use.

## 14. Machine handoff

Initial V1 candidate:

- one active production PRIMARY per account/symbol scope;
- same-scope movement between laptops is sequential, not active-active;
- source/runtime recovery package may be used to seed the next machine;
- the new machine must complete broker reconciliation before write authority;
- previous writer must be stopped/released first.

## 15. Backup health

Backup health is operational truth, not a trading signal by itself.

The runtime/dashboard should eventually distinguish:

- last successful runtime backup;
- backup age;
- backup verification/fingerprint state;
- backup failure reason;
- configured destination availability;
- restore drill/evidence status.

Whether a backup failure blocks new entries is a separate policy question. It must not be guessed implicitly.

## 16. Failure cases to test

Deterministic test design must later cover at least:

- corrupted durable DB/checksum;
- crash before Intent send;
- crash after send before reconciliation;
- broker-side SL/TP while runtime offline;
- restart with broker exposure unknown;
- stale Opportunity after long downtime;
- backup destination unavailable;
- interrupted backup write;
- corrupted backup manifest;
- restore incompatible schema;
- attempted same-scope second writer;
- graceful shutdown succeeds locally with network/GitHub unavailable.

## 17. GitHub independence

GitHub remote unavailability must not prevent safe local shutdown, state flush or local backup.

Repository synchronization happens through controlled developer/operator source-control workflow, not the trading lifecycle.
