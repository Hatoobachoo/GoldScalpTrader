# GoldScalpTrader — Final Build / Replication Prompt

**Status:** POST-AUDIT-1 IMPLEMENTATION / REPLICATION BRIEF — IMPLEMENTATION NOT STARTED
**Version:** 1.0-fresh-zero-handoff
**Authority:** Whole-project handoff for a capable coding AI/developer with no chat history. Topic contracts always override this summary.

## 1. Mission

Build/verify/reconstruct **GoldScalpTrader**, a local Exness MT5 XAUUSD/XAUUSDm selective scalping system.

It is an institutional-style governed multi-desk system, not a simple EMA bot and not HFT.

Canonical path:

```text
one MT5 read boundary
→ immutable MarketSnapshot
→ causal independent intelligence
→ six independent scalp families
→ BUY / SELL fusion + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing + event freshness
→ family-aware structural TradePlan
→ gross + cost-adjusted room
→ STANDARD monetary Risk
→ hard session/news/system/account/controller authorities
→ central Gate
→ durable one-shot Intent
→ sole MT5Writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close
→ exactly-once learning
→ governed research/discovery/promotion
→ local recovery
```

Logical parallel analysis, serial financial/broker authority.

## 2. Authority order

`SYSTEM_CONTRACT` → owning topic contract → active `DESIGN_DECISIONS` / remaining `OPEN_QUESTIONS` → Architecture/Trading Floor → Coding/Module/File-Test maps → operator/testing/recovery guides → this prompt.

If canonical documents conflict, stop affected coding and repair the graph.

## 3. Frozen timeframe roles

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote current executable condition
```

M1/tick history has no hidden V1 production trigger authority.

## 4. Frozen six families

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

Keep attribution and correlation/event-lineage control. No unanimity/filter soup.

## 5. Opportunity / timing

Persistent Opportunity identity is distinct from current timing. M5 timing can WAIT/ENTER/MISSED/INVALID. Re-arm requires a genuinely fresh causal event. Event age/chase distance are first-class; exact thresholds calibrate later.

## 6. TradePlan / costs

Keep separate Signal Price, Approved Entry Reference, fresh Executable Quote and Actual Fill.

TradePlan owns family-aware structural invalidation, SL, objectives, original R, gross structural quality and current known cost-adjusted room. It never sizes lots or moves structure to fit an account.

Old Swing 1.20R is not active policy; exact gross/net thresholds are calibration pending.

## 7. STANDARD monetary Risk

V1 has one production Risk policy, not automatic equity tiers.

```text
TradePlan
→ theoretical volume
→ broker min/step/max normalization
→ actual all-in risk at executable normalized volume
→ hard ceiling/margin/exposure/daily/cooldown/re-entry checks
→ PASS / BLOCK / UNKNOWN
```

Minimum-lot affordability uses actual broker facts. Do not tighten SL to make 0.01 fit.

Historical aggressive 8%/16% values are not active. Any later aggressive experiment is explicit, disabled by default and research-governed.

## 8. Session / News

For new entry:

```text
OPEN + NEWS_CLEAR    → may continue
OPEN + NEWS_BLACKOUT → BLOCK
OPEN + NEWS_UNKNOWN  → BLOCK / LIMITED
```

Existing management/protection/mandatory CLOSE remains action-sensitive. UNKNOWN never becomes CLEAR.

## 9. Execution scope

READINESS/DRY_RUN first. Controlled DEMO writer only after implementation/deterministic proof. REAL is outside V1 and requires separate governance.

When writer exists:

```text
TradePlan/Risk/hard authorities
→ Gate ALLOW
→ persist Intent
→ fresh broker checks
→ persist SUBMITTING
→ exactly one sole-writer call
→ acknowledgement classification
→ reconciliation
```

Ambiguous acknowledgement never gets blind retry.

## 10. Trade Manager

Actions are HOLD/PROTECT/TRAIL/RUNNER/EXIT. Time/efficiency weakness is an EXIT reason, not separate action. Protection only tightens earned causal structure; Runner is exceptional with fresh continuation/new objective.

## 11. Persistence / ownership

Use strict local transactional state. Restart is not fresh risk day. Unknown exposure is never zero. Current broker truth outranks restored context. Manual/foreign positions are never silently adopted.

## 12. Runtime backup

```text
transactional StateStore
→ rolling local checkpoint
→ final graceful-shutdown local checkpoint
→ optional portable runtime recovery package
```

No runtime Git commit/push/pull or GitHub credential dependency.

## 13. Development/source backup

After major coherent bulk:

```text
one remote fast-forward commit
→ operator git pull --ff-only
→ local clone = latest source + full Git history
→ optional secret-clean ZIP milestone snapshot
```

Git bundle is optional advanced/manual only.

## 14. Learning / research

Learning is downstream. Actual/counterfactual/system-fault evidence stay distinct. Candidate invention is declarative, cannot self-promote and cannot bypass hard safety.

Replay is chronological/no-lookahead and scalp research explicitly models costs, latency, duration and min-lot affordability.

## 15. Dashboards

Terminal dashboard is primary read-only operator surface; optional localhost graphical dashboard is secondary/read-only. Presentation cannot recalculate authority.

Show upstream blocker separately from actual Gate state.

## 16. Engineering rules

Prefer smallest clear typed/auditable production code; MetaTrader5 calls stay at adapter/writer boundaries; logical analytical independence does not require physical concurrency; one-worker semantics are canonical and any worker pool must prove parity.

Every material change updates full affected Documents/source/tests/operator/research/release graph.

## 17. Evidence boundary

Never confuse frozen design, calibrated values, deterministic tests, replay, connected MT5 reads, controlled DEMO lifecycle, live learning, fresh-machine recovery and profitability.

## 18. Current next step

Post-Audit-1 contradiction scan/freeze must be clean. Then implementation starts with packaging/config/domain/read-only MT5 market truth — not order execution.