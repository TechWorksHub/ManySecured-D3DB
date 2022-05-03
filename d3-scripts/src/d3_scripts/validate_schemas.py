from pathlib import Path
from jsonschema import validate
from .json_tools import load_json


def get_schema_from_path(yaml_path: str):
    schema_store = Path(__file__).parent / "schemas"
    d3_type = Path(yaml_path).suffixes[0].replace(".", "")
    schema_path = schema_store / f"{d3_type}.json"
    return load_json(str(schema_path.resolve()))


def validate_schema(json_data: dict, schema: dict):
    validate(instance=json_data, schema=schema)
    return True
