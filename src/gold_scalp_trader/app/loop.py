import time
def run_loop(step,*,interval_seconds:float=1.0,max_cycles:int|None=None):
    count=0
    while max_cycles is None or count<max_cycles:
        yield step(); count+=1
        if max_cycles is None or count<max_cycles:time.sleep(interval_seconds)
