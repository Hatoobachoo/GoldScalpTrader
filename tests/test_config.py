from gold_scalp_trader.config import Settings, validate_settings


def test_defaults_are_dry_run_and_single_position():
    settings = Settings()
    validate_settings(settings)
    assert settings.mode == "DRY_RUN"
    assert settings.max_open_positions == 1
    assert settings.live_trading_enabled is False


def test_live_requires_explicit_confirmation():
    assert Settings(mode="LIVE", live_trading_confirm="NO").live_trading_enabled is False
    assert (
        Settings(mode="LIVE", live_trading_confirm="YES_I_UNDERSTAND").live_trading_enabled
        is True
    )


def test_risk_above_two_percent_is_rejected():
    try:
        validate_settings(Settings(risk_percent=2.01))
    except ValueError as exc:
        assert "RISK_PERCENT" in str(exc)
    else:
        raise AssertionError("unsafe risk setting was accepted")
