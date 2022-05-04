# ManySecured d3-scripts

Utility scripts for ManySecured-D3 claims

## Installation

These utility scripts require Python to use.

When developing these scripts, [Python Poetry](https://python-poetry.org/)
is used to install and manage dependencies, however,
in future, `poetry` will be used to publish these scripts in a format
that any Python package manager can understand (e.g. `pip`-compatable).

Poetry will create a python isolated virtual environment in the `./.venv` folder and install dependencies if you run:

```bash
poetry install
```

You cannot run scripts directly from the `./src/d3-scripts` since we are using [Python relative imports](https://realpython.com/absolute-vs-relative-python-imports/#relative-imports).

Instead, you must run a script defined in the `[tool.poetry.scripts]` field of [`pyproject.toml`](./pyproject.toml):

## Usage

D3 Linter

```console
alois@nqm-alois-entroware:~/Documents/ManySecured-D3DB/d3-scripts$ poetry run d3lint --help
usage: d3lint [-h] D3_FILE [D3_FILE ...]

Lint D3 files for YAML syntax errors

positional arguments:
  D3_FILE     Files to lint

options:
  -h, --help  show this help message and exit

Example: d3_lint.py *.d3
```

## Tests

Tests can be run via:

```bash
poetry run pytest
```
