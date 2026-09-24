# GoldScalpTrader — Final Release Audit

**Status:** DRAFT AUDIT TEMPLATE — NOT RUN
**Version:** 0.1-scalp-final-release
**Authority:** Evidence-backed release decision for one exact build, configuration, dataset, terminal and environment.

## 1. Purpose and scope

This is an evidence record, not a permanent completion claim.

Initial release target is local Windows + Exness MT5, documentation-first, DRY_RUN before any governed DEMO broker-write milestone, one active PRIMARY per account/symbol scope and local-only backup/recovery.

This file must never claim profitability or REAL authorization.

## 2. Audit identity

```text
Audit ID:
Git revision:
Audit timestamp UTC:
Release owner:
Target broker/account/server/symbol (redacted):
Runtime mode:
OS / Python / dependencies:
Configuration fingerprint:
Policy/schema versions:
Evidence package fingerprint:
Local backup/recovery package:
```

## 3. Allowed statuses

```text
PASS
FAIL
BLOCKED
NOT RUN
EXTERNAL PROOF PENDING
CALIBRATION PENDING
NOT APPLICABLE
```

Every PASS must identify concrete evidence.

## 4. Canonical Documents audit

Verify:

- complete expected canonical filename tree;
- Status/Version/Authority on substantive docs;
- no unresolved contradiction among System Contract/topic contracts/Architecture/Coder Guide/Module Map/Catalog;
- affected-graph synchronization;
- fresh-zero challenge completed;
- unresolved items classified in `OPEN_QUESTIONS.md`;
- pre-challenge wording removed/frozen only where justified;
- no runtime Git auto-push requirement anywhere.

## 5. Source/module audit

Traverse every source group from `MODULE_STRUCTURE.md` and `FILE_AND_TEST_CATALOG.md`.

For each material component record:

```text
purpose
canonical owner
implementation files
focused tests
negative/failure semantics
persistence/recovery effect
operator effect
research effect
connected/calibration evidence
verdict
```

Aggregate test success cannot substitute for this traversal.

## 6. Chronology / intelligence audit

Verify:

- completed-candle authority;
- correct knowledge timestamps;
- no future-confirmed swing/event leakage;
- final timeframe roles;
- snapshot freshness/quality;
- serial/parallel semantic parity;
- optional confluence remains optional where contract says so;
- event freshness is traceable.

## 7. Strategy / TradePlan / Risk audit

Verify:

- final approved family set;
- independent BUY/SELL fusion/Red Team;
- persistent Opportunity and timing separation;
- fresh-event re-arm semantics;
- family-specific invalidation only from proven geometry;
- final structural-R/cost-room policy;
- immutable original R;
- dynamic/min-lot monetary sizing;
- final risk bands/daily lock/cooldown/re-entry policy;
- no stop distortion to fit account.

## 8. Execution / lifecycle audit

Where broker-write capability exists, verify:

- intended mode/account/server/symbol;
- final Gate hard-authority composition;
- fresh spread/drift/trigger-age checks;
- one-shot Intent / persist-before-send;
- sole writer confinement;
- ambiguous acknowledgement → reconciliation only;
- controller fencing;
- foreign exposure non-adoption;
- exact broker-side close proof;
- action-sensitive MODIFY/CLOSE;
- restart no-duplicate semantics.

Before that milestone these items remain NOT RUN/NOT APPLICABLE, never fake PASS.

## 9. Management / learning audit

Verify:

- HOLD/PROTECT/TRAIL/RUNNER/EXIT semantics;
- no stop widening;
- scalp time/efficiency policy once frozen;
- close receipt + queue ordering;
- frozen learning identity;
- causal path metrics;
- exactly-once actual learning;
- close origin attribution;
- research cannot acquire broker authority.

## 10. Research audit

Verify:

- production-semantics replay;
- one-position capacity;
- no-lookahead;
- explicit spread/slippage/latency assumptions;
- regime/session coverage;
- min-lot small-account classification;
- fixed-policy walk-forward;
- one-shot final holdout;
- stress;
- Shadow/DEMO canary boundaries;
- self-promotion denial.

No backtest result is a release permission by itself.

## 11. Operator audit

Verify:

- primary dashboard read-only;
- graphical dashboard local/read-only;
- upstream blocker vs actual Gate truth;
- no fabricated geometry/performance;
- News/session truth;
- narrow/wide/fallback behaviour;
- UI crash isolation;
- verified production performance provenance.

## 12. Local backup / recovery audit

Verify:

- consistent StateStore backup;
- complete checkpoint namespaces;
- manifest/hashes/catalog;
- secrets excluded;
- backup root outside repo;
- final local backup after authority release;
- no runtime Git commit/push;
- deliberate local source bundle where required;
- restore into new DB/path;
- fresh broker reconciliation after restore;
- same-scope sequential laptop handoff only.

## 13. Connected DEMO evidence

When applicable record exact evidence for:

```text
READINESS identity/data
natural qualified setup
OPEN
MODIFY/SL/TP
CLOSE
broker-side SL/TP
known manual close recovery
actual learning
restart/reconcile
pre-close/reopen
local backup/independent restore
```

No rule may be weakened to manufacture an evidence event.

## 14. Calibration evidence

Record what remains unresolved numerically, including as applicable:

- timeframe/M1 role;
- structural R;
- cost-room/spread/drift/freshness;
- risk bands/daily limits;
- session/news windows;
- hold-time/management thresholds;
- strategy weights;
- research sample thresholds.

## 15. Final verdict

```text
RELEASE PASS
RELEASE FAIL
RELEASE BLOCKED
SOFTWARE VERIFIED — EXTERNAL PROOF PENDING
CALIBRATION PENDING
```

Verdict must identify exact scope/revision.

## 16. Current state

As of this pre-implementation draft:

```text
AUDIT RESULT: NOT RUN
Reason: canonical manual is still being completed/challenged; production implementation and connected evidence do not yet exist.
```
