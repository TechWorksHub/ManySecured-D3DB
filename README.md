# ManySecured-D3DB

A repo for the ManySecured D3 data management pipeline from claims and behaviours.

Links:
- [ManySecured Docs](https://specs.manysecured.net/)
- [ManySecured Docs: D3](https://specs.manysecured.net/d3)
- [ManySecured Docs: D3 Claims](https://specs.manysecured.net/d3/D3%20claims)
- [ManySecured Docs: D3 Behaviours](https://specs.manysecured.net/d3/D3%20behaviourss)

## How to add a new D3 claim

For contributing changes to code, please see [CONTRIBUTING.md](./CONTRIBUTING.md).

1. Start a new branch.
2. Within the `manufacturers folder` folder, create the claim files for the manufacturers products. If you organisae your files into subdirectories they will be recuresed into automatically at compile time.
3. Add a YAML file with the details for your D3 spec. See
    - The file name convention is `fileName.<d3-type>.d3.yaml`
    - `fileName` is the name of the company/organisation/manufacturer associated with the device
    - `<d3-type>` is one of the valid D3 types
        - `behaviour`: Claim of type `d3-behaviour` ([DOCS](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type-static-behaviour), [EXAMPLE]()).
        - `firmware`: Claim of type `d3-firmware` ([DOCS (TBD)](https://specs.manysecured.net/d3), [EXAMPLE]()).
        - `inheritance`: Claim of type `d3-device-type-inheritance` ([DOCS](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type-inheritance), [EXAMPLE]()).
        - `type`: Claim of type `d3-device-type-assertion` ([DOCS](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type), [EXAMPLE]()).
        - `vuln`: Claim of type `d3-device-type-vuln` ([DOCS](https://specs.manysecured.net/d3/D3%20claims/#assert-device-type-vulnerability), [EXAMPLE]()).
    - Example templates for each type are in the `./examples` folder.
    - The YAML file values must not be preceded by tabs. If you want to achieve a visual indent use space characters.
    - If you want to generate UUID/GUIDs for your yaml definitions, refer to the uuid helper script in the [Workflow section](#workflow) below. 
4. If you are running on your local machine (requires Python 3 and [Python Poetry](https://python-poetry.org/))
    - Run `cd d3-scripts/ && poetry install` to install the packages
    - Run `poetry run d3build` to run the D3 compiler against the repo locally. Any issues will manifest as errors.
    - Run `poetry run d3export` to run the exporter locally. This generates CSVs in the same schema as the SQL tables used by ManySecured devices
5. If you can't check locally or after your satisfied with your local changes, push your branch changes to github, and create a pull request.
6. The Github Actions CI will run the tests on the library and if it passes you can merge the changes.

## Project Details

### Folder Structure
- `./manufacturers`: Store for YAML D3 claims/behaviours
- `./manufacturers_json`: (Auto generated) Store for the compiled D3 claims
- `./D3DB`: (Auto generated) Location of the exported D3 claim CSV tables
- `./examples`: example claim and behaviour definitions
- `./schemas`: Folder containing the JSON schemas for each D3 claim
- `./d3-scripts`: Folder containing the scripts for compiling the D3 YAML claims
- `./d3-scripts/src/d3_scripts/schemas/`: Folder containing the schemas used in the compilation process

### Workflow

`cd d3-scripts/ && poetry install`

This installs the scripts listed in the `[tool.poetry.scripts]` field of [`pyproject.toml`](./d3-scripts/pyproject.toml).
- Run `poetry run d3build` to run the D3 compiler against the repo locally. Any issues will manifest as errors.
- Run `poetry run d3export` to run the exporter locally. This generates CSVs in the same schema as the SQL tables used by ManySecured devices

#### Scripts

- `poetry run d3build`: Runs all tests
- `poetry run d3lint`: Checks YAML files conform to the standard
- `poetry run d3export`: Convert claims to CSV format for the ManySecured router database
- `poetry run uuid`, `poetry run guid`: Helpers to generate a UUID/GUID to add to your claim defintion
    - See also: [`uuidgen`](https://man7.org/linux/man-pages/man1/uuidgen.1.html) on Linux, or [https://www.uuidgenerator.net/](https://www.uuidgenerator.net/version4) online

#### D3 Compilation Process

The steps below detail the steps in the compilation process to help you
debug the compilation should you encounter an error.
1. Iterates over every file in `./manufacturers/**/*.*`
2. All files must be D3 YAML claim files (`*.d3.yaml`)
3. The file must have a valid claim type extension (`*.{behaviour,firmware,inheritence,type,vuln}.d3.yaml`)
4. The GUIDs in each file are checked for uniqueness and format correctness
5. The compiler checks if the claim has changed since the last compile and ignores the file if it's the same
6. The claim's schema is validated
7. The system checks if URIs are valid and warns if they don't resolve
8. Inherited behaviours are resolved
9. Finally, the compiled claims are exported to JSON which can be used for the CSV export tool.
