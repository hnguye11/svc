#!/bin/sh
nohup python proxy_with_driver.py &
nohup python controller.py &
nohup python disturbance.py &
nohup python plc.py &
nohup python pmu.py &
nohup python anim.py &
