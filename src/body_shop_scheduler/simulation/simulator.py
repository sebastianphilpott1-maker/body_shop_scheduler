"""
simulation.simulator
====================

Discrete-event simulator that advances a Schedule through time under
sampled disturbances. Produces a `RealisedSchedule` showing the actual
(as opposed to planned) start/end times of each operation, plus a flag
for whether each operation completed or was preempted by an out-of-band
event (kit not yet arrived, operator absent, etc.).
"""

# TODO: simulate(schedule, scenario, disturbances) -> RealisedSchedule
