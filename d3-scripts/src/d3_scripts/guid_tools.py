from yaml_tools import load_claim, is_valid_yaml_claim
import typing
import uuid


def get_guid(file_name: str) -> str:
    """
    Finds the GUID in a YAML filepath
    Args:
        file_name: The filepath to the YAML file
    Returns:
        The GUID found in the YAML file (if it exsist) | None
    """
    if(is_valid_yaml_claim(file_name)):
        yaml_data = load_claim(file_name)
        # If the claim exists an ID field
        if(yaml_data.get("credentialSubject", {}).get("id", False)):
            return yaml_data['credentialSubject']['id']
    return False


def is_valid_guid(guid: str):
    """
    Function for checking if a given string is a valid UUID

    Args:
        guid: The string to check

    Returns:
        Boolean indicating if the string is a valid UUID
    """
    try:
        uuid.uuid(guid)
        return True
    except ValueError:
        return False


def check_guids(guids: typing.List[str], file_names: typing.List[str]) -> bool:
    """
    Checks all GUIDs are unique and of the correct type
    Args:
        guids: A list of GUIDs
        file_name: The filepaths to the YAML files
    Returns:
        Boolean indicating if the GUIDs are unique and of the correct type
    """
    # ensure no duplicate GUIDs
    assert (
        len(guids) == len(set(guids))
    ), f"Duplicate GUIDs found: \n{get_duplicate_guids(guids, file_names)}"

    # ensure each GUID is a valid UUID
    for guid in guids:
        assert (
            is_valid_guid(guid)
        ), f"Invalid GUID format: \n{find_guid_file_names(guid, file_names)}"

    return True


def get_duplicate_guids(
    guids: typing.List[str],
    file_names: typing.List[str]
) -> str:
    """
    Find duplicate GUIDs, and the name of their containing filename.
    Args:
        guids: A list of GUIDs
        file_name: The filepaths to the YAML files
    Returns:
        Message containing duplicate GUIDs and their filenames
    """
    import collections
    guids_counter = collections.Counter(guids)
    duplicates = [guid for guid in guids_counter if guids_counter[guid] > 1]
    return "\n".join(
        [find_guid_file_names(guid, file_names) for guid in duplicates])


def find_guid_file_names(guid_id: str, file_names: typing.List[str]) -> str:
    """
    Function for finding the file name(s) in which a `guid_id` is found
    Args:
        guid_id: The guid to search for
        file_names: The filepaths to the YAML files
    Returns:
        Message displaying the files that have the given GUID
    """
    files = []
    for file_name in file_names:
        if(get_guid(file_name) == guid_id):
            files.append(file_name)
    return guid_id + " in files:\n" + "\n".join(list(files))
