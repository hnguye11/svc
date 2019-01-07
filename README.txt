CONTROLLER:
- receive pilot bus voltages from PMU over udp
- compute gen bus voltage setpoints periodically
- send gen bus voltage setpoints to PLC over udp

PLC:
- receive gen bus voltage setpoints from CONTROLLER over udp
- write gen bus voltage setpoints to PROXY's shared buffer

PMU:
- read pilot bus voltages from PROXY's shared buffer
- send pilot bus voltages to CONTROLLER over udp periodically

DISTURBANCE:
- write load reactive powers to PROXY's shared buffer periodically

PROXY:
- read gen bus voltage setpoints from shared buffer
- read load reactive powers from shared buffer
- run power flow
- write pilot bus voltages to shared buffer
- write measurements to shared buffer for plotting
