from __future__ import division
import time
import numpy as np
import socket

import shared_buffer
from config import *
from util import *


def recv_gen_bus_v(debug=False):
    sb = shared_buffer.shared_buffer_array()
    for gen in GEN: sb.open(GEN_BUS_V%gen, isProxy=False)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", GEN_BUS_V_PORT))

    while True:
        data, addr = sock.recvfrom(1000)
        key, value = str_to_kv(data)
        assert(key in GEN)
        sb.write(GEN_BUS_V%key, data, CONTROLLER_ID)
        if debug and key == 30: print_buffer(GEN_BUS_V%key, data, isWrite=True)
    

if __name__ == "__main__":
    recv_gen_bus_v(debug=True)
