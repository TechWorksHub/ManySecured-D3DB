#! /usr/bin/python3
from pathlib import Path
from tqdm import tqdm

from .export_tools import (
    create_csv_templates, d3_json_export_csv
)
from .d3_build import d3_build

project_dir = Path(__file__).absolute().parents[3]
json_dir = project_dir / "manufacturers_json"


def d3_build_db():
    if not json_dir.exists():
        print("D3 claims not compiled. Compiling now...")
        d3_build()

    print("Exporting D3 claims...")
    files_to_process = list(json_dir.glob("**/*.d3.json"))

    create_csv_templates()

    bar_format = "{bar}| {percentage:3.0f}% ({n_fmt}/{total_fmt}) [{elapsed}]"
    for file in tqdm(files_to_process, bar_format=bar_format, ncols=80):
        d3_json_export_csv(file)


if __name__ == "__main__":
    d3_build_db()
