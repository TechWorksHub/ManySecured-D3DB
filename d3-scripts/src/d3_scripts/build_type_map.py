from .claim_graph import build_claim_graph
import networkx as nx
from typing import List


def build_type_map(
        type_jsons: List[dict],
        type_graph: nx.DiGraph = None) -> dict:
    """
    Build type mapping, map between type id and type claim object, using inheritance from parents
    to determine type claim properties.

    Args:
        json_data: The JSON object to check
        schema: The JSON schema to use
        behaviour_jsons: The list of behaviour JSONs to check
    Returns:
        Behaviour JSON object
    """
    type_map = {claim["credentialSubject"]["id"]: claim for claim in type_jsons}
    if type_graph is None:
        type_graph = build_claim_graph(type_map)
    sorted_nodes = list(nx.topological_sort(type_graph))
    for type_id in sorted_nodes:
        try:
            type = type_map[type_id]
        except KeyError:
            raise KeyError(f"Parent type with id {type_id} of {list(type_graph.successors(type_id))} doesn't exist")
        parents = type["credentialSubject"].get("parents", [])
        inherited_properties = {}
        for parent in parents:
            parent_id = parent["id"]
            for property in parent["properties"]:
                if property in inherited_properties:
                    raise KeyError(f"""Duplicate inherited properties in type definition {type_id},
                    attempted to inherit property `{property}` from multiple parent types""")
                try:
                    inherited_properties[property] = type_map[parent_id]["credentialSubject"][property]
                except KeyError:
                    raise KeyError(f"Attempted to inherit missing property {property} from {parent_id} in {type_id}")
        type_map[type_id]["credentialSubject"] = {**inherited_properties, **type["credentialSubject"]}
    return type_map


def build_type_graph(type_jsons):
    type_map = {claim["credentialSubject"]["id"]: claim for claim in type_jsons}
    type_graph = build_claim_graph(type_map)
    return type_graph


def reformat_graph_data(type_graph, type_map):
    nodes = []
    links = []
    for node in type_graph.nodes():
        type_claim = type_map[node]
        nodes.append({"id": node, "name": type_claim["credentialSubject"].get("name", "")})
    for edge in type_graph.edges():
        links.append({"source": edge[0], "target": edge[1]})
    return {"nodes": nodes, "links": links}
