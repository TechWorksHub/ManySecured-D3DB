from pathlib import Path
import typing

import yaml
import yamllint.linter
import yamllint.cli
from yamllint.config import YamlLintConfig


def get_yaml_suffixes(file_name):
    try:
        *_, d3_type, d3_ext, yaml_ext = Path(file_name).suffixes
        return d3_type, d3_ext, yaml_ext
    except ValueError:
        print(f"{file_name}: invalid d3 claim format e.g. claim.type.d3.yaml")
        raise


def is_valid_yaml_claim(file_name: str):
    """Validates a YAML claim file against the D3 expected extensions
    e.g. exmaple.type.d3.yaml

    Args:
        file_name: The filepath to the YAML claim file

    Returns:
        Boolean indicating if the file is valid else throws an exception
    """
    file_path = Path(file_name)
    suffixes = file_path.suffixes
    file_str = file_path.relative_to(file_path.parents[2])
    example = "e.g. example_claim.type.d3.yaml"

    assert (
        len(suffixes) == 3
    ), f"File ({file_str}) has invalid d3 claim format {example}"

    d3_type, d3_ext, yaml_ext = get_yaml_suffixes(file_name)
    assert (
        d3_ext == ".d3"
    ), f"File ({file_str}) missing .d3 extension {example}"
    assert (
        yaml_ext == ".yaml"
    ), f"File ({file_str}) missing .yaml extension {example}"
    return True


def load_claim(file_name: str):
    """Loads a YAML claim file and returns the data as a Python dict

    Args:
        file_name: The filepath to the YAML claim file

    Returns:
        The data from the YAML claim file as a Python dict
    """
    yaml_data = {}
    with open(file_name) as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data


def lint_yaml(file_name: str, show_problems=True) -> typing.Literal[0, 1]:
    config = YamlLintConfig(
        r"""
        extends: default
        rules:
            document-start:
                # so we don't need to start YAML files with ---
                present: false
            line-length:
                # 80 characters is too small for 1080p/4K monitors
                max: 120
    """
    )
    contents = Path(file_name).read_text()
    problems = yamllint.linter.run(contents, conf=config, filepath=file_name)

    if show_problems:
        prob_level = yamllint.cli.show_problems(
            problems, file_name, args_format="auto", no_warn=False
        )
        problems_exist = prob_level > 0
    else:
        # problems is a generator,
        # so will be emptied by yamllint.cli.show_problems
        problems_exist = len(problems) > 0

    if problems_exist:
        raise Exception(f"YAML linting failed for {file_name}")

    return True
