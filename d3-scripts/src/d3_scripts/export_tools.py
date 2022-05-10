from csv import DictWriter
from pathlib import Path
from typing import Union
from uuid import UUID, uuid5

from .d3_constants import csv_headers, behaviour_rule_types
from .json_tools import load_json
from .yaml_tools import get_yaml_suffixes

path_type = Union[Path, str]
id_type = Union[str, UUID]

src_dir = Path(__file__).absolute()
json_dir = src_dir.parents[3] / "manufacturers_json"
csv_dir = src_dir.parents[3] / "D3DB"


def get_ruleid(id: id_type, name: str) -> str:
    """Generates a UUID for a rule based on the UUID of the parent behaviour
    and a name.

    This means the rule id can persist between generations if the name
    doesn't change.

    Args:
        id: The uuid of the parent behaviour.
        name: The name of the rule.

    Returns:
        A UUID string.
    """
    parent_id = UUID(id)
    rule_id = uuid5(parent_id, name)
    return str(rule_id)


def create_csv_templates() -> None:
    """Creates the csv files + header for the D3DB output CSVs"""
    for name, header in csv_headers.items():
        file_name = csv_dir / f"{name}.csv"
        with open(file_name, "w") as csv_file:
            csv_writer = DictWriter(
                csv_file, fieldnames=header, dialect="unix"
            )
            csv_writer.writeheader()


def write_csv_data(
    file_name: path_type,
    headers: "list[str]",
    data: dict
) -> None:
    """Writes data to a csv file from a list of headers and a dict of data.

    Args:
        file_name: The path to the csv file.
        headers: A list of headers.
        data: A dict of data (keyed on the headers).
    """
    with open(file_name, "a") as csv_file:
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writerow(data)


def export_type_csv(file_path: path_type) -> None:
    """Exports a D3 type claim JSON to a csv file entry

    Args:
        file_path: The path to the D3 type claim JSON.
    """
    file_name = csv_dir / "type.csv"
    data = load_json(file_path)["credentialSubject"]
    data = {k.lower(): v for k, v in data.items()}
    write_csv_data(file_name, csv_headers["type"], data)


def export_behaviour_csv(file_path: path_type) -> None:
    """Exports a D3 behaviour claim JSON to a csv file entry

    Args:
        file_path: The path to the D3 behaviour claim JSON.
    """
    behaviour_file = csv_dir / "behaviour.csv"
    data = load_json(file_path)["credentialSubject"]
    behaviour = {"id": data["id"]}
    behaviour_name = data["ruleName"] if data["ruleName"] else file_path.stem

    for i, rule in enumerate(data["rules"]):
        rule_name = rule["name"] if rule["name"] else f"rule_{i}"
        behaviour["ruleid"] = get_ruleid(behaviour["id"], rule_name)
        behaviour["rulename"] = f"{behaviour_name}/{rule_name}"
        write_csv_data(behaviour_file, csv_headers["behaviour"], behaviour)

        for rule_type in behaviour_rule_types:
            export_rule_csv(rule_type, rule, behaviour["ruleid"])


def export_rule_csv(rule_type: str, rule: dict, entry_id: id_type) -> None:
    """Exports a rule from a D3 behviour claim to a csv file entry

    Args:
        rule_type: The type of rule to export.
        rule: The rule data to export.
        entry_id: The unique id of the entry.
    """
    data = rule["matches"].get(rule_type, False)
    data = {k.lower(): v for k, v in data.items()}
    data["id"] = entry_id
    rule_stem = f"behaviour_{rule_type}"
    file_name = csv_dir / f"{rule_stem}.csv"

    write_csv_data(file_name, csv_headers[rule_stem], data)


def d3_json_export_csv(file_path: path_type) -> None:
    """Exports a D3 claim JSON to a csv file entry based on its type.

    Args:
        file_path: The path to the D3 claim JSON.
    """
    d3_type = get_yaml_suffixes(file_path)[0].replace(".", "")
    if d3_type == "type":
        export_type_csv(file_path)
    elif d3_type == "behaviour":
        export_behaviour_csv(file_path)
    else:
        raise ValueError(f"Unknown D3 claim type: {d3_type}")
