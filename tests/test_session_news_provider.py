import json
from datetime import datetime,timedelta,timezone
import pytest
from gold_scalp_trader.app.session_news import ProviderContractError,load_scoped_file
from gold_scalp_trader.domain.enums import MarketState,ProviderHealth
UTC=timezone.utc
def write(tmp_path,payload):
    path=tmp_path/"session_news.json"; path.write_text(json.dumps(payload),encoding="utf-8"); return path
def base(now):
    return {"schema_version":1,"provider":"TEST","scope":{"account_login":123,"server":"Exness-Demo","symbol":"XAUUSDm"},"session":{"observed_at_utc":now.isoformat(),"valid_until_utc":(now+timedelta(minutes=30)).isoformat(),"schedule_verified":True,"tradeable":True,"market_state":"OPEN","clean_completed_m5_since_reopen":2,"execution_normalized":True,"unresolved_gap_or_reconciliation":False},"news":{"provider_health":"VERIFIED","fetched_at_utc":now.isoformat(),"events":[]}}
def load(path,now):return load_scoped_file(path,account_login=123,server="Exness-Demo",symbol="XAUUSDm",as_of_utc=now)
def test_verified_open_and_news_are_separate(tmp_path):
    now=datetime(2026,9,26,10,tzinfo=UTC); snapshot=load(write(tmp_path,base(now)),now); assert snapshot.session.state is MarketState.OPEN; assert snapshot.session.hard_new_entry_allowed; assert snapshot.news.health is ProviderHealth.VERIFIED; assert snapshot.news.hard_trading_permission is None
def test_news_missing_does_not_change_verified_session(tmp_path):
    now=datetime(2026,9,26,10,tzinfo=UTC); payload=base(now); payload.pop("news"); snapshot=load(write(tmp_path,payload),now); assert snapshot.session.state is MarketState.OPEN; assert snapshot.session.hard_new_entry_allowed; assert snapshot.news.health is ProviderHealth.UNAVAILABLE
def test_expired_session_becomes_unknown_while_news_can_still_be_visible(tmp_path):
    now=datetime(2026,9,26,10,tzinfo=UTC); payload=base(now); payload["session"]["valid_until_utc"]=(now-timedelta(seconds=1)).isoformat(); payload["session"]["observed_at_utc"]=(now-timedelta(hours=1)).isoformat(); snapshot=load(write(tmp_path,payload),now); assert snapshot.session.state is MarketState.UNKNOWN; assert not snapshot.session.hard_new_entry_allowed
def test_stale_news_is_soft_only(tmp_path):
    now=datetime(2026,9,26,10,tzinfo=UTC); payload=base(now); payload["news"]["fetched_at_utc"]=(now-timedelta(seconds=1801)).isoformat(); snapshot=load(write(tmp_path,payload),now); assert snapshot.session.hard_new_entry_allowed; assert snapshot.news.health is ProviderHealth.STALE
def test_preclose_is_never_new_entry_allowed(tmp_path):
    now=datetime(2026,9,26,10,tzinfo=UTC); payload=base(now); payload["session"]["market_state"]="PRE_CLOSE"; snapshot=load(write(tmp_path,payload),now); assert snapshot.session.state is MarketState.PRE_CLOSE; assert not snapshot.session.hard_new_entry_allowed
def test_scope_mismatch_rejected(tmp_path):
    now=datetime(2026,9,26,10,tzinfo=UTC); payload=base(now); payload["scope"]["account_login"]=999; path=write(tmp_path,payload)
    with pytest.raises(ProviderContractError):load(path,now)
def test_missing_file_returns_unknown_session_and_unavailable_news(tmp_path):
    now=datetime(2026,9,26,10,tzinfo=UTC); snapshot=load(tmp_path/"missing.json",now); assert snapshot.session.state is MarketState.UNKNOWN; assert snapshot.news.health is ProviderHealth.UNAVAILABLE
