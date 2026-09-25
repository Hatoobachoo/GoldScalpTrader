"""Approved one-screen/no-scroll local graphical dashboard.

Timeframe, indicator, drawing and settings controls are real local interactions.
They mutate presentation state only and never trading authority. Broker/runtime
polling occurs only on the fixed timer, never because a chart button was clicked.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from .controls import ChartControlState
from .chart import draw_candles


class DashboardApp:
    def __init__(
        self,
        provider: Callable,
        *,
        refresh_ms: int = 2000,
        on_close: Callable[[], None] | None = None,
    ):
        self.provider = provider
        self.refresh_ms = max(250, int(refresh_ms))
        self.on_close = on_close
        self.root = tk.Tk()
        self.root.title("GoldScalpTraderAI")
        self.root.geometry("1600x900")
        self.root.minsize(1280, 720)
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self.state = ChartControlState()
        self._last_candles = ()
        self._latest_data = None
        self._latest_candles_by_tf = {}
        self._closed = False
        self._after_id = None
        self._build()
        self._after_id = self.root.after(0, self._poll)

    def _build(self):
        self.root.configure(bg="#06111f")
        style = ttk.Style()
        style.theme_use("clam")

        top = tk.Frame(self.root, bg="#06111f")
        top.pack(fill="x", padx=8, pady=6)
        tk.Label(
            top,
            text="GoldScalpTraderAI",
            fg="#e6b84a",
            bg="#06111f",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left")
        self.status = tk.Label(
            top,
            text="STARTING...",
            fg="#52e8e8",
            bg="#06111f",
            font=("Consolas", 10),
        )
        self.status.pack(side="right")

        body = tk.Frame(self.root, bg="#06111f")
        body.pack(fill="both", expand=True, padx=8, pady=4)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.left = tk.Text(
            body,
            width=32,
            bg="#0a1b2e",
            fg="#d8ecff",
            relief="flat",
            font=("Consolas", 10),
            wrap="word",
        )
        self.left.grid(row=0, column=0, sticky="ns", padx=(0, 6))
        self.left.configure(state="disabled")

        center = tk.Frame(body, bg="#071827")
        center.grid(row=0, column=1, sticky="nsew")
        center.grid_rowconfigure(1, weight=1)
        center.grid_columnconfigure(0, weight=1)

        controls = tk.Frame(center, bg="#071827")
        controls.grid(row=0, column=0, sticky="ew")
        for tf in ("M1", "M5", "M15", "H1", "H4"):
            tk.Button(
                controls,
                text=tf,
                command=lambda value=tf: self._tf(value),
                bg="#0d2940",
                fg="#8ff",
                relief="flat",
            ).pack(side="left", padx=2, pady=3)
        tk.Button(
            controls,
            text="Indicators",
            command=self._ind,
            bg="#0d2940",
            fg="#8ff",
            relief="flat",
        ).pack(side="left", padx=8)
        tk.Button(
            controls,
            text="Drawings",
            command=self._draw,
            bg="#0d2940",
            fg="#8ff",
            relief="flat",
        ).pack(side="left", padx=2)
        tk.Button(
            controls,
            text="Settings",
            command=self._settings,
            bg="#0d2940",
            fg="#8ff",
            relief="flat",
        ).pack(side="left", padx=2)

        self.canvas = tk.Canvas(
            center,
            bg="#071827",
            highlightthickness=1,
            highlightbackground="#1b8497",
        )
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self._canvas_click)
        self.canvas.bind("<MouseWheel>", self._zoom)

        self.right = tk.Text(
            body,
            width=48,
            bg="#0a1b2e",
            fg="#d8ecff",
            relief="flat",
            font=("Consolas", 10),
            wrap="word",
        )
        self.right.grid(row=0, column=2, sticky="ns", padx=(6, 0))
        self.right.configure(state="disabled")

        bottom = tk.Frame(self.root, bg="#071827")
        bottom.pack(fill="x", padx=8, pady=(4, 8))
        self.bottom = tk.Label(
            bottom,
            text="",
            anchor="w",
            justify="left",
            fg="#b8d8ec",
            bg="#071827",
            font=("Consolas", 9),
        )
        self.bottom.pack(fill="x")

    def _poll(self):
        if self._closed:
            return
        try:
            data, candles_by_tf = self.provider()
            self._latest_data = data
            self._latest_candles_by_tf = candles_by_tf
            self.refresh()
        except PermissionError as exc:
            self.status.configure(text=f"SAFETY STOP | {exc}", fg="#ff647c")
            self._set_text(self.right, f"SAFETY STOP\n\n{exc}\n\nNo further broker cycles scheduled.")
            return
        except Exception as exc:
            self.status.configure(text=f"DEGRADED | {type(exc).__name__}: {exc}", fg="#ffb86c")
        if not self._closed:
            self._after_id = self.root.after(self.refresh_ms, self._poll)

    def _tf(self, timeframe):
        self.state.set_timeframe(timeframe)
        self.refresh()

    def _ind(self):
        self.state.toggle_indicators()
        self.refresh()

    def _draw(self):
        self.state.toggle_drawings()
        self.refresh()

    def _settings(self):
        self.state.toggle_settings()
        if self.state.settings_open:
            self._open_settings()
        self.refresh()

    def _open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Chart Settings")
        win.configure(bg="#0a1b2e")
        win.transient(self.root)
        tk.Label(win, text="Candle count", bg="#0a1b2e", fg="#d8ecff").grid(
            row=0, column=0, padx=8, pady=8
        )
        var = tk.IntVar(value=self.state.candle_limit)
        tk.Spinbox(win, from_=20, to=300, textvariable=var, width=8).grid(
            row=0, column=1, padx=8, pady=8
        )
        for idx, name in enumerate(("EMA20", "EMA50"), start=1):
            enabled = tk.BooleanVar(value=name in self.state.overlays)
            tk.Checkbutton(
                win,
                text=name,
                variable=enabled,
                bg="#0a1b2e",
                fg="#d8ecff",
                selectcolor="#0d2940",
                command=lambda n=name, value=enabled: self._set_overlay(n, value.get()),
            ).grid(row=idx, column=0, columnspan=2, sticky="w", padx=8)

        def apply():
            self.state.set_candle_limit(int(var.get()))
            self.state.settings_open = False
            win.destroy()
            self.refresh()

        tk.Button(win, text="Apply", command=apply).grid(row=4, column=0, padx=8, pady=10)
        tk.Button(
            win,
            text="Clear drawings",
            command=lambda: (self.state.clear_drawings(), self.refresh()),
        ).grid(row=4, column=1, padx=8, pady=10)
        win.protocol(
            "WM_DELETE_WINDOW",
            lambda: (setattr(self.state, "settings_open", False), win.destroy(), self.refresh()),
        )

    def _set_overlay(self, name, enabled):
        if (name in self.state.overlays) != enabled:
            self.state.toggle_overlay(name)
        self.refresh()

    def _zoom(self, event):
        step = -10 if event.delta > 0 else 10
        target = max(20, min(300, self.state.candle_limit + step))
        if target != self.state.candle_limit:
            self.state.set_candle_limit(target)
            self.refresh()

    def _canvas_click(self, event):
        if not self.state.drawings_enabled or not self._last_candles:
            return
        visible = self._last_candles[-self.state.candle_limit :]
        high = max(candle.high for candle in visible)
        low = min(candle.low for candle in visible)
        height = max(1, self.canvas.winfo_height())
        price = high - (event.y / height) * (high - low)
        self.state.add_horizontal_drawing(price)
        self.refresh()

    def _set_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def refresh(self):
        """Redraw only the cached presentation snapshot; never poll/trade here."""
        data = self._latest_data
        if data is None:
            return
        candles = self._latest_candles_by_tf.get(self.state.timeframe, ())
        self._last_candles = candles
        self.status.configure(
            text=f"{data.market_state} | {data.bot_status} | {self.state.timeframe}",
            fg="#52e8e8",
        )
        self._set_text(
            self.left,
            f"MARKET / مارکیٹ\n"
            f"SYMBOL  {data.symbol}\n"
            f"BID     {data.bid}\n"
            f"ASK     {data.ask}\n"
            f"SPREAD  {data.spread}\n"
            f"SESSION {data.soft_session}\n\n"
            f"RISK / رسک\n{data.risk_text}\n\n"
            f"TRADE PLAN\n{data.trade_plan_text}\n\n"
            f"NEWS / CONTEXT\n{data.news_text}",
        )
        shadows = "\n".join(data.shadow_setups or ("None",))
        self._set_text(
            self.right,
            f"DETECTED SETUP / موجودہ سیٹ اپ\n{data.detected_setup}\n\n"
            f"ACTIVE TEST FAMILY / فعال حکمت عملی\n{data.active_family}\n\n"
            f"LIVE ACTION / عمل\n{data.live_action}\n\n"
            f"REASON\n{data.reason}\n\n"
            f"SHADOW / OBSERVE ONLY\n{shadows}\n\n"
            f"MANAGED TRADE\n{data.managed_trade_text}\n\n"
            f"EXECUTION\n{data.execution_text}\n\n"
            f"GATE\n{data.gate_text}",
        )
        self.bottom.configure(
            text=(
                f"Indicators={'ON' if self.state.indicators_visible else 'OFF'} | "
                f"Drawings={'ON' if self.state.drawings_enabled else 'OFF'} | "
                f"Bars={self.state.candle_limit} | "
                f"{data.activity_text} | {data.learning_text} | {data.system_text}"
            )
        )
        self.canvas.after_idle(
            lambda: draw_candles(
                self.canvas,
                candles,
                indicators_visible=self.state.indicators_visible,
                overlays=self.state.overlays,
                horizontal_drawings=self.state.horizontal_drawings,
                candle_limit=self.state.candle_limit,
            )
        )

    def _close(self):
        if self._closed:
            return
        self._closed = True
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
        if self.on_close is not None:
            self.on_close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
