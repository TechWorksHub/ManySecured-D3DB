from .claim_graph import build_claim_graph
import networkx as nx

always_inherited_properties = ["vulnerabilities"]


def build_type_map(type_jsons):
    type_map = {claim["credentialSubject"]["id"]: claim for claim in type_jsons}
    type_graph = build_claim_graph(type_map)
    sorted_nodes = list(nx.topological_sort(type_graph))
    for type_id in sorted_nodes:
        try:
            type_instance = type_map[type_id]
        except KeyError:
            raise KeyError(f"Parent type with id {type_id} of {list(type_graph.predecessors(type_id))} doesn't exist")
        parents = type_instance["credentialSubject"].get("parents", [])
        type_vulnerabilities = type_instance["credentialSubject"].get("vulnerabilities", [])
        inherited_properties = {"vulnerabilities": type_vulnerabilities}
        for parent in parents:
            parent_id = parent["id"]
            properties_to_inherit = set(always_inherited_properties + parent["properties"])
            for property in properties_to_inherit:
                try:
                    if property in inherited_properties:
                        if type(inherited_properties[property]) == list:
                            inherited_properties[property] + type_map[parent_id]["credentialSubject"][property]
                        else:
                            raise KeyError(f"""Duplicate inherited properties in type definition {type_id},
                            attempted to inherit property `{property}` from multiple parent types""")
                    inherited_properties[property] = type_map[parent_id]["credentialSubject"][property]
                except KeyError:
                    raise KeyError(f"Attempted to inherit missing property {property} from {parent_id} in {type_id}")
        inherited_properties["vulnerabilities"] = list(set(inherited_properties["vulnerabilities"]))
        type_map[type_id]["credentialSubject"] = {**type_instance["credentialSubject"], **inherited_properties}
        type_map[type_id]["credentialSubject"]["children"] = [
            {"id": child_id} for child_id in list(type_graph.successors(type_id))
        ]
    return type_map
