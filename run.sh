#!/bin/sh
nohup python disturbance.py &
nohup python proxy_with_driver.py &
nohup python pmu.py &
nohup python controller.py &
nohup python plc.py &
nohup python anim.py &
