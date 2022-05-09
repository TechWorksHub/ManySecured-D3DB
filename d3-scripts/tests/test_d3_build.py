import pytest
from pathlib import Path

import d3_scripts.d3_build

def test_duplicated_guids():
    # should throw an error due to duplicate UUID
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(d3_files=(Path(__file__).parent / "__fixtures__" / "duplicate-uuid").glob("*.yaml"))
    assert "Duplicate GUIDs" in excinfo.value.args[0]

def test_build():
    # should succeed
    d3_scripts.d3_build.d3_build(d3_files=(Path(__file__).parent / "__fixtures__" / "d3-build").glob("*.yaml"))
