"""
simulation.disturbances
=======================

Stochastic generators for the simulator: late kits, sick operators,
process-time noise, quality rework. Sampling functions take a deterministic
scenario and a random seed and return a realised set of disturbances for
one simulation run.

See `docs/body_shop_formulation.pdf` §6 for the stochastic specification.
"""

# TODO: sample_kit_delays, sample_absences, sample_process_noise, sample_rework
