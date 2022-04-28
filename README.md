# ManySecured-D3DB

(OUT OF DATE)
A repo for the ManySecured D3 data management pipeline from claims and behaviours.

Links:
- [ManySecured Docs](https://specs.manysecured.net/)
- [ManySecured Docs: D3](https://specs.manysecured.net/d3)
- [ManySecured Docs: D3 Claims](https://specs.manysecured.net/d3/D3%20claims)
- [ManySecured Docs: D3 Behaviours](https://specs.manysecured.net/d3/D3%20behaviourss)

## How to add a new D3 claim

1. Start a new branch.
2. Within the `yaml` folder, find the sub-folder for the type of definition you wish to add e.g. `./yaml/assert-device-type` to add a device type.
3. Within the folder add a YAML file with the details for your D3 spec. See 
    - The file name convention is `companyName-deviceName-deviceModel.yaml`
    - `companyName` is the name of the company/organisation/manufacturer associated with the device
    - `deviceName` is the name of the device
    - `deviceModel` is the model or version information for the device
4. If you are running on your local machine (requires Python 3)
    - Run `pip3 install requirements.txt ` to install the packages
    - Run `python3 ./src/d3_build.py` to run the test suite against your files. Any issues will manifest as errors
5. If you can't check locally or after your satisfied with your local changes, push your branch changes to github, and create a pull request.
6. The Github Actions CI will run the tests on the library and if it passes you can merge the changes.
7. JSON files will be created automatically from valid YAML files, you do not need to define these manually. 

## Project Details 

### Folder Structure
- `./yaml`: Store for YAML D3 claims/behaviours
- `./yaml/$D3_SPEC_TYPE`: Subfolders for the YAML D3 claims and behaviours by claim type
- `./json`: (**Auto-generated**) Store for the JSON equivalents of the YAML claims/behaviours
- `./json/$D3_SPEC_TYPE`: (**Auto-generated**) Store for the JSON equivalents of the YAML claims/behaviours
- `./examples`: example claim and behaviour definitions
- `./schemas`: Folder containing the JSON schemas for each D3 claim 
- `./src`: Folder containing the JSON schemas for each D3 claim 

### Workflow
Useage `python3 ./src/script.py`

#### Scripts
- `d3_build.py`: runs all tests
- `d3_build_db.py`: Convert claims to database format for the ManySecured router
- `uuid.py`, `guid.py`: A helper to generate a UUID/GUID to add to your claim defintion

#### Pipeline scripts/utils
- `yaml_lint.py`: Checks YAML files conform to the YAML standard and naming conventions
- `yaml_to_json.py`: converts YAML to JSON
- `validate_schemas.py`: validates the YAML and JSON files against the schema for the given claim/behaviour type
- `check_uri_resolve.py`: checks any URI parameters can be resolved 
- `yaml_test.py`: YAML specific tests
- `json_test.py`: JSON specific tests
