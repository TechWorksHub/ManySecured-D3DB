from .guid_tools import is_valid_guid


def check_behaviours_resolve(json_data: dict, schema: dict) -> None:
    """Checks whether behaviours resolve, trows if not.
    Args:
        json_data: The JSON object to check
        schema: The JSON schema to use
    Returns:
        None
    """
    if(schema.get("behaviours") and json_data.get("behaviours")):
        # Check if behaviours are valid
        for behaviour in json_data["behaviours"]:
            if not is_behaviour_valid(behaviour):
                raise Exception(f"Behaviour {behaviour} is not valid")


def is_behaviour_valid(behaviour: dict) -> bool:
    """Checks whether a behaviour is valid.
    Args:
        behaviour: The behaviour to check
    Returns:
        Boolean indicating if the behaviour is valid
    """
    if (behaviour.get("id") and not is_valid_guid(behaviour["id"])):
        return False
    if (behaviour.get("name") and not isinstance(behaviour["name"], str)):
        return False
    return True
