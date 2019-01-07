from __future__ import division
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import shared_buffer
from config import *
from util import *


def update(num):
    sender_id, msg = sb.read(PLOT_PILOT_BUS_V)
    if msg != "":
        print_buffer(PLOT_PILOT_BUS_V, msg, isWrite=False)
            
        for kv_pair in msg.split(";"):
            key, value = kv_pair.split(",")
            bus = int(key)
            assert(bus in PILOT_BUS)
            vp_t[bus].pop(0)
            vp_t[bus].append(float(value) - BUS_VM[bus])

    sender_id, msg = sb.read(PLOT_GEN_BUS_V)
    if msg != "":
        print_buffer(PLOT_GEN_BUS_V, msg, isWrite=False)
            
        for kv_pair in msg.split(";"):
            key, value = kv_pair.split(",")
            gen = int(key)
            assert(gen in GEN)
            vg_t[gen].pop(0)
            vg_t[gen].append(float(value) - BUS_VM[gen])


    sender_id, msg = sb.read(PLOT_LOAD_BUS_Q)
    if msg != "":
        print_buffer(PLOT_LOAD_BUS_Q, msg, isWrite=False)
            
        for kv_pair in msg.split(";"):
            key, value = kv_pair.split(",")
            load = int(key)
            assert(load in LOAD)
            q_t[load].pop(0)
            q_t[load].append(float(value))

    for ax in [ax1, ax2, ax3]:
        ax.clear()
        ax.grid(True)
        ax.set_xticks([])
        
    for bus in PILOT_BUS:
        ax1.plot(range(size), vp_t[bus], "-o", markersize=3, label="Bus %d"%bus)
        ax1.set_title("Pilot bus voltage deviations")
        ax1.set_ylim(-0.015, 0.015)
        ax1.legend(loc=2)
        
    for gen in GEN:
        ax2.plot(range(size), vg_t[gen], "-o", markersize=3, label="Gen %d"%gen)
        ax2.set_title("Generator bus voltage deviations")
        ax2.set_ylim(-0.015, 0.015)
        ax2.legend(loc=2)
        
    for load in LOAD:
        ax3.plot(range(size), q_t[load], "-", markersize=3) #, label="Load %d"%load)
        ax3.set_title("Reactive power fluctuations")
        ax3.set_ylim(0.85, 1.15)
        # ax3.legend(loc=2,ncol=2)
        
size = 20
vg_t = {gen:[0]*size for gen in GEN}
vp_t = {bus:[0]*size for bus in PILOT_BUS}
q_t = {load:[1]*size for load in LOAD}

sb = shared_buffer.shared_buffer_array()
sb.open(PLOT_GEN_BUS_V, isProxy=False)
sb.open(PLOT_LOAD_BUS_Q, isProxy=False)
sb.open(PLOT_PILOT_BUS_V, isProxy=False)

fig = plt.figure()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
ani = animation.FuncAnimation(fig, update, fargs=[], interval=1000)

plt.show()

