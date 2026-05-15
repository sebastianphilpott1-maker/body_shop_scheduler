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

def _load_stations(path: Path) -> dict[str, Station]:
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

def _load_variants(variant_path: Path, routings_path: Path) -> dict[str, Variant]:
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
            
            


if __name__ == "__main__":
    from pathlib import Path
    data_dir = Path(__file__).parent.parent.parent.parent / "data"
    stations = _load_stations(data_dir / "stations.csv")
    for s in stations.values():
        print(s)
    print("---")
    operators = _load_operators(data_dir / "operators.csv")
    for o in operators.values():
        print(o)
    variants = _load_variants(data_dir / "variants.csv", data_dir / "routings.csv")
    for v in variants.values():
        print(v)
    material_kits = _load_material_kits(data_dir / "material_kits.csv")
    for m in material_kits.values():
        print(m)