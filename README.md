# Body Shop Scheduler

A rolling-horizon production scheduler for automotive body-in-white (BIW) lines,
with operator assignment, material-delivery constraints, and stochastic
simulation to evaluate schedule robustness.

## Status

Work in progress. Currently building the deterministic CP-SAT core;
stochastic simulator and rolling-horizon controller to follow.

## Problem

A BIW body shop welds car frames through a sequence of stations. Multiple
variants (Sedan, SUV, Ute) share the line with variant-specific routings.
Operators are skill-qualified and must be assigned to stations across a
shift, subject to qualification matching and station-operator headcount.
Material kits are delivered from an upstream stamping shop on a schedule
with variability.

Given a daily production order list (mix of variants, due dates), planned
kit arrivals, and on-shift operator roster, the scheduler decides:

- The order in which frames enter the line
- Which operators staff each station for each operation
- Start times for every operation

with the objective of minimising weighted tardiness against per-order due
dates, with makespan as a lexicographic tiebreaker.

## Roadmap

- [ ] V1 deterministic CP-SAT model (operator assignment + material constraints)
- [ ] CSV data loaders
- [ ] Gantt visualisation
- [ ] Stochastic simulator (material delays, operator absences, process noise)
- [ ] Rolling-horizon controller
- [ ] Comparison experiments: deterministic vs. rolling-horizon under disruption

## Install

```bash
git clone https://github.com/your-username/body_shop_scheduler.git
cd body_shop_scheduler
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell
# source .venv/bin/activate     # macOS / Linux
pip install -e ".[dev]"
```

## Usage

(Coming soon.)

## Reference

The mathematical formulation lives at
[`docs/body_shop_formulation.pdf`](docs/body_shop_formulation.pdf).
The PDF is the contract: the code in `src/` is its implementation.

## Layout

```
body_shop_scheduler/
├── data/                       CSV inputs (stations, operators, orders, kits)
├── docs/                       Formulation PDF + LaTeX source
├── src/body_shop_scheduler/
│   ├── domain/                 Dataclasses for shop entities and state
│   ├── scheduling/             Data loader, CP-SAT model builder, solver
│   ├── simulation/             Stochastic disturbance model + simulator
│   ├── controller/             Rolling-horizon orchestration
│   └── viz/                    Gantt chart rendering
├── scripts/                    Top-level entry points
├── tests/                      pytest suite
└── notebooks/                  Exploratory analysis
```
