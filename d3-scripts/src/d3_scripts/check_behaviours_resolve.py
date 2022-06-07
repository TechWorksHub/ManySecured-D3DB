from typing import Sequence, Callable, TypeVar, Mapping, Dict, Any

BehaviourJson = Mapping[str, Any]
BehaviourJsons = Sequence[BehaviourJson]
BehaviourMap = Dict[str, BehaviourJson]


def check_behaviours_resolve(
    json_data: dict,
    schema: dict,
    behaviour_jsons: BehaviourJsons,
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
            b = behaviour_name
            i = json_data["id"]
            raise Exception(f"Behaviour '{b}' of GUID {i} is invalid")
        json_data["behaviour"] = {
            "id": behaviour["credentialSubject"]["id"],
            "name": behaviour["credentialSubject"].get("ruleName", ""),
        }
    return json_data


def retrieve_behaviour(name: str, behaviour_jsons: BehaviourJsons) -> bool:
    """Checks whether a behaviour exists with name or id = value.
    Args:
        name: The value to check
        behaviour_jsons: The list of behaviours to check
    Returns:
        Boolean indicating if the behaviour exists
    """
    id_map = _behaviour_id_map(behaviour_jsons)
    if name in id_map:
        return id_map[name]
    name_map = _behaviour_name_map(behaviour_jsons)
    if name in name_map:
        return name_map[name]
    return None


T = TypeVar("T")


def _cache_map_based_on_behaviour_jsons(f: Callable[[BehaviourJsons], T]) -> Callable[[BehaviourJsons], T]:
    """Decorator that caches the result of a function based on the ID of behaviour_jsons.

    We can't use @functools.lru_cache because it doesn't work with lists/dicts, since
    lists and dicts are mutable.

    Instead, we rely on the user not to change the behaviour_jsons list contents after the
    first call.
    """
    behaviour_jsons_id = None
    behaviour_jsons_map = None

    def wrapper(behaviour_jsons: BehaviourJsons):
        nonlocal behaviour_jsons_id
        nonlocal behaviour_jsons_map

        current_behaviour_jsons_id = id(behaviour_jsons)
        if current_behaviour_jsons_id != behaviour_jsons_id:
            behaviour_jsons_id = current_behaviour_jsons_id
            behaviour_jsons_map = f(behaviour_jsons)
        return behaviour_jsons_map

    return wrapper


@_cache_map_based_on_behaviour_jsons
def _behaviour_name_map(behaviour_jsons: BehaviourJsons) -> Dict[str, BehaviourJson]:
    return {json["credentialSubject"]["ruleName"]: json for json in behaviour_jsons}


@_cache_map_based_on_behaviour_jsons
def _behaviour_id_map(behaviour_jsons: BehaviourJsons) -> Dict[str, BehaviourJson]:
    return {json["credentialSubject"]["id"]: json for json in behaviour_jsons}
