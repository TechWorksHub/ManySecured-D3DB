import json
import pandas as pd


def flatten_dict(dict):
    return list(pd.json_normalize(dict).T.to_dict().values())[0]


def load_json(file_name: str):
    """Loads a JSON file and returns the data as a Python dict.

    Args:
        file_name: The filepath to the JSON file

    Returns:
        The data from the JSON file as a Python dict
    """
    with open(file_name) as f:
        json_data = json.load(f)
    return json_data


def is_json_unchanged(file_name: str, claim: dict):
    """Checks if a JSON file contents are the same as the source claim

    Args:
        file_name: The filepath to the JSON file

    Returns:
        Boolean indicating if the JSON file is unchanged from the YAML file
    """
    try:
        with open(file_name) as f:
            json_data = json.load(f)
        return is_json_same_as_claim(json_data, claim)
    except FileNotFoundError:
        return False


def is_json_same_as_claim(json_data, claim):
    """Checks if json data is equivalent to claim data"""
    flat_json_data = flatten_dict(json_data)
    flat_claim_data = flatten_dict(claim)
    for key in flat_claim_data:
        equal = compare_properties(key, flat_json_data, flat_claim_data)
        if not equal:
            return False
    return True


def compare_properties(key, flat_json_data, flat_claim_data):
    if key == "credentialSubject.behaviour":
        return (flat_claim_data[key] == flat_json_data["credentialSubject.behaviour.id"] or
                flat_claim_data[key] == flat_json_data["credentialSubject.behaviour.name"])
    else:
        return flat_json_data[key] == flat_claim_data[key]


def get_json_file_name(yaml_file_name: str):
    """Returns the filepath to the JSON file for a given YAML file.

    Args:
        yaml_file_name: The filepath to the YAML file

    Returns:
        The filepath to the JSON file
    """
    json_file_name = (
        yaml_file_name
        .replace(".yaml", ".json")
        .replace("/manufacturers", "/manufacturers_json")
        .replace("\\manufacturers", "\\manufacturers_json")
    )
    return json_file_name


def write_json(file_name: str, json_data: dict):
    """Writes a JSON file from a Python dict.

    Args:
        file_name: The filepath to the JSON file
        json_data: The data to write to the JSON file

    Returns:
        Boolean indicating if the JSON file was successfully written
    """
    with open(file_name, "w") as f:
        json.dump(json_data, f, indent=2)
    return True
