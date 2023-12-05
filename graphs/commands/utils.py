from typing import Callable
from argparse import ArgumentParser, Namespace

from ..utils import AVAILABLE_FORMATS


def add_common_arguments(
    parser: ArgumentParser, cmd: Callable[[Namespace], None]
) -> None:
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        type=str,
        dest="input_file",
        default=None,
        help="Provide the program a file that describe an input graph. If not provided, then program reads stdin",
    )
    parser.add_argument(
        "--input-format",
        action="store",
        choices=AVAILABLE_FORMATS,
        type=str,  # type: ignore
        default="regular-matrix",
        dest="input_format",
        help="""Input format of graph. In \"regular-matrix\" format it read graph as matrix size and matrix.
        In "edge-set" it read graph as set of vertexes defined as alphabet and set of edges as pair of alphabet""",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        type=str,
        dest="output_file",
        default=None,
        help="""Allow you to specify an output file which will contain a result of the algorithm work.
        If you not provide it, the program will show result in stdout""",
    )
    parser.add_argument(
        "--output-format",
        action="store",
        choices=AVAILABLE_FORMATS,
        type=str,  # type: ignore
        default="regular-matrix",
        dest="output_format",
        help='See "--input-format" description',
    )
    parser.set_defaults(cmd=cmd)
