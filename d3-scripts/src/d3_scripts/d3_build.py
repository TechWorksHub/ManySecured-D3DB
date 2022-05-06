#! /usr/bin/python3

from pathlib import Path
import multiprocessing as mp
from tqdm import tqdm
import functools
from .d3_utils import process_claim_file
from .guid_tools import get_guid, check_guids
from .yaml_tools import is_valid_yaml_claim, get_yaml_suffixes, load_claim


def claim_handler(file_name):
    stringified_file_name = str(file_name)
    if is_valid_yaml_claim(stringified_file_name):
        return stringified_file_name
    return False


def d3_build():
    print("Compiling D3 claims...")
    bar_format = "{desc: <20}|{bar}| {percentage:3.0f}% [{elapsed}]"
    pbar = tqdm(total=100, ncols=80, bar_format=bar_format)
    pbar.set_description("Setting up worker pool ")
    pool_size = max(mp.cpu_count() - 1, 1)
    pool = mp.Pool(processes=pool_size)
    pbar.update(10)

    # Get list of YAML files and check for invalid claims
    pbar.set_description("Finding claims")
    yaml_store = Path(__file__).parents[3] / "manufacturers"
    files_to_process = pool.map(claim_handler, yaml_store.glob("**/*.*"))
    files_to_process = [file for file in files_to_process if file]
    pbar.update(30)

    # check for duplicate GUID/UUIDs
    pbar.set_description("Checking UUIDs")
    guids = [guid for guid in pool.map(get_guid, files_to_process) if guid]
    check_guids(guids, files_to_process)
    pbar.update(30)

    pbar.set_description("Processing claims")
    # Pass behaviour files into process_claim_file function
    behaviour_files = get_files_by_type(files_to_process, "behaviour")
    behaviour_jsons = pool.map(load_claim, behaviour_files)
    process_claim = functools.partial(
        process_claim_file,
        behaviour_jsons=behaviour_jsons)

    pool.map(process_claim, files_to_process)
    pool.close()
    pbar.update(30)
    pbar.set_description("Done!")
    pbar.close()


def get_files_by_type(files, type_code):
    return [file for file in files
            if get_yaml_suffixes(file)[0] == "." + type_code]


if __name__ == "__main__":
    d3_build()
