from __future__ import division
import subprocess
import numpy as np
import time

import shared_buffer
from config import *
from util import *
from pss_driver import MatPowerDriver


def proxy(debug=False):
    # Voltage setpoints at generator buses, later modified by controller
    vg = {gen:BUS_VM[gen] for gen in GEN}

    # Reactive power at load buses, later modified by disturbance
    q = {load:LOAD_PQ[load][1] for load in LOAD}
    
    sb = shared_buffer.shared_buffer_array()    
    for load in LOAD: sb.open(LOAD_BUS_Q%load, isProxy=True)
    for gen in GEN: sb.open(GEN_BUS_V%gen, isProxy=True)
    for bus in PILOT_BUS: sb.open(PILOT_BUS_V%bus, isProxy=True)
    
    sb.open(PLOT_LOAD_BUS_Q, isProxy=True)
    sb.open(PLOT_GEN_BUS_V, isProxy=True)
    sb.open(PLOT_PILOT_BUS_V, isProxy=True)

    mp = MatPowerDriver(workingdir="data")
    mp.open("/home/frank/Workspace/svc/data/case39")
    
    while True:
        writelist = []

        for gen in GEN:
            sender_id, msg = sb.read(GEN_BUS_V%gen)
            if msg != "":
                key, value = str_to_kv(msg)
                assert(key in GEN)
                vg[gen] = value
                if debug and gen == 30: print_buffer(GEN_BUS_V%gen, msg, isWrite=False)

            writelist += [("gen", str(gen), "v", str(vg[gen]))]
            
        for load in LOAD:
            sender_id, msg = sb.read(LOAD_BUS_Q%load)
            if msg != "":
                key, value = str_to_kv(msg)
                assert(key in LOAD)
                q[load] = value
                if debug and load == 1: print_buffer(LOAD_BUS_Q%load, msg, isWrite=False)
            
            writelist += [("load", str(load), "q", str(q[load]))]

        mp.write_multiple(writelist)
        
        # Solve power flow
        mp.run_pf()
        
        # Read result
        vp = {bus:float(mp.read("bus", str(bus), "v")) for bus in PILOT_BUS}
        
        # Write result to shared buffer
        for bus in PILOT_BUS:
            msg = kv_to_str(bus, vp[bus])
            sb.write(PILOT_BUS_V%bus, msg, PROXY_ID)
            if debug and bus == 2: print_buffer(PILOT_BUS_V%bus, msg, isWrite=True)
                
        msg = ";".join(kv_to_str(bus, vp[bus]) for bus in PILOT_BUS)
        sb.write(PLOT_PILOT_BUS_V, msg, PROXY_ID)

        msg = ";".join(kv_to_str(load, q[load]) for load in LOAD)
        sb.write(PLOT_LOAD_BUS_Q, msg, PROXY_ID)

        msg = ";".join(kv_to_str(gen, vg[gen]) for gen in GEN)
        sb.write(PLOT_GEN_BUS_V, msg, PROXY_ID)

        time.sleep(BUSY_WAITING_TIME)


if __name__ == "__main__":
    proxy(debug=True)
