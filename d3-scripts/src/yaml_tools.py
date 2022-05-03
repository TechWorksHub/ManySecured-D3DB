import yaml
from pathlib import Path
from d3_constants import d3_types


def is_valid_yaml_claim(file_name: str):
    # Filename takes the form ...<d3_type>.<d3_ext>.yaml
    # [-3:] bypasses ValueError if file_name takes form:
    # brother-firmware MFC15.05.95.firmware.d3.yaml
    d3_type, d3_ext, yaml_ext = Path(file_name).suffixes[-3:]
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
