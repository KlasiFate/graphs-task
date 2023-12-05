from collections import deque
import numpy as np

from .base import Graph, Vertex


def dfs_building_tree(start: int | Vertex, graph: Graph) -> Graph:
    visited = np.zeros((graph.vertex_count,), dtype=bool)
    # second element is integer that define what index of neighbor should be start of searching in adjacency matrix
    if isinstance(start, Vertex):
        # just in case to be ensure that vertex belongs graph
        start = start.idx
    stack = deque([(graph.vertex(start), 0)])
    new_graph = Graph.new(graph.vertex_count)
    while stack:
        current_vertex, start_neighbor_idx = stack[-1]
        visited[current_vertex] = True
        for neighbor in current_vertex.neighbors(start_neighbor_idx):
            if not visited[neighbor]:
                stack[-1] = (current_vertex, neighbor.idx + 1)
                new_graph.change_neighborhood(current_vertex, neighbor)
                stack.append((neighbor, 0))
                break
        else:
            stack.pop()
    return new_graph
