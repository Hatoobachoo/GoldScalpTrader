from .ui import DashboardApp


def run(provider, *, refresh_ms: int = 2000, on_close=None):
    DashboardApp(provider, refresh_ms=refresh_ms, on_close=on_close).run()
