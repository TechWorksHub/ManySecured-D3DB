#!/usr/bin/env python3

import argparse
import logging

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
        "D3_FILE",
        nargs="+",
        help="Files to lint",
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

    validate_d3_claim_files(args.D3_FILE)


if __name__ == "__main__":
    cli()
