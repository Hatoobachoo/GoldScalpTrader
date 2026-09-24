# GoldScalpTrader — Learning Backup and Multi-Machine Contract

**Status:** FROZEN V1 LOCAL RECOVERY / SOURCE-BACKUP ARCHITECTURE — RETENTION / EXTERNAL RESTORE PROOF PENDING
**Version:** 1.0-local-first-no-runtime-git
**Authority:** Durable runtime/learning backup, local recovery packages, development/source backup workflow, closure receipts, laptop handoff and per-scope multi-machine boundary.

## 1. Purpose

GoldScalpTrader must not lose runtime lifecycle, risk history, broker-operation lineage, pending/completed learning, discovery or promotion state across restart or machine migration.

Separately, development/source work should be easy to keep locally with **minimal GitHub usage**.

## 2. Hard runtime rule

The trading runtime has:

```text
NO automatic Git commit
NO automatic Git push
NO automatic Git pull/fetch requirement
NO GitHub credential dependency
```

Graceful shutdown remains safe when GitHub/network is unavailable after broker authority is released.

## 3. Runtime backup layers

```text
live/research producers
→ integrity-protected transactional StateStore
→ rolling local full checkpoints
→ graceful-shutdown final verified local checkpoint
→ optional focused learning artifact
→ portable runtime recovery package for deliberate handoff
```

Full checkpoint/recovery package is the runtime recovery authority. Focused learning exports are not complete machine recovery.

## 4. Full checkpoint completeness

Preserve all required durable namespaces, including where present:

- risk-day/cash-flow/loss-lock/reset/cooldown;
- Opportunity/Episode/TradePlan;
- ExecutionIntent lifecycle;
- ManagedTrade;
- closed-trade learning queue + closure receipt;
- StrategyMemory observations/summaries;
- research episode journal;
- candidate/discovery/promotion/rollback state;
- configuration/policy/schema identities;
- other canonical durable namespaces.

Do not rebuild a “full” backup from a convenient subset.

## 5. Credential boundary

Automatic/shareable artifacts exclude:

```text
broker password/token
GitHub PAT/access token
API/client secret
auth/refresh token
SSH/private/recovery key
credential-bearing remote URL
real .env secrets
```

Secret/integrity scan must fail closed before an artifact is called portable/shareable.

## 6. Runtime backup root

Conceptual default outside repository:

```text
C:\GoldScalpTrader_Backups\runtime\
C:\GoldScalpTrader_Backups\learning\
C:\GoldScalpTrader_Backups\recovery-packages\
C:\GoldScalpTrader_Backups\source-zips\
```

Path is configurable. Optional second physical HDD/SSD/USB copy can improve device-failure resilience.

## 7. Development/source backup — operator-preferred normal workflow

After a **major coherent documentation/code bulk**, normal workflow is:

```text
one remote fast-forward commit
→ operator runs: git pull --ff-only
→ local working clone now contains latest project + complete Git history
```

This local clone is the primary development/source backup.

Do **not** ask the operator to pull after every tiny patch. Consolidate coherent bulks where safe.

## 8. Optional source ZIP

After an important milestone, an optional Windows-friendly ZIP may be created locally for an extra offline snapshot.

Default ZIP content should include current source/documents/config samples/tests/scripts while excluding secrets and machine/runtime noise such as:

```text
.env / secret files
.venv / venv
__pycache__ / test caches
logs
runtime SQLite/checkpoints
nested backup directories
credentials/private keys
```

Including `.git` inside ZIP is unnecessary by default because the pulled local clone already preserves full history. If the operator wants a history-bearing offline archive, an advanced/manual Git bundle can be created separately.

## 9. Git bundle boundary

Git bundle is optional advanced/manual source-history backup, not normal trading-runtime behaviour and not required after every bulk.

The project may later provide an explicit operator helper, but the runtime itself never invokes it.

## 10. Focused learning package

May contain StrategyMemory, pending learning queue, episode journal, candidate/discovery/promotion records and evidence/config fingerprints. It is not a substitute for full checkpoint because lifecycle-only risk/Intent/receipt state may be required for safe recovery.

## 11. Closure receipt / learning queue

```text
closed_trade_learning_queue     → pending post-close learning
managed_trade_closure_receipt   → durable proof managed lifecycle ended
```

Queue may disappear after successful exactly-once ingestion. Closure receipt remains lifecycle proof. Full backup preserves both.

## 12. Production learning ownership

One writer per account/symbol production scope. Different independent scopes may have separate runtime state. Two same-scope independent databases cannot safely evolve as one bot.

Blind union, newest-file-wins and last-write-wins are not accepted merge strategies.

## 13. Same-scope split-brain boundary

File sync/GitHub/Drive/Dropbox is archival transport, not real-time controller fencing or transactional coordination.

Same-scope simultaneous PRIMARY writers are unsupported.

## 14. Sequential laptop handoff

```text
Laptop A PRIMARY
→ stop new work
→ safe shutdown / controller release
→ final verified local checkpoint/package
→ deliberate transfer
→ Laptop B restore into NEW runtime DB
→ configure credentials separately
→ connect intended account/symbol
→ fresh broker positions/deals/quote/identity
→ reconcile lifecycle/risk/learning
→ acquire controller
→ READY only after all authorities pass
```

If old machine status is uncertain, new machine remains blocked until single-writer safety can be established.

## 15. Learning durability path

```text
verified OPEN
→ ManagedTrade freezes learning identity
→ verified close mechanism
→ learning queue + closure receipt
→ causal outcome
→ exactly one production StrategyMemory observation
→ queue consumed after durable save
→ rolling/full local backup preserves state
```

No repository mutation is part of this path.

## 16. Failure semantics

| Failure | Required behaviour |
|---|---|
| corrupt durable record | reject/degraded; never clean empty state |
| duplicate identical learning source | idempotent |
| duplicate conflicting source | explicit conflict |
| incomplete exit evidence | recovery/queue pending |
| verified checkpoint unavailable | no guessed restore |
| secret detected | package/source ZIP fails shareable check |
| backup destination collision | no destructive overwrite |
| backup disk unavailable/full | explicit failure; preserve last good state |
| abrupt machine loss | final shutdown backup not guaranteed; rely on transactional state + rolling checkpoints |
| same-scope second writer | block |

## 17. Planned implementation ownership

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

Optional development helper may later live under `scripts/` for safe source ZIP; it has no broker/runtime authority.

## 18. Planned proof

Tests prove full-state preservation, queue/receipt survival, secret exclusion, idempotency/conflict, backup integrity/catalog, same-scope single-writer, sequential handoff, no auto-merge and explicit absence of runtime Git operations.

Fresh-machine connected proof separately validates real restore/reconciliation.

## 19. Calibration / implementation choices pending

Runtime backup cadence/retention, disk-space thresholds, optional encryption, secondary-drive copy and exact source-ZIP helper implementation remain later evidence/implementation choices.