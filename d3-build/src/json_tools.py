def check_json_unchanged(file_name: str, data: dict):
    pass


def get_json_file_name(yaml_file_name: str):
    json_file_name = (
        yaml_file_name
        .replace(".yaml", ".json")
        .replace("/manufacturers", "/_manufacturers_json")
        .replace("\\manufacturers", "\\_manufacturers_json")
    )
    return json_file_name


def write_json(file_name: str, json_data: dict):
    pass
