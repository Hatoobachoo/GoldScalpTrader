# GoldScalpTrader — Learning Backup and Multi-Machine Contract

**Status:** FROZEN V1 LOCAL RECOVERY / SOURCE-BACKUP ARCHITECTURE — RETENTION / EXTERNAL RESTORE PROOF PENDING
**Version:** 1.1-profiled-risk-local-first
**Authority:** Durable runtime/learning backup, preserved Risk identity, local recovery packages, development/source backup workflow, closure receipts, laptop handoff and per-scope multi-machine boundary.

## 1. Purpose

GoldScalpTrader must not lose runtime lifecycle, Risk-day/profile state, broker-operation lineage, pending/completed learning, discovery or promotion state across restart or machine migration.

Separately, development/source work should remain easy to keep locally with minimal GitHub usage.

## 2. Hard runtime rule

Trading runtime has:

```text
NO automatic Git commit
NO automatic Git push
NO automatic Git pull/fetch requirement
NO GitHub credential dependency
```

Graceful shutdown remains safe when GitHub/network is unavailable.

## 3. Runtime backup layers

```text
transactional StateStore
→ rolling local full checkpoints
→ graceful-shutdown final verified local checkpoint
→ optional focused learning artifact
→ portable runtime recovery package for deliberate handoff
```

Full checkpoint/recovery package is runtime recovery authority. Focused learning export alone is not full-machine recovery.

## 4. Full checkpoint completeness

Preserve all required durable namespaces, including where present:

- Risk-day ID / DayStartEquity;
- fixed `SMALL / MEDIUM / NORMAL` profile identity;
- `AGGRESSIVE_SMALL_ACCOUNT` enabled/disabled state + policy identity;
- Account Safety P/L / cash-flow baseline / loss lock;
- governed reset count/state;
- consecutive-loss counter / cooldown / same-episode re-entry state;
- Opportunity/Episode/TradePlan;
- ExecutionIntent lifecycle;
- ManagedTrade, objective stage and remaining volume;
- verified partial-management lineage where applicable;
- closed-trade learning queue + closure receipt;
- StrategyMemory observations/summaries;
- research episode journal;
- candidate/discovery/promotion/rollback state;
- configuration/policy/schema identities;
- every other canonical durable namespace.

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

Secret/integrity scan fails closed before an artifact is called portable/shareable.

## 6. Runtime backup root

Conceptual root outside repository:

```text
C:\GoldScalpTrader_Backups\runtime\
C:\GoldScalpTrader_Backups\learning\
C:\GoldScalpTrader_Backups\recovery-packages\
C:\GoldScalpTrader_Backups\source-zips\
```

Path is configurable. Optional second physical HDD/SSD/USB can improve device-failure resilience.

## 7. Development/source backup — operator-preferred workflow

After a major coherent documentation/code bulk:

```text
one remote fast-forward commit
→ operator runs git pull --ff-only
→ local working clone contains latest project + complete Git history
```

The local clone is primary development/source backup. Do not require a pull after every tiny patch.

## 8. Optional source ZIP

An important milestone may create a Windows-friendly secret-clean ZIP.

Default archive includes current source/Documents/config samples/tests/scripts while excluding:

```text
.env / secret files
.venv / venv
__pycache__ / test caches
logs
runtime SQLite/checkpoints
nested backup directories
credentials/private keys
```

Including `.git` inside ZIP is unnecessary by default because the pulled clone already preserves history.

## 9. Git bundle boundary

A history-bearing Git bundle is optional advanced/manual backup only. It is not required after every bulk and trading runtime never invokes it.

## 10. Focused learning package

May contain StrategyMemory, pending learning queue, episode journal, candidate/discovery/promotion records and evidence/config fingerprints.

It is not a substitute for full checkpoint because lifecycle/Risk/Intent/receipt state may be required for safe recovery.

## 11. Closure receipt / learning queue

```text
closed_trade_learning_queue   → pending post-close learning
managed_trade_closure_receipt → durable proof managed lifecycle ended
```

Queue may disappear after successful exactly-once ingestion. Closure receipt remains lifecycle proof. Full backup preserves both while applicable.

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
→ reconcile lifecycle/Risk/learning
→ verify fixed risk-day profile/aggressive-overlay state
→ acquire controller
→ READY only after all authorities pass
```

If old-machine writer status is uncertain, new machine remains blocked until single-writer safety is established.

## 15. Learning durability path

```text
verified OPEN
→ ManagedTrade freezes learning + Risk-policy identity
→ verified close mechanism
→ learning queue + closure receipt
→ causal outcome
→ exactly one MAIN_DEMO StrategyMemory observation
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
| backup collision | no destructive overwrite |
| backup disk unavailable/full | explicit failure; preserve last good state |
| abrupt machine loss | final shutdown backup not guaranteed; transactional state + rolling checkpoints remain crash boundary |
| same-scope second writer | block |
| restored aggressive mode inconsistent with config/eligibility | recovery/Risk validation blocks affected new entry |

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

Optional source-ZIP helper may live under `scripts/`; it has no broker/runtime authority.

## 18. Planned proof

Tests prove full-state preservation including Risk profile/overlay/reset/cooldown/re-entry identity, queue/receipt survival, secret exclusion, idempotency/conflict, backup integrity/catalog, same-scope single-writer, sequential handoff, no auto-merge and absence of runtime Git operations.

Fresh-machine connected proof separately validates real restore/reconciliation.

## 19. Implementation/external choices pending

Runtime backup cadence/retention, disk-space thresholds, optional encryption, secondary-drive copy and exact source-ZIP helper remain later implementation/evidence choices.

Source pull workflow, no-runtime-Git rule, profile/overlay durability and sequential same-scope handoff are frozen.