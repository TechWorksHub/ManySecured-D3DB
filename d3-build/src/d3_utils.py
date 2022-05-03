#!/usr/bin/python3
from yaml_tools import is_valid_yaml_claim, load_claim
from json_tools import check_json_unchanged, get_json_file_name, write_json
from validate_schemas import get_schema_from_path, validate_schema
from check_uri_resolve import check_uri_resolve

d3_type_codes = {
    "behaviour": "d3-device-type-behaviour",
    "firmware": "d3-firmware-assertion",  # TODO: check definition
    "inheritance": "d3-device-type-inheritance",
    "type": "d3-device-type-assertion",
    "vuln": "d3-device-instance-vuln"
}
d3_types = d3_type_codes.keys()
d3_codes = d3_type_codes.values()


def process_claim_file(yaml_file_name: str):
    # check if file is YAML with right extension
    is_valid_yaml_claim(yaml_file_name)

    json_file_name = get_json_file_name(yaml_file_name)

    # import yaml claim to Python dict (JSON)
    claim = load_claim(yaml_file_name)

    # if JSON already exists and is unchanged then skip
    check_json_unchanged(json_file_name, claim)

    # validate schema
    schema = get_schema_from_path(yaml_file_name)
    validate_schema(claim, schema)

    # check URIs and other refs resolve
    check_uri_resolve(claim, schema)

    # write JSON if valid
    write_json(json_file_name, claim)
    return True


def yaml_to_json(yaml_data: dict):
    pass
