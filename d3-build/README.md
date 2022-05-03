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

Then, to run a script in the poetry virtual environment, do:

```bash
poetry run python3 <your-script-name-here>.py
```
