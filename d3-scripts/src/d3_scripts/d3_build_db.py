#! /usr/bin/python3
from pathlib import Path
from tqdm import tqdm

from .export_tools import (
    create_csv_templates, d3_json_export_csv
)

src_path = Path(__file__).absolute()
yaml_store = src_path.parents[3] / "manufacturers_json"
csv_store = src_path.parents[3] / "D3DB"


def d3_build_db():
    print("Exporting D3 claims...")
    files_to_process = list(yaml_store.glob("**/*.d3.json"))

    create_csv_templates()

    bar_format = "{bar}| {percentage:3.0f}% ({n_fmt}/{total_fmt}) [{elapsed}]"
    for file in tqdm(files_to_process, bar_format=bar_format, ncols=80):
        d3_json_export_csv(file)


if __name__ == "__main__":
    d3_build_db()
