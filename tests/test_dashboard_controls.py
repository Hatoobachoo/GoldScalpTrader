from graphical_dashboard.controls import ChartControlState

def test_chart_controls_are_functional_presentation_state_only():
    s=ChartControlState(); s.set_timeframe("M1"); assert s.timeframe=="M1"
    old=s.indicators_visible; s.toggle_indicators(); assert s.indicators_visible is not old
    s.toggle_drawings(); assert s.drawings_enabled
    s.toggle_settings(); assert s.settings_open
