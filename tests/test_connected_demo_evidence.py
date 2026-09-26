from __future__ import annotations
from copy import deepcopy
import pytest
from gold_scalp_trader.diagnostics.connected_demo import EXTERNAL_DRILL_KEYS,aggregate_connected_demo_reports,apply_operator_drill_evidence

EXPECTED_EXTERNAL_DRILLS={"broker_side_close_visibility","manual_known_trade_close_drill","ambiguous_ack_no_duplicate_drill","restart_during_active_lifecycle","fresh_machine_restore_handoff","broker_schedule_preclose_dst_holiday","spread_slippage_deviation_distribution","latency_distribution","protect_trail_modify_drill","broker_side_tp_sl_close_drill","strategy_isolation_attribution","m1_refinement_timing","three_loss_cooldown_persistence","shadow_learning_report"}

def _report(*,spread:float=.20,age:float=.10,open_:str="PENDING",modify:str="PENDING",close:str="PENDING",learning:str="PENDING",unresolved:str="PASS"):
    return {"captured_at_utc":"2026-09-25T12:00:00+00:00","mode":"DEMO","broker_write_performed_by_this_tool":False,"real_release_enabled":False,"account_scope_sha256":"scope-a","symbol":"XAUUSDm","quote":{"spread":spread,"age_seconds":age},"positions_verified_count":0,"phase15":{"connected_demo_identity":"PASS","symbol_spec_observed":"PASS","fresh_quote_observed":"PASS","state_integrity":"PASS","verified_open_observed":open_,"verified_modify_observed":modify,"verified_close_observed":close,"broker_side_close_visibility":"PENDING","actual_learning_observed":learning,"unresolved_intent_clear":unresolved,"manual_known_trade_close_drill":"PENDING_OPERATOR_DRILL","ambiguous_ack_no_duplicate_drill":"PENDING_SAFE_CONNECTED_DRILL","restart_during_active_lifecycle":"PENDING_CONNECTED_DRILL","fresh_machine_restore_handoff":"PENDING_CONNECTED_DRILL","broker_schedule_preclose_dst_holiday":"PENDING_OBSERVATION","spread_slippage_deviation_distribution":"PENDING_SAMPLE","latency_distribution":"PENDING_SAMPLE","protect_trail_modify_drill":"PENDING_CONNECTED_DRILL","broker_side_tp_sl_close_drill":"PENDING_CONNECTED_DRILL","strategy_isolation_attribution":"PENDING_CONNECTED_DRILL","m1_refinement_timing":"PENDING_SAMPLE","three_loss_cooldown_persistence":"PENDING_CONNECTED_DRILL","shadow_learning_report":"PENDING_SAMPLE"}}

def _evidence(drill:str,*,observed:str="2026-09-25T11:59:00+00:00",valid_until:str|None=None):
    return {"schema_version":1,"mode":"DEMO","account_scope_sha256":"scope-a","symbol":"XAUUSDm","drill":drill,"result":"PASS","observed_at_utc":observed,"artifact_name":"evidence.txt","artifact_sha256":"a"*64,"valid_until_utc":valid_until,"note":"controlled connected drill","broker_write_performed_by_this_tool":False,"real_release_enabled":False}

def test_canonical_external_drill_set_is_not_silently_shrunk():assert set(EXTERNAL_DRILL_KEYS)==EXPECTED_EXTERNAL_DRILLS

def test_accumulator_keeps_lifecycle_evidence_without_false_full_pass():
    a=_report(open_="PASS",modify="PASS"); b=_report(close="PASS",learning="PASS",spread=.30,age=.20); b["captured_at_utc"]="2026-09-25T12:01:00+00:00"; s=aggregate_connected_demo_reports([a,b]); assert s["core_demo_lifecycle_observed"]=="PASS" and s["full_connected_certification"]=="INCOMPLETE"; assert s["quote"]["spread_min"]==pytest.approx(.20) and s["quote"]["spread_max"]==pytest.approx(.30)

def test_external_drills_accumulate_only_after_explicit_pass():
    a=_report(); b=_report(); b["captured_at_utc"]="2026-09-25T12:01:00+00:00"; b["phase15"]["broker_side_close_visibility"]="PASS"; b["phase15"]["manual_known_trade_close_drill"]="PASS"; s=aggregate_connected_demo_reports([a,b]); assert s["phase15"]["broker_side_close_visibility"]=="PASS"; assert s["phase15"]["restart_during_active_lifecycle"].startswith("PENDING")

def test_latest_unresolved_intent_state_is_not_laundered():
    a=_report(open_="PASS",modify="PASS",close="PASS",learning="PASS",unresolved="PASS"); b=_report(unresolved="PENDING"); b["captured_at_utc"]="2026-09-25T12:01:00+00:00"; s=aggregate_connected_demo_reports([a,b]); assert s["phase15"]["unresolved_intent_clear"]=="PENDING" and s["core_demo_lifecycle_observed"]=="INCOMPLETE"

def test_scope_mismatch_is_rejected():
    a=_report(); b=deepcopy(a); b["account_scope_sha256"]="scope-b"
    with pytest.raises(ValueError,match="different account/symbol scopes"):aggregate_connected_demo_reports([a,b])

def test_monitor_evidence_cannot_claim_real_or_broker_write():
    r=_report(); r["real_release_enabled"]=True
    with pytest.raises(ValueError,match="REAL release"):aggregate_connected_demo_reports([r])
    r=_report(); r["broker_write_performed_by_this_tool"]=True
    with pytest.raises(ValueError,match="unexpected broker write"):aggregate_connected_demo_reports([r])

def test_operator_drill_evidence_requires_exact_scope_artifact_and_read_only_claims():
    r=_report(); e=_evidence("restart_during_active_lifecycle"); applied=apply_operator_drill_evidence(r,[e]); assert applied["phase15"]["restart_during_active_lifecycle"]=="PASS"
    bad=dict(e); bad["account_scope_sha256"]="other"
    with pytest.raises(ValueError,match="scope/symbol mismatch"):apply_operator_drill_evidence(r,[bad])
    bad=dict(e); bad["artifact_sha256"]="not-a-hash"
    with pytest.raises(ValueError,match="artifact_name"):apply_operator_drill_evidence(r,[bad])
    bad=dict(e); bad["broker_write_performed_by_this_tool"]=True
    with pytest.raises(ValueError,match="unexpected broker write"):apply_operator_drill_evidence(r,[bad])
    bad=dict(e); bad["real_release_enabled"]=True
    with pytest.raises(ValueError,match="REAL release"):apply_operator_drill_evidence(r,[bad])

def test_schedule_evidence_expires_instead_of_laundering_old_schedule_truth():
    r=_report(); expired=_evidence("broker_schedule_preclose_dst_holiday",valid_until="2026-09-25T11:59:30+00:00"); applied=apply_operator_drill_evidence(r,[expired]); assert applied["phase15"]["broker_schedule_preclose_dst_holiday"].startswith("PENDING")
    current=_evidence("broker_schedule_preclose_dst_holiday",valid_until="2026-09-25T13:00:00+00:00"); applied=apply_operator_drill_evidence(r,[current]); assert applied["phase15"]["broker_schedule_preclose_dst_holiday"]=="PASS"

def test_full_certification_requires_every_canonical_external_drill():
    r=_report(open_="PASS",modify="PASS",close="PASS",learning="PASS"); r["phase15"]["broker_side_close_visibility"]="PASS"; records=[]
    for drill in EXTERNAL_DRILL_KEYS:
        if drill=="broker_side_close_visibility":continue
        records.append(_evidence(drill,valid_until="2026-09-25T13:00:00+00:00" if drill=="broker_schedule_preclose_dst_holiday" else None))
    complete=apply_operator_drill_evidence(r,records); assert aggregate_connected_demo_reports([complete])["full_connected_certification"]=="PASS"
    incomplete=deepcopy(complete); incomplete["phase15"]["m1_refinement_timing"]="PENDING_SAMPLE"; assert aggregate_connected_demo_reports([incomplete])["full_connected_certification"]=="INCOMPLETE"
