from typing import Any, Generator, Union
import numpy as np


class MinimizedAdjacencyMatrix:
    def __init__(self, min_adj_matrix: np.ndarray[Any, np.dtype[bool]], vertex_count: int) -> None:  # type: ignore
        self._min_adj_matrix = min_adj_matrix
        self.vertex_count = vertex_count

    def are_neighbors(self, a: int, b: int) -> bool:
        if not (0 <= a < self.vertex_count and 0 <= b < self.vertex_count):
            raise ValueError("No such vertexes in the graph")
        if a == b:
            return True
        if a >= b:
            a, b = b, a
        return self._min_adj_matrix[self._calc_idx(a, b, self.vertex_count)]

    def all_neighbors(
        self, a: int, start_neighbor_idx: int = 0
    ) -> Generator[int, None, None]:
        if not (0 <= a < self.vertex_count and 0 <= start_neighbor_idx):
            raise ValueError("No such vertexes in the graph")
        for b in range(start_neighbor_idx, self.vertex_count):
            if a != b and self.are_neighbors(a, b):
                yield b

    @staticmethod
    def _calc_idx(row_idx: int, col_idx: int, vertex_count: int) -> int:
        if row_idx >= col_idx:
            raise ValueError(
                "Invalid values. The column index should be greater than the row one"
            )
        if vertex_count < 2:
            raise ValueError("Too small graph")

        return int(
            (vertex_count - 1) * row_idx - (row_idx + 1) * row_idx / 2 + col_idx - 1
        )

    @classmethod
    def from_regular_adj_matrix(cls, adj_matrix: np.ndarray[Any, np.dtype[bool]]) -> "MinimizedAdjacencyMatrix":  # type: ignore
        if (
            len(adj_matrix.shape) != 2
            or adj_matrix.shape[0] != adj_matrix.shape[1]
            or adj_matrix.shape[0] < 2
        ):
            raise ValueError("Invalid adjacency matrix")

        n = adj_matrix.shape[0]
        # minimized adjacency matrix
        min_adj_matrix = np.zeros(((n**2 - n) // 2,), dtype=bool)  # type: ignore

        # pylint: disable=consider-using-enumerate
        for row_idx in range(len(adj_matrix)):
            for col_idx in range(row_idx + 1, len(adj_matrix[row_idx])):
                if not adj_matrix[row_idx][col_idx]:
                    continue
                min_adj_matrix[cls._calc_idx(row_idx, col_idx, n)] = True

        return cls(min_adj_matrix, n)

    @classmethod
    def new(cls, vertex_count: int) -> "MinimizedAdjacencyMatrix":
        if vertex_count < 2:
            raise ValueError("Too small graph")
        min_adj_matrix = np.zeros(((vertex_count**2 - vertex_count) // 2,), dtype=bool)  # type: ignore
        return cls(min_adj_matrix, vertex_count)

    def change_neighborhood(self, a: int, b: int, are_neighbors: bool = True) -> None:
        if not (0 <= a < self.vertex_count and 0 <= b < self.vertex_count):
            raise ValueError("No such vertexes in the graph")
        if a == b:
            return
        if a >= b:
            a, b = b, a
        self._min_adj_matrix[self._calc_idx(a, b, self.vertex_count)] = are_neighbors

    def all_edges(self) -> Generator[tuple[int, int], None, None]:
        for a in range(self.vertex_count):
            for b in range(a + 1, self.vertex_count):
                if self.are_neighbors(a, b):
                    yield (a, b)

    def regular_adjacency_matrix(self) -> np.ndarray[Any, np.dtype[bool]]:  # type: ignore
        regular_adj_matrix = np.zeros(
            (self.vertex_count, self.vertex_count), dtype=bool
        )
        for a in range(self.vertex_count):
            for b in range(a + 1, self.vertex_count):
                if self.are_neighbors(a, b):
                    regular_adj_matrix[a][b] = regular_adj_matrix[b][a] = True
        return regular_adj_matrix


class Vertex:
    __slots__ = ("graph", "idx")

    def __init__(self, graph: "Graph", idx: int) -> None:
        self.graph = graph
        self.idx = idx

    def __int__(self) -> int:
        return self.idx

    def __index__(self) -> int:
        return self.idx

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, Vertex) and self.idx == other.idx) or (
            isinstance(other, int) and self.idx == other
        )

    def __iter__(self) -> Generator["Vertex", None, None]:
        return self.neighbors()

    def neighbors(
        self, start_neighbor_idx: Union["Vertex", int] = 0
    ) -> Generator["Vertex", None, None]:
        return self.graph.all_neighbors(self, start_neighbor_idx)

    def change_neighborhood(
        self, neighbor: Union["Vertex", int], are_neighbors: bool = True
    ) -> None:
        self.graph.change_neighborhood(self, neighbor, are_neighbors)


class Graph:
    def __init__(self, min_adj_matrix: MinimizedAdjacencyMatrix) -> None:
        self.min_adj_matrix = min_adj_matrix

    def vertex(self, idx: int) -> Vertex:
        if not 0 <= idx < self.min_adj_matrix.vertex_count:
            raise ValueError("No such vertex in the graph")
        return Vertex(self, idx)

    @property
    def vertex_count(self) -> int:
        return self.min_adj_matrix.vertex_count

    @classmethod
    def from_adj_matrix(
        cls, adj_matrix: np.ndarray | MinimizedAdjacencyMatrix
    ) -> "Graph":
        if not isinstance(adj_matrix, MinimizedAdjacencyMatrix):
            adj_matrix = MinimizedAdjacencyMatrix.from_regular_adj_matrix(adj_matrix)
        return cls(adj_matrix)

    @classmethod
    def new(cls, vertex_count: int) -> "Graph":
        return cls(MinimizedAdjacencyMatrix.new(vertex_count))

    def all_neighbors(
        self, vertex: int | Vertex, start_neighbor_idx: Vertex | int = 0
    ) -> Generator[Vertex, None, None]:
        if isinstance(vertex, Vertex):
            vertex = vertex.idx
        if isinstance(start_neighbor_idx, Vertex):
            start_neighbor_idx = start_neighbor_idx.idx
        for neighbor in self.min_adj_matrix.all_neighbors(vertex, start_neighbor_idx):
            yield Vertex(self, neighbor)

    def change_neighborhood(
        self, a: Vertex | int, b: Vertex | int, are_neighbors: bool = True
    ) -> None:
        if isinstance(a, Vertex):
            a = a.idx
        if isinstance(b, Vertex):
            b = b.idx
        self.min_adj_matrix.change_neighborhood(a, b, are_neighbors)

    def all_edges(self) -> Generator[tuple[Vertex, Vertex], None, None]:
        for edge in self.min_adj_matrix.all_edges():
            yield (Vertex(self, edge[0]), Vertex(self, edge[1]))

    def regular_adjacency_matrix(self) -> np.ndarray[Any, np.dtype[bool]]:  # type: ignore
        return self.min_adj_matrix.regular_adjacency_matrix()
