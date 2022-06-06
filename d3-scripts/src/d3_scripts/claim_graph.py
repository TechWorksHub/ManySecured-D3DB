import networkx as nx
import matplotlib.pyplot as plt
from .check_behaviours_resolve import BehaviourMap


def build_claim_graph(behaviour_map: BehaviourMap) -> nx.DiGraph:
    graph = nx.DiGraph()
    for (id, claim) in behaviour_map.items():
        parents = claim.get("credentialSubject", {}).get("parents", [])
        parents_ids = [parent["id"] for parent in parents]
        if id not in graph:
            graph.add_node(id)
        for parent_id in parents_ids:
            if parent_id not in graph:
                graph.add_node(parent_id)
            graph.add_edge(parent_id, id)
            if not nx.is_directed_acyclic_graph(graph):
                path = [id] + nx.shortest_path(graph, parent_id, id)
                cyclic_chain = " -> ".join(path)
                raise ValueError(f"Graph has Cyclic dependency: {cyclic_chain}")
    return graph


def plot_graph(graph: nx.DiGraph) -> None:
    nx.draw_networkx(graph, arrows=True)
    plt.show()
