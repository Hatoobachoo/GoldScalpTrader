# GoldScalpTrader — Learning Backup and Multi-Machine Contract

**Status:** DRAFT PRE-CHALLENGE LOCAL RECOVERY CONTRACT
**Version:** 0.2-local-only-learning-backup
**Authority:** Durable full-state backup, learning lineage, local recovery packages, closure receipts, laptop handoff and per-scope multi-machine safety boundary.

## 1. Purpose

GoldScalpTrader must not lose runtime lifecycle, risk history, broker-operation lineage, pending/completed learning, discovery or promotion history when the process restarts or the operator changes laptops.

V1 scope rule:

> Preserve all durable project/runtime/research state and allow only one active production PRIMARY writer for the same account/symbol scope at a time.

Different independent account/symbol scopes may run separately with separate broker exposure, state, learning and backups.

## 2. Difference from GoldSwingTraderAI

The reference project automatically committed/pushed verified shutdown archives to GitHub.

GoldScalpTrader explicitly removes that feature.

```text
graceful PRIMARY shutdown
→ final verified local full checkpoint
→ optional focused local learning artifact
→ local backup catalog updated
→ controller/MT5 already safely released
→ shutdown result shown

NO automatic Git commit
NO automatic Git push
NO GitHub credential dependency
```

## 3. Backup layers

```text
live/research producers
→ checksum/integrity-protected StateStore
→ rolling local full checkpoints
→ graceful-shutdown final local checkpoint
→ optional focused local learning package
→ portable recovery package for deliberate handoff
```

The full checkpoint is the runtime recovery authority. Focused learning packages are review/research conveniences, not complete machine-recovery authority.

## 4. Full checkpoint completeness

The full StateStore snapshot preserves all current durable records plus required event history, including when present:

- risk-day/cash-flow/loss-lock/reset/cooldown;
- Opportunity/Episode/TradePlan;
- ExecutionIntent lifecycle;
- ManagedTrade;
- `closed_trade_learning_queue`;
- `managed_trade_closure_receipt`;
- StrategyMemory raw observations/summaries;
- research episode journal;
- strategy candidate/discovery state;
- promotion/holdout/rollback/disable state;
- configuration/policy/schema identities;
- all other canonical durable namespaces.

Backup must not rebuild state from a hand-picked subset.

## 5. Credential boundary

Automatic/local recovery artifacts must exclude authority-bearing credentials:

```text
broker password/token
GitHub PAT/access token
API/client secret
auth/refresh token
SSH/private/recovery key
credential-bearing remote URL
real .env secrets
```

Non-secret runtime identity needed for safe scope verification may be included where disclosure risk is acceptable.

Secret scanning fails closed before a package is marked portable/shareable.

## 6. Local rolling backup root

Conceptual default:

```text
C:\GoldScalpTrader_Backups\runtime\
C:\GoldScalpTrader_Backups\learning\
C:\GoldScalpTrader_Backups\recovery-packages\
```

The root is configurable and should normally be outside the Git working tree.

A second physical drive/USB destination may be used for device-failure resilience.

## 7. Focused learning package

A focused local learning artifact may contain audited learning/research namespaces such as:

- StrategyMemory;
- pending learning queue;
- research episode journal;
- candidate/discovery/promotion records;
- evidence/config fingerprints.

It is not a substitute for full runtime checkpoint because lifecycle-only records such as closure receipts/risk/Intent state may be required for safe recovery.

## 8. Closure receipt and learning queue

```text
closed_trade_learning_queue     → pending post-close learning
managed_trade_closure_receipt   → durable proof managed lifecycle ended
```

The queue may disappear after successful StrategyMemory ingestion. The closure receipt remains as lifecycle proof.

Full backup preserves both automatically.

## 9. Production learning ownership

Exactly one writer per account/symbol production scope:

```text
Scope A PRIMARY → may mutate Scope A StrategyMemory
Scope B PRIMARY → independent Scope B may run separately
second writer for Scope A → prohibited
offline research DB → separate scope
```

Idempotent source IDs make duplicate/conflicting evidence visible; they do not make two independently evolving same-scope databases safely mergeable.

Blind union/newest-file-wins/last-write-wins are not accepted merge algorithms.

## 10. Same-scope split-brain boundary

Two laptops with independent local runtime/coordination DBs cannot safely act as one bot for the same broker account/symbol:

- controller ownership can diverge;
- Intents can diverge;
- ManagedTrade/recovery truth can diverge;
- StrategyMemory can diverge;
- candidate/promotion history can diverge.

GitHub, Drive, Dropbox or ordinary file sync is archival transport—not real-time fencing/transactional coordination.

## 11. Supported operator topology

Initial V1:

```text
READINESS  read-only diagnostic
PRIMARY    one active governed runtime per account/symbol scope
STANDBY    not offered as safe same-scope cross-laptop mode
```

Different accounts/scopes may each have their own PRIMARY.

## 12. Sequential same-scope laptop handoff

```text
Laptop A PRIMARY
→ stop new work
→ safe shutdown / controller release
→ final verified local checkpoint/recovery package
→ deliberately transfer package
→ Laptop B restore into NEW runtime DB
→ connect intended account/symbol
→ fresh positions/deals/quote/identity read
→ reconcile lifecycle/risk/learning/broker truth
→ acquire local controller epoch
→ READY only after all authorities pass
```

At no time may both be active writers for the same scope.

Credentials are configured separately on the new machine.

## 13. If old machine status is uncertain

If the old PRIMARY cannot be positively known to be stopped, the new machine remains BLOCKED/incident-recovery state until operational, broker, controller and durable-state reconciliation establish a safe single-writer condition.

A copied backup alone cannot fence an old process.

## 14. Future simultaneous failover requirements

True same-scope PRIMARY/STANDBY would require both:

- shared cross-machine atomic coordination/fencing with global monotonic epoch;
- shared or globally ordered durable Intent/ManagedTrade/risk/learning state.

It would also require network-partition, stale-client, crash/takeover and real two-machine DEMO drills.

This is deferred and not a V1 release gate.

## 15. Actual learning durability path

Future governed DEMO path:

```text
verified OPEN
→ ManagedTrade freezes learning identity
→ verified bot EXIT / SL / TP / exact manual close
→ learning queue + closure receipt
→ causal broker/path outcome
→ one MAIN_DEMO StrategyMemory observation
→ queue consumed after durable save
→ rolling/full local backup preserves state
→ graceful shutdown creates fresh final local checkpoint
```

No repository mutation is part of this runtime path.

## 16. Failure semantics

| Failure | Required behaviour |
|---|---|
| corrupt durable record | reject/degraded; never clean empty state |
| duplicate identical learning source | idempotent |
| duplicate conflicting source | explicit conflict |
| incomplete exit evidence | keep queue/recovery pending |
| verified checkpoint unavailable | no restore from guessed state |
| dangerous credential detected | package fails security check |
| backup destination exists unexpectedly | no destructive overwrite |
| backup disk unavailable/full | explicit failure; preserve existing durable state/last good backup |
| abrupt machine loss | final shutdown backup not guaranteed; rely on SQLite + rolling checkpoints |
| same-scope second active writer | block; no automatic merge |
| different independent scopes | allowed with isolated state/authority |

## 17. Source-history local backup

Source/document backup is distinct from production learning backup.

At deliberate milestones the operator/development tooling may create a local Git bundle in the external source-backup directory. This is not generated on every trading shutdown.

The trading runtime itself has no Git commit/push authority.

## 18. Planned implementation ownership

```text
src/gold_scalp_trader/persistence/store.py
src/gold_scalp_trader/persistence/checkpoint.py
src/gold_scalp_trader/persistence/backup.py
src/gold_scalp_trader/persistence/local_recovery_package.py
src/gold_scalp_trader/research/learning.py
src/gold_scalp_trader/research/live_learning.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/execution/controller.py
src/gold_scalp_trader/execution/sqlite_coordination.py
```

## 19. Planned proof

Tests must prove full-state preservation, queue/receipt survival, secret exclusion, idempotency/conflict, local backup integrity/catalog, same-scope single-writer rule, sequential handoff semantics, no auto-merge and explicit absence of runtime Git publication.

Connected fresh-machine/Windows MT5 proof separately validates real handoff/reconciliation.

## 20. Open questions

Retention counts, backup cadence, secondary-drive replication, optional encryption-at-rest, source-bundle cadence, disk-space thresholds and fresh-machine drill acceptance criteria remain pre-challenge decisions.
