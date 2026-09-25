"""Tk Canvas candlestick renderer without scrollbars."""
from __future__ import annotations

def draw_candles(canvas,candles):
    canvas.delete("all")
    if not candles:return
    w=max(1,int(canvas.winfo_width() or 800)); h=max(1,int(canvas.winfo_height() or 420)); visible=candles[-80:]
    hi=max(c.high for c in visible); lo=min(c.low for c in visible); span=max(hi-lo,1e-9); step=w/max(len(visible),1)
    def y(p):return h-(p-lo)/span*h
    for i,c in enumerate(visible):
        x=(i+.5)*step; up=c.close>=c.open; color="#35e0b7" if up else "#ff647c"; canvas.create_line(x,y(c.low),x,y(c.high),fill=color,width=1); canvas.create_rectangle(x-step*.28,y(max(c.open,c.close)),x+step*.28,y(min(c.open,c.close)),outline=color,fill=color)
