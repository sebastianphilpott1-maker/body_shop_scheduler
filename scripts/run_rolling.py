"""
run_rolling.py
==============

Run the full rolling-horizon controller: solve, simulate-until-trigger,
re-solve, ... until the shift completes. Compare against the static
schedule's realised performance from `simulate_static.py`.

Usage:
    python scripts/run_rolling.py [--runs 100] [--seed 42]
"""

# TODO: controller orchestration, KPI rollup, comparison plots
