from typing import Any, Literal, cast
import sys
from pathlib import Path
from io import TextIOBase
from string import ascii_lowercase as eng_alphabet
import numpy as np

from .base import MinimizedAdjacencyMatrix, Graph

AvailableFormats = Literal["regular-matrix", "edge-set"]

DEFAULT_ENCODING = "utf-8"
AVAILABLE_FORMATS: list[AvailableFormats] = ["regular-matrix", "edge-set"]
MAX_LINE_LENGTH = 120
DEFAULT_FORMAT: Literal["regular-matrix"] = "regular-matrix"


def read_regular_adj_matrix(file: str | Path | TextIOBase | None = None, encoding: str | None = None) -> np.ndarray[Any, np.dtype[bool]]:  # type: ignore
    if encoding is None:
        encoding = DEFAULT_ENCODING

    def read_file(file: TextIOBase) -> np.ndarray[Any, np.dtype[bool]]:  # type: ignore
        try:
            if file is sys.stdin:
                sys.stdout.write("Please enter vertex count: ")
                sys.stdout.flush()
            vertex_count = int(file.readline())
        except ValueError as error:
            raise ValueError("Invalid format. Not provided vertex count") from error

        if file is sys.stdin:
            sys.stdout.write("Please enter matrix:\n")
            sys.stdout.flush()
        adjacency_matrix = np.zeros((vertex_count, vertex_count), dtype=bool)
        i = -1
        for i in range(vertex_count):
            j = -1
            for j, edge in enumerate(file.readline().split()):
                try:
                    adjacency_matrix[i][j] = bool(int(edge))
                except ValueError as error:
                    raise ValueError(
                        "Invalid format. Edge as number not provided"
                    ) from error
            if j != vertex_count - 1:
                raise ValueError(f'Not all columns provided for "{i}" row')
        if i != vertex_count - 1:
            raise ValueError("Not all rows provided")
        return adjacency_matrix

    if isinstance(file, (str, Path)):
        with open(file, "r", encoding=encoding) as file_:
            return read_file(file_)
    elif file is None:
        file = cast(TextIOBase, sys.stdin)
    return read_file(file)


def read_min_adj_matrix_as_edges_set(
    file: str | Path | TextIOBase | None = None, encoding: str | None = None
) -> MinimizedAdjacencyMatrix:
    if encoding is None:
        encoding = DEFAULT_ENCODING

    def read_file(file: TextIOBase) -> MinimizedAdjacencyMatrix:
        if file is sys.stdin:
            sys.stdout.write("Please enter vertexes as alphabet characters: ")
            sys.stdout.flush()
        alphabet_char_to_idx: dict[str, int] = {}
        for i, alphabet_char in enumerate(file.readline().split()):
            if alphabet_char in alphabet_char_to_idx:
                raise ValueError("Such vertex already exists")
            alphabet_char_to_idx[alphabet_char] = i
        if file is sys.stdin:
            sys.stdout.write("Please enter edges as pairs of alphabet characters:\n")
            sys.stdout.flush()
        min_adj_matrix = MinimizedAdjacencyMatrix.new(len(alphabet_char_to_idx))
        line = file.readline()
        for edge in line.split():
            if len(edge) != 2:
                raise ValueError(
                    f'Invalid edge "{edge}". It should be pair of alphabet (without spaces) chars represents vertexes'
                )
            a = alphabet_char_to_idx.get(edge[0])
            b = alphabet_char_to_idx.get(edge[1])
            if a is None or b is None:
                raise ValueError(f'Not found vertexes described by edge "{edge}"')
            min_adj_matrix.change_neighborhood(a, b)
        return min_adj_matrix

    if isinstance(file, (str, Path)):
        with open(file, "r", encoding=encoding) as file_:
            return read_file(file_)
    elif file is None:
        file = cast(TextIOBase, sys.stdin)
    return read_file(file)


def read_min_adj_matrix(
    file: str | Path | TextIOBase | None = None,
    format: AvailableFormats = DEFAULT_FORMAT,
    encoding: str | None = None,
) -> MinimizedAdjacencyMatrix:
    if format == "regular-matrix":
        return MinimizedAdjacencyMatrix.from_regular_adj_matrix(
            read_regular_adj_matrix(file, encoding)
        )
    return read_min_adj_matrix_as_edges_set(file, encoding)


def read_graph(
    file: str | Path | TextIOBase | None = None,
    format: AvailableFormats = DEFAULT_FORMAT,
    encoding: str | None = None,
) -> Graph:
    return Graph.from_adj_matrix(
        read_min_adj_matrix(file, format=format, encoding=encoding)
    )


def format_regular_adj_matrix(graph: np.ndarray[Any, np.dtype[bool]] | MinimizedAdjacencyMatrix | Graph) -> str:  # type: ignore
    if isinstance(graph, Graph):
        graph = graph.min_adj_matrix
    if isinstance(graph, MinimizedAdjacencyMatrix):
        graph = graph.regular_adjacency_matrix()
    return (
        f"{graph.shape[0]}\n"
        + "\n".join(
            " ".join("1" if a else "0" for a in graph[row_idx])
            for row_idx in range(graph.shape[0])
        )
        + "\n"
    )


def format_graph_as_edge_set(graph: MinimizedAdjacencyMatrix | Graph) -> str:
    if isinstance(graph, Graph):
        graph = graph.min_adj_matrix
    if graph.vertex_count > len(eng_alphabet):
        raise ValueError("Too large graph to show it as edge set")
    lines = [" ".join(eng_alphabet[: graph.vertex_count])]
    line: list[str] = []
    for a, b in graph.all_edges():
        if len(line) * 2 + len(line) + 2 > MAX_LINE_LENGTH:
            lines.append(" ".join(line))
            line = []
        line.append(f"{eng_alphabet[a]}{eng_alphabet[b]}")
    if line:
        lines.append(" ".join(line))
    return "\n".join(lines) + "\n"


def format_graph(graph: MinimizedAdjacencyMatrix | Graph, format: AvailableFormats = DEFAULT_FORMAT) -> str:  # type: ignore
    if isinstance(graph, Graph):
        graph = graph.min_adj_matrix
    if format == "regular-matrix":
        return format_regular_adj_matrix(graph)
    return format_graph_as_edge_set(graph)


def write_output_graph(graph: MinimizedAdjacencyMatrix | Graph, file: str | Path | TextIOBase | None = None, format: AvailableFormats = DEFAULT_FORMAT, encoding: str | None = None) -> None:  # type: ignore
    if isinstance(graph, Graph):
        graph = graph.min_adj_matrix
    output = format_graph(graph, format=format)

    if encoding is None:
        encoding = DEFAULT_ENCODING

    def write(file: TextIOBase) -> None:
        if file is sys.stdout and format == "regular-matrix":
            sys.stdout.write("Matrix size and matrix:\n")
            sys.stdout.flush()
        elif file is sys.stdout:
            sys.stdout.write("Vertexes and edges:\n")
            sys.stdout.flush()
        file.write(output)

    if isinstance(file, (str, Path)):
        with open(file, "w", encoding=encoding) as file_:
            return write(file_)
    elif file is None:
        file = cast(TextIOBase, sys.stdout)
    return write(file)
