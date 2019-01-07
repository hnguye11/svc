#!/bin/sh
nohup python proxy.py &
nohup python controller.py &
nohup python disturbance.py &
nohup python plc.py &
nohup python pmu.py &
nohup python anim.py &
