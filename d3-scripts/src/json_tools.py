import json


def load_json(file_name: str):
    with open(file_name) as f:
        json_data = json.load(f)
    return json_data


def check_json_unchanged(file_name: str, claim: dict):
    with open(file_name) as f:
        json_data = json.load(f)
    return json_data == claim


def get_json_file_name(yaml_file_name: str):
    json_file_name = (
        yaml_file_name
        .replace(".yaml", ".json")
        .replace("/manufacturers", "/_manufacturers_json")
        .replace("\\manufacturers", "\\_manufacturers_json")
    )
    return json_file_name


def write_json(file_name: str, json_data: dict):
    with open(file_name, "w") as f:
        json.dump(json_data, f, indent=4)
    return True
