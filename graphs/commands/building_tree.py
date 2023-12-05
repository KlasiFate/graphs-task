from typing import cast
import sys
from argparse import Namespace, ArgumentParser, _SubParsersAction

from ..utils import read_graph, write_output_graph
from ..building_tree import dfs_building_tree
from .utils import add_common_arguments


def run(options: Namespace) -> None:
    graph = read_graph(options.input_file, format=options.input_format)
    if options.start_vertex is None:
        sys.stdout.write("Please enter start vertex index: ")
        sys.stdout.flush()
        try:
            start_vertex = int(sys.stdin.readline())
        except ValueError as error:
            raise ValueError("Invalid start vertex") from error
    else:
        start_vertex = options.start_vertex
    output_graph = dfs_building_tree(start_vertex, graph)
    write_output_graph(output_graph, options.output_file, format=options.output_format)


def add_subparser(subparsers: _SubParsersAction) -> None:
    building_tree_parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "building-tree",
            help="Build tree from provided graph",
            description="At this moment there is only one implementation. It is based on DFS",
        ),
    )
    add_common_arguments(building_tree_parser, run)
    building_tree_parser.add_argument(
        "-v",
        "--vertex",
        action="store",
        type=int,
        default=None,
        dest="start_vertex",
        help="""Provide a start vertex from which the algorithm starts. If not provided, the program ask it.
        At this moment there is no way to specify start vertex as alphabet character when input format is \"edge-set\"""",
    )
