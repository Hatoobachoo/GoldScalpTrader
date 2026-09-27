import pytest

from gold_scalp_trader.config import PRESERVED_RISK_BANDS, Settings, validate_settings
from gold_scalp_trader.domain.enums import RuntimeMode, StrategyFamily


def test_preserved_risk_bands_are_exact():
    assert PRESERVED_RISK_BANDS["SMALL"].normal_min_pct == 3.0
    assert PRESERVED_RISK_BANDS["SMALL"].normal_max_pct == 4.5
    assert PRESERVED_RISK_BANDS["SMALL"].hard_ceiling_pct == 7.0
    assert PRESERVED_RISK_BANDS["SMALL"].daily_loss_lock_pct == 12.0
    assert PRESERVED_RISK_BANDS["MEDIUM"].hard_ceiling_pct == 5.0
    assert PRESERVED_RISK_BANDS["NORMAL"].hard_ceiling_pct == 4.0


def test_safe_defaults_have_no_write_capability():
    settings = Settings()
    validate_settings(settings)
    assert settings.mode is RuntimeMode.DRY_RUN
    assert settings.broker_write_enabled is False
    assert settings.aggressive_small_account is False
    assert settings.manual_daily_loss_reset_enabled is False
    assert settings.max_open_positions == 1


def test_demo_uses_structural_router_not_manual_active_family():
    validate_settings(
        Settings(
            mode=RuntimeMode.DEMO,
            active_strategy_family=None,
            target_risk_percent=3.0,
            demo_trading_confirm="YES_I_APPROVE_DEMO",
        )
    )

    # Legacy/research focus remains accepted for compatibility, but production
    # routing does not consult it.
    validate_settings(
        Settings(
            mode=RuntimeMode.DEMO,
            active_strategy_family=StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
            target_risk_percent=3.0,
            demo_trading_confirm="YES_I_APPROVE_DEMO",
        )
    )


def test_demo_still_requires_target_risk_percent():
    with pytest.raises(ValueError, match="TARGET_RISK_PERCENT"):
        validate_settings(Settings(mode=RuntimeMode.DEMO))
