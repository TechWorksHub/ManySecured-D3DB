from typing import List


def check_behaviours_resolve(
    json_data: dict,
    schema: dict,
    behaviour_jsons: List,
) -> dict:
    """Checks whether behaviours resolve, throws if not.
    Args:
        json_data: The JSON object to check
        schema: The JSON schema to use
        behaviour_jsons: The list of behaviour JSONs to check
    Returns:
        Behaviour JSON object
    """
    # If both the schema and data contain a behaviour field, check it resolves
    if(schema["properties"].get("behaviour") and json_data.get("behaviour")):
        behaviour_name = json_data["behaviour"]
        behaviour = retrieve_behaviour(behaviour_name, behaviour_jsons)
        if not behaviour:
            b = behaviour
            i = json_data["id"]
            raise Exception(f"Behaviour '{b}' of GUID {i} is invlid")
        json_data["behaviour"] = {
            "id": behaviour["credentialSubject"]["id"],
            "name": behaviour["credentialSubject"]["name"]
        }
    return json_data


def retrieve_behaviour(name: str, behaviour_jsons: List) -> bool:
    """Checks whether a behaviour exists with name or id = value.
    Args:
        name: The value to check
        behaviour_jsons: The list of behaviours to check
    Returns:
        Boolean indicating if the behaviour exists
    """
    return next(
        json for json in behaviour_jsons if
        json["credentialSubject"]["name"] == name or
        json["credentialSubject"]["id"] == name
    )
