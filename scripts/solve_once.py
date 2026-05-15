"""
solve_once.py
=============

Load a scenario from CSVs, build the CP-SAT model, solve it once,
print the schedule, render a Gantt chart.

Usage:
    python scripts/solve_once.py [--data-dir data/] [--mode lex|weighted]
"""

# TODO: argparse, call data_loader -> model_builder -> solver -> gantt
