#! /usr/bin/python3

import argparse
from pathlib import Path
import multiprocessing as mp
import logging
from tqdm import tqdm
import functools
from .d3_utils import process_claim_file
from .guid_tools import get_guid, check_guids
from .yaml_tools import is_valid_yaml_claim, get_yaml_suffixes, load_claim
import typing

src_file = Path(__file__)
yaml_dir = Path(__file__).parents[3] / "manufacturers"


def claim_handler(file_name):
    stringified_file_name = str(file_name)
    if is_valid_yaml_claim(stringified_file_name):
        return stringified_file_name
    return False


def d3_build(
    d3_files: typing.Iterable[Path] = yaml_dir.glob("**/*.yaml"),
    check_uri_resolves: bool = True,
):
    """Build compressed D3 files from D3 YAML files

    Args:
        d3_files: The D3 YAML files to build from.
                  Default is all YAML files in the
                  ../../../manufacturers directory
        check_uri_resolves: Whether to check that URIs/refs resolve.
                            This can be very slow, so you may want to
                            leave this off normally.
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
        behaviour_jsons=behaviour_jsons,
        check_uri_resolves=check_uri_resolves,
    )
    pbar.update(10)

    pbar.set_description("Processing claims")
    for i, warnings in enumerate(pool.map(process_claim, files_to_process)):
        for warning in warnings:
            logging.warning(f"{warning} in {files_to_process[i]}")

    pool.close()
    pbar.update(20)
    pbar.set_description("Done!")
    pbar.close()


def get_files_by_type(files, type_code):
    return [file for file in files
            if get_yaml_suffixes(file)[0] == "." + type_code]


def cli(argv=None):
    parser = argparse.ArgumentParser(
        description="Build D3 YAML files into JSON files",
        epilog="Example: d3build manufacturers/",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "D3_FOLDER",
        nargs="*",
        help="Folders containing D3 YAML files.",
        default=[f"{yaml_dir}"],
        type=Path,
    )
    parser.add_argument(
        "--check_uri_resolves",
        action="store_true",
        help="Check that URIs/refs resolve. This can be very slow, so you may want to leave this off normally.",
    )
    debug_level_group = parser.add_mutually_exclusive_group()
    debug_level_group.add_argument(
        "--verbose",
        "-v",
        dest="log_level",
        action="append_const",
        const=-10,
    )
    debug_level_group.add_argument(
        "--quiet",
        "-q",
        dest="log_level",
        action="append_const",
        const=10,
    )

    args = parser.parse_args(argv)

    log_level_sum = min(
        sum(args.log_level or tuple(), logging.INFO),
        logging.ERROR
    )
    logging.basicConfig(level=log_level_sum)

    d3_build(
        d3_files=(
          d3_file
          for d3_folder in args.D3_FOLDER
          for d3_file in Path(d3_folder).glob("**/*.yaml")
        ),
        check_uri_resolves=args.check_uri_resolves,
    )


if __name__ == "__main__":
    cli()
