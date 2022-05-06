from typing import List


def check_behaviours_resolve(
    json_data: dict,
    schema: dict,
    behaviour_jsons: List,
) -> None:
    """Checks whether behaviours resolve, throws if not.
    Args:
        json_data: The JSON object to check
        schema: The JSON schema to use
        behaviour_jsons: The list of behaviour JSONs to check
    Returns:
        None
    """
    # If both the schema and data contain a behaviour field, check it resolves
    if(schema["properties"].get("behaviour") and json_data.get("behaviour")):
        behaviour = json_data["behaviour"]
        if not behaviour_resolves(behaviour, behaviour_jsons):
            b = behaviour
            i = json_data["id"]
            raise Exception(f"Behaviour '{b}' of GUID {i} is invlid")


def behaviour_resolves(name: str, behaviour_jsons: List) -> bool:
    """Checks whether a behaviour exists with name = value.
    Args:
        name: The value to check
        behaviour_jsons: The list of behaviours to check
    Returns:
        Boolean indicating if the behaviour exists
    """
    return any(
        json for json in behaviour_jsons if
        json["credentialSubject"]["name"] == name
    )
