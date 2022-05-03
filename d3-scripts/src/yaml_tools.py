import yaml
from pathlib import Path
from d3_utils import d3_types


def is_valid_yaml_claim(file_name: str):
    d3_type, d3_ext, yaml_ext = Path(file_name).suffixes
    assert (
        d3_type[1:] in d3_types
    ), f"File has invalid d3 type extension {d3_types} ({file_name})"
    assert (
        d3_ext == ".d3"
    ), f"File missing .d3 extension ({file_name}) e.g. type.d3.yaml"
    assert (
        yaml_ext == ".yaml"
    ), f"File missing .yaml extension ({file_name}) e.g. type.d3.yaml"
    return True


def load_claim(file_name: str):
    yaml_data = {}
    with open(file_name) as f:
        yaml_data = yaml.safe_load(f)
        return yaml_data


def lint_yaml(file_name: str):
    pass
