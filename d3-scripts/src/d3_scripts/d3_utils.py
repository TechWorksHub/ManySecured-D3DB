import logging
import typing

from pathlib import Path
from .yaml_tools import is_valid_yaml_claim, load_claim, lint_yaml
from .json_tools import is_json_unchanged, get_json_file_name, write_json
from .validate_schemas import (
    get_schema_from_path, get_schema_from_d3_claim,
    validate_claim_meta_schema, validate_schema
)
from .check_uri_resolve import check_uri_resolve
from .check_behaviours_resolve import check_behaviours_resolve, BehaviourJsons


def validate_d3_claim_files(yaml_file_names: typing.List[str]):
    """Checks whether D3 claim files are valid.

    Performs each check sequentially, (e.g. like a normal CI task)
    so if one fails, the rest are not checked.
    """
    logging.info("Checking if D3 files have correct filename")
    for file in yaml_file_names:
        # check if file is YAML with right extension
        is_valid_yaml_claim(file)

    logging.info("Linting D3 files")
    for file in yaml_file_names:
        # check if files have good quality yaml
        lint_yaml(file)

    logging.info("Checking whether D3 files match JSONSchema")
    for file in yaml_file_names:
        # import yaml claim to Python dict (JSON)
        claim = load_claim(file)
        # validate schema
        schema = get_schema_from_d3_claim(file)
        validate_schema(claim["credentialSubject"], schema)

    logging.info("Checking whether D3 files have valid URIs/refs")
    for file in yaml_file_names:
        # import yaml claim to Python dict (JSON)
        claim = load_claim(file)
        schema = get_schema_from_path(file)
        # check URIs and other refs resolve
        check_uri_resolve(claim["credentialSubject"], schema)
    return True


def process_claim_file(yaml_file_name: str, behaviour_jsons: BehaviourJsons):
    """Processes a single D3 claim file.
    Checks include:
    - is unchanged claim
    - is valid claim relative to JSONSchema for type
    - are all URIs/refs resolveable/valid
    - behaviour statements are valid

    Args:
        yaml_file_name: The filepath to the YAML file

    Returns:
        Boolean indicating if the file was successfully processed
    """
    json_file_name = get_json_file_name(yaml_file_name)
    Path(json_file_name).parent.mkdir(parents=True, exist_ok=True)

    # import yaml claim to Python dict (JSON)
    claim = load_claim(yaml_file_name)

    # if JSON already exists and is unchanged then skip
    if is_json_unchanged(json_file_name, claim):
        return True

    # validate schema
    schema = get_schema_from_path(yaml_file_name)
    validate_claim_meta_schema(claim)
    validate_schema(claim["credentialSubject"], schema)

    # check URIs and other refs resolve
    check_uri_resolve(claim["credentialSubject"], schema)

    # check behaviour statement is valid, if so add to claim
    claim["credentialSubject"] = check_behaviours_resolve(
        claim["credentialSubject"],
        schema,
        behaviour_jsons)

    # write JSON if valid
    write_json(json_file_name, claim)
    return True
