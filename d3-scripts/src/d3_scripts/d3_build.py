#! /usr/bin/python3

from pathlib import Path
import multiprocessing as mp
from d3_utils import process_claim_file
from guid_tools import get_guid, check_guids

if __name__ == "__main__":
    # Get list of YAML files
    file_path = Path(__file__).absolute()
    yaml_store = Path(file_path / ".." / ".." / ".." / ".." / "manufacturers")\
        .resolve()
    files_to_process = [str(fname) for fname in yaml_store.glob("**/*.*")]

    # Create pool for parallel processing
    pool_size = max(mp.cpu_count() - 1, 1)
    pool = mp.Pool(processes=pool_size)

    # check for duplicate GUID/UUIDs
    guids = pool.map(get_guid, files_to_process)
    check_guids(guids, files_to_process)

    # process claims
    pool.map(process_claim_file, files_to_process)
    pool.close()
    print("Done!")
