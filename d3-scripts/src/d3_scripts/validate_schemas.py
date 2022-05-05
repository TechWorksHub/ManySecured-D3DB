from pathlib import Path
import jsonschema
from .d3_constants import d3_type_codes_to_schemas
from .json_tools import load_json
from .yaml_tools import load_claim, get_yaml_suffixes

schema_store = Path(__file__).parent / "schemas"


def get_schema_from_d3_claim(yaml_path: str):
    """Gets the schema from the D3 claim file type field

    Args:
        yaml_path: The filepath to the YAML claim file

    Returns:
        The JSON schema for the D3 claim file type
    """
    # import yaml claim to Python dict (JSON)
    claim = load_claim(yaml_path)
    claim_type = claim["type"]
    try:
        d3_schema_name = d3_type_codes_to_schemas[claim_type]
    except KeyError:
        raise KeyError(
            f"Unknown D3 claim type='{claim_type} in D3 file {yaml_path}'"
        )

    schema_path = schema_store / f"{d3_schema_name}.json"
    return load_json(str(schema_path.resolve()))


def get_schema_from_path(yaml_path: str):
    """Gets the schema from the D3 claim file extension

    Args:
        yaml_path: The filepath to the YAML claim file

    Returns:
        The JSON schema for the D3 claim file type
    """
    d3_type = get_yaml_suffixes(yaml_path)[0].replace(".", "")
    schema_path = schema_store / f"{d3_type}.json"
    return load_json(str(schema_path.resolve()))


def validate_schema(json_data: dict, schema: dict):
    """Validates a JSON data against a JSON schema

    Args:
        json_data: The data to validate
        schema: The JSON schema to validate against

    Returns:
        Boolean indicating if the data is valid else throws an exception
    """
    jsonschema.validate(
        instance=json_data,
        schema=schema,
    )
    return True


def get_d3_master_claim_schema():
    """Loads the D3 master claim schema

    Returns:
        The D3 master claim schema as a Python dict
    """
    schema_dir = Path(__file__).parent / "schemas"
    d3_schema = load_json(schema_dir / "d3-claim.json")
    return d3_schema


def validate_claim_meta_schema(claim: dict):
    """Validates a D3 claim against the D3 meta claim schema

    Args:
        claim: The D3 claim to validate (dict)

    Returns:
        Boolean indicating if the claim is valid else throws an exception
    """
    d3_master_schema = get_d3_master_claim_schema()
    validate_schema(claim, d3_master_schema)
    return True
