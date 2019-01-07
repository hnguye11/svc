from __future__ import division
import time
import numpy as np
import threading
import sys
import socket

import shared_buffer
from config import *
from util import *


def send_pilot_bus_v(debug=False):
    sb = shared_buffer.shared_buffer_array()
    for bus in PILOT_BUS: sb.open(PILOT_BUS_V%bus, isProxy=False)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        for bus in PILOT_BUS:
            sender_id, msg = sb.read(PILOT_BUS_V%bus)
            sock.sendto(msg, (CONTROLLER_IP_ADDR, PILOT_BUS_V_PORT))
            if debug and bus==2: print_udp(CONTROLLER_IP_ADDR, PILOT_BUS_V_PORT, msg, isSend=True)

        time.sleep(SLEEP_TIME)
    

if __name__ == "__main__":
    send_pilot_bus_v(debug=True)
