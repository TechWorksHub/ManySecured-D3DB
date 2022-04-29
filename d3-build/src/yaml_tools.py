import yaml
from pathlib import Path
from d3_utils import d3_types


def is_valid_yaml_claim(file_name: str):
    d3_type, d3_ext, yaml_ext = Path(file_name).suffixes
    assert (
        d3_type[1:] in d3_types
    ), f"File must have have a valid d3 type extension {d3_types} {file_name}"
    assert d3_ext == ".d3", f"File must have .d3 extension {file_name}"
    assert yaml_ext == ".yaml", f"File must have .yaml extension {file_name}"
    return True


def read_yaml(file_name: str):
    yaml_data = {}
    with open(file_name) as f:
        yaml_data = yaml.safe_load_all(f)
    return yaml_data


def lint_yaml(file_name: str):
    pass
