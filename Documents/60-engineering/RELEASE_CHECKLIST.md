# GoldScalpTrader — Release Checklist

**Status:** DRAFT PRE-CHALLENGE RELEASE GATE
**Version:** 0.1-scalp-release-gate
**Authority:** Ordered release preparation, module/feature verification, evidence classification and sign-off.

## 1. Evidence rule

This is a gate, not a progress diary.

Classify every applicable item as:

```text
PASS
FAIL
BLOCKED
EXTERNAL PROOF PENDING
CALIBRATION PENDING
NOT RUN
NOT APPLICABLE
```

Attach exact revision/environment evidence. Green tests are not connected-broker certification or profitability proof.

## 2. Release order

```text
canonical Documents challenged + frozen
→ module/feature traversal
→ code quality + deterministic suites
→ connected read-only readiness
→ natural governed DEMO lifecycle
→ verified actual learning
→ local backup/restore/recovery drill
→ final scoped audit/sign-off
```

## 3. Build identity

- [ ] exact revision;
- [ ] OS/Python/dependency identity;
- [ ] policy/state-schema identity;
- [ ] redacted DEMO account/server/symbol scope;
- [ ] evidence package/reviewer;
- [ ] local backup/recovery-package identity where relevant.

## 4. Canonical documentation gate

- [ ] `Documents/` is sole active documentation authority.
- [ ] All reference-equivalent canonical filenames exist or explicit governed exception exists.
- [ ] Every substantive doc has Status/Version/Authority.
- [ ] System Contract/topic contracts/Architecture/Coder Guide/Module Structure/File-Test Catalog agree.
- [ ] final timeframe roles are consistent.
- [ ] final News-UNKNOWN policy is consistent.
- [ ] upstream Plan/Risk blocker is not called central Gate BLOCK.
- [ ] local backup/no-runtime-Git-push boundary is consistent everywhere.
- [ ] one PRIMARY per same account/symbol scope is explicit.
- [ ] canonical Documents verifier passes once implemented.

## 5. Module/feature traversal

For every meaningful module/feature:

- [ ] purpose + forbidden ownership identified;
- [ ] canonical behaviour owner identified;
- [ ] implementation inspected;
- [ ] focused tests/evidence identified;
- [ ] UNKNOWN/stale/corrupt/failure semantics checked;
- [ ] restart/persistence/idempotency checked where relevant;
- [ ] dashboard/research impact checked;
- [ ] external/calibration evidence separated;
- [ ] explicit status recorded.

## 6. Code/dependency/security gate

- [ ] editable/install/run path works on intended Windows/Python environment;
- [ ] lint/static/compile checks pass;
- [ ] full Pytest passes;
- [ ] Documents verifier passes;
- [ ] financial-secret scan passes;
- [ ] no raw broker write outside sole writer;
- [ ] no analytical/operator/research path grants broker authority;
- [ ] bounded parallel work preserves serial parity/order;
- [ ] secondary UI failure cannot stop/authorize trading;
- [ ] runtime has no Git commit/push authority;
- [ ] backups contain no secrets.

## 7. Market / chronology / intelligence

- [ ] final timeframe roles are implemented exactly;
- [ ] completed-candle/knowledge-time semantics pass;
- [ ] stale/sparse/corrupt/future facts explicit;
- [ ] expected broker closure gaps not misclassified;
- [ ] event freshness retained;
- [ ] optional confluence is not hidden veto;
- [ ] serial/bounded-parallel parity passes;
- [ ] cost/spread facts are descriptive until owning contract applies them.

## 8. Strategy / timing / TradePlan / Risk

- [ ] final family architecture passes;
- [ ] BUY/SELL independent;
- [ ] Opportunity persists independently from executable timing;
- [ ] WAIT/MISSED/INVALID/re-arm semantics pass;
- [ ] family-aware invalidation passes;
- [ ] TradePlan precedes monetary Risk;
- [ ] final structural-R/cost-room policy passes;
- [ ] original R immutable;
- [ ] min-lot/dynamic sizing/actual all-in risk pass;
- [ ] final profile/daily-loss/cooldown/re-entry rules pass;
- [ ] structural SL never tightened merely to fit account/lot.

## 9. Session / News

- [ ] verified Exness XAU normal schedule + pre-close/reopen policy tested;
- [ ] final `OPEN + News UNKNOWN` policy tested exactly;
- [ ] known blackout blocks new entry;
- [ ] CLOSED/PRE_CLOSE/WARMUP/session UNKNOWN remain hard as frozen;
- [ ] altered holiday ambiguity remains fail-safe;
- [ ] missing News never displays CLEAR;
- [ ] provider availability is not confused with market-session truth.

## 10. Execution / controller / recovery

- [ ] write-capable mode guard + intended identity pass;
- [ ] native account/terminal/symbol permissions checked;
- [ ] central Gate reached only after upstream Plan/Risk readiness;
- [ ] one-shot Intent/persist-before-send/no blind retry pass;
- [ ] ambiguous acknowledgement reconciles without duplicate;
- [ ] local controller stale-holder denial passes;
- [ ] unknown/foreign Gold exposure not adopted;
- [ ] missing known ManagedTrade requires exact close proof;
- [ ] MODIFY/CLOSE uses same governed execution spine;
- [ ] action-sensitive mandatory CLOSE policy proven.

## 11. Operator/dashboard

- [ ] dashboard visible in closed/stale/warming/reconciling states;
- [ ] live feed distinct from trade readiness;
- [ ] narrow/wide/fallback paths proven;
- [ ] upstream block → Gate NOT EVALUATED;
- [ ] actual Gate BLOCK named correctly;
- [ ] News UNKNOWN visible truthfully;
- [ ] graphical dashboard localhost/read-only/no controls;
- [ ] production performance only from verified actual closes;
- [ ] scalp event age/cost/drift facts are presentation only.

## 12. Learning / research

- [ ] verified OPEN freezes learning identity/original R;
- [ ] close queue/receipt/order pass;
- [ ] exactly-once actual DEMO observation;
- [ ] causal MFE/MAE boundaries;
- [ ] replay/validation/holdout/shadow/canary/actual evidence distinct;
- [ ] cost/latency/hold-time research retained;
- [ ] discovery cannot self-promote/write broker;
- [ ] broader historical calibration remains evidence, not assumed edge.

## 13. Local backup / restore / machine movement

- [ ] full checkpoint schema/hash/manifest verified;
- [ ] all durable namespaces included;
- [ ] active SQLite backed up consistently;
- [ ] automatic backup root outside repo;
- [ ] credentials/real `.env` excluded;
- [ ] graceful PRIMARY releases authority before final local checkpoint;
- [ ] no runtime Git commit/push path;
- [ ] local Git bundle creation is deliberate milestone action only;
- [ ] recovery package verifies before restore;
- [ ] restore goes to new DB/path;
- [ ] fresh broker reconciliation/controller authority precede writes;
- [ ] same-scope laptop movement sequential only;
- [ ] second physical-drive option tested if part of deployment.

## 14. Connected DEMO proof

- [ ] intended DEMO account/server/symbol and healthy data retained as evidence;
- [ ] natural qualified candidate reaches Plan/Risk/Gate without safety bypass;
- [ ] governed OPEN broker verified;
- [ ] MODIFY/SL/TP broker verified;
- [ ] governed CLOSE verified;
- [ ] SL/TP/exact known manual close recovery verified;
- [ ] actual learning appears exactly once;
- [ ] restart/reconciliation does not duplicate exposure;
- [ ] pre-close/reopen observed;
- [ ] graceful local backup and deliberate independent restore drill retained.

## 15. External/calibration items

Keep pending until real evidence exists:

- final risk/structural-R/cost/freshness thresholds;
- broader XAU regime-diverse history;
- special holiday schedule;
- real spread/slippage/latency distributions;
- connected DEMO lifecycle;
- fresh-machine recovery;
- any future simultaneous same-scope failover.

## 16. Sign-off rule

Release evidence identifies exact revision and scope.

Use scoped claims such as `software verified`, `connected DEMO OPEN verified`, or `local restore verified`.

Never infer profitability, REAL authorization or unperformed connected proof from deterministic PASS.
