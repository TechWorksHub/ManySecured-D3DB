import pytest

import d3_scripts.d3_lint

def test_lint():
    # should pass with no Exception
    d3_scripts.d3_lint.cli([
        "../manufacturers/AmazonTe/device.type.d3.yaml",
    ])
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_lint.cli([
            __file__, # this file is a python file, not a valid yaml
        ])
