from collections import defaultdict, deque
from itertools import groupby
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from tasks import Task, A, B, C


def print_results(D: nx.DiGraph, foata_normal_form: list[list[str]]) -> None:
    result = (
        "RESULTS:\n"
        f"\tD = {parse_edge_list(list(D.edges))}\n"
        f"\tI = {parse_edge_list(list(nx.complement(D).edges))}\n"
        f"\tFNF = {parse_fnf(foata_normal_form)}"
    )
    print(result)


def parse_fnf(fnf_list: list[list[str]]) -> str:
    return "".join(map(lambda x: f"( {', '.join(x)} )", fnf_list))


def parse_edge_list(edge_list: list[str]) -> str:
    return f"{edge_list}" if len(edge_list) < 10 else f"{edge_list[:10]}..."


def calculate_foata_form_groups(D: nx.DiGraph) -> list[list[str]]:
    nodes = D.nodes
    shortest_paths = {node: 0 for node in nodes}
    queue = deque([(node, 0) for node in nodes if len(D.in_edges(node)) == 0])
    while queue:
        current_node, previous_path_length = queue.popleft()
        shortest_paths[current_node] = max(
            shortest_paths[current_node], previous_path_length + 1
        )
        neighbors = D.neighbors(current_node)
        queue.extend((neighbor, previous_path_length + 1) for neighbor in neighbors)

    sorted_items = sorted(shortest_paths.items(), key=lambda x: x[1])
    foata_groups = {
        key: list(group) for key, group in groupby(sorted_items, key=lambda x: x[1])
    }

    return [
        [item[0] for item in foata_groups[score]]
        for score in sorted(foata_groups.keys())
    ]


def form_dependencies(n: int) -> dict[Task, list[Task]]:
    connections_graph = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, n + 1):
                # Standard dependencies
                connections_graph[A(i, j)].append(B(i, k, j))
                connections_graph[B(i, k, j)].append(C(i, k, j))

                # C->B and C->C dependencies
                if i > 0 and k > i:
                    connections_graph[C(i - 1, k, j - 1)].append(B(i, k, j))
                    connections_graph[C(i - 1, k, j)].append(C(i, k, j))

            # C -> A dependencies
            if i > 0:
                connections_graph[C(i - 1, i, i)].append(A(i, j))
                connections_graph[C(i - 1, i, j)].append(A(i, j))

    return connections_graph


def prepare_dependency_graph(n: int) -> nx.DiGraph:
    formed_graph = form_dependencies(n)
    relabeled_graph = {
        key.get_id(): [value.get_id() for value in formed_graph[key]]
        for key in formed_graph
    }

    return create_dekiert_graph(nx.DiGraph(relabeled_graph))


def create_dekiert_graph(D: nx.DiGraph) -> nx.DiGraph:
    n = len(D)
    for v in D:
        for w in D:
            for k in D:
                if v != w and w != k and D.has_edge(v, k):
                    if D.has_edge(v, w) and D.has_edge(w, k):
                        D.remove_edge(v, k)
    draw_graph(D)
    return D


def draw_graph(G: nx.DiGraph) -> None:
    pos = graphviz_layout(G, prog="dot")
    nx.draw(
        G,
        pos,
        with_labels=True,
        font_weight="bold",
        node_size=400,
        node_color="#FF7F50",
        edge_color="#1F78B4",
        arrowsize=20,
        font_color="black",
        font_size=10,
        linewidths=1,
        width=2,
    )
    plt.show()
