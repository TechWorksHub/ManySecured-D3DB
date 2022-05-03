#!/usr/bin/env python3

import argparse
import sys

from .d3_utils import validate_d3_claim_files

def cli(argv = None) -> int:
    parser = argparse.ArgumentParser(
        description = "Lint D3 files for YAML syntax/schema errors",
        epilog = "Example: d3_lint.py *.d3",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "D3_FILE",
        nargs = "+",
        help = "Files to lint",
    )
    args = parser.parse_args(argv)

    validate_d3_claim_files(args.D3_FILE)

if __name__ == "__main__":
    cli()
