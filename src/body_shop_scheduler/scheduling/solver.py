"""
scheduling.solver
=================

Runs CP-SAT against the built model. Implements the two-stage
lexicographic solve (tardiness first, makespan second) described in
`docs/body_shop_formulation.pdf` §5, plus the single-stage weighted-sum
mode for development/testing.

Extracts the solution into a `Schedule` object: per-operation start/end
times, per-operation operator assignments, and summary KPIs.
"""

# TODO: solve(model, handles, mode: str = "lex") -> Schedule
