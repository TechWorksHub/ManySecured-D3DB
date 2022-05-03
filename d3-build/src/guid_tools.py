from yaml_tools import load_claim, is_valid_yaml_claim
import re


def get_guid(file_name: str):
    if(is_valid_yaml_claim(file_name)):
        yaml_data = load_claim(file_name)
        # If the claim exists an ID field
        if(yaml_data.get("credentialSubject", {}).get("id", False)):
            return yaml_data['credentialSubject']['id']
    pass


def check_guids(guids, file_names):
    # ensure no duplicate GUIDs
    assert (
        len(guids) == len(set(guids))
    ), f"Duplicate GUIDs found: \n{list_duplicate_guids(guids, file_names)}"

    # ensure each GUID is a valid UUID
    for guid in guids:
        assert (re.match(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            guid
        )), f"Invalid GUID format: \n{find_guid_file_names(guid, file_names)}"

    return True


def list_duplicate_guids(guids, file_names):
    seen = set()
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_before = set(x for x in guids if x in seen or seen.add(x))
    # turn the set into a list (as requested)
    return "\n".join(map(
        lambda x: find_guid_file_names(x, file_names),
        list(seen_before)
    ))


def find_guid_file_names(guid_id, file_names):
    files = []
    for file_name in file_names:
        if(is_valid_yaml_claim(file_name)):
            yaml_data = load_claim(file_name)
            if(yaml_data.get("credentialSubject", {}).get("id", False)):
                if(yaml_data['credentialSubject']['id'] == guid_id):
                    files.append(file_name)
    return guid_id + " in files:\n" + "\n".join(list(files))
