import networkx as nx
from .check_behaviours_resolve import BehaviourMap
from iteration_utilities import unique_everseen


def resolve_behaviour_rules(claim: dict, claim_map: BehaviourMap, claim_graph: nx.DiGraph) -> list[dict]:
    """
    Resolve rules which apply for behaviour claim, and checks that any named rules exist and that
    there are no duplicate rule names in claim behaviour.

    Args:
        claim: The D3 behaviour claim to resolve behaviour for
        claim_tree: The claim inheritance tree for the claim 

    Returns:
        The rules which apply to the behaviour claim. 

    """
    aggregated_rules = []
    rules = claim["credentialSubject"].get("rules", [])
    aggregated_rules += rules
    id = claim["credentialSubject"]["id"]
    parents = nx.ancestors(claim_graph, id)
    for parent_id in parents:
        try:
            parent_claim = claim_map[parent_id]
        except KeyError:
            raise KeyError(f"Parent behaviour id {parent_id} of {id} doesn't exist")
        parent_rules = parent_claim["credentialSubject"].get("rules", [])
        aggregated_rules += parent_rules
    unique_aggregated_rules = list(unique_everseen(aggregated_rules))  # De-duplicate any duplicate rules
    return unique_aggregated_rules
