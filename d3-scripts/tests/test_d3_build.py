import pytest
from pathlib import Path

import d3_scripts.d3_build


def test_duplicated_guids():
    # should throw an error due to duplicate UUID
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "duplicate-uuid").glob("*.yaml")
        )
    assert "Duplicate GUIDs" in excinfo.value.args[0]


def test_invalid_uri(caplog):
    """Test whether invalid uris log a warning and whether valid URIs don't log a warning
    """
    for json_file in (Path(__file__).parent / "__fixtures__" / "invalid-uri").glob("*.json"):
        try:
            json_file.unlink()
        except FileNotFoundError:
            pass  # can't use missing_ok = True since it's only added in Python 3.8

    d3_scripts.d3_build.d3_build(
        d3_files=(Path(__file__).parent / "__fixtures__" / "invalid-uri").glob("invalid-uri.*.yaml"),
        check_uri_resolves=True,
    )
    for record in caplog.records:
        assert "URI https://nquiringminds.com.invalid cannot be resolved" in record.message

    caplog.clear()
    # should work as long as nquiringminds.com is resolvable
    d3_scripts.d3_build.d3_build(
        d3_files=(Path(__file__).parent / "__fixtures__" / "invalid-uri").glob("valid-uri.*.yaml"),
        check_uri_resolves=True,
    )
    # should be empty, as all URIs are valid
    assert len(caplog.records) == 0


def test_non_existent_parents():
    """Test whether behaviours with non-existent parents raise an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "non-existent-parents").glob("*.yaml")
        )
    assert "One of parent ids" in excinfo.value.args[0]
    assert "doesn't exist in claims" in excinfo.value.args[0]


def test_circular_dependencies():
    """Test whether behaviours with circular parent dependencies raise an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "circular-dependence").glob("*.yaml")
        )
    assert "Circular Dependency" in excinfo.value.args[0]


def test_non_existent_rules():
    """Test whether behaviours with parent rules which don't exist raise an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "non-existent-rules").glob("*.yaml")
        )
    assert "attempted to inherit non-existent rule" in excinfo.value.args[0]


def test_duplicate_rules():
    """Test whether behaviours with duplicate rules raise an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "duplicate-rules").glob("*.yaml")
        )
    assert "Duplicate Rule Error" in excinfo.value.args[0]


def test_build():
    # should succeed
    d3_scripts.d3_build.d3_build(d3_files=(Path(__file__).parent / "__fixtures__" / "d3-build").glob("*.yaml"))
