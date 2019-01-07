from __future__ import division
import time
import random

import shared_buffer
from config import *
from util import *


def update_load_bus_q(debug=False):
    sb = shared_buffer.shared_buffer_array()
    for load in LOAD: sb.open(LOAD_BUS_Q%load, isProxy=False)
    q = {load:1.0 for load in LOAD}
    count = 0
    
    while True:
        # q = {load:1+0.1*(1-(count//10)%3) for load in LOAD}
        for load in LOAD:
            if count % 20 == 0:
                q[load] = 1.0 + 0.1 * (1 - (count//20)%3)
            else:
                q[load] += 0.01 * (0.5 - random.random())
                q[load] = min(1.1, max(0.9, q[load]))

            msg = kv_to_str(load, q[load])
            sb.write(LOAD_BUS_Q%load, msg, DISTURBANCE_ID)
            if debug and load == 1: print_buffer(LOAD_BUS_Q%load, msg, isWrite=True)
            
        count += 1
        time.sleep(SLEEP_TIME)

        
if __name__ == "__main__":
    update_load_bus_q(debug=True)
