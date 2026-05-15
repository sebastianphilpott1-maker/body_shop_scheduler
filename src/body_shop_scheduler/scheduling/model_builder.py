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

# TODO: build_model(scenario: Scenario) -> (model, handles)
