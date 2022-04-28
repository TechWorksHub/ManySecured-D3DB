#! /usr/bin/python3

from glob import glob
import multiprocessing as mp
from yaml_tools import is_yaml_file, read_yaml
from json_tools import check_json_unchanged, get_json_file_name
from d3_utils import yaml_to_json, check_uri_refs
from validate_schemas import get_schema_from_path, validate_schema
from check_uri_resolve import check_uri_refs

def process_claim_file(yaml_file_name, guids):
    # check if file is YAML with right extension
    is_yaml_file(file_name)    
    
    json_file_name = get_json_file_name(yaml_file_name)
    
    # import yaml
    yaml_data = read_yaml(file_name)
    
    # convert to JSON
    json_data = yaml_to_json(yaml_data)
    
    # if JSON already exists and is unchanged then skip
    check_json_unchanged(json_file_name, json_data)

    # validate schema
    schema = get_schema_from_path(yaml_file_name)

    # check URIs and other refs resolve
    check_uri_refs(json_data, schema)

    # write JSON if valid
    write_json(json_file_name, json_data)
    return json_data['guid']

if name == '__main__':
  # Get list of YAML files
  files_to_process = glob('../yaml/**/*')
  
  # Create pool for parallel processing
  pool_size = max(mp.cpu_count() - 1, 1)
  pool = mp.Pool(processes=pool_size)

  # check for duplicate GUID/UUIDs
  guids = pool.map(get_guid, files_to_process)
  check_guids(guids, files_to_process)
  
  # process claims
  pool.map(multiprocess_claims, files_to_process)
  print('Done!')
