import d3_scripts.d3_lint

def test_lint():
    # should pass
    assert 0 == d3_scripts.d3_lint.cli([
        "../manufacturers/Amazon/Echo/echo.behaviour.d3.yaml",
    ])
    assert 1 == d3_scripts.d3_lint.cli([
        __file__, # this file is a python file, not a valid yaml
    ])
