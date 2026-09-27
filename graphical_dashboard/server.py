"""Localhost-only read-only browser dashboard server."""
from __future__ import annotations

from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import webbrowser

from graphical_dashboard.ui import HTML

HOST = "127.0.0.1"
DEFAULT_PORT = 8765
STALE_AFTER_SECONDS = 6.0
SUPPORTED_SCHEMAS = {1, 2}


def load_snapshot(path: Path, *, now_utc: datetime | None = None) -> dict[str, object]:
    now = now_utc or datetime.now(timezone.utc)
    if not path.exists():
        return {"ok": False, "online": False, "age_seconds": None,
                "message": "Waiting for the bot to publish its first dashboard snapshot.",
                "snapshot": None}
    try:
        if path.stat().st_size > 2_000_000:
            raise ValueError("oversized snapshot")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("schema_version") not in SUPPORTED_SCHEMAS:
            raise ValueError("unsupported snapshot schema")
        generated = datetime.fromisoformat(str(payload["generated_at_utc"]))
        if generated.tzinfo is None or generated.utcoffset() is None:
            raise ValueError("snapshot timestamp is not timezone-aware")
        age = (now - generated.astimezone(timezone.utc)).total_seconds()
        if age < -1:
            raise ValueError("snapshot clock is ahead")
        age = max(0.0, age)
        json.dumps(payload, allow_nan=False)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        return {"ok": False, "online": False, "age_seconds": None,
                "message": f"Snapshot unavailable: {type(exc).__name__}", "snapshot": None}
    return {"ok": True, "online": age <= STALE_AFTER_SECONDS,
            "age_seconds": round(age, 2),
            "message": "LIVE" if age <= STALE_AFTER_SECONDS else "BOT OFFLINE / SNAPSHOT STALE",
            "snapshot": payload}


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "GoldScalpTraderAI-VisualFloor/2.0"

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/", "/index.html"}:
            self._send(HTTPStatus.OK, "text/html; charset=utf-8", HTML.encode("utf-8")); return
        if self.path == "/api/snapshot":
            path = getattr(self.server, "snapshot_path")
            payload = json.dumps(load_snapshot(path), ensure_ascii=False,
                                 separators=(",", ":"), allow_nan=False).encode("utf-8")
            self._send(HTTPStatus.OK, "application/json; charset=utf-8", payload); return
        if self.path == "/favicon.ico":
            self._send(HTTPStatus.NO_CONTENT, "image/x-icon", b""); return
        self._send(HTTPStatus.NOT_FOUND, "text/plain; charset=utf-8", b"Not found")

    def do_HEAD(self) -> None:  # noqa: N802
        if self.path in {"/", "/index.html", "/api/snapshot"}:
            self.send_response(HTTPStatus.OK); self._headers(); self.end_headers(); return
        self.send_response(HTTPStatus.NOT_FOUND); self._headers(); self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        self._send(HTTPStatus.METHOD_NOT_ALLOWED, "application/json; charset=utf-8",
                   b'{"error":"read-only dashboard"}')

    def do_PUT(self) -> None:  # noqa: N802
        self.do_POST()

    def do_DELETE(self) -> None:  # noqa: N802
        self.do_POST()

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send(self, status: HTTPStatus, content_type: str, payload: bytes) -> None:
        self.send_response(status); self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload))); self._headers(); self.end_headers()
        if self.command != "HEAD" and payload:
            self.wfile.write(payload)

    def _headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; img-src 'self' data:")


def start_background(snapshot_path: Path, *, port: int = DEFAULT_PORT,
                     open_browser: bool = True) -> tuple[ThreadingHTTPServer, threading.Thread]:
    if not 1 <= port <= 65535:
        raise ValueError("port must be 1..65535")
    server = ThreadingHTTPServer((HOST, port), DashboardHandler)
    server.snapshot_path = snapshot_path  # type: ignore[attr-defined]
    url = f"http://{HOST}:{port}"
    thread = threading.Thread(target=server.serve_forever,
                              kwargs={"poll_interval": 0.5}, daemon=True)
    thread.start()
    print("GoldScalpTraderAI Visual Floor (SECONDARY)")
    print(f"Read-only localhost: {url}")
    print(f"Snapshot: {snapshot_path}")
    print("Primary operator dashboard remains the terminal. Browser has no MT5 writer authority.")
    if open_browser:
        threading.Timer(0.35, lambda: webbrowser.open(url)).start()
    return server, thread


def stop_background(server: ThreadingHTTPServer, thread: threading.Thread) -> None:
    server.shutdown(); server.server_close(); thread.join(timeout=2.0)


def serve(snapshot_path: Path, *, port: int = DEFAULT_PORT, open_browser: bool = True) -> None:
    server, thread = start_background(snapshot_path, port=port, open_browser=open_browser)
    try:
        while thread.is_alive():
            thread.join(timeout=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        stop_background(server, thread)


__all__ = ["DEFAULT_PORT", "DashboardHandler", "HOST", "STALE_AFTER_SECONDS",
           "SUPPORTED_SCHEMAS", "load_snapshot", "serve", "start_background", "stop_background"]
