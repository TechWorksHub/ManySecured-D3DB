import networkx as nx
import matplotlib.pyplot as plt
from .check_behaviours_resolve import BehaviourMap
from .guid_tools import get_parent_claims


def build_claim_graph(claim_map: BehaviourMap) -> nx.DiGraph:
    graph = nx.DiGraph()
    for (id, claim) in claim_map.items():
        parents = get_parent_claims(claim)
        if id not in graph:
            graph.add_node(id)
        for parent_id in parents:
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
