#! /usr/bin/python3

from pathlib import Path
import multiprocessing as mp
from .d3_utils import process_claim_file
from .guid_tools import get_guid, check_guids
from .yaml_tools import is_valid_yaml_claim


def claim_handler(file_name):
    stringified_file_name = str(file_name)
    if is_valid_yaml_claim(stringified_file_name):
        return stringified_file_name
    return False


def d3_build():
    # Create pool for parallel processing
    pool_size = max(mp.cpu_count() - 1, 1)
    pool = mp.Pool(processes=pool_size)

    # Get list of YAML files and check for invalid claims
    yaml_store = Path(__file__).parents[3] / "manufacturers"
    files_to_process = pool.map(claim_handler, yaml_store.glob("**/*.*"))
    files_to_process = [file for file in files_to_process if file]

    # check for duplicate GUID/UUIDs
    guids = [guid for guid in pool.map(get_guid, files_to_process) if guid]
    check_guids(guids, files_to_process)

    # process claims
    pool.map(process_claim_file, files_to_process)
    pool.close()
    print("Done!")


if __name__ == "__main__":
    d3_build()
