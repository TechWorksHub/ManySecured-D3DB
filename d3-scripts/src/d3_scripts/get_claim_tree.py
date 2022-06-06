from typing import Sequence, List, Mapping, Any

BehaviourJson = Mapping[str, Any]
BehaviourJsons = Sequence[BehaviourJson]


def get_claim_tree(claim: dict, behaviour_jsons: BehaviourJsons):
    """Resolve and validate a claim inheritance tree.
    
    Validates that parents of claim exist and that parents doesn't include
    claim itself.

    Args:
        claim: The D3 claim to get behaviour claim tree for (dict)
        behaviour_jsons: The array of behaviours (array of dict)

    Returns:
        Claim inheritance tree. First element is claim, next element is parents of claim,
        next element is parents of parents of claim and so on. Final element should be an empty list with second to
        last element being final parents in inheritance tree. (array of array of dict)
    """
    parents = get_parents([[claim]], behaviour_jsons)
    return parents


def get_parents(claims: List[List[dict]], behaviour_jsons: BehaviourJsons):
    """
    Get parent claims of claims

    Args:
        claims: The D3 claims to get parents for
        behaviour_jsons: The array of behaviours

    Returns:
        Array of claims and parent claims (array of array of dict)
    """
    last_claims = claims[-1]
    # If no more parent claims - end of dependency tree
    if len(last_claims) == 0:
        return claims
    else:
        claims_flat = [claim["credentialSubject"]["id"] for claim in sum(claims, [])]
        claims_set = set(claims_flat)
        if len(claims_flat) != len(claims_set):
            raise ValueError(f"Circular Dependency in {get_dependency_tree(claims)}")
        next_parents = [get_parents_of_claim(claim, behaviour_jsons) for claim in last_claims]
        next_parents_flat = sum(next_parents, [])
        claims.append(next_parents_flat)
        return get_parents(claims, behaviour_jsons)


def get_parents_of_claim(claim: dict, behaviour_jsons: BehaviourJsons):
    """
    Get all parent claims of claim

    Args:
        claim: The D3 claim to validate
        behaviour_jsons: The array of behaviours

    Returns:
        Array of parent claims
    """
    if claim.get("credentialSubject", {}).get("parents", False):
        parent_ids = [parent["id"] for parent in claim["credentialSubject"]["parents"]]
        parent_claims = [claim for claim in behaviour_jsons if claim["credentialSubject"]["id"] in parent_ids]
        if len(parent_ids) != len(parent_claims):
            raise ValueError(f"One of parent ids ${parent_ids} doesn't exist in claims")
        return parent_claims
    return []


def get_dependency_tree(claims) -> str:
    """Creates a human readable string from a claim dependency tree.
    """
    tree_string = ""
    for index, claims_level in enumerate(claims):
        claim_ids = [claim["credentialSubject"]["id"] for claim in claims_level]
        tree_string += f"{claim_ids}"
        if index < len(claims)-1:
            tree_string += " -> "
    return tree_string