"""
scheduling.data_loader
======================

Parses the CSV files in `data/` into domain entity dataclasses.
Returns a single `Scenario` dataclass that bundles all inputs ready
for the model builder.
"""
import csv
from pathlib import Path
from collections import defaultdict
from ..domain.entities import Station
from ..domain.entities import Operator
from ..domain.entities import RoutingStep
from ..domain.entities import Variant
from ..domain.entities import MaterialKit
from ..domain.entities import FrameOrder
from ..domain.entities import Scenario

def _load_stations(path: Path) -> dict[str, Station]:
    """Parse stations.csv into a map keyed by station_id."""
    stations: dict[str, Station] = {}
    with open(path, newline = "") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = Station(
                station_id             = row["station_id"],
                station_name           = row["name"],
                required_operators     = int(row["operators_needed"]),
                required_qualification = row["qualification_required"],
            )
            stations[s.station_id] = s
    return stations

def _load_operators(path: Path) -> dict[str, Operator]:
    """Parse operators.csv into a map keyed by operator_id"""
    operators: dict[str, Operator] = {}
    with open(path, newline = "") as f:
        reader = csv.DictReader(f)
        for row in reader:
            o = Operator(
                operator_id    = row["operator_id"],
                operator_name  = row["name"],
                qualifications = frozenset(
                    q.strip() for q in row["qualifications"].split(";") if q.strip()
                ),
            )
            operators[o.operator_id] = o
    return operators

def _load_orders(orders_path: Path) -> dict[str, FrameOrder]:
    """Parse production_orders.csv into a tuple of FrameOrder, in CSV order."""
    frame_orders: dict[str, FrameOrder] = {}
    with open(orders_path, newline = "") as f:
        reader = csv.DictReader(f)
        for row in reader:
            frame_order = FrameOrder(
                order_id   = row["order_id"],
                variant_id = row["variant_id"],
                due_date   = int(row["due_date"]),
                weight     = int(row["weight"]),
            )
            frame_orders[frame_order.order_id] = frame_order
    return frame_orders

def _load_variants(variant_path: Path, routings_path: Path) -> dict[str, Variant]:
    """Parse variants and their routings into a map keyed by a variant_id.
    
    Joins variants.csv (car variant data) with routings.csv (ordered routing
    steps per variant). Each variant's routing tuple is built by bucketing
    routings rows by variant_id, then sorting by the sequence column.
    """
    variants: dict[str, Variant] = {}

    # make the key value pairs as they appear so we don't get errors
    routing_steps_dict: dict[str, list[tuple[int, RoutingStep]]] = defaultdict(list)
    with open(routings_path, newline = "") as f:
        reader = csv.DictReader(f)

        # we iterate over the routings first since routings actually contains... the routings
        # and since to create a variant object we need a tuple of RoutingSteps of length n and to
        # create a RoutingStep we need a station_id, processing_time and predecessor_station_ids
        # we iterate over this first
        for row in reader:
            row_variant_id          = row["variant_id"]
            station_id              = row["station_id"]
            processing_time         = int(row["processing_time"])
            predecessor_station_ids = frozenset(
                p.strip() for p in row["predecessor_stations"].split(";") if p.strip()
            )
            sequence_id             = int(row["sequence"])

            # we are building a dictionary key'd by build variant which contains a tuple pair of sequence id and a routing step
            routing_steps_dict[row_variant_id].append((sequence_id, RoutingStep(station_id, processing_time, predecessor_station_ids)))
    
    with open(variant_path, newline = "") as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant_id = row["variant_id"]
            name       = row["name"]

            # the tuples (sequence, RoutingStep) which are key'd by the variant, are not in order
            # using the variant_id, within each list, the tuple entries are sorted by their first value (sequence) 
            sorted_pairs  = sorted(routing_steps_dict[variant_id], key = lambda pair: pair[0])

            # removes the sequence number and gives us a tuple of RoutingSteps
            routing_tuple = tuple(step for seq, step in sorted_pairs)

            variants[variant_id] = Variant(
                variant_id = variant_id,
                name       = name,
                routing    = routing_tuple,
            )
    return variants

def _load_material_kits(material_path: Path) -> dict[str, MaterialKit]:
    """Parse material_kits.csv into a dict keyed by order_id."""
    material_kits: dict[str, MaterialKit] = {}
    with open(material_path, newline = "") as f:
        reader = csv.DictReader(f)
        for row in reader:
            m = MaterialKit(
                order_id        = row["order_id"],
                planned_arrival = row["planned_arrival"],
            )
            material_kits[m.order_id] = m
    return material_kits




def load_scenario(data_dir: Path, horizon: int) -> Scenario:
    """Load all CSVs in `data_dir` and bundle them into a single Scenario.

    The only public function of this module — wires the five private
    `_load_*` helpers together.

    Args:
        data_dir: directory containing the six required CSVs.
        horizon: shift length in minutes (H in the formulation).

    Returns:
        A fully-populated Scenario, ready for the model builder.
    """
    stations  = _load_stations(data_dir / "stations.csv")
    operators = _load_operators(data_dir / "operators.csv")
    variants  = _load_variants(data_dir / "variants.csv", data_dir / "routings.csv")
    orders    = _load_orders(data_dir / "production_orders.csv")
    kits      = _load_material_kits(data_dir / "material_kits.csv")
    return Scenario(
        stations  = stations,
        operators = operators,
        variants  = variants,
        orders    = orders,
        kits      = kits,
        horizon   = horizon,
    )


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent.parent.parent / "data"
    scenario = load_scenario(data_dir, horizon = 480)
    print(f"Stations:  {len(scenario.stations)}")
    print(f"Operators: {len(scenario.operators)}")
    print(f"Variants:  {len(scenario.variants)}")
    print(f"Orders:    {len(scenario.orders)}")
    print(f"Kits:      {len(scenario.kits)}")
    print(f"Horizon:   {scenario.horizon}")