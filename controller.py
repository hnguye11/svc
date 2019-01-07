from __future__ import division
import time
import numpy as np
import threading
import sys
import socket

from config import *
from util import *


def recv_pilot_bus_v(vp, debug=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PILOT_BUS_V_PORT))

    while True:
        data, addr = sock.recvfrom(1000)
        if data != "":
            key, value = str_to_kv(data)
            assert(key in PILOT_BUS)
            vp[key] = value
            if debug and key == 2: print_udp("0.0.0.0", PILOT_BUS_V_PORT, data, isSend=False)


def svc(debug=False):
    vp = {bus:BUS_VM[bus] for bus in PILOT_BUS}
    _vp_nom = np.array([BUS_VM[bus] for bus in PILOT_BUS])
    _vg = np.array([BUS_VM[gen] for gen in GEN])
    
    t = threading.Thread(target=recv_pilot_bus_v, args=(vp,True))
    t.daemon = True
    t.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    C = loadObjectBinary("C.bin")
    Cp = np.matrix([C[i] for i in range(LOAD_NO) if LOAD[i] in PILOT_BUS])
    Cpi = Cp.I
    alpha = 0.5
    
    while True:
        _vp = np.array([vp[bus] for bus in PILOT_BUS])
        u = np.dot(Cpi, alpha * (_vp - _vp_nom)).A1 # 1-d base array
        _vg = np.array(_vg + u)

        for i in range(GEN_NO):
            msg = kv_to_str(GEN[i],_vg[i])
            sock.sendto(msg, (PLC_IP_ADDR, GEN_BUS_V_PORT))
            if debug and GEN[i]==30: print_udp(PLC_IP_ADDR, GEN_BUS_V_PORT, msg, isSend=True)
        
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    svc(debug=True)
