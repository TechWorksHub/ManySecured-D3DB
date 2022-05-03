#!/usr/bin/env python3

import argparse
import sys

from .yaml_tools import lint_yaml

def cli(argv = None) -> int:
    parser = argparse.ArgumentParser(
        description = "Lint D3 files for YAML syntax errors",
        epilog = "Example: d3_lint.py *.d3",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "D3_FILE",
        nargs = "+",
        help = "Files to lint",
    )
    args = parser.parse_args(argv)

    return max(lint_yaml(file) for file in args.D3_FILE)

if __name__ == "__main__":
    exit_code = cli()
    sys.exit(exit_code)
