#! /usr/bin/python3

from pathlib import Path
import multiprocessing as mp
from tqdm import tqdm
import functools
from .d3_utils import process_claim_file
from .guid_tools import get_guid, check_guids
from .yaml_tools import is_valid_yaml_claim, get_yaml_suffixes, load_claim
import typing


def claim_handler(file_name):
    stringified_file_name = str(file_name)
    if is_valid_yaml_claim(stringified_file_name):
        return stringified_file_name
    return False


def d3_build(
    d3_files: typing.Iterable[Path] =
        (Path(__file__).parents[3] / "manufacturers").glob("**/*.yaml"),
):
    """Build compressed D3 files from D3 YAML files

    Args:
        d3_files: The D3 YAML files to build from.
                  Default is all YAML files in the
                  ../../../manufacturers directory
    """
    print("Compiling D3 claims...")
    bar_format = "{desc: <20}|{bar}| {percentage:3.0f}% [{elapsed}]"
    pbar = tqdm(total=100, ncols=80, bar_format=bar_format)
    pbar.set_description("Setting up worker pool ")
    pool_size = max(mp.cpu_count() - 1, 1)
    pool = mp.Pool(processes=pool_size)
    pbar.update(10)

    # Get list of YAML files and check for invalid claims
    pbar.set_description("Finding claims")
    files_to_process = pool.map(claim_handler, d3_files)
    files_to_process = [file for file in files_to_process if file]
    pbar.update(30)

    # check for duplicate GUID/UUIDs
    pbar.set_description("Checking UUIDs")
    guids = [guid for guid in pool.map(get_guid, files_to_process) if guid]
    check_guids(guids, files_to_process)
    pbar.update(30)

    # Pass behaviour files into process_claim_file function
    pbar.set_description("Loading claims")
    behaviour_files = get_files_by_type(files_to_process, "behaviour")
    behaviour_jsons = tuple(pool.map(load_claim, behaviour_files))
    process_claim = functools.partial(
        process_claim_file,
        behaviour_jsons=behaviour_jsons)
    pbar.update(10)

    pbar.set_description("Processing claims")
    pool.map(process_claim, files_to_process)
    pool.close()
    pbar.update(20)
    pbar.set_description("Done!")
    pbar.close()


def get_files_by_type(files, type_code):
    return [file for file in files
            if get_yaml_suffixes(file)[0] == "." + type_code]


if __name__ == "__main__":
    d3_build()
