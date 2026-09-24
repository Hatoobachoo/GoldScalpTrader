# GoldScalpTrader — Learning Backup and Multi-Machine Contract

**Status:** DRAFT PRE-CHALLENGE BACKUP/PORTABILITY CONTRACT
**Version:** 0.1-local-first-no-autopush
**Authority:** Durable project/runtime/research backup, learning lineage portability, local recovery packaging, laptop handoff and multi-machine safety boundary.

## 1. Purpose

GoldScalpTrader must not lose project history, runtime lifecycle, risk history, broker-operation lineage, pending/completed learning, governed discovery or promotion history when the process restarts or the operator changes laptops.

This contract intentionally differs from GoldSwingTraderAI in one important respect:

> GoldScalpTrader does **not** perform automatic GitHub publication/push on graceful shutdown.

GitHub remains a controlled source-control/remote-backup surface outside trading authority.

## 2. Scope rule

The current V1 candidate is scoped by account/symbol identity:

> Preserve all durable project/runtime/research state while allowing only one production PRIMARY writer for the same account/symbol scope at a time.

Different independent account/symbol scopes may later run on different machines if their state and broker exposure are genuinely independent.

A second machine must not control the same account/symbol scope concurrently without a future distributed-coordination design.

## 3. Backup layers

The design separates four recovery concerns:

### Layer A — Working source clone

Normal local repository working directory and `.git` history.

Purpose:
- day-to-day source work;
- local commit history;
- immediate rollback/inspection.

### Layer B — Rolling runtime state

Consistent snapshots of runtime/persistence/research state stored outside the repository.

Purpose:
- DB corruption recovery;
- restart/laptop migration context;
- risk/Intent/learning continuity.

### Layer C — Local source/history bundle

A local Git bundle or equivalent complete Git-history artifact created at controlled milestones/manual command.

Purpose:
- reconstruct source/history even when GitHub is unavailable;
- portable offline project backup.

### Layer D — Portable recovery package

Manifest-driven package containing approved source/history + runtime/research state + fingerprints.

Purpose:
- deliberate fresh-machine restore;
- disaster-recovery drill;
- portable handoff.

## 4. Backup destination

Default concept:

```text
C:\GoldScalpTrader_Backups\
    source\
    runtime\
    learning\
    recovery-packages\
    manifests\
```

The path must be configurable.

Backups should live outside the repository working tree to prevent:
- recursive inclusion;
- accidental Git tracking;
- repository bloat;
- runtime state becoming source authority.

An operator may point the root to another local drive or removable USB for stronger protection against failure of the primary disk.

## 5. What must be preservable

Subject to implementation schemas, durable recovery should preserve:

- Git source/history artifact when requested;
- runtime DB/checkpoints/events;
- risk-day state;
- Opportunity/Trade Plan lineage required for recovery;
- pending/uncertain ExecutionIntents;
- ManagedTrade/closure receipts;
- broker-activity attribution state;
- StrategyMemory;
- pending/completed live-learning queue/receipts;
- research candidate registry/evidence lineage;
- promotion/rollback records;
- policy/schema/config fingerprint;
- backup manifests/checksums.

## 6. Secret exclusion

Automatic backups and portable packages MUST exclude:

- `.env`;
- broker passwords;
- API keys/tokens;
- GitHub credentials;
- private SSH keys;
- unrelated browser/profile data;
- any secret not explicitly governed by a separate operator-controlled recovery procedure.

The backup system must not print secret values in manifests/logs.

## 7. Source bundle policy

Preferred source-history mechanism is local `git bundle` because it can preserve Git history without network publication.

Candidate milestone/manual process:

```text
git bundle create <backup-root>\source\GoldScalpTrader-<timestamp>.bundle --all
```

The exact command/path will be implemented and tested later; this document defines the ownership and purpose, not shell quoting details.

A source bundle is not required on every trading shutdown.

## 8. Runtime backup policy

Runtime backups should be lightweight, consistent and rolling.

Candidate triggers:
- after verified startup baseline/reconciliation;
- periodically when state changed;
- after selected critical lifecycle milestones if I/O tests justify it;
- graceful shutdown;
- explicit operator command.

Exact cadence/retention remains an implementation choice.

## 9. Learning portability

Learning state must remain tied to evidence lineage and production policy identity.

On restore/migration:
- StrategyMemory keeps version/policy/dataset or broker lineage as applicable;
- pending learning cannot be ingested twice;
- already-completed learning receipts prevent duplicate ingestion;
- corrupted/missing required evidence remains UNKNOWN/blocked rather than reconstructed from guesses;
- a restored learning database never gains broker authority.

## 10. Manifest

Every portable recovery package should carry a machine-readable/human-readable manifest with fields such as:

- package ID;
- creation UTC timestamp;
- project/repository revision where known;
- package type;
- runtime schema version;
- policy/config fingerprint excluding secrets;
- account/symbol scope identity in non-secret form where appropriate;
- included artifact list;
- per-artifact size/hash;
- backup method/version;
- verification result;
- source machine label if configured;
- notes/exclusions.

## 11. Retention

Pre-challenge retention model:

- runtime rolling backups: keep a bounded recent set;
- verified milestone backups: keep longer;
- portable recovery packages: operator-controlled bounded archive;
- source Git bundles: milestone/manual, not high-frequency.

Retention numbers are not frozen until disk-use and recovery-needs are tested.

Deletion/rotation must never remove the only currently verified recovery artifact before a replacement is verified.

## 12. Restore drill

A backup system is incomplete until restoration is tested.

Target drill:

1. select a known backup package;
2. verify manifest/checksums;
3. restore source into a new folder or clone from local bundle;
4. restore runtime state into a new safe location;
5. install/verify dependencies locally;
6. configure secrets manually from operator-held source;
7. start in READINESS/recovery mode;
8. connect to MT5;
9. reconcile current broker truth;
10. verify no duplicate Intent/order authority;
11. verify learning receipts/state;
12. only then allow normal PRIMARY startup.

## 13. Same-scope laptop handoff

Candidate V1 sequence:

```text
old PRIMARY stops accepting new entries
→ durable state flush + local runtime backup
→ optional portable recovery package
→ old PRIMARY fully stops/releases ownership
→ package/source moves to new laptop
→ new laptop restores in READINESS mode
→ broker/state reconciliation
→ ownership/fencing verification
→ new PRIMARY may start
```

There is no simultaneous same-scope active-active handoff.

## 14. GitHub relationship

GitHub may remain an additional remote source/history backup through normal developer pushes.

But:
- runtime does not require GitHub connectivity;
- runtime does not hold GitHub credentials for trading;
- graceful shutdown does not push;
- backup success does not depend on GitHub;
- local restore can be tested with GitHub unavailable.

## 15. Zero-cost principle

This local backup design requires no paid cloud storage or compute.

Potential storage costs are only the operator's existing local disk/USB hardware. The software architecture itself uses local filesystem/Git/SQLite capabilities.

## 16. Operator visibility

The operator should eventually see, without secrets:

- configured backup root;
- last runtime backup time/status;
- last verified package/bundle time;
- backup age;
- most recent verification result;
- restore drill status;
- warning when destination is unavailable/full/failed.

These indicators are read-only and do not become strategy signals.

## 17. Challenge targets

Fresh-zero review must decide:
- runtime backup cadence;
- retention counts/age policy;
- whether source bundle should be generated automatically on development milestones or manual only;
- whether graceful shutdown backup is mandatory for every runtime mode;
- which logs/research datasets belong in portable packages;
- backup compression format;
- checksum algorithm/manifest format;
- whether optional second-drive mirroring belongs in V1;
- how backup-health failure affects trading permission, if at all.
