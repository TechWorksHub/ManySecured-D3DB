#!/usr/bin/python3
from yaml_tools import is_valid_yaml_claim, read_yaml
from json_tools import check_json_unchanged, get_json_file_name, write_json
from validate_schemas import get_schema_from_path, validate_schema
from check_uri_resolve import check_uri_resolve


def process_claim_file(yaml_file_name: str):
    # check if file is YAML with right extension
    is_valid_yaml_claim(yaml_file_name)

    json_file_name = get_json_file_name(yaml_file_name)

    # import yaml
    yaml_data = read_yaml(yaml_file_name)

    # convert to JSON
    json_data = yaml_to_json(yaml_data)

    # if JSON already exists and is unchanged then skip
    check_json_unchanged(json_file_name, json_data)

    # validate schema
    schema = get_schema_from_path(yaml_file_name)
    validate_schema(json_data, schema)

    # check URIs and other refs resolve
    check_uri_resolve(json_data, schema)

    # write JSON if valid
    write_json(json_file_name, json_data)
    return True


def yaml_to_json(yaml_data: dict):
    pass
