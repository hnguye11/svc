from __future__ import division
import time
import random

import shared_buffer
from config import *
from util import *


def update_load_bus_q(debug=False):
    sb = shared_buffer.shared_buffer_array()
    for load in LOAD: sb.open(LOAD_BUS_Q%load, isProxy=False)
    q = {load:LOAD_PQ[load][1] for load in LOAD}
    count = -3
    scale = 1
    cycle = 20
    
    while True:
        if count % cycle == 0:
            scale = (1.0 + 0.1 * (1 - (count // cycle) % 3))
            
        for load in LOAD:
            q[load] = LOAD_PQ[load][1] * scale
            msg = kv_to_str(load, q[load])
            sb.write(LOAD_BUS_Q%load, msg, DISTURBANCE_ID)
            if debug and load == 1: print_buffer(LOAD_BUS_Q%load, msg, isWrite=True)
            
        count += 1
        time.sleep(SLEEP_TIME)

        
if __name__ == "__main__":
    update_load_bus_q(debug=True)
