from pathlib import Path
import jsonschema
import functools
from .json_tools import load_json
from .yaml_tools import get_yaml_suffixes, load_claim

schema_store = Path(__file__).parent / "schemas"


@functools.lru_cache(maxsize=None)
def get_d3_claim_schema_validator(d3_type: str) -> jsonschema.Validator:
    """Loads a jsonschema validator for a specific d3 type

    Returns:
        The D3 master claim schema as a Python dict
    """
    schema_path = schema_store / f"{d3_type}.json"
    d3_schema = load_json(schema_path)

    jsonschema.Draft202012Validator.check_schema(d3_schema)
    return jsonschema.Draft202012Validator(schema=d3_schema)


def get_schema_validator_from_path(yaml_path: str) -> jsonschema.Validator:
    """Gets the schema validator from the D3 claim file extension

    Args:
        yaml_path: The filepath to the YAML claim file

    Returns:
        The JSON schema validator for the D3 claim file type
    """
    d3_type = get_yaml_suffixes(yaml_path)[0].replace(".", "")
    return get_d3_claim_schema_validator(d3_type)


@functools.lru_cache(maxsize=None)
def d3_master_claim_schema_validator() -> jsonschema.Validator:
    """Loads a jsonschema validator for the D3 master claim schema

    Returns:
        The D3 master claim schema as a Python dict
    """
    schema_dir = Path(__file__).parent / "schemas"
    d3_schema = load_json(schema_dir / "d3-claim.json")

    jsonschema.Draft202012Validator.check_schema(d3_schema)
    return jsonschema.Draft202012Validator(schema=d3_schema)


def validate_claim_meta_schema(claim: dict):
    """Validates a D3 claim against the D3 meta claim schema

    Args:
        claim: The D3 claim to validate (dict)

    Returns:
        Boolean indicating if the claim is valid else throws an exception
    """
    d3_master_schema_validator = d3_master_claim_schema_validator()
    d3_master_schema_validator.validate(claim)
    return True


def validate_d3_claim_schema(yaml_file_path: str):
    """Loads and validates a D3 claim file against the JSON Schema.

    For performance reasons, it's usually better to manually load the D3 claim
    file yourself.

    Raises:
        jsonschema.ValidationError: If the loaded claim is not valid
    """
    # import yaml claim to Python dict (JSON)
    claim = load_claim(yaml_file_path)
    # validate schema
    schema_validator = get_schema_validator_from_path(yaml_file_path)
    schema_validator.validate(claim["credentialSubject"])
