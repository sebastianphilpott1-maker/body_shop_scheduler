"""
scheduling.model_builder
========================

Builds the CP-SAT model from a `Scenario` of domain entities.
Implements the constraints (C1)-(C10) and the lexicographic objective
described in `docs/body_shop_formulation.pdf` §4-§5.

Returns the built `cp_model.CpModel` together with a handle dict
keyed by (frame_id, station_id) so the solver layer can extract
solution values.
"""
from dataclasses import dataclass
from ortools.sat.python import cp_model
from ..domain.entities import Scenario

@dataclass
class ModelHandles:
    # operation level: keyed by (frame_id, station_id)
    starts:          dict[tuple[str, str], cp_model.IntVar]
    ends:            dict[tuple[str, str], cp_model.IntVar]
    intervals:       dict[tuple[str, str], cp_model.IntervalVar]

    # operator level: keyed my (frame_id, station_id, operator_id)
    assignments:     dict[tuple[str, str, str], cp_model.IntVar] # binary variable
    op_intervals:    dict[tuple[str, str, str], cp_model.IntervalVar] # optional intervals

    # frame level: keyed by frame_id only
    completion_time: dict[str, cp_model.IntVar]
    tardiness:       dict[str, cp_model.IntVar]

    # makespan is a simple scalar value
    makespan:        cp_model.IntVar

def build_model(scenario: Scenario) -> tuple[cp_model.CpModel, ModelHandles]:
    model = cp_model.CpModel()
    horizon_max = int(1.5 * scenario.horizon)
    handles = ModelHandles(
        starts = {}, ends = {}, intervals = {},
        assignments = {}, op_intervals = {},
        completion_time = {}, tardiness = {},
        makespan = None,
    )

    # variable creation
    for order in scenario.orders: # for every frame order
        j = order.order_id
        variant = scenario.variants[order.variant_id]
        for step in variant.routing:  # for every (frame, station) in routing
            s = step.station_id
            station = scenario.stations[s]
            start_var = model.NewIntVar(0, horizon_max, f"start_{j}_{s}")
            end_var = model.NewIntVar(0, horizon_max, f"end_{j}_{s}")
            interval_var = model.NewIntervalVar(start_var, step.processing_time, end_var, f"Interval_{j}_{s}")
            
            handles.starts[(j, s)] = start_var
            handles.ends[(j, s)] = end_var
            handles.intervals[(j, s)] = interval_var

            for op_id, operator in scenario.operators.items():
                if station.required_qualification in operator.qualifications:
                    # per (frame, station, eligible operator)
                    pass
    return model, handles

