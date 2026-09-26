"""Verify that implementation still matches the frozen GoldScalpTrader contracts.

This local/static guard does not replace connected Exness DEMO proof. It checks
document topology, canonical source/test ownership, preserved Risk constants,
REAL hard-disable, market-first isolation, typed Session/News separation and
forbidden broker dependencies in analytical/research/read-only layers.
"""
from __future__ import annotations
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/"src"/"gold_scalp_trader"; DOCS=ROOT/"Documents"
EXPECTED_DOC_COUNTS={"01-foundation":5,"02-market-intelligence":7,"03-trading-decisions":7,"04-risk-execution":6,"05-research-learning":7,"06-operator":3,"07-engineering":14,"08-governance":8}
REQUIRED_SOURCE_PATHS=("config/settings.py","domain/enums.py","domain/ids.py","domain/market.py","domain/models.py","diagnostics/logging.py","diagnostics/reasons.py","diagnostics/health.py","diagnostics/metrics.py","diagnostics/connected_demo.py","security/financial_secrets.py","market_data/account_mode.py","market_data/mt5_reader.py","market_data/activity.py","market_data/snapshot.py","intelligence/candle_structure.py","intelligence/indicators.py","intelligence/technical.py","intelligence/liquidity.py","intelligence/confluence.py","intelligence/session.py","intelligence/news.py","intelligence/snapshot.py","strategies/floor.py","strategies/setup_detector.py","strategies/isolation.py","strategies/scheduler.py","strategies/confluence.py","decisions/fusion.py","decisions/snapshot.py","decisions/opportunity.py","decisions/timing.py","decisions/family_trade_plan.py","decisions/trade_plan.py","decisions/executable_quality.py","risk/engine.py","risk/state.py","risk/runtime.py","risk/permissions.py","execution/models.py","execution/checks.py","execution/gate.py","execution/intent_store.py","execution/service.py","execution/mt5_writer.py","execution/reconcile.py","execution/controller.py","execution/sqlite_coordination.py","management/models.py","management/manager.py","management/execution.py","management/closure.py","management/store.py","persistence/store.py","persistence/runtime_state.py","persistence/checkpoint.py","persistence/backup.py","persistence/local_recovery_package.py","research/learning.py","research/live_learning.py","research/replay.py","research/management_replay.py","research/session_history.py","research/stress.py","research/validation.py","research/datasets.py","research/acquisition.py","research/evidence.py","research/packages.py","research/metrics.py","research/outcomes.py","research/ablation.py","research/episode_journal.py","research/discovery.py","research/invention.py","research/models.py","research/promotion.py","operator/presentation.py","operator/terminal_dashboard.py","operator/graphical_snapshot.py","app/main.py","app/runtime.py","app/startup.py","app/recovery.py","app/recovery_mt5.py","app/cycle.py","app/loop.py","app/dashboard.py","app/live_presentation.py","app/session_news.py","app/demo_runner.py","app/graphical_demo_runner.py")
REQUIRED_ROOT_PATHS=("graphical_dashboard/ui.py","graphical_dashboard/chart.py","graphical_dashboard/controls.py","graphical_dashboard/server.py","graphical_dashboard/__main__.py")
REQUIRED_SCRIPTS=("scripts/run_walk_forward.py","scripts/acquire_mt5_dataset.py","scripts/report_demo_learning_evidence.py","scripts/certify_connected_demo.py","scripts/monitor_connected_demo.py","scripts/restore_runtime_checkpoint.py","scripts/create_local_recovery_package.py","scripts/create_source_zip.py","scripts/scan_financial_secrets.py","scripts/verify_documents_manual.py","scripts/verify_contract_sync.py","scripts/verify_offline_release.py")
CRITICAL_TESTS=("tests/test_cycle_no_forcing.py","tests/test_strategy_isolation.py","tests/test_decision_pipeline.py","tests/test_executable_quality.py","tests/test_risk_profiles.py","tests/test_risk_state.py","tests/test_risk_runtime_state.py","tests/test_session_news_provider.py","tests/test_execution_intent.py","tests/test_gate.py","tests/test_controller.py","tests/test_guarded_demo_runtime.py","tests/test_management_lifecycle.py","tests/test_action_reconciliation.py","tests/test_deal_history_reader.py","tests/test_writer_attribution.py","tests/test_demo_launcher.py","tests/test_dashboard_controls.py","tests/test_graphical_runtime.py","tests/test_live_learning_pipeline.py","tests/test_research_governance.py","tests/test_research_integrity.py","tests/test_checkpoint.py","tests/test_full_checkpoint.py","tests/test_recovery_package.py","tests/test_connected_demo_evidence.py")
ANALYTICAL_NO_BROKER_DIRS=(SRC/"intelligence",SRC/"strategies",SRC/"risk",SRC/"research",SRC/"operator",SRC/"diagnostics",ROOT/"graphical_dashboard")
FORBIDDEN_IMPORT_FRAGMENTS=("MetaTrader5","execution.mt5_writer","from gold_scalp_trader.execution import mt5_writer")
STALE_POLICY_TERMS=("NEWS_BLACKOUT","POST_NEWS_WARMUP","M1 diagnostic-only","M1 diagnostic only")
CONNECTED_EVIDENCE_PATHS=(ROOT/"scripts"/"certify_connected_demo.py",ROOT/"scripts"/"monitor_connected_demo.py",SRC/"diagnostics"/"connected_demo.py")
def _fail(errors:list[str],message:str)->None:errors.append(message)
def _parse_module(path:Path)->ast.Module:
    try:return ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
    except (OSError,SyntaxError) as exc:raise RuntimeError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
def _literal_assignment(tree:ast.Module,name:str):
    for node in tree.body:
        if isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            if any(isinstance(target,ast.Name) and target.id==name for target in targets):
                value=node.value
                if value is None:return None
                return ast.literal_eval(value)
    raise KeyError(name)
def check_documents(errors:list[str])->None:
    for folder,expected in EXPECTED_DOC_COUNTS.items():
        path=DOCS/folder; actual=len(list(path.glob("*.md"))) if path.is_dir() else -1
        if actual!=expected:_fail(errors,f"document count {folder}: expected {expected}, got {actual}")
    total=len(list(DOCS.rglob("*.md")))
    if total!=66:_fail(errors,f"document total: expected 66, got {total}")
def check_required_paths(errors:list[str])->None:
    for rel in REQUIRED_SOURCE_PATHS:
        if not (SRC/rel).is_file():_fail(errors,f"missing canonical source owner: src/gold_scalp_trader/{rel}")
    for rel in REQUIRED_ROOT_PATHS+REQUIRED_SCRIPTS+CRITICAL_TESTS:
        if not (ROOT/rel).is_file():_fail(errors,f"missing required implementation/proof file: {rel}")
def check_preserved_policy(errors:list[str])->None:
    path=SRC/"config"/"settings.py"; text=path.read_text(encoding="utf-8"); tree=_parse_module(path)
    try:real_enabled=_literal_assignment(tree,"REAL_RELEASE_ENABLED")
    except (KeyError,ValueError) as exc:_fail(errors,f"REAL_RELEASE_ENABLED cannot be statically verified: {exc}")
    else:
        if real_enabled is not False:_fail(errors,"REAL_RELEASE_ENABLED must remain False before Phase 16 approval")
    for expected in ('"SMALL": RiskBand(3.0, 4.5, 6.5, 7.0, 12.0)','"MEDIUM": RiskBand(2.0, 3.0, 4.5, 5.0, 9.0)','"NORMAL": RiskBand(1.0, 2.0, 3.5, 4.0, 7.0)'):
        if expected not in text:_fail(errors,f"preserved Risk band changed or missing: {expected}")
    for expected in ("max_open_positions: int = 1","max_consecutive_losses: int = 3","consecutive_loss_cooldown_minutes: int = 30","context_cache_ttl_seconds: int = 1800","aggressive_small_account: bool = False","manual_daily_loss_reset_enabled: bool = False"):
        if expected not in text:_fail(errors,f"preserved setting changed or missing: {expected}")
def check_architecture_boundaries(errors:list[str])->None:
    for directory in ANALYTICAL_NO_BROKER_DIRS:
        for path in directory.glob("*.py"):
            text=path.read_text(encoding="utf-8")
            for fragment in FORBIDDEN_IMPORT_FRAGMENTS:
                if fragment in text:_fail(errors,f"forbidden broker dependency in {path.relative_to(ROOT)}: {fragment}")
            if "order_send(" in text or "order_send (" in text:_fail(errors,f"raw order_send outside sole writer boundary: {path.relative_to(ROOT)}")
    writer=SRC/"execution"/"mt5_writer.py"
    if "order_send" not in writer.read_text(encoding="utf-8"):_fail(errors,"sole MT5 writer no longer contains the raw order_send boundary")
    setup=(SRC/"strategies"/"setup_detector.py").read_text(encoding="utf-8"); isolation=(SRC/"strategies"/"isolation.py").read_text(encoding="utf-8")
    if "detect" not in setup.lower():_fail(errors,"setup_detector.py no longer exposes recognizable market-first detection logic")
    if "active" not in isolation.lower() or "shadow" not in isolation.lower():_fail(errors,"strategy isolation no longer visibly separates active and shadow states")
    risk_runtime=SRC/"risk"/"runtime.py"
    if risk_runtime.is_file():
        text=risk_runtime.read_text(encoding="utf-8")
        if "order_send(" in text or "execution.mt5_writer" in text:_fail(errors,"durable Risk runtime gained broker-write authority")
        if "StateStore" not in text or "risk_day" not in (SRC/"risk"/"state.py").read_text(encoding="utf-8"):_fail(errors,"durable Risk-day state ownership is no longer explicit")
    provider=SRC/"app"/"session_news.py"
    if provider.is_file():
        text=provider.read_text(encoding="utf-8")
        if "order_send(" in text or "execution.mt5_writer" in text:_fail(errors,"Session/News provider gained broker-write authority")
        if "hard_trading_permission" not in text or "MarketState.UNKNOWN" not in text:_fail(errors,"Session/News authority separation is no longer explicit")
def check_connected_evidence_is_read_only(errors:list[str])->None:
    for path in CONNECTED_EVIDENCE_PATHS:
        if not path.is_file():continue
        text=path.read_text(encoding="utf-8")
        if "order_send(" in text or "execution.mt5_writer" in text:_fail(errors,f"connected evidence tooling gained broker-write authority: {path.relative_to(ROOT)}")
        if "REAL_RELEASE_ENABLED = True" in text:_fail(errors,f"connected evidence tooling attempts REAL enablement: {path.relative_to(ROOT)}")
    monitor=ROOT/"scripts"/"monitor_connected_demo.py"
    if monitor.is_file():
        text=monitor.read_text(encoding="utf-8")
        if "--interval-seconds" not in text or "at least 5 seconds" not in text:_fail(errors,"connected DEMO monitor lost bounded sampling interval guard")
def check_no_legacy_policy_code(errors:list[str])->None:
    for path in SRC.rglob("*.py"):
        text=path.read_text(encoding="utf-8")
        for term in STALE_POLICY_TERMS:
            if term in text:_fail(errors,f"legacy policy term found in code {path.relative_to(ROOT)}: {term}")
def main()->int:
    errors=[]; check_documents(errors); check_required_paths(errors); check_preserved_policy(errors); check_architecture_boundaries(errors); check_connected_evidence_is_read_only(errors); check_no_legacy_policy_code(errors)
    print("DOCUMENT / CODE CONTRACT SYNC AUDIT")
    if errors:
        for error in errors:print(f"  FAIL  {error}")
        print(f"CONTRACT SYNC: FAIL ({len(errors)} issue(s))"); return 1
    print("  PASS  66-document topology"); print("  PASS  canonical source / script / proof ownership paths"); print("  PASS  preserved Risk / cooldown / REAL-disable policy"); print("  PASS  durable UTC Risk-day component remains read/accounting-only"); print("  PASS  Session hard / News soft provider boundary remains read-only"); print("  PASS  setup-detection / isolation boundaries"); print("  PASS  sole-writer / no-broker analytical boundaries"); print("  PASS  connected-DEMO evidence tooling remains read-only"); print("CONTRACT SYNC: PASS"); print("CONNECTED DEMO FACTS: NOT PROVEN BY THIS STATIC AUDIT"); return 0
if __name__=="__main__":raise SystemExit(main())
