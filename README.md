# ManySecured-D3DB <!-- omit in toc -->

A repo for the management and storage of ManySecured D3 claims.

To view the D3 types within this repo, please check out the [D3DB website](https://techworkshub.github.io/ManySecured-D3DB).

## Index <!-- omit in toc -->

- [ManySecured Working Group Documentation and Specifications](#manysecured-working-group-documentation-and-specifications)
- [D3 Architecture Summary](#d3-architecture-summary)
  - [D3 Claim Type Summaries](#d3-claim-type-summaries)
    - [Device TYPE assertions (DOCS)](#device-type-assertions-docs)
    - [Device BEHAVIOUR assertions (DOCS)](#device-behaviour-assertions-docs)
    - [Device FIRMWARE assertions (DOCS)](#device-firmware-assertions-docs)
    - [Device VULNERABILITY assertions (DOCS)](#device-vulnerability-assertions-docs)
- [How to add a new D3 claim](#how-to-add-a-new-d3-claim)
- [Project Details](#project-details)
  - [Repo Folder Structure](#repo-folder-structure)
  - [D3 Claim Workflow](#d3-claim-workflow)
    - [Scripts](#scripts)
    - [D3 Compilation Process](#d3-compilation-process)

## ManySecured Working Group Documentation and Specifications

- [ManySecured Docs](https://specs.manysecured.net/)
- [ManySecured Docs: D3](https://specs.manysecured.net/d3)
- [ManySecured Docs: D3 Claims](https://specs.manysecured.net/d3/D3%20claims)
- [ManySecured Docs: D3 Claims Examples](https://specs.manysecured.net/d3/D3%20claim%20examples)

## D3 Architecture Summary

![Relationship Graph for the D3 Claim Types](https://specs.manysecured.net/assets/images/D3-claim-dep-graph-96f91e185abcfdffb986e2410386fba1.svg)

**Overview**:
1. Types are the core of the claim assertion structure
2. A type can inherit the properties of many other types
3. A type can reference one behaviour
4. A behaviour can be referenced by many types
5. A behaviour can describe many rules
6. A rule can be expected malicious=false(default) or malicious malicious=true
7. A behaviour can inherit rules from multiple behaviours
8. A type can have many firmwares
9. A firmware can be referenced by many device types
10. A device may have many vulnerabilities
11. A vulnerability can be referenced by many device types

### D3 Claim Type Summaries

#### Device TYPE assertions ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-type-assertion))

Device types are the core description of an instance of a given device. The type assertion encapsulates the device's details and refers (by GUID reference) to the behaviours, vulnerabilities, and firmware associated with that device. Type assertions operate an inheritance model, where a type assertion can inherit the properties from parent types and then overload/add properties unique to that device type instance.

#### Device BEHAVIOUR assertions ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-behaviour-assertion))

Device behaviour claims detail the activity the device should and should not exhibit on the network. A behaviour claim is a collection of multiple network activity rules which define the network activity parameters the device should comply with. Behaviour rules are one of two types, expected and malicious. Expected rules detail the activity that a device is expected to conform to under normal operation. Malicious rules define network activity the device should categorically not exhibit (these can usually be inherited from the master behaviour definition for a pre-defined list of known malicious activity).

On a ManySecured enabled router, the router can use the behaviour claim to check the connected device behaves according to its type and identify unexpected behaviour (behaviour that does not match any expected rule) and suspicious behaviour (behaviour that matches a malicious behaviour rule).

Behaviour claims comprise a set of rules and can also elect to inherit the rules from other behaviours into a more comprehensive set of rules, e.g. The behaviour claim for a 3-in-one printer might inherit the behaviour claims of a printer, scanner, and copier.

#### Device FIRMWARE assertions ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-firmware-assertions))

Firmware assertions are used to describe the firmware versions a device can have, provide links to the spec, and be used to match against known vulnerabilities for that firmware.

#### Device VULNERABILITY assertions ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-vulnerability-assertion))

Vulnerability assertions allow claims to be made about the vulnerabilities associated with the device. Vulnerability claims are generally auto-populated from the NIST and CVE vulnerability databases but can also be manually added.

## How to add a new D3 claim

For contributing changes to code, please see [CONTRIBUTING.md](./CONTRIBUTING.md).

1. [Fork this repo](https://github.com/TechWorksHub/ManySecured-D3DB/fork), and **start a new branch**.
2. Within the `manufacturers folder` folder, **create/find the folder for the device manufacturer** within the alphabetised folder structure. If you organise your files into sub-directories (e.g. by product line or year) they will be searched recursively automatically at compile time.
3. Add **YAML files with the details for your D3 claims**. See
    - The file name convention is `fileName.<d3-type>.d3.yaml`
    - `fileName` is the name of the company/organisation/manufacturer associated with the device
    - `<d3-type>` is one of the valid D3 types
        - `type`: Claim of type `d3-device-type-assertion` ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-type-assertion), [EXAMPLE](./examples/type-template.type.d3.yaml)).
        - `behaviour`: Claim of type `d3-device-type-behaviour` ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-behaviour-assertion), [EXAMPLE](./examples/behaviour-template.behaviour.d3.yaml)).
        - `firmware`: Claim of type `d3-firmware-assertion` ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-firmware-assertions), [EXAMPLE](./examples/firmware-template.firmware.d3.yaml)).
        - `vuln`: Claim of type `d3-device-type-vuln` ([DOCS](https://specs.manysecured.net/d3/D3%20claim%20examples#device-vulnerability-assertion), [EXAMPLE](./examples/vulnerability-template.vuln.d3.yaml)).
    - Example templates for each type are in the `./examples` folder.
    - The YAML file values must not be preceded by tabs. If you want to achieve a visual indent use space characters.
    - If you want to generate UUID/GUIDs for your yaml definitions, refer to the uuid helper script in the [Workflow section](#workflow) below.
4. If you are **running on your local machine** (requires Python 3 and [Python Poetry](https://python-poetry.org/))
    - Run `cd d3-scripts/ && poetry install` to install the packages
    - Run `poetry run d3build` to run the D3 compiler against the repo locally. Any issues will manifest as errors.
    - Run `poetry run d3export` to run the exporter locally. This generates CSVs in the same schema as the SQL tables used by ManySecured devices
5. If you can't check locally or after your satisfied with your local changes, **push your branch changes to github, and create a pull request**.
6. **The Github Actions CI will run the tests on the library and if it passes you can merge the changes.**

## Project Details

### Repo Folder Structure
- `./manufacturers`: Store for YAML D3 claims
- `./manufacturers/D3_CORE`: contains useful common claim definitions
- `./manufacturers_json`: (Auto generated on local compile) Store for the compiled D3 claims, each claim will have all it's inheritance references resolved. The compiled claims are in the JSON format.
- `./D3DB`: (Auto generated) Location of the exported D3 claim schemas (all branches) and CSV tables (on the `csv` branch)
- `./examples`: example claim and behaviour definitions
- `./d3-scripts`: Folder containing the scripts for compiling the D3 YAML claims
- `./d3-scripts/src/d3_scripts/schemas/`: Folder containing the JSON schemas used in the compilation process should you want to

### D3 Claim Workflow

`cd d3-scripts/ && poetry install`

This installs the scripts listed in the `[tool.poetry.scripts]` field of [`pyproject.toml`](./d3-scripts/pyproject.toml).
- Run `poetry run d3lint` to run the D3 linter against the claim files in the manufacturers folder. Any issues will manifest as errors.
- Run `poetry run d3build` to run the D3 compiler against the repo locally. Any issues will manifest as errors.
- Run `poetry run d3export` to run the exporter locally. This generates CSVs in the same schema as the SQL tables used by ManySecured devices

#### Scripts

- `poetry run d3lint`: Checks YAML files conform to the standard
- `poetry run d3build`: Runs the D3 claim compiler
- `poetry run d3export`: Convert claims to CSV format for the ManySecured router database
- `poetry run uuid`, `poetry run guid`: Helpers to generate a UUID/GUID to add to your claim definition
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
9. Inherited types are resolved
10. Finally, the compiled claims are exported to JSON which can be used for the CSV export tool.
11. Vulnerabilities are updated periodically in the background.
