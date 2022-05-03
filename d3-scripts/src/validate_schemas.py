from pathlib import Path
from json_tools import load_json
from jsonschema import validate


def get_schema_from_path(yaml_path: str):
    file_path = Path(__file__).absolute()
    schema_store = Path(file_path / ".." / ".." / ".." / "schemas")
    d3_type = Path(yaml_path).suffixes[0][1:]
    schema_path = schema_store / f"{d3_type}.json"
    return load_json(str(schema_path.resolve()))


def validate_schema(json_data: dict, schema: dict):
    validate(instance=json_data, schema=schema)
    return True
