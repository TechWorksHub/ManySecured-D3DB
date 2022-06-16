from .claim_graph import build_claim_graph
import networkx as nx


def build_type_map(type_jsons):
    type_map = {claim["credentialSubject"]["id"]: claim for claim in type_jsons}
    type_graph = build_claim_graph(type_map)
    sorted_nodes = list(nx.topological_sort(type_graph))
    for type_id in sorted_nodes:
        try:
            type = type_map[type_id]
        except KeyError:
            raise KeyError(f"Parent type with id {type_id} of {list(type_graph.predecessors(type_id))} doesn't exist")
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
        type_map[type_id]["credentialSubject"]["children"] = [
            {"id": child_id} for child_id in list(type_graph.successors(type_id))
        ]
    return type_map
