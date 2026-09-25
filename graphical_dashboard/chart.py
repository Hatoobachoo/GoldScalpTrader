"""Tk Canvas candlestick renderer with optional EMA and local drawings."""
def _ema(values:list[float],period:int)->list[float|None]:
    out=[None]*len(values)
    if len(values)<period:return out
    value=sum(values[:period])/period;out[period-1]=value;alpha=2/(period+1)
    for i in range(period,len(values)):value=values[i]*alpha+value*(1-alpha);out[i]=value
    return out
def draw_candles(canvas,candles,*,indicators_visible=True,overlays=frozenset(),horizontal_drawings=(),candle_limit=80):
    canvas.delete("all")
    if not candles:canvas.create_text(20,20,text="No chart data",fill="#8ba9bd",anchor="nw");return
    w=max(1,int(canvas.winfo_width() or 800));h=max(1,int(canvas.winfo_height() or 420));visible=tuple(candles[-candle_limit:]);extra=list(horizontal_drawings);hi=max([c.high for c in visible]+extra);lo=min([c.low for c in visible]+extra);span=max(hi-lo,1e-9);step=w/max(len(visible),1)
    def y(p):return h-(p-lo)/span*h
    for i,c in enumerate(visible):
        x=(i+.5)*step;color="#35e0b7" if c.close>=c.open else "#ff647c";canvas.create_line(x,y(c.low),x,y(c.high),fill=color,width=1);canvas.create_rectangle(x-step*.28,y(max(c.open,c.close)),x+step*.28,y(min(c.open,c.close)),outline=color,fill=color)
    if indicators_visible:
        closes=[c.close for c in visible]
        for period,name,color in ((20,"EMA20","#5ee7ff"),(50,"EMA50","#e6b84a")):
            if name not in overlays:continue
            points=[]
            for i,value in enumerate(_ema(closes,period)):
                if value is not None:points.extend(((i+.5)*step,y(value)))
            if len(points)>=4:canvas.create_line(*points,fill=color,width=2,smooth=True)
    for price in horizontal_drawings:
        yy=y(price);canvas.create_line(0,yy,w,yy,fill="#c084fc",dash=(5,3));canvas.create_text(w-8,yy-2,text=f"{price:.3f}",fill="#c084fc",anchor="se")
