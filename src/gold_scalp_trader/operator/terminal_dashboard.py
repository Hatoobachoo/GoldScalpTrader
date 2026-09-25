from .presentation import DashboardData
def render(d:DashboardData)->str:
    return f"{d.symbol} {d.bid}/{d.ask} | SETUP {d.detected_setup} | ACTIVE {d.active_family} | {d.live_action} | {d.reason}"
