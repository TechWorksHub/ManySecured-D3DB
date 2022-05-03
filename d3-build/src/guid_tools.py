from yaml_tools import load_claim, is_valid_yaml_claim


def get_guid(file_name: str):
    if(is_valid_yaml_claim(file_name)):
        yaml_data = load_claim(file_name)
        # If the claim exists an ID field
        if(yaml_data.get("credentialSubject", {}).get("id", False)):
            return yaml_data['credentialSubject']['id']
    pass


def check_guids(guids, files_to_process):
    pass
