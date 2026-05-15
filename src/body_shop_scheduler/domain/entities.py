"""
domain.entities
===============

Dataclasses representing the static entities of the shop floor:
stations, operators, variants, routings, frame orders, and material kits.

See `docs/body_shop_formulation.pdf` §2 for the formal definitions.
"""
from dataclasses import dataclass


@dataclass(frozen = True)
class Station:
    station_id:              str
    station_name:            str
    required_operators:      int
    required_qualification:  str

@dataclass(frozen = True)
class Operator:
    operator_id:    str
    operator_name:  str
    qualifications: frozenset[str]

@dataclass(frozen = True)
class RoutingStep:
    station_id:              str
    processing_time:         int # in minutes
    predecessor_station_ids: frozenset[str]

@dataclass(frozen = True)
class Variant:
    variant_id: str
    name:       str
    routing:    tuple[RoutingStep, ...]

@dataclass(frozen = True)
class FrameOrder:
    order_id:   str
    variant_id: str
    due_date:   int # minutes from shift start
    weight:     int # tardiness weight w_j

@dataclass(frozen = True)
class MaterialKit:
    order_id:        str
    planned_arrival: int # minutes from shift start

@dataclass(frozen = True)
class Scenario:
    stations:  dict[str, Station]
    operators: dict[str, Operator]
    variants:  dict[str, Variant]
    orders:    tuple[FrameOrder, ...]
    kits:      dict[str, MaterialKit]
    horizon:   int