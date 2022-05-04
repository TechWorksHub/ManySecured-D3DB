from pathlib import Path
import typing

import yaml
import yamllint.linter
import yamllint.cli
from yamllint.config import YamlLintConfig

from .d3_constants import d3_types


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


def lint_yaml(file_name: str, show_problems=True) -> typing.Literal[0, 1]:
    config = YamlLintConfig(r"""
        extends: default
        rules:
            document-start:
                # so we don't need to start YAML files with ---
                present: false
            line-length:
                # 80 characters is too small for 1080p/4K monitors
                max: 120
    """)
    contents = Path(file_name).read_text()
    problems = yamllint.linter.run(contents, conf=config, filepath=file_name)

    if show_problems:
        prob_level = yamllint.cli.show_problems(problems, file_name, args_format='auto', no_warn=False)
        problems_exist = prob_level > 0
    else:
        # problems is a generator, so will be emptied by yamllint.cli.show_problems
        problems_exist = len(problems) > 0

    if problems_exist:
        raise Exception(f"YAML linting failed for {file_name}")

    return True
