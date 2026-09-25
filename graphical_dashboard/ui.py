"""Approved one-screen/no-scroll local graphical dashboard."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from .controls import ChartControlState
from .chart import draw_candles
class DashboardApp:
    def __init__(self,provider):
        self.provider=provider; self.root=tk.Tk(); self.root.title("GoldScalpTraderAI"); self.root.geometry("1600x900"); self.root.minsize(1280,720); self.state=ChartControlState(); self._build(); self.refresh()
    def _build(self):
        self.root.configure(bg="#06111f"); style=ttk.Style(); style.theme_use("clam")
        top=tk.Frame(self.root,bg="#06111f"); top.pack(fill="x",padx=8,pady=6); tk.Label(top,text="GoldScalpTraderAI",fg="#e6b84a",bg="#06111f",font=("Segoe UI",18,"bold")).pack(side="left"); self.status=tk.Label(top,text="",fg="#52e8e8",bg="#06111f",font=("Consolas",10)); self.status.pack(side="right")
        body=tk.Frame(self.root,bg="#06111f"); body.pack(fill="both",expand=True,padx=8,pady=4); body.grid_columnconfigure(1,weight=1); body.grid_rowconfigure(0,weight=1)
        self.left=tk.Text(body,width=30,bg="#0a1b2e",fg="#d8ecff",relief="flat",font=("Consolas",10)); self.left.grid(row=0,column=0,sticky="ns",padx=(0,6)); self.left.configure(state="disabled")
        center=tk.Frame(body,bg="#071827"); center.grid(row=0,column=1,sticky="nsew"); center.grid_rowconfigure(1,weight=1); center.grid_columnconfigure(0,weight=1)
        controls=tk.Frame(center,bg="#071827"); controls.grid(row=0,column=0,sticky="ew")
        for tf in ("M1","M5","M15","H1","H4"):tk.Button(controls,text=tf,command=lambda x=tf:self._tf(x),bg="#0d2940",fg="#8ff",relief="flat").pack(side="left",padx=2,pady=3)
        tk.Button(controls,text="Indicators",command=self._ind,bg="#0d2940",fg="#8ff",relief="flat").pack(side="left",padx=8); tk.Button(controls,text="Drawings",command=self._draw,bg="#0d2940",fg="#8ff",relief="flat").pack(side="left",padx=2); tk.Button(controls,text="Settings",command=self._settings,bg="#0d2940",fg="#8ff",relief="flat").pack(side="left",padx=2)
        self.canvas=tk.Canvas(center,bg="#071827",highlightthickness=1,highlightbackground="#1b8497"); self.canvas.grid(row=1,column=0,sticky="nsew")
        self.right=tk.Text(body,width=42,bg="#0a1b2e",fg="#d8ecff",relief="flat",font=("Consolas",10)); self.right.grid(row=0,column=2,sticky="ns",padx=(6,0)); self.right.configure(state="disabled")
        bottom=tk.Frame(self.root,bg="#071827"); bottom.pack(fill="x",padx=8,pady=(4,8)); self.bottom=tk.Label(bottom,text="",anchor="w",justify="left",fg="#b8d8ec",bg="#071827",font=("Consolas",9)); self.bottom.pack(fill="x")
    def _tf(self,tf):self.state.set_timeframe(tf); self.refresh()
    def _ind(self):self.state.toggle_indicators(); self.refresh()
    def _draw(self):self.state.toggle_drawings(); self.refresh()
    def _settings(self):self.state.toggle_settings(); self.refresh()
    def _set_text(self,widget,text):widget.configure(state="normal"); widget.delete("1.0","end"); widget.insert("1.0",text); widget.configure(state="disabled")
    def refresh(self):
        data,candles_by_tf=self.provider(); candles=candles_by_tf.get(self.state.timeframe,())
        self.status.configure(text=f"{data.market_state} | {data.bot_status} | {self.state.timeframe}")
        self._set_text(self.left,f"SYMBOL  {data.symbol}\nBID     {data.bid}\nASK     {data.ask}\nSPREAD  {data.spread}\nSESSION {data.soft_session}\n\nRISK\n{data.risk_text}\n\nNEWS\n{data.news_text}")
        self._set_text(self.right,f"DETECTED SETUP\n{data.detected_setup}\n\nACTIVE TEST FAMILY\n{data.active_family}\n\nLIVE ACTION\n{data.live_action}\n\nREASON\n{data.reason}\n\nSHADOW\n"+"\n".join(data.shadow_setups or ("None",))+f"\n\nGATE\n{data.gate_text}")
        self.bottom.configure(text=f"Indicators={'ON' if self.state.indicators_visible else 'OFF'} | Drawings={'ON' if self.state.drawings_enabled else 'OFF'} | Settings={'OPEN' if self.state.settings_open else 'CLOSED'} | {data.system_text}")
        self.canvas.after_idle(lambda:draw_candles(self.canvas,candles))
    def run(self):self.root.mainloop()
