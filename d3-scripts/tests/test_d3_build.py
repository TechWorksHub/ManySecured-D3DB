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


def test_non_existent_parent_behaviour():
    """Test whether behaviours with non-existent parents raises an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "non-existent-parent-behaviour").glob("*.yaml")
        )
    assert "Parent behaviour id" in excinfo.value.args[0]
    assert "doesn't exist" in excinfo.value.args[0]


def test_circular_behaviour_dependencies():
    """Test whether behaviours with circular parent dependencies raise an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "circular-type-dependence").glob("*.yaml")
        )
    assert "Graph has Cyclic dependency" in excinfo.value.args[0]


def test_non_existent_parent_type():
    """Test whether types with non-existent parents raises an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "non-existent-parent-type").glob("*.yaml")
        )
    assert "Parent type with id" in excinfo.value.args[0]
    assert "doesn't exist" in excinfo.value.args[0]


def test_duplicate_property_type_inheritance_single_parent():
    """Test whether inheriting duplicate properties from a single parent type raises an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "duplicate-property-type-inheritance-single-parent").glob("*.yaml")
        )
    assert "Duplicate inherited properties in type definition" in excinfo.value.args[0]


def test_duplicate_property_type_inheritance():
    """Test whether inheriting duplicate properties from types raises an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "duplicate-property-type-inheritance").glob("*.yaml")
        )
    assert "Duplicate inherited properties in type definition" in excinfo.value.args[0]


def test_inherit_missing_property():
    """Test whether attempting to inherit missing properties from parent types raises an error"""
    with pytest.raises(Exception) as excinfo:
        d3_scripts.d3_build.d3_build(
            d3_files=(Path(__file__).parent / "__fixtures__" / "missing-property-type-inheritance").glob("*.yaml")
        )
    assert "Attempted to inherit missing property" in excinfo.value.args[0]


def test_build():
    # should succeed
    d3_scripts.d3_build.d3_build(d3_files=(Path(__file__).parent / "__fixtures__" / "d3-build").glob("*.yaml"))
