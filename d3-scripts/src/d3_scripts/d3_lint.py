#!/usr/bin/env python3

import argparse
import logging
import glob

from .d3_utils import validate_d3_claim_files

LOG_LEVELS = {
    -1: logging.DEBUG,
    0: logging.INFO,
    1: logging.WARNING,
    2: logging.ERROR,
}


def cli(argv=None):
    parser = argparse.ArgumentParser(
        description="Lint D3 files for YAML syntax/schema errors",
        epilog="Example: d3_lint.py *.d3",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--glob-pattern",
        action="append",
        type=str,
        help="A glob pattern to search for D3 files. Can be repeated for multiple glob patterns."
    )
    parser.add_argument(
        "D3_FILE",
        nargs="*",
        help="Files to lint",
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

    yaml_file_names = (
        *args.D3_FILE,
        *(file for pattern in args.glob_pattern for file in glob.iglob(pattern))
    )
    validate_d3_claim_files(yaml_file_names, check_uri_resolves=args.check_uri_resolves)


if __name__ == "__main__":
    cli()
