# ManySecured-D3DB

A repo for the ManySecured D3 data management pipeline from claims and behaviours.

Links:
- [ManySecured Docs](https://specs.manysecured.net/)
- [ManySecured Docs: D3](https://specs.manysecured.net/d3)
- [ManySecured Docs: D3 Claims](https://specs.manysecured.net/d3/D3%20claims)
- [ManySecured Docs: D3 Behaviours](https://specs.manysecured.net/d3/D3%20behaviourss)

## How to add a new D3 claim

1. Start a new branch.
2. Within the `manufacturers folder` folder, create the claim files for the manufacturers products. If you organisae your files into subdirectories they will be recuresed into automatically at compile time.
3. Add a YAML file with the details for your D3 spec. See
    - The file name convention is `fileName.<d3-type>.d3.yaml`
    - `fileName` is the name of the company/organisation/manufacturer associated with the device
    - `<d3-type>` is one of the valid D3 types
        - `behaviour`: Claim of type `d3-behaviour` ([DOCS(?)](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type-static-behaviour), [EXAMPLE]()).
        - `firmware`: Claim of type `d3-firmware` ([DOCS(TBD)](https://specs.manysecured.net/d3), [EXAMPLE]()).
        - `inheritance`: Claim of type `d3-device-type-inheritance` ([DOCS](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type-inheritance), [EXAMPLE]()).
        - `type`: Claim of type `d3-device-type-assertion` ([DOCS](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type), [EXAMPLE]()).
        - `vuln`: Claim of type `d3-device-type-vuln` ([DOCS](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type-vulnerability), [EXAMPLE]()).
    - Example templates for each type are in the `./exmaples` folder.
    - The YAML file values must not be preceded by tabs. If you want to achieve a visual indent use space characters.
4. If you are running on your local machine (requires Python 3 and [Python Poetry](https://python-poetry.org/))
    - Run `cd d3-scripts/ && poetry install` to install the packages
    - Run `poetry run python3 ./src/d3_build.py` to run the test suite against your files. Any issues will manifest as errors.
5. If you can't check locally or after your satisfied with your local changes, push your branch changes to github, and create a pull request.
6. The Github Actions CI will run the tests on the library and if it passes you can merge the changes.
7. JSON files will be created automatically from valid YAML files, you do not need to define these manually.

## Project Details

### Folder Structure
- `./manufacturers`: Store for YAML D3 claims/behaviours
- `./examples`: example claim and behaviour definitions
- `./schemas`: Folder containing the JSON schemas for each D3 claim
- `./d3-scripts/src`: Folder containing the scripts for compiling the D3 YAML claims

### Workflow

`cd d3-scripts/ && poetry install`

This installs the scripts listed in the `[tool.poetry.scripts]` field of [`pyproject.toml`](./d3-scripts/pyproject.toml).

#### Scripts

- `poetry run d3build`: Runs all tests
- `poetry run d3lint`: Checks YAML files conform to the standard
- _Unimplemented_ `d3_build_db.py`: Convert claims to database format for the ManySecured router
- _Unimplemented_ `uuid.py`, `guid.py`: A helper to generate a UUID/GUID to add to your claim defintion

#### Pipeline scripts/utils
- `yaml_lint.py`: Checks YAML files conform to the YAML standard and naming conventions
- `yaml_to_json.py`: converts YAML to JSON
- `validate_schemas.py`: validates the YAML and JSON files against the schema for the given claim/behaviour type
- `check_uri_resolve.py`: checks any URI parameters can be resolved
- `yaml_test.py`: YAML specific tests
- `json_test.py`: JSON specific tests
